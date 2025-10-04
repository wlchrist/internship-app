#!/bin/bash

# Startup script for the Internship Aggregator API
echo "🚀 Starting Internship Aggregator API..."

# Check if virtual environment exists
if [ ! -d "api/fastapi" ]; then
    echo "❌ Virtual environment not found. Creating one..."
    cd api
    python3 -m venv fastapi
    cd ..
fi

# Activate virtual environment and run everything in the same shell session
echo "📦 Activating virtual environment..."
source api/fastapi/bin/activate

# Install dependencies if needed
echo "🔧 Installing dependencies..."
pip install -r api/requirements.txt

# Start the FastAPI server
echo "🌐 Starting FastAPI server on http://localhost:8000"
echo "📚 API documentation available at http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

cd api && python main.py