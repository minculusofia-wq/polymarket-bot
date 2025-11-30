#!/bin/bash

# Get the directory where the script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "🚀 Starting Polymarket Bot..."

# Check for Virtual Environment
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found. Setting it up..."
    python3 -m venv venv
    source venv/bin/activate
    
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
    
    echo "✅ Setup complete!"
else
    source venv/bin/activate
fi

# Start API in background
echo "📊 Starting Dashboard API..."
python api.py > api.log 2>&1 &
API_PID=$!

# Wait a moment for API to start
sleep 2

# Open Dashboard in Browser
echo "🌐 Opening Dashboard..."
open "http://localhost:5000"

# Start Scanner in foreground (WebSocket Mode)
echo "🐋 Starting Whale Scanner (Real-Time WebSocket)..."
python scanner_ws.py

# Cleanup on exit
kill $API_PID
