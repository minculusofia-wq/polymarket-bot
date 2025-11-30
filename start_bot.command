#!/bin/bash

# Get the directory where the script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "🚀 Starting Polymarket Bot..."

# Activate Virtual Environment
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "❌ Virtual environment not found! Please run 'python3 -m venv venv' and install requirements."
    exit 1
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
