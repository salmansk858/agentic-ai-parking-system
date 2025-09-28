#!/bin/bash
# Development server runner

set -e

echo "🚗 Starting Agentic AI Parking System (Development Mode)"

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "❌ Virtual environment not found. Run scripts/setup.sh first."
    exit 1
fi

# Check .env file
if [ ! -f ".env" ]; then
    echo "❌ .env file not found. Copy .env.example to .env and configure."
    exit 1
fi

# Start development server
export DEBUG=true
export LOG_LEVEL=DEBUG

echo "🚀 Starting FastAPI server..."
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
