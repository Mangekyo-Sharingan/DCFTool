#!/bin/bash
# Deployment script for DCF Valuation Tool

echo "🚀 Starting DCF Valuation Tool deployment..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Build and start the application
echo "📦 Building Docker images..."
docker-compose build

echo "🌐 Starting DCF Valuation Tool..."
docker-compose up -d

echo "✅ DCF Valuation Tool is now running!"
echo "🔗 Access the application at: http://localhost:5000"
echo ""
echo "📊 To view logs: docker-compose logs -f"
echo "🛑 To stop: docker-compose down"
