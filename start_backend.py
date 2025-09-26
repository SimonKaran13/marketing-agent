#!/usr/bin/env python3
"""
Script to run the FastAPI backend server
"""

import uvicorn
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("🚀 Starting AgenticMarketers Backend Server...")
    print("📍 Backend will be available at: http://localhost:8000")
    print("📖 API docs will be available at: http://localhost:8000/docs")
    print("🔍 Health check: http://localhost:8000/health")
    print("\n" + "="*50)
    
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
