#!/usr/bin/env python3
"""
FastAPI backend for AgenticMarketers
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import sys
import os
from dotenv import load_dotenv
import json

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.writer.writer import WriterAgent
from prompts.InputPrompt import InputPrompt

# Load environment variables
load_dotenv()

app = FastAPI(
    title="AgenticMarketers API",
    description="AI-powered marketing content generation",
    version="1.0.0"
)

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
async def start_workflow(request: WorkflowRequest):
    """
    Main workflow endpoint that processes the form data and generates content
    """
    try:
        if not writer_agent:
            raise HTTPException(
                status_code=500, 
                detail="WriterAgent not initialized. Check OpenAI API key."
            )
        
        # Convert request to InputPrompt object
        input_prompt = InputPrompt(
            product_images=request.product_images,
            product_name=request.product_name,
            product_description=request.product_description,
            product_main_features=request.product_main_features,
            product_benefits=request.product_benefits,
            product_use_cases=request.product_use_cases,
            product_pricing=request.product_pricing,
            product_target_audience=request.product_target_audience,
            background_scene=request.background_scene,
            composition_style=request.composition_style,
            lighting_preferences=request.lighting_preferences,
            mood=request.mood,
            camera_setup=request.camera_setup,
            color_palette=request.color_palette,
            additional_modifiers=request.additional_modifiers
        )
        
        # Generate content using WriterAgent
        print(f"🚀 Starting workflow for product: {request.product_name}")
        content_result = writer_agent.invoke(prompt_data=input_prompt)
        
        # DEBUG: Print the raw result
        print(f"🔍 DEBUG - Raw content_result type: {type(content_result)}")
        print(f"🔍 DEBUG - Raw content_result: {content_result}")
        print(f"🔍 DEBUG - Raw content_result repr: {repr(content_result)}")
        
        try:
            # Handle different types of content_result
            if isinstance(content_result, str):
                print("🔍 DEBUG - Parsing as JSON string")
                parsed_result = json.loads(content_result)
            elif isinstance(content_result, dict):
                print("🔍 DEBUG - content_result is already a dict, using as-is")
                parsed_result = content_result
            else:
                print("🔍 DEBUG - Converting to dict or using as-is")
                parsed_result = content_result
            
            print(f"🔍 DEBUG - Parsed result type: {type(parsed_result)}")
            print(f"🔍 DEBUG - Parsed result: {parsed_result}")
            
            # Handle the specific structure: {'role': 'assistant', 'content': [{'text': '...'}]}
            if isinstance(parsed_result, dict) and 'content' in parsed_result:
                print("🔍 DEBUG - Found 'content' key in parsed_result")
                content_list = parsed_result['content']
                print(f"🔍 DEBUG - Content list type: {type(content_list)}")
                print(f"🔍 DEBUG - Content list: {content_list}")
                
                if isinstance(content_list, list) and len(content_list) > 0:
                    print(f"🔍 DEBUG - Content list has {len(content_list)} items")
                    # Get the first item and extract text
                    first_item = content_list[0]
                    print(f"🔍 DEBUG - First item type: {type(first_item)}")
                    print(f"🔍 DEBUG - First item: {first_item}")
                    
                    if isinstance(first_item, dict) and 'text' in first_item:
                        caption = first_item['text']
                        print(f"🔍 DEBUG - Extracted text: {caption[:100]}...")
                    else:
                        caption = str(first_item)
                        print(f"🔍 DEBUG - Using first_item as string: {caption[:100]}...")
                else:
                    caption = str(content_list)
                    print(f"🔍 DEBUG - Using content_list as string: {caption[:100]}...")
            else:
                # Fallback to string representation
                caption = str(content_result)
                print(f"🔍 DEBUG - Fallback to string representation: {caption[:100]}...")
                
        except (json.JSONDecodeError, AttributeError, KeyError, IndexError) as e:
            # If JSON parsing fails, use string representation
            print(f"🔍 DEBUG - Exception occurred: {e}")
            caption = str(content_result)
            print(f"🔍 DEBUG - Using content_result as string: {caption[:100]}...")
        
        # Mock image URL for now
        mock_image = "https://via.placeholder.com/400x400/000000/FFFFFF?text=Product+Image"
        
        return WorkflowResponse(
            success=True,
            message="Content generated successfully!",
            caption=caption,
            image=mock_image
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
