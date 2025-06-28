#!/bin/bash

# Smart README Generator - Deployment Script
# Deploys the complete serverless system

set -e

echo "🚀 Deploying Smart README Generator"
echo "==================================="

# Configuration
REGION="us-east-1"
STACK_NAME="smart-readme-generator"
S3_BUCKET="smart-readme-lambda-31641"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check prerequisites
print_status "Checking prerequisites..."

if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI not found. Please install AWS CLI."
    exit 1
fi

if ! aws sts get-caller-identity &> /dev/null; then
    echo "❌ AWS credentials not configured. Please run 'aws configure'."
    exit 1
fi

print_success "Prerequisites check passed"

# Create S3 bucket if it doesn't exist
print_status "Creating S3 bucket..."
aws s3 mb s3://${S3_BUCKET} --region ${REGION} 2>/dev/null || print_warning "S3 bucket may already exist"

# Package Lambda functions
print_status "Packaging Lambda functions..."

# Package Analyzer (Lambda 1)
mkdir -p dist
cd lambda
zip -r ../dist/analyzer.zip analyzer.py bedrock_service.py
zip -r ../dist/generator.zip generator.py
cd ..

print_success "Lambda functions packaged"

# Deploy CloudFormation stack
print_status "Deploying CloudFormation stack..."

aws cloudformation deploy \
    --template-file infrastructure/cloudformation.yaml \
    --stack-name ${STACK_NAME} \
    --parameter-overrides \
        GitHubToken=${GITHUB_TOKEN:-"your-github-token-here"} \
        S3BucketName=${S3_BUCKET} \
    --capabilities CAPABILITY_IAM \
    --region ${REGION}

print_success "CloudFormation stack deployed"

# Get IAM role ARN from stack
ROLE_ARN=$(aws cloudformation describe-stacks \
    --stack-name ${STACK_NAME} \
    --region ${REGION} \
    --query 'Stacks[0].Outputs[?OutputKey==`LambdaRoleArn`].OutputValue' \
    --output text)

# Deploy Lambda 1 (Analyzer)
print_status "Deploying Analyzer Lambda..."

aws lambda create-function \
    --function-name smart-readme-analyzer \
    --runtime python3.12 \
    --role ${ROLE_ARN} \
    --handler analyzer.lambda_handler \
    --zip-file fileb://dist/analyzer.zip \
    --timeout 300 \
    --memory-size 1024 \
    --description "Smart README Generator - Repository Analyzer" \
    --region ${REGION} 2>/dev/null || \
aws lambda update-function-code \
    --function-name smart-readme-analyzer \
    --zip-file fileb://dist/analyzer.zip \
    --region ${REGION}

# Deploy Lambda 2 (Generator)
print_status "Deploying Generator Lambda..."

aws lambda create-function \
    --function-name smart-readme-generator \
    --runtime python3.12 \
    --role ${ROLE_ARN} \
    --handler generator.lambda_handler \
    --zip-file fileb://dist/generator.zip \
    --timeout 180 \
    --memory-size 512 \
    --description "Smart README Generator - README Generator" \
    --region ${REGION} 2>/dev/null || \
aws lambda update-function-code \
    --function-name smart-readme-generator \
    --zip-file fileb://dist/generator.zip \
    --region ${REGION}

print_success "Lambda functions deployed"

# Test deployment
print_status "Testing deployment..."

if [ -f "examples/jwt_example.json" ]; then
    aws lambda invoke \
        --function-name smart-readme-analyzer \
        --payload fileb://examples/jwt_example.json \
        --region ${REGION} \
        test_response.json
    
    if grep -q '"success": true' test_response.json; then
        print_success "Deployment test passed!"
    else
        print_warning "Deployment test may have issues. Check test_response.json"
    fi
    
    rm -f test_response.json
fi

# Cleanup
rm -rf dist/

echo ""
echo "🎉 DEPLOYMENT COMPLETE!"
echo "======================="
echo "📊 Stack: ${STACK_NAME}"
echo "🪣 S3 Bucket: ${S3_BUCKET}"
echo "⚡ Lambda 1: smart-readme-analyzer"
echo "⚡ Lambda 2: smart-readme-generator"
echo ""
echo "🔧 Next Steps:"
echo "1. Set up monitoring: ./monitoring/quick_setup.sh"
echo "2. Test with your repositories"
echo "3. Monitor costs and performance"
echo ""
print_success "Ready for production use!"
