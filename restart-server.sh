#!/bin/bash
# Complete server restart with cache clearing

echo "========================================="
echo "  KCM Converter - Complete Restart"
echo "========================================="

cd "$(dirname "$0")"

# Kill all Python processes
echo "Stopping all Python processes..."
pkill -9 -f "kcm_converter_server" 2>/dev/null || true
pkill -9 -f "python.*kcm" 2>/dev/null || true
sleep 2

# Clear all Python cache
echo "Clearing Python cache..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true
find . -name "*.pyo" -delete 2>/dev/null || true

# Clear port
echo "Clearing port 5000..."
lsof -ti:5000 | xargs kill -9 2>/dev/null || true
sleep 1

# Start server
echo "Starting fresh server..."
cd kcm-converter
python kcm_converter_server.py > server.log 2>&1 &

sleep 3

# Check if running
if curl -s http://localhost:5000/health > /dev/null 2>&1; then
    echo "✓ Server started successfully on port 5000"
else
    echo "✗ Server failed to start. Check server.log"
    tail -20 server.log
fi

echo "========================================="
