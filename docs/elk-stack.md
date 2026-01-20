# ClinOps AI with ELK Stack - Deployment Guide

## Overview

This Docker Compose setup includes:
- **ClinOps AI** - Medical document analysis application
- **Elasticsearch** - Log storage and search
- **Logstash** - Log processing and transformation
- **Kibana** - Log visualization and dashboards
- **Filebeat** - Log shipping

---

## Services

| Service | Port | Description |
|---------|------|-------------|
| ClinOps AI | 8000 | Main application |
| Elasticsearch | 9200, 9300 | Log storage |
| Logstash | 5000, 9600 | Log processing |
| Kibana | 5601 | Web UI for logs |

---

## Quick Start

### 1. Prerequisites
```bash
# Ensure you have:
- Docker
- Docker Compose
- 4GB+ RAM available
- GROQ API Key
```

### 2. Configuration
```bash
# Create .env file
cp .env.example .env

# Edit .env and add your GROQ_API_KEY
GROQ_API_KEY=your_api_key_here
ENVIRONMENT=production
```

### 3. Start Services
```bash
# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

### 4. Access Services

- **ClinOps AI**: http://localhost:8000
- **Kibana**: http://localhost:5601
- **Elasticsearch**: http://localhost:9200

---

## Accessing Logs in Kibana

### First Time Setup

1. **Open Kibana**: http://localhost:5601

2. **Create Index Pattern**:
   - Go to "Stack Management" → "Index Patterns"
   - Click "Create index pattern"
   - Enter: `clinops-ai-*`
   - Select timestamp field: `@timestamp`
   - Click "Create index pattern"

3. **View Logs**:
   - Go to "Discover"
   - Select the `clinops-ai-*` index pattern
   - View real-time logs!

### Useful Queries

#### View All Errors
```
level: "ERROR"
```

#### View Urgency Detections
```
event_type: "urgency_detection"
```

#### View Specific Agent Logs
```
logger: "src.workflow"
```

#### View Analysis Events
```
event_type: "analysis"
```

---

## Creating Dashboards

### 1. Request Volume Dashboard

1. Go to Kibana → "Dashboard" → "Create dashboard"
2. Add visualization: "Count of requests over time"
3. Set time range
4. Save dashboard

### 2. Error Rate Dashboard

1. Create visualization
2. Filter by `level: "ERROR"`
3. Group by time
4. Calculate rate
5. Add to dashboard

### 3. Urgency Distribution

1. Create pie chart
2. Split slices by urgency level
3. Filter by event_type: "urgency_detection"
4. Save

---

## Log Management

### View Real-time Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f clinops-ai

# Elasticsearch only
docker-compose logs -f elasticsearch
```

### Check Log Files
```bash
# Application logs
ls -lh logs/

# Elasticsearch data
docker volume inspect clinopsai_elasticsearch-data
```

### Clean Up Old Logs
```bash
# Delete indices older than 30 days (run in Kibana Dev Tools)
DELETE /clinops-ai-*
{
  "query": {
    "range": {
      "@timestamp": {
        "lt": "now-30d"
      }
    }
  }
}
```

---

## Monitoring

### Health Checks

```bash
# Check all services
docker-compose ps

# Check Elasticsearch health
curl http://localhost:9200/_cluster/health?pretty

# Check Kibana health
curl http://localhost:5601/api/status

# Check ClinOps AI health
curl http://localhost:8000/health
```

### Resource Usage

```bash
# View container stats
docker stats

# View disk usage
docker system df

# View volume usage
docker volume ls
```

---

## Troubleshooting

### Elasticsearch Won't Start

**Problem**: Elasticsearch container exits immediately

**Solution**: Increase Docker memory
```bash
# Docker Desktop: Settings → Resources → Memory → 4GB+
```

Or modify docker-compose.yml:
```yaml
elasticsearch:
  environment:
    - "ES_JAVA_OPTS=-Xms256m -Xmx256m"  # Reduce memory
```

### No Logs Appearing in Kibana

**Check**:
1. Verify index exists:
   ```bash
   curl http://localhost:9200/_cat/indices?v
   ```

2. Check Logstash is processing:
   ```bash
   docker-compose logs logstash
   ```

3. Verify Filebeat is running:
   ```bash
   docker-compose logs filebeat
   ```

### Port Conflicts

**Problem**: Port 9200 or 5601 already in use

**Solution**: Change port in docker-compose.yml
```yaml
elasticsearch:
  ports:
    - "9201:9200"  # Use different host port
```

---

## Scaling

### Scale ClinOps AI

```bash
docker-compose up -d --scale clinops-ai=3
```

### Add Load Balancer

```yaml
# Add to docker-compose.yml
nginx:
  image: nginx:alpine
  ports:
    - "80:80"
  volumes:
    - ./nginx.conf:/etc/nginx/nginx.conf
  depends_on:
    - clinops-ai
```

---

## Backup and Restore

### Backup Elasticsearch Data

```bash
# Create snapshot repository
curl -X PUT "localhost:9200/_snapshot/backups" -H 'Content-Type: application/json' -d'
{
  "type": "fs",
  "settings": {
    "location": "/usr/share/elasticsearch/backup"
  }
}
'

# Create snapshot
curl -X PUT "localhost:9200/_snapshot/backups/snapshot_1?wait_for_completion=true"
```

### Restore Data

```bash
curl -X POST "localhost:9200/_snapshot/backups/snapshot_1/_restore"
```

---

## Production Considerations

### 1. Security

- Enable Elasticsearch security (xpack.security)
- Use environment variables for secrets
- Implement authentication
- Use HTTPS/TLS

### 2. Performance

- Adjust heap sizes based on available RAM
- Use SSD for Elasticsearch data
- Configure index lifecycle management
- Implement log rotation

### 3. High Availability

- Run multiple Elasticsearch nodes
- Use external load balancer
- Implement proper monitoring
- Set up alerts

---

## Stopping Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (WARNING: deletes all data)
docker-compose down -v

# Stop specific service
docker-compose stop clinops-ai
```

---

## Resource Requirements

### Minimum
- **RAM**: 4GB
- **Disk**: 20GB
- **CPU**: 2 cores

### Recommended
- **RAM**: 8GB+
- **Disk**: 50GB+ SSD
- **CPU**: 4+ cores

---

## Support

For issues:
1. Check logs: `docker-compose logs`
2. Verify health: `docker-compose ps`
3. Check resources: `docker stats`
4. Review documentation
5. Create GitHub issue

---

## Additional Resources

- [Elasticsearch Documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html)
- [Logstash Documentation](https://www.elastic.co/guide/en/logstash/current/index.html)
- [Kibana Documentation](https://www.elastic.co/guide/en/kibana/current/index.html)
- [Filebeat Documentation](https://www.elastic.co/guide/en/beats/filebeat/current/index.html)
