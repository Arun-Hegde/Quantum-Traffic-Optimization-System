# 🚀 Deployment Guide

Complete guide for deploying the Quantum Traffic Optimization System to production.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Local Development](#local-development)
- [Docker Deployment](#docker-deployment)
- [Cloud Deployment](#cloud-deployment)
- [Configuration](#configuration)
- [Monitoring](#monitoring)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

### System Requirements
- **OS**: Linux (Ubuntu 20.04+), macOS, or Windows with WSL2
- **CPU**: 4+ cores recommended
- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: 20GB free space
- **Python**: 3.11 or higher
- **Docker**: 20.10+ (for containerized deployment)
- **Docker Compose**: 2.0+

### External Services (Optional)
- **PostgreSQL**: 15+ (for production database)
- **Redis**: 7+ (for caching)
- **Google Maps API Key** (for real-time traffic)
- **OpenWeather API Key** (for weather data)

---

## Local Development

### 1. Clone Repository
```bash
git clone <repository-url>
cd quantum-traffic-optimization
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
```bash
cp .env.example .env
# Edit .env with your configuration
```

### 5. Initialize Database
```bash
python -c "from src.database.database import init_db; init_db()"
```

### 6. Run Application
```bash
# Option 1: One-click launcher
python run.py

# Option 2: Manual start
# Terminal 1 - API
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2 - Frontend
streamlit run frontend/app.py
```

### 7. Access Applications
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Frontend**: http://localhost:8501

---

## Docker Deployment

### Quick Start
```bash
# 1. Configure environment
cp .env.example .env
# Edit .env with your settings

# 2. Build and start all services
docker-compose up -d

# 3. Check status
docker-compose ps

# 4. View logs
docker-compose logs -f
```

### Services
The Docker Compose stack includes:
- **API** (FastAPI) - Port 8000
- **Frontend** (Streamlit) - Port 8501
- **PostgreSQL** - Port 5432
- **Redis** - Port 6379
- **Prometheus** - Port 9090
- **Grafana** - Port 3000

### Useful Commands
```bash
# Stop all services
docker-compose down

# Rebuild after code changes
docker-compose up -d --build

# View logs for specific service
docker-compose logs -f api

# Execute command in container
docker-compose exec api python -c "from src.database.database import init_db; init_db()"

# Scale API service
docker-compose up -d --scale api=4
```

---

## Cloud Deployment

### AWS Deployment

#### Using ECS (Elastic Container Service)

1. **Build and Push Docker Image**
```bash
# Login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Build image
docker build -t quantum-traffic-api .

# Tag image
docker tag quantum-traffic-api:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/quantum-traffic-api:latest

# Push image
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/quantum-traffic-api:latest
```

2. **Create ECS Task Definition**
```json
{
  "family": "quantum-traffic-api",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "containerDefinitions": [
    {
      "name": "api",
      "image": "<account-id>.dkr.ecr.us-east-1.amazonaws.com/quantum-traffic-api:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {"name": "DATABASE_URL", "value": "postgresql://..."},
        {"name": "REDIS_URL", "value": "redis://..."}
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/quantum-traffic-api",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

3. **Create ECS Service**
```bash
aws ecs create-service \
  --cluster quantum-traffic-cluster \
  --service-name quantum-traffic-api \
  --task-definition quantum-traffic-api \
  --desired-count 2 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx],assignPublicIp=ENABLED}"
```

#### Using EC2

1. **Launch EC2 Instance**
   - AMI: Ubuntu 22.04 LTS
   - Instance Type: t3.medium or larger
   - Security Group: Allow ports 22, 80, 443, 8000, 8501

2. **Install Docker**
```bash
sudo apt update
sudo apt install -y docker.io docker-compose
sudo usermod -aG docker ubuntu
```

3. **Deploy Application**
```bash
# Clone repository
git clone <repository-url>
cd quantum-traffic-optimization

# Configure environment
cp .env.example .env
nano .env  # Edit configuration

# Start services
docker-compose up -d
```

4. **Setup Nginx Reverse Proxy**
```nginx
# /etc/nginx/sites-available/quantum-traffic
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Google Cloud Platform (GCP)

#### Using Cloud Run

1. **Build and Push to Container Registry**
```bash
# Configure gcloud
gcloud auth configure-docker

# Build image
docker build -t gcr.io/<project-id>/quantum-traffic-api .

# Push image
docker push gcr.io/<project-id>/quantum-traffic-api
```

2. **Deploy to Cloud Run**
```bash
gcloud run deploy quantum-traffic-api \
  --image gcr.io/<project-id>/quantum-traffic-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars DATABASE_URL=postgresql://...,REDIS_URL=redis://...
```

### Azure Deployment

#### Using Azure Container Instances

```bash
# Create resource group
az group create --name quantum-traffic-rg --location eastus

# Create container
az container create \
  --resource-group quantum-traffic-rg \
  --name quantum-traffic-api \
  --image <registry>/quantum-traffic-api:latest \
  --dns-name-label quantum-traffic \
  --ports 8000 8501 \
  --environment-variables \
    DATABASE_URL=postgresql://... \
    REDIS_URL=redis://...
```

---

## Configuration

### Environment Variables

#### Required
```bash
# Database
DATABASE_URL=postgresql://user:password@host:5432/dbname

# Redis
REDIS_URL=redis://host:6379/0
```

#### Optional
```bash
# External APIs
GOOGLE_MAPS_API_KEY=your_key_here
OPENWEATHER_API_KEY=your_key_here
TOMTOM_API_KEY=your_key_here

# Quantum Settings
QAOA_REPS=2
QAOA_MAX_ITER=50

# Features
ENABLE_REAL_TIME_TRAFFIC=true
ENABLE_WEATHER_INTEGRATION=true
ENABLE_METRICS=true

# Security
SECRET_KEY=your-secret-key-change-in-production
API_KEY_ENABLED=false
ALLOWED_ORIGINS=https://yourdomain.com

# Monitoring
SENTRY_DSN=your_sentry_dsn_here
```

### Database Setup

#### PostgreSQL
```bash
# Create database
createdb traffic_optimization

# Run migrations
python -c "from src.database.database import init_db; init_db()"
```

#### Redis
```bash
# Start Redis
redis-server

# Or with Docker
docker run -d -p 6379:6379 redis:7-alpine
```

---

## Monitoring

### Prometheus Metrics

Access Prometheus at `http://localhost:9090`

**Key Metrics:**
- `optimization_runs_total` - Total optimization runs
- `optimization_duration_seconds` - Optimization latency
- `api_requests_total` - API request count
- `cache_hits_total` / `cache_misses_total` - Cache performance

### Grafana Dashboards

Access Grafana at `http://localhost:3000` (admin/admin)

**Pre-configured Dashboards:**
1. Traffic Optimization Overview
2. API Performance Metrics
3. Cache Performance
4. Database Queries

### Logging

Logs are stored in `logs/app.log` with rotation.

**View logs:**
```bash
# Docker
docker-compose logs -f api

# Local
tail -f logs/app.log
```

### Health Checks

```bash
# API health
curl http://localhost:8000/health

# Metrics
curl http://localhost:8000/metrics
```

---

## Troubleshooting

### Common Issues

#### 1. Database Connection Error
```
Error: could not connect to server
```
**Solution:**
- Check DATABASE_URL in .env
- Ensure PostgreSQL is running
- Verify network connectivity

#### 2. Redis Connection Error
```
Error: Error connecting to Redis
```
**Solution:**
- Check REDIS_URL in .env
- Ensure Redis is running
- Application will fallback to in-memory cache

#### 3. Quantum Optimization Timeout
```
Error: Quantum solver returned no result
```
**Solution:**
- Increase QAOA_MAX_ITER in .env
- Reduce QAOA_REPS for faster results
- Check system resources (CPU/RAM)

#### 4. API Key Errors
```
Error: Invalid API key
```
**Solution:**
- Verify API keys in .env
- Check API quota limits
- Disable real-time features if keys unavailable

### Performance Optimization

#### 1. Enable Caching
```bash
REDIS_URL=redis://localhost:6379/0
CACHE_TTL=300
```

#### 2. Scale API Workers
```bash
# Docker Compose
docker-compose up -d --scale api=4

# Uvicorn
uvicorn api.main:app --workers 4
```

#### 3. Database Optimization
```sql
-- Create indexes
CREATE INDEX idx_optimization_runs_city ON optimization_runs(city);
CREATE INDEX idx_optimization_runs_timestamp ON optimization_runs(timestamp);
```

#### 4. Enable CDN
Use CloudFlare or AWS CloudFront for static assets.

---

## Security Checklist

- [ ] Change default SECRET_KEY
- [ ] Enable API key authentication
- [ ] Configure CORS allowed origins
- [ ] Use HTTPS in production
- [ ] Secure database credentials
- [ ] Enable rate limiting
- [ ] Setup firewall rules
- [ ] Regular security updates
- [ ] Enable audit logging
- [ ] Backup database regularly

---

## Backup & Recovery

### Database Backup
```bash
# PostgreSQL
pg_dump -U postgres traffic_optimization > backup.sql

# Restore
psql -U postgres traffic_optimization < backup.sql
```

### Docker Volumes
```bash
# Backup volumes
docker run --rm -v quantum-traffic-optimization_postgres_data:/data -v $(pwd):/backup ubuntu tar czf /backup/postgres_backup.tar.gz /data

# Restore volumes
docker run --rm -v quantum-traffic-optimization_postgres_data:/data -v $(pwd):/backup ubuntu tar xzf /backup/postgres_backup.tar.gz -C /
```

---

## Support

For deployment issues:
- 📧 Email: devops@example.com
- 💬 Slack: #deployment-support
- 📖 Docs: https://docs.example.com/deployment
