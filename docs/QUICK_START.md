# Quick Deployment Guide

## 🚢 Using Pre-built Docker Images

The easiest way to deploy Habits Tracker is using pre-built Docker images from GitHub Container Registry.

### One-Line Install

```bash
curl -sSL https://raw.githubusercontent.com/mvelusce/habits-tracker/master/install.sh | bash
```

### Manual Install

```bash
# Download docker-compose.yml
wget -O docker-compose.yml https://raw.githubusercontent.com/mvelusce/habits-tracker/master/docker-compose.deploy.yml

# Download .env
wget -O .env https://raw.githubusercontent.com/mvelusce/habits-tracker/master/.env.deploy.example

# Create data directory
mkdir -p data

# Start services
docker-compose up -d
```

### Access Your App

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000  
- **API Docs**: http://localhost:8000/docs

## 📦 Available Images

Pre-built images support both **amd64** (x86_64) and **arm64** (Raspberry Pi, Apple Silicon):

- `ghcr.io/mvelusce/habits-tracker-backend:latest`
- `ghcr.io/mvelusce/habits-tracker-frontend:latest`

## 🔄 Updating

```bash
docker-compose pull
docker-compose up -d
```

## 📖 Full Documentation

For detailed deployment options, see [DEPLOYMENT.md](DEPLOYMENT.md):
- Remote server deployment
- Raspberry Pi setup
- SSL/HTTPS configuration
- PostgreSQL setup
- Reverse proxy configuration
- And more!

## 🛠️ Building from Source

If you prefer to build from source:

```bash
git clone https://github.com/mvelusce/habits-tracker.git
cd habits-tracker
docker-compose up --build -d
```

See the [main README.md](README.md) for full development instructions.

