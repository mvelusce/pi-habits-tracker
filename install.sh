#!/bin/bash

# Wellness Log - Quick Install Script
# This script downloads and sets up the wellness log using pre-built Docker images

set -e

REPO="mvelusce/habits-tracker"
BRANCH="${BRANCH:-master}"  # or main
GITHUB_RAW="https://raw.githubusercontent.com/${REPO}/${BRANCH}"

echo "🌟 Wellness Log - Quick Install"
echo "=================================="
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

# Create installation directory
INSTALL_DIR="${INSTALL_DIR:-./habits-tracker}"
echo "📁 Installation directory: $INSTALL_DIR"

if [ -d "$INSTALL_DIR" ]; then
    read -p "Directory $INSTALL_DIR already exists. Continue? (y/N): " confirm
    if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
        echo "Installation cancelled."
        exit 0
    fi
else
    mkdir -p "$INSTALL_DIR"
fi

cd "$INSTALL_DIR"

# Download docker-compose.yml
echo ""
echo "📥 Downloading docker-compose.yml..."
if ! wget -q -O docker-compose.yml "${GITHUB_RAW}/docker-compose.deploy.yml"; then
    echo "❌ Failed to download docker-compose.yml"
    exit 1
fi
echo "✅ docker-compose.yml downloaded"

# Download .env.example
echo ""
echo "📥 Downloading .env.example..."
if ! wget -q -O .env.example "${GITHUB_RAW}/.env.deploy.example"; then
    echo "❌ Failed to download .env.example"
    exit 1
fi
echo "✅ .env.example downloaded"

# Create .env if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "✅ .env file created"
else
    echo ""
    echo "ℹ️  .env file already exists, keeping current configuration"
fi

# Create data directory
mkdir -p data
echo "✅ Data directory created"

# Pull images
echo ""
echo "🐳 Pulling Docker images..."
docker-compose pull

# Start services
echo ""
echo "🚀 Starting services..."
docker-compose up -d

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Wellness Log is now running!"
    echo ""
    echo "📱 Access your app:"
    echo "   Frontend: http://localhost:3000"
    echo "   Backend API: http://localhost:8000"
    echo "   API Docs: http://localhost:8000/docs"
    echo ""
    echo "📊 To import existing data:"
    echo "   1. Place your CSV files in the ./data directory"
    echo "   2. Run: docker-compose exec backend python import_legacy_data.py --habits=/app/data/Habits.csv --checkmarks=/app/data/Checkmarks.csv"
    echo ""
    echo "🛑 To stop: docker-compose down"
    echo "📊 To view logs: docker-compose logs -f"
    echo "🔄 To update: docker-compose pull && docker-compose up -d"
    echo ""
    echo "📖 Documentation: https://github.com/${REPO}"
    echo ""
else
    echo ""
    echo "❌ Failed to start services. Check the error messages above."
    exit 1
fi

