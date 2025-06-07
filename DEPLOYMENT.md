# 🚀 Deployment Guide

## Production Deployment Options

### 🐳 **Docker Deployment (Recommended)**

#### **1. Create Docker Compose**
```yaml
# docker-compose.yml
version: '3.8'

services:
  backend:
    build: ./langserve_backend
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=production
      - SECRET_KEY=${SECRET_KEY}
    volumes:
      - ./data:/app/data
    restart: unless-stopped

  frontend:
    build: ./streamlit_ui
    ports:
      - "8501:8501"
    environment:
      - BACKEND_URL=http://backend:8000
    depends_on:
      - backend
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - frontend
      - backend
    restart: unless-stopped
```

#### **2. Build and Deploy**
```bash
# Production deployment
docker-compose -f docker-compose.prod.yml up -d

# Development deployment
docker-compose up -d
```

### ☁️ **Cloud Deployment**

#### **AWS Deployment**
```bash
# Using AWS ECS
aws ecs create-cluster --cluster-name medical-diagnostics
aws ecs register-task-definition --cli-input-json file://task-definition.json
aws ecs create-service --cluster medical-diagnostics --service-name medical-app
```

#### **Google Cloud Platform**
```bash
# Using Google Cloud Run
gcloud run deploy medical-backend --source ./langserve_backend --port 8000
gcloud run deploy medical-frontend --source ./streamlit_ui --port 8501
```

#### **Azure Container Instances**
```bash
# Using Azure CLI
az container create --resource-group medical-rg --name medical-app
```

### 🔧 **Environment Configuration**

#### **Production Environment Variables**
```bash
# Security
SECRET_KEY=your-production-secret-key-256-bit
SESSION_TIMEOUT=7200
MAX_LOGIN_ATTEMPTS=5
LOCKOUT_DURATION=600

# Database
DB_TYPE=postgresql
DB_HOST=your-db-host
DB_PORT=5432
DB_NAME=medical_diagnostics_prod
DB_USERNAME=medical_user
DB_PASSWORD=secure-db-password

# OAuth Providers
GOOGLE_CLIENT_ID=your-production-google-client-id
GOOGLE_CLIENT_SECRET=your-production-google-secret
FIREBASE_API_KEY=your-production-firebase-key

# Monitoring
SENTRY_DSN=your-sentry-dsn
LOG_LEVEL=INFO
ENABLE_METRICS=true

# SSL/TLS
SSL_CERT_PATH=/etc/ssl/certs/medical-app.crt
SSL_KEY_PATH=/etc/ssl/private/medical-app.key
```

### 🛡️ **Security Checklist**

- [ ] **Change Default Passwords**: Update all default credentials
- [ ] **SSL/TLS Certificates**: Enable HTTPS with valid certificates
- [ ] **Environment Variables**: Use secure secret management
- [ ] **Database Security**: Enable encryption at rest and in transit
- [ ] **Network Security**: Configure firewalls and VPCs
- [ ] **Access Control**: Implement proper IAM policies
- [ ] **Monitoring**: Set up logging and alerting
- [ ] **Backup Strategy**: Implement automated backups

### 📊 **Monitoring & Logging**

#### **Application Monitoring**
```python
# Add to requirements.txt
sentry-sdk[fastapi]==1.38.0
prometheus-client==0.19.0
```

#### **Health Checks**
```bash
# Backend health check
curl http://localhost:8000/health

# Frontend health check
curl http://localhost:8501/healthz
```

#### **Log Aggregation**
```yaml
# docker-compose.yml logging section
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"
```

### 🔄 **CI/CD Pipeline**

#### **GitHub Actions Example**
```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Tests
        run: |
          python -m pytest langserve_backend/tests/
          
  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to AWS
        run: |
          aws ecs update-service --cluster medical-diagnostics
```

### 📈 **Scaling Considerations**

#### **Horizontal Scaling**
- Load balancer configuration
- Database connection pooling
- Session store (Redis/Memcached)
- CDN for static assets

#### **Performance Optimization**
- API response caching
- Database query optimization
- Async processing for AI calls
- Resource monitoring and auto-scaling

### 🔧 **Maintenance**

#### **Regular Tasks**
```bash
# Database backup
pg_dump medical_diagnostics > backup_$(date +%Y%m%d).sql

# Log rotation
logrotate /etc/logrotate.d/medical-app

# Security updates
docker-compose pull && docker-compose up -d

# Health monitoring
curl -f http://localhost:8000/health || exit 1
```

#### **Troubleshooting**
```bash
# Check container logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Database connection test
docker exec -it medical_db psql -U medical_user -d medical_diagnostics

# Performance monitoring
docker stats
```

### 📋 **Post-Deployment Checklist**

- [ ] **Functionality Testing**: All features work correctly
- [ ] **Performance Testing**: Response times are acceptable
- [ ] **Security Testing**: Vulnerability scanning completed
- [ ] **Backup Verification**: Backup and restore procedures tested
- [ ] **Monitoring Setup**: Alerts and dashboards configured
- [ ] **Documentation**: Deployment procedures documented
- [ ] **Team Training**: Operations team trained on maintenance

### 🆘 **Emergency Procedures**

#### **Rollback Strategy**
```bash
# Quick rollback to previous version
docker-compose down
docker-compose -f docker-compose.backup.yml up -d
```

#### **Incident Response**
1. **Identify**: Monitor alerts and logs
2. **Assess**: Determine impact and severity
3. **Respond**: Execute appropriate response plan
4. **Recover**: Restore service functionality
5. **Review**: Post-incident analysis and improvements
