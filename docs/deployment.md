# ClinOps AI Deployment Guide

## Deployment Options

1. **Local Development** - Run directly with Python
2. **Docker** - Containerized deployment
3. **Docker Compose** - Full stack with dependencies
4. **Cloud** - AWS, Azure, GCP deployment

---

## 1. Local Development Deployment

### Prerequisites
- Python 3.12+
- Virtual environment tool (venv, uv, conda)
- Groq API key

### Steps

#### 1.1 Clone Repository
```bash
git clone <repository-url>
cd ClinOpsAI
```

#### 1.2 Create Virtual Environment
```bash
# Using venv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Or using uv (faster)
uv venv
.venv\Scripts\activate
```

#### 1.3 Install Dependencies
```bash
# Using pip
pip install -r requirements.txt

# Or using uv (faster)
uv pip install -r requirements.txt
```

#### 1.4 Configure Environment
```bash
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

#### 1.5 Run Application
```bash
python main.py
```

Application will be available at: `http://localhost:8000`

---

## 2. Docker Deployment

### Prerequisites
- Docker installed
- Groq API key

### Steps

#### 2.1 Build Image
```bash
docker build -t clinops-ai .
```

#### 2.2 Run Container
```bash
docker run -d \
  --name clinops-ai \
  -p 8000:8000 \
  -e GROQ_API_KEY=your_api_key_here \
  clinops-ai
```

#### 2.3 Check Logs
```bash
docker logs -f clinops-ai
```

#### 2.4 Stop Container
```bash
docker stop clinops-ai
docker rm clinops-ai
```

---

## 3. Docker Compose Deployment

### Prerequisites
- Docker and Docker Compose installed
- Groq API key

### Steps

#### 3.1 Configure Environment
```bash
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

#### 3.2 Start Services
```bash
docker-compose up -d
```

#### 3.3 View Logs
```bash
docker-compose logs -f
```

#### 3.4 Stop Services
```bash
docker-compose down
```

---

## 4. Cloud Deployment

### AWS EC2

#### 4.1 Launch EC2 Instance
- AMI: Ubuntu 22.04
- Instance Type: t3.medium (2 vCPU, 4GB RAM)
- Security Group: Allow port 8000

#### 4.2 Connect and Setup
```bash
ssh -i your-key.pem ubuntu@your-ec2-ip

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Clone repository
git clone <repository-url>
cd ClinOpsAI

# Set environment
echo "GROQ_API_KEY=your_key" > .env

# Run with Docker Compose
docker-compose up -d
```

### Azure Container Instances

```bash
# Login to Azure
az login

# Create resource group
az group create --name clinops-rg --location eastus

# Create container instance
az container create \
  --resource-group clinops-rg \
  --name clinops-ai \
  --image your-registry/clinops-ai:latest \
  --dns-name-label clinops-ai \
  --ports 8000 \
  --environment-variables GROQ_API_KEY=your_key
```

### Google Cloud Run

```bash
# Build and push image
gcloud builds submit --tag gcr.io/your-project/clinops-ai

# Deploy to Cloud Run
gcloud run deploy clinops-ai \
  --image gcr.io/your-project/clinops-ai \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GROQ_API_KEY=your_key
```

---

## Environment Variables

### Required
```bash
GROQ_API_KEY=your_groq_api_key_here
```

### Optional
```bash
LOG_LEVEL=DEBUG          # Logging level (DEBUG, INFO, WARNING, ERROR)
HOST=0.0.0.0            # Server host
PORT=8000               # Server port
RELOAD=true             # Auto-reload on code changes (development)
```

---

## Health Checks

### Docker Health Check
```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8000/health')"
```

### Kubernetes Readiness Probe
```yaml
readinessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 10
  periodSeconds: 5
```

### Kubernetes Liveness Probe
```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 30
  periodSeconds: 10
```

---

## Load Balancing

### Nginx Configuration

```nginx
upstream clinops {
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
    server 127.0.0.1:8003;
}

server {
    listen 80;
    server_name clinops.example.com;

    location / {
        proxy_pass http://clinops;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## SSL/TLS Configuration

### Using Let's Encrypt (Certbot)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d clinops.example.com

# Auto-renewal
sudo certbot renew --dry-run
```

### Nginx with SSL
```nginx
server {
    listen 443 ssl;
    server_name clinops.example.com;

    ssl_certificate /etc/letsencrypt/live/clinops.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/clinops.example.com/privkey.pem;

    location / {
        proxy_pass http://localhost:8000;
    }
}
```

---

## Monitoring

### Prometheus Metrics

Add to application (future):
```python
from prometheus_client import Counter, Histogram

request_count = Counter('clinops_requests_total', 'Total requests')
request_duration = Histogram('clinops_request_duration_seconds', 'Request duration')
```

### Grafana Dashboard

Import dashboard JSON for:
- Request rate
- Response time
- Error rate
- CPU/Memory usage

---

## Scaling

### Horizontal Scaling

```yaml
# docker-compose.yml
services:
  clinops-ai:
    image: clinops-ai:latest
    deploy:
      replicas: 3
    ports:
      - "8000-8002:8000"
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: clinops-ai
spec:
  replicas: 3
  selector:
    matchLabels:
      app: clinops-ai
  template:
    metadata:
      labels:
        app: clinops-ai
    spec:
      containers:
      - name: clinops-ai
        image: clinops-ai:latest
        ports:
        - containerPort: 8000
        env:
        - name: GROQ_API_KEY
          valueFrom:
            secretKeyRef:
              name: clinops-secrets
              key: groq-api-key
```

---

## Backup and Recovery

### Database Backup (Future)
```bash
# Backup
pg_dump clinops_db > backup.sql

# Restore
psql clinops_db < backup.sql
```

### Configuration Backup
```bash
# Backup environment and configs
tar -czf clinops-config-$(date +%Y%m%d).tar.gz .env docker-compose.yml
```

---

## Troubleshooting

### Container Won't Start
```bash
# Check logs
docker logs clinops-ai

# Check environment
docker exec clinops-ai env

# Verify image
docker inspect clinops-ai
```

### Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>
```

### Out of Memory
```bash
# Increase Docker memory limit
docker run -m 4g clinops-ai

# Or in docker-compose.yml
services:
  clinops-ai:
    mem_limit: 4g
```

---

## Security Best Practices

1. **Never commit `.env` file**
2. **Use secrets management** (AWS Secrets Manager, Azure Key Vault)
3. **Enable HTTPS** in production
4. **Implement rate limiting**
5. **Regular security updates**
6. **Monitor for vulnerabilities**
7. **Use non-root Docker user**
8. **Scan Docker images** for vulnerabilities

---

## Performance Tuning

### Uvicorn Workers
```bash
uvicorn api.main:app --workers 4 --host 0.0.0.0 --port 8000
```

### Gunicorn with Uvicorn
```bash
gunicorn api.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

---

## Maintenance

### Update Application
```bash
# Pull latest code
git pull

# Rebuild and restart
docker-compose down
docker-compose build
docker-compose up -d
```

### Clean Up
```bash
# Remove unused images
docker image prune -a

# Remove unused volumes
docker volume prune

# Clean system
docker system prune -a
```

---

## Cost Optimization

### Cloud Cost Estimates

**AWS EC2 (t3.medium)**
- Instance: $30/month
- Storage: $5/month
- Data transfer: $10/month
- **Total**: ~$45/month

**Google Cloud Run**
- Request-based pricing
- ~$0.40 per million requests
- **Total**: $5-20/month (estimate)

### Groq API Costs
- Check current Groq pricing
- Monitor usage
- Implement caching to reduce calls
