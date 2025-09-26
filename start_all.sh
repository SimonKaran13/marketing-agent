#!/bin/bash

# Script to start both backend and frontend
echo "🚀 Starting AgenticMarketers Full Stack Application..."
echo ""
echo "This will start:"
echo "  - Backend API on http://localhost:8000"
echo "  - Frontend on http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop both services"
echo "="*50

# Function to cleanup background processes
cleanup() {
    echo ""
    echo "🛑 Stopping services..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Start backend in background
echo "🐍 Starting Backend..."
uv run python start_backend.py &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Start frontend in background
echo "🎨 Starting Frontend..."
./start_frontend.sh &
FRONTEND_PID=$!

# Wait for both processes
wait
