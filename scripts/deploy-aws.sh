#!/bin/bash
# AWS Lambda deployment script

set -e

echo "☁️ Deploying to AWS Lambda..."

# Check AWS CLI
if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI not found. Please install it first."
    exit 1
fi

# Check environment variables
if [ -z "$AWS_ACCESS_KEY_ID" ] || [ -z "$AWS_SECRET_ACCESS_KEY" ]; then
    echo "❌ AWS credentials not set. Please configure AWS CLI."
    exit 1
fi

# Create deployment package
echo "📦 Creating deployment package..."
rm -rf lambda-package deployment-package.zip

mkdir lambda-package
cp -r src lambda-package/
cp requirements.txt lambda-package/

# Install dependencies
cd lambda-package
pip install -r requirements.txt -t . --platform linux_x86_64 --only-binary=all

# Create Lambda handler
cat > lambda_handler.py << 'EOF'
"""AWS Lambda handler for the agentic parking system."""
from mangum import Mangum
from src.main import app

handler = Mangum(app)
EOF

# Create zip file
zip -r ../deployment-package.zip . -x "*.pyc" "__pycache__/*"
cd ..

# Deploy to Lambda
echo "🚀 Deploying to AWS Lambda..."
aws lambda update-function-code \
    --function-name agentic-parking-system \
    --zip-file fileb://deployment-package.zip

echo "✅ Deployment completed!"

# Cleanup
rm -rf lambda-package deployment-package.zip
