#!/bin/bash

# Q Developer + Bedrock Production Deployment Script

set -e

echo "🚀 Deploying Q Developer + Bedrock AI Code Intelligence System"
echo "================================================================"

# Configuration
STACK_NAME="q-developer-production-stack"
REGION="us-east-1"
GITHUB_TOKEN="${GITHUB_TOKEN:-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}"

echo "📋 Configuration:"
echo "  Stack Name: $STACK_NAME"
echo "  Region: $REGION"
echo "  GitHub Token: ${GITHUB_TOKEN:0:20}..."

# Deploy CloudFormation stack
echo ""
echo "🏗️  Deploying CloudFormation stack..."
aws cloudformation deploy \
    --template-file infrastructure/cloudformation.yaml \
    --stack-name $STACK_NAME \
    --parameter-overrides GitHubToken=$GITHUB_TOKEN \
    --capabilities CAPABILITY_NAMED_IAM \
    --region $REGION

# Get stack outputs
echo ""
echo "📊 Getting stack outputs..."
LAMBDA_ARN=$(aws cloudformation describe-stacks \
    --stack-name $STACK_NAME \
    --region $REGION \
    --query 'Stacks[0].Outputs[?OutputKey==`LambdaFunctionArn`].OutputValue' \
    --output text)

API_ENDPOINT=$(aws cloudformation describe-stacks \
    --stack-name $STACK_NAME \
    --region $REGION \
    --query 'Stacks[0].Outputs[?OutputKey==`APIEndpoint`].OutputValue' \
    --output text)

S3_BUCKET=$(aws cloudformation describe-stacks \
    --stack-name $STACK_NAME \
    --region $REGION \
    --query 'Stacks[0].Outputs[?OutputKey==`S3BucketName`].OutputValue' \
    --output text)

# Update Lambda function code
echo ""
echo "📦 Updating Lambda function code..."
aws lambda update-function-code \
    --function-name q-developer-code-analyzer \
    --zip-file fileb://deployment/q-developer-production.zip \
    --region $REGION

echo ""
echo "✅ Deployment completed successfully!"
echo "================================================================"
echo "🎯 Production Endpoints:"
echo "  API Gateway: $API_ENDPOINT"
echo "  Lambda ARN: $LAMBDA_ARN"
echo "  S3 Bucket: $S3_BUCKET"
echo ""
echo "🧪 Test your deployment:"
echo "curl -X POST \"$API_ENDPOINT\" -H \"Content-Type: application/json\" -d '{\"github_url\": \"https://github.com/user/repo\"}'"
echo ""
echo "🎉 Q Developer + Bedrock system is now live in production!"
