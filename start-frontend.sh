#!/bin/bash

# Startup script for the Internship Aggregator Frontend
echo "🚀 Starting Internship Aggregator Frontend..."

# Check if node_modules exists
if [ ! -d "web/internship-app-frontend/node_modules" ]; then
    echo "📦 Installing dependencies..."
    cd web/internship-app-frontend
    npm install
    cd ../..
fi

# Start the Next.js development server
echo "🌐 Starting Next.js development server on http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

cd web/internship-app-frontend
npm run dev