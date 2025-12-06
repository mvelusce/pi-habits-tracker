#!/bin/bash

# Habits Tracker Setup Script

echo "🎯 Setting up Habits Tracker..."
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    echo "Visit: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"
echo ""

# Create data directory
echo "📁 Creating data directory..."
mkdir -p data
echo "✅ Data directory created"
echo ""

# Check if .env files exist, create from examples if not
if [ ! -f "frontend/.env" ]; then
    echo "📝 Creating frontend/.env from example..."
    cp frontend/.env.example frontend/.env 2>/dev/null || echo "VITE_API_URL=http://localhost:8000" > frontend/.env
    echo "✅ frontend/.env created"
fi

# Build and start containers
echo ""
echo "🐳 Building and starting Docker containers..."
echo "This may take a few minutes on first run..."
echo ""

docker-compose up -d --build

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Habits Tracker is now running!"
    echo ""
    echo "📱 Access your app:"
    echo "   Frontend: http://localhost:3000"
    echo "   Backend API: http://localhost:8000"
    echo "   API Docs: http://localhost:8000/docs"
    echo ""
    echo "🛑 To stop: docker-compose down"
    echo "📊 To view logs: docker-compose logs -f"
    echo ""
else
    echo ""
    echo "❌ Failed to start containers. Check the error messages above."
    exit 1
fi

