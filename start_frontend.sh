#!/bin/bash

# Script to start the Next.js frontend
echo "🎨 Starting AgenticMarketers Frontend..."
echo "📍 Frontend will be available at: http://localhost:3000"
echo "🔗 Make sure the backend is running on http://localhost:8000"
echo ""
echo "="*50

cd frontend
npm run dev
