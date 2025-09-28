# FAIR-Agent Docker Deployment

This directory contains Docker configuration files for deploying the FAIR-Agent system in containerized environments.

## 🐳 Quick Start with Docker

### Prerequisites
- Docker (version 20.10 or higher)
- Docker Compose (version 2.0 or higher)

### Option 1: Using the Deployment Script (Recommended)

The easiest way to deploy FAIR-Agent with Docker:

```bash
# Make the script executable (if not already)
chmod +x docker-deploy.sh

# Build and start the system
./docker-deploy.sh start

# View logs
./docker-deploy.sh logs

# Stop the system
./docker-deploy.sh stop
```

### Option 2: Manual Docker Commands

```bash
# Build the image
docker build -t fair-agent:latest .

# Run the container
docker run -p 8000:8000 \
  -v $(pwd)/config:/app/config:ro \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/data:/app/data \
  fair-agent:latest
```

### Option 3: Using Docker Compose

```bash
# Start services in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 📋 Available Commands

The `docker-deploy.sh` script provides the following commands:

| Command | Description |
|---------|-------------|
| `build` | Build the Docker image |
| `start` | Build and start the web interface |
| `stop` | Stop all services |
| `restart` | Restart all services |
| `logs` | View real-time logs |
| `cli` | Run in interactive CLI mode |
| `status` | Show service status |
| `update` | Update and restart services |
| `cleanup` | Stop services and remove images |
| `help` | Show help message |

## 🔧 Configuration

### Environment Variables

The following environment variables can be configured:

- `DJANGO_SETTINGS_MODULE`: Django settings module (default: `webapp.settings`)
- `PYTHONPATH`: Python path (default: `/app`)

### Volume Mounts

The Docker setup uses volume mounts for persistence:

- `./config:/app/config:ro` - Configuration files (read-only)
- `./logs:/app/logs` - Log files (persistent)
- `./data:/app/data` - Model data and cache (persistent)
- `./webapp/db.sqlite3:/app/webapp/db.sqlite3` - Database file (persistent)

## 🚀 Deployment Modes

### Web Interface Mode (Default)
```bash
./docker-deploy.sh start
# Access at http://localhost:8000
```

### CLI Mode
```bash
./docker-deploy.sh cli
# Interactive command-line interface
```

### API Mode
The web interface includes REST API endpoints accessible at:
- `http://localhost:8000/api/query/process/` - Process queries
- `http://localhost:8000/api/metrics/` - Get FAIR metrics

## 🔍 Monitoring and Debugging

### View Logs
```bash
# All logs
./docker-deploy.sh logs

# Specific service logs
docker-compose logs fair-agent

# Follow logs in real-time
docker-compose logs -f
```

### Health Checks
The container includes built-in health checks:
```bash
# Check container health
docker ps
# Look for "healthy" status

# Manual health check
curl http://localhost:8000/
```

### Service Status
```bash
./docker-deploy.sh status
```

## 🐛 Troubleshooting

### Common Issues

1. **Port 8000 already in use**
   ```bash
   # Find process using port 8000
   lsof -i :8000
   # Kill the process or use a different port
   ```

2. **Permission denied for mounted volumes**
   ```bash
   # Fix permissions
   sudo chown -R $(id -u):$(id -g) logs data
   ```

3. **Container fails to start**
   ```bash
   # Check logs for errors
   ./docker-deploy.sh logs
   
   # Rebuild image
   ./docker-deploy.sh cleanup
   ./docker-deploy.sh build
   ```

4. **Database migration issues**
   ```bash
   # Run migrations manually
   docker-compose exec fair-agent python webapp/manage.py migrate
   ```

### Performance Tuning

For production deployments, consider:

1. **Resource Limits**: Add resource constraints to docker-compose.yml
   ```yaml
   services:
     fair-agent:
       deploy:
         resources:
           limits:
             memory: 2G
             cpus: '1.0'
   ```

2. **Environment Optimization**:
   ```yaml
   environment:
     - DJANGO_DEBUG=False
     - DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
   ```

## 🔐 Security Considerations

1. **Non-root User**: The container runs as a non-root user `fairagent`
2. **Read-only Mounts**: Configuration files are mounted read-only
3. **Network Isolation**: Uses custom Docker network
4. **Health Checks**: Built-in health monitoring

## 📦 Image Details

- **Base Image**: `python:3.11-slim`
- **Exposed Port**: 8000
- **Working Directory**: `/app`
- **User**: `fairagent` (non-root)
- **Health Check**: HTTP GET to `/`

## 🔄 Updates and Maintenance

### Update the System
```bash
# Pull latest code and rebuild
git pull
./docker-deploy.sh update
```

### Clean Up
```bash
# Remove all containers and images
./docker-deploy.sh cleanup

# Remove unused Docker resources
docker system prune -f
```

## 📊 Production Deployment

For production environments, consider using:

1. **Docker Swarm** or **Kubernetes** for orchestration
2. **Reverse proxy** (nginx) for SSL termination
3. **External database** (PostgreSQL) instead of SQLite
4. **Redis** for caching and session storage
5. **Environment-specific configurations**

Example production docker-compose.override.yml:
```yaml
version: '3.8'
services:
  fair-agent:
    environment:
      - DJANGO_DEBUG=False
      - DATABASE_URL=postgresql://user:pass@db:5432/fairagent
    depends_on:
      - db
      - redis
  
  db:
    image: postgres:13
    environment:
      POSTGRES_DB: fairagent
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  redis:
    image: redis:6-alpine
    
volumes:
  postgres_data:
```

## 📞 Support

For Docker-related issues:
1. Check the logs: `./docker-deploy.sh logs`
2. Verify Docker installation: `docker --version`
3. Check system resources: `docker system df`
4. Review container status: `./docker-deploy.sh status`