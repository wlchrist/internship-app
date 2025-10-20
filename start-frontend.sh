#!/bin/bash

# Startup script for the Internship Aggregator Frontend
# WSL-compatible version
echo "🚀 Starting Internship Aggregator Frontend..."

# Check if we're in WSL
if grep -qi microsoft /proc/version; then
    echo "🐧 WSL environment detected"
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    echo "   Visit: https://nodejs.org/"
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm first."
    exit 1
fi

# Display Node.js and npm versions
echo "📋 Node.js version: $(node --version)"
echo "📋 npm version: $(npm --version)"

# Navigate to frontend directory
FRONTEND_DIR="web/internship-app-frontend"

if [ ! -d "$FRONTEND_DIR" ]; then
    echo "❌ Frontend directory not found: $FRONTEND_DIR"
    echo "   Make sure you're running this script from the project root"
    exit 1
fi

# Check if package.json exists
if [ ! -f "$FRONTEND_DIR/package.json" ]; then
    echo "❌ package.json not found in $FRONTEND_DIR"
    exit 1
fi

# Check if node_modules exists, install if not
if [ ! -d "$FRONTEND_DIR/node_modules" ]; then
    echo "📦 Installing dependencies..."
    cd "$FRONTEND_DIR"
    npm install
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install dependencies"
        exit 1
    fi
    cd - > /dev/null
else
    echo "✅ Dependencies already installed"
fi

# Check if port 3000 is available
if lsof -i:3000 &> /dev/null; then
    echo "⚠️  Port 3000 is already in use"
    echo "   You may need to stop the existing process or use a different port"
    echo "   Run: lsof -i:3000 to see what's using the port"
fi

# Start the Next.js development server
echo ""
echo "🌐 Starting Next.js development server on http://localhost:3000"
echo "   If you're using WSL, you might need to access via:"
echo "   http://localhost:3000 (from Windows browser)"
echo "   or http://$(hostname -I | awk '{print $1}'):3000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

cd "$FRONTEND_DIR"
npm run dev