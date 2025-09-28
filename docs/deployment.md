# Deployment Guide

This guide covers different deployment options for the Agentic AI Frictionless Parking System.

## Prerequisites

- Python 3.9+
- Docker (for containerized deployment)
- AWS CLI (for Lambda deployment)  
- kubectl (for Kubernetes deployment)

## Environment Setup

1. Clone the repository:
```bash
git clone https://github.com/salmansk858/agentic-ai-parking-system.git
cd agentic-ai-parking-system
```

2. Configure environment:
```bash
cp .env.example .env
# Edit .env with your API keys
```

3. Required API keys:
- `OPENAI_API_KEY` - OpenAI API access
- `GOOGLE_MAPS_API_KEY` - Google Maps integration
- `PARKING_API_KEY` - Parking data APIs  
- `SERPER_API_KEY` - Web search capabilities

## Local Development

### Using Scripts

```bash
# Setup development environment
./scripts/setup.sh

# Start development server
./scripts/run-dev.sh
```

### Manual Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies  
pip install -r requirements.txt

# Start FastAPI server
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

# Or start Streamlit interface
streamlit run examples/web_interface.py
```

Access the application:
- API: http://localhost:8000
- Web Interface: http://localhost:8501
- API Documentation: http://localhost:8000/docs

## Docker Deployment

### Development with Docker Compose

```bash
# Start development stack
./scripts/run-docker.sh

# Or manually:
cd docker
docker-compose -f docker-compose.dev.yml up --build
```

### Production with Docker Compose

```bash
# Production deployment
cd docker
docker-compose up -d --build

# View logs
docker-compose logs -f

# Scale services
docker-compose up -d --scale parking-system=3
```

Services available:
- **API Server**: http://localhost:8000
- **Web Interface**: http://localhost:8501  
- **Redis**: localhost:6379

## AWS Lambda Deployment

### Using Deployment Script

```bash
# Configure AWS credentials
aws configure

# Deploy to Lambda
./scripts/deploy-aws.sh
```

### Manual Lambda Setup

1. **Create Lambda Function:**
```bash
aws lambda create-function \
  --function-name agentic-parking-system \
  --runtime python3.11 \
  --role arn:aws:iam::ACCOUNT:role/lambda-execution-role \
  --handler lambda_handler.handler \
  --zip-file fileb://deployment-package.zip \
  --timeout 30 \
  --memory-size 512
```

2. **Create Lambda Handler (lambda_handler.py):**
```python
from mangum import Mangum
from src.main import app

handler = Mangum(app)
```

3. **Configure Environment Variables:**
```bash
aws lambda update-function-configuration \
  --function-name agentic-parking-system \
  --environment Variables='{
    "OPENAI_API_KEY":"your-key",
    "LOG_LEVEL":"INFO"
  }'
```

## Performance Tuning

### Application Level
```python
# Increase worker processes for production
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
```

### Database Optimization
- Use connection pooling
- Implement Redis caching
- Optimize database queries
- Consider read replicas for scale

### Load Balancing
- Use NGINX or cloud load balancers
- Implement health checks
- Configure proper timeouts
- Enable session affinity if needed

## Troubleshooting

### Common Issues

1. **Agent Initialization Failures**
```bash
# Check API keys
echo $OPENAI_API_KEY

# Verify model access
curl -H "Authorization: Bearer $OPENAI_API_KEY" \
  https://api.openai.com/v1/models
```

2. **Memory Issues**
```bash
# Increase container memory
docker run -m 2g your-image

# Monitor memory usage
docker stats
```

3. **Network Connectivity**
```bash
# Test API endpoints
curl http://localhost:8000/

# Check DNS resolution
nslookup api.openai.com
```

### Debug Mode

Enable debug logging:
```bash
export DEBUG=true
export LOG_LEVEL=DEBUG
python -m src.main
```

### Health Checks

Monitor system health:
```bash
# API health
curl http://localhost:8000/

# Agent status  
curl http://localhost:8000/agents

# System metrics
curl http://localhost:8000/system/metrics
```

## Scaling Considerations

### Horizontal Scaling
- Stateless application design
- Redis for session management
- Database connection pooling
- Load balancer configuration

### Vertical Scaling
- Monitor resource usage
- Adjust memory/CPU limits
- Optimize agent performance
- Cache frequently accessed data

For production deployments, consider implementing:
- Auto-scaling policies
- Circuit breakers
- Graceful shutdowns
- Blue-green deployments
- Disaster recovery procedures
