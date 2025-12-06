# Deployment Guide

## Quick Install (Recommended)

Install using pre-built Docker images from GitHub Container Registry:

### One-Line Install

```bash
curl -sSL https://raw.githubusercontent.com/mvelusce/habits-tracker/master/install.sh | bash
```

### Manual Install

```bash
# Download docker-compose.yml
wget -O docker-compose.yml https://raw.githubusercontent.com/mvelusce/habits-tracker/master/docker-compose.deploy.yml

# Download .env.example
wget -O .env https://raw.githubusercontent.com/mvelusce/habits-tracker/master/.env.deploy.example

# Create data directory
mkdir -p data

# Start services
docker-compose up -d
```

## Access Your App

After installation:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## Docker Images

Pre-built images are available on GitHub Container Registry:
- `ghcr.io/mvelusce/habits-tracker-backend:latest`
- `ghcr.io/mvelusce/habits-tracker-frontend:latest`

### Supported Platforms
- `linux/amd64` (x86_64)
- `linux/arm64` (ARM, Raspberry Pi, Apple Silicon)

## Configuration

### Environment Variables

Edit `.env` file to configure:

```bash
# Database (SQLite by default)
DATABASE_URL=sqlite:///./data/habits_tracker.db

# For PostgreSQL
# DATABASE_URL=postgresql://user:password@postgres:5432/habits_tracker

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Environment
ENVIRONMENT=production
```

### Custom API URL

If your backend is on a different host/port, update the frontend container:

```yaml
frontend:
  image: ghcr.io/mvelusce/habits-tracker-frontend:latest
  environment:
    - VITE_API_URL=http://your-backend-url:8000
```

## Deployment Options

### 1. Local Machine

```bash
# Default installation
./install.sh
```

### 2. Remote Server (VPS, Cloud)

```bash
# SSH into your server
ssh user@your-server.com

# Run installation
curl -sSL https://raw.githubusercontent.com/mvelusce/habits-tracker/master/install.sh | bash

# Configure firewall
sudo ufw allow 3000  # Frontend
sudo ufw allow 8000  # Backend API
```

### 3. Raspberry Pi

Works on all Raspberry Pi models with Docker support:

```bash
# Install Docker if needed
curl -sSL https://get.docker.com | sh
sudo usermod -aG docker $USER

# Install habits tracker
curl -sSL https://raw.githubusercontent.com/mvelusce/habits-tracker/master/install.sh | bash
```

### 4. Behind Reverse Proxy (Nginx, Traefik)

#### Nginx Configuration

```nginx
# Frontend
server {
    listen 80;
    server_name habits.yourdomain.com;
    
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# Backend
server {
    listen 80;
    server_name api.habits.yourdomain.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

#### Traefik Labels

Add to `docker-compose.yml`:

```yaml
services:
  frontend:
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.habits-frontend.rule=Host(`habits.yourdomain.com`)"
      - "traefik.http.services.habits-frontend.loadbalancer.server.port=80"
  
  backend:
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.habits-api.rule=Host(`api.habits.yourdomain.com`)"
      - "traefik.http.services.habits-api.loadbalancer.server.port=8000"
```

## SSL/TLS (HTTPS)

### Using Let's Encrypt with Certbot

```bash
# Install certbot
sudo apt-get update
sudo apt-get install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d habits.yourdomain.com -d api.habits.yourdomain.com

# Auto-renewal
sudo certbot renew --dry-run
```

## Database

### SQLite (Default)

Data stored in: `./data/habits_tracker.db`

**Backup:**
```bash
docker-compose exec backend sqlite3 /app/data/habits_tracker.db ".backup /app/data/backup.db"
```

### PostgreSQL (Production)

1. Update `docker-compose.yml`:

```yaml
services:
  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=habits_tracker
      - POSTGRES_USER=habits
      - POSTGRES_PASSWORD=your_secure_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  backend:
    environment:
      - DATABASE_URL=postgresql://habits:your_secure_password@postgres:5432/habits_tracker
    depends_on:
      - postgres

volumes:
  postgres_data:
```

## Updating

### Pull Latest Images

```bash
docker-compose pull
docker-compose up -d
```

### Specific Version

```bash
# Edit docker-compose.yml
backend:
  image: ghcr.io/mvelusce/habits-tracker-backend:v1.0.0

frontend:
  image: ghcr.io/mvelusce/habits-tracker-frontend:v1.0.0
```

## Backup & Restore

### Backup

```bash
# Full backup
tar -czf habits-backup-$(date +%Y%m%d).tar.gz data/

# Database only
cp data/habits_tracker.db data/habits_tracker_backup_$(date +%Y%m%d).db
```

### Restore

```bash
# From full backup
tar -xzf habits-backup-20251206.tar.gz

# From database backup
cp data/habits_tracker_backup_20251206.db data/habits_tracker.db
docker-compose restart backend
```

## Monitoring

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Health Checks

```bash
# Backend health
curl http://localhost:8000/health

# Check container status
docker-compose ps
```

## Troubleshooting

### Containers won't start

```bash
# Check logs
docker-compose logs

# Remove and recreate
docker-compose down
docker-compose up -d
```

### Database locked error

```bash
# Stop all containers
docker-compose down

# Start again
docker-compose up -d
```

### Images not found (403 error)

Images are public, but if you get errors:

```bash
# Login to GitHub Container Registry (optional)
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# Pull images
docker-compose pull
```

### Port already in use

Edit `docker-compose.yml` to use different ports:

```yaml
ports:
  - "3001:80"  # Frontend on port 3001
  - "8001:8000"  # Backend on port 8001
```

## Security Considerations

1. **Change default ports** in production
2. **Use HTTPS** with valid SSL certificates
3. **Firewall**: Only expose necessary ports
4. **Strong passwords** for PostgreSQL
5. **Regular backups**
6. **Keep images updated**: `docker-compose pull`

## Performance Tips

1. **Use PostgreSQL** for better concurrency
2. **Add Redis** for caching (future enhancement)
3. **Limit logs**: Add to docker-compose.yml:
   ```yaml
   logging:
     driver: "json-file"
     options:
       max-size: "10m"
       max-file: "3"
   ```

## Need Help?

- **Issues**: https://github.com/mvelusce/habits-tracker/issues
- **Discussions**: https://github.com/mvelusce/habits-tracker/discussions
- **Documentation**: Check README.md

---

Happy tracking! 🎯

