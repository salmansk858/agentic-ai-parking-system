#!/bin/bash
# Docker deployment runner

set -e

echo "🐳 Starting Agentic AI Parking System with Docker"

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found. Copy .env.example to .env and configure."
    exit 1
fi

# Build and start containers
echo "🔨 Building Docker containers..."
cd docker
docker-compose build

echo "🚀 Starting services..."
docker-compose up -d

echo "✅ Services started successfully!"
echo ""
echo "📊 Service URLs:"
echo "  - API Server: http://localhost:8000"
echo "  - Web Interface: http://localhost:8501" 
echo "  - Redis: localhost:6379"
echo ""
echo "📝 View logs: docker-compose -f docker/docker-compose.yml logs -f"
echo "🛑 Stop services: docker-compose -f docker/docker-compose.yml down"
