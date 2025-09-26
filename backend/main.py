#!/usr/bin/env python3
"""
FastAPI backend for AgenticMarketers
"""

from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import sys
import os
from dotenv import load_dotenv
import json
import shutil

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.writer.writer import WriterAgent
from prompts.InputPrompt import InputPrompt

# Load environment variables
load_dotenv()

# Create uploads directory if it doesn't exist
UPLOADS_DIR = "uploads"
os.makedirs(UPLOADS_DIR, exist_ok=True)

app = FastAPI(
    title="AgenticMarketers API",
    description="AI-powered marketing content generation",
    version="1.0.0"
)

# Mount static files for serving uploaded images
app.mount("/uploads", StaticFiles(directory=UPLOADS_DIR), name="uploads")

# Configure CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins in development
    allow_credentials=False,  # Set to False when using allow_origins=["*"]
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class WorkflowRequest(BaseModel):
    product_images: List[str] = []
    product_name: str
    product_description: str
    product_main_features: Optional[str] = None
    product_benefits: Optional[str] = None
    product_use_cases: Optional[str] = None
    product_pricing: Optional[str] = None
    product_target_audience: Optional[str] = None
    background_scene: Optional[str] = None
    composition_style: Optional[str] = None
    lighting_preferences: Optional[str] = None
    mood: Optional[str] = None
    camera_setup: Optional[str] = None
    color_palette: Optional[str] = None
    additional_modifiers: Optional[str] = None

class WorkflowResponse(BaseModel):
    success: bool
    message: str
    caption: Optional[str] = None
    image: Optional[str] = None

# Initialize WriterAgent
try:
    writer_agent = WriterAgent()
    print("✅ WriterAgent initialized successfully")
except Exception as e:
    print(f"❌ Failed to initialize WriterAgent: {e}")
    writer_agent = None

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "AgenticMarketers API is running",
        "status": "healthy",
        "agent_ready": writer_agent is not None
    }

@app.post("/start_workflow", response_model=WorkflowResponse)
async def start_workflow(
    product_images: List[UploadFile] = File(default=[]),
    product_name: str = Form(...),
    product_description: str = Form(...),
    product_main_features: Optional[str] = Form(None),
    product_benefits: Optional[str] = Form(None),
    product_use_cases: Optional[str] = Form(None),
    product_pricing: Optional[str] = Form(None),
    product_target_audience: Optional[str] = Form(None),
    background_scene: Optional[str] = Form(None),
    composition_style: Optional[str] = Form(None),
    lighting_preferences: Optional[str] = Form(None),
    mood: Optional[str] = Form(None),
    camera_setup: Optional[str] = Form(None),
    color_palette: Optional[str] = Form(None),
    additional_modifiers: Optional[str] = Form(None)
):
    """
    Main workflow endpoint that processes form data with file uploads and generates content
    """
    try:
        if not writer_agent:
            raise HTTPException(
                status_code=500, 
                detail="WriterAgent not initialized. Check OpenAI API key."
            )
        
        # Process uploaded images
        image_paths = []
        for image in product_images:
            if image.filename:
                # Save uploaded file to uploads directory
                file_path = os.path.join(UPLOADS_DIR, image.filename)
                with open(file_path, "wb") as buffer:
                    content = await image.read()
                    buffer.write(content)
                image_paths.append(file_path)
        
        # Convert form data to InputPrompt object
        input_prompt = InputPrompt(
            product_images=image_paths,
            product_name=product_name,
            product_description=product_description,
            product_main_features=product_main_features,
            product_benefits=product_benefits,
            product_use_cases=product_use_cases,
            product_pricing=product_pricing,
            product_target_audience=product_target_audience,
            background_scene=background_scene,
            composition_style=composition_style,
            lighting_preferences=lighting_preferences,
            mood=mood,
            camera_setup=camera_setup,
            color_palette=color_palette,
            additional_modifiers=additional_modifiers
        )
        
        # Generate content using WriterAgent
        print(f"🚀 Starting workflow for product: {product_name}")
        content_result = writer_agent.invoke(prompt_data=input_prompt)
        
        try:
            # Handle different types of content_result
            if isinstance(content_result, str):
                parsed_result = json.loads(content_result)
            elif isinstance(content_result, dict):
                parsed_result = content_result
            else:
                parsed_result = content_result
            
            # Handle the specific structure: {'role': 'assistant', 'content': [{'text': '...'}]}
            if isinstance(parsed_result, dict) and 'content' in parsed_result:
                content_list = parsed_result['content']
                
                if isinstance(content_list, list) and len(content_list) > 0:
                    first_item = content_list[0]
                    
                    if isinstance(first_item, dict) and 'text' in first_item:
                        caption = first_item['text']
                    else:
                        caption = str(first_item)
                else:
                    caption = str(content_list)
            else:
                caption = str(content_result)
                
        except (json.JSONDecodeError, AttributeError, KeyError, IndexError) as e:
            caption = str(content_result)
        
        # Use first uploaded image if available, otherwise use mock
        if image_paths:
            # Return the URL to the uploaded image
            image_url = f"/uploads/{os.path.basename(image_paths[0])}"
        else:
            image_url = "https://via.placeholder.com/400x400/000000/FFFFFF?text=Product+Image"
        
        return WorkflowResponse(
            success=True,
            message="Content generated successfully!",
            caption=caption,
            image=image_url
        )
        
    except Exception as e:
        print(f"❌ Workflow error: {e}")
        return WorkflowResponse(
            success=False,
            message=f"Failed to generate content: {str(e)}",
            caption=None,
            image=None
        )

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "agent_ready": writer_agent is not None,
        "openai_configured": bool(os.getenv("OPENAI_API_KEY")),
        "environment": "development"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        log_level="info"
    )
