# SmartReadme API Documentation

## Overview
The SmartReadme API provides AI-powered README generation for GitHub repositories using AWS serverless architecture. The system processes repositories through a Step Functions workflow that orchestrates Lambda functions for analysis, storage, and notifications.

## Base URL
```
https://ccki297o82.execute-api.us-east-1.amazonaws.com/prod
```

## Authentication
- **Type**: API Key (Header)
- **Header**: `x-api-key`
- **Note**: API key required for all endpoints

---

## Endpoints

### 1. Generate README

**Endpoint**: `POST /generate`

**Description**: Initiates README generation for a GitHub repository using the complete Step Functions workflow.

**Request Headers**:
```
Content-Type: application/json
x-api-key: YOUR_API_KEY
```

**Request Body**:
```json
{
  "github_url": "https://github.com/username/repository",
  "user_email": "user@example.com"
}
```

**Request Parameters**:
- `github_url` (string, required): Full GitHub repository URL
- `user_email` (string, required): Email address for completion notification

**Response** (202 Accepted):
```json
{
  "statusCode": 202,
  "body": {
    "success": true,
    "message": "README generation started",
    "execution_arn": "arn:aws:states:us-east-1:695221387268:execution:smart-readme-generator-workflow:uuid",
    "github_url": "https://github.com/username/repository",
    "user_email": "user@example.com",
    "estimated_completion": "30-60 seconds"
  }
}
```

**Error Response** (400 Bad Request):
```json
{
  "statusCode": 400,
  "body": {
    "success": false,
    "error": "Invalid GitHub URL format",
    "message": "Please provide a valid GitHub repository URL"
  }
}
```

---

### 2. Check Generation Status

**Endpoint**: `GET /status/{execution_id}`

**Description**: Check the status of a README generation workflow execution.

**Request Headers**:
```
x-api-key: YOUR_API_KEY
```

**Path Parameters**:
- `execution_id` (string, required): Step Functions execution ID

**Response** (200 OK):
```json
{
  "statusCode": 200,
  "body": {
    "status": "SUCCEEDED",
    "github_url": "https://github.com/username/repository",
    "user_email": "user@example.com",
    "readme_content": "# Project Title\n\n...",
    "readme_url": "https://smart-readme-files.s3.amazonaws.com/readmes/uuid.md",
    "readme_length": 2847,
    "s3_location": "s3://smart-readme-files/readmes/uuid.md",
    "processing_time": "28.5 seconds",
    "files_analyzed": 15,
    "analysis_method": "enhanced_cache_busting",
    "version": "3.2_cache_busting",
    "confidence_score": 95,
    "timestamp": "2025-07-06T07:00:00Z"
  }
}
```

**Status Values**:
- `RUNNING`: Workflow in progress
- `SUCCEEDED`: README generated successfully
- `FAILED`: Generation failed
- `TIMED_OUT`: Workflow exceeded timeout
- `ABORTED`: Workflow was cancelled

---

### 3. Direct Lambda Invocation (Development)

**Endpoint**: `POST /lambda/generate`

**Description**: Direct invocation of the fresh-readme-generator Lambda function (bypasses Step Functions).

**Request Headers**:
```
Content-Type: application/json
x-api-key: YOUR_API_KEY
```

**Request Body**:
```json
{
  "github_url": "https://github.com/username/repository"
}
```

**Response** (200 OK):
```json
{
  "statusCode": 200,
  "body": {
    "success": true,
    "data": {
      "readme_content": "# Project Title\n\n...",
      "download_url": "https://smart-readme-files.s3.amazonaws.com/readmes/uuid.md",
      "readme_length": 2847,
      "s3_location": "s3://smart-readme-files/readmes/uuid.md",
      "processing_time": "28.5 seconds",
      "files_analyzed": 15,
      "analysis_method": "enhanced_cache_busting",
      "version": "3.2_cache_busting"
    }
  }
}
```

---

### 4. Get Generation History

**Endpoint**: `GET /history`

**Description**: Retrieve generation history and analytics from DynamoDB.

**Request Headers**:
```
x-api-key: YOUR_API_KEY
```

**Query Parameters**:
- `limit` (integer, optional): Number of records to return (default: 10, max: 100)
- `github_url` (string, optional): Filter by specific repository URL

**Response** (200 OK):
```json
{
  "statusCode": 200,
  "body": {
    "success": true,
    "data": {
      "total_generations": 2000,
      "recent_generations": [
        {
          "generation_id": "uuid",
          "github_url": "https://github.com/username/repository",
          "user_email": "user@example.com",
          "timestamp": "2025-07-06T07:00:00Z",
          "status": "SUCCESS",
          "processing_time": "28.5 seconds",
          "files_analyzed": 15,
          "readme_length": 2847,
          "confidence_score": 95
        }
      ]
    }
  }
}
```

---

## Workflow Architecture

The API integrates with the following AWS services:

### Step Functions Workflow
1. **AnalyzeRepository**: Invokes `fresh-readme-generator` Lambda
2. **ParseAnalysisResponse**: Processes Lambda response
3. **CheckAnalysisSuccess**: Validates generation success
4. **UpdateDynamoDB**: Stores analytics via `smart-readme-dynamodb-handler`
5. **SendEmailNotification**: Sends completion email via `readme-email-notification`
6. **ProcessingComplete**: Returns final response

### Lambda Functions
- **fresh-readme-generator**: Main AI engine (Python 3.12, 1024MB, 300s timeout)
- **smart-readme-dynamodb-handler**: Analytics storage (Python 3.12, 256MB, 30s timeout)
- **readme-email-notification**: Email service (Python 3.12, 256MB, 30s timeout)

### Supporting Services
- **Amazon Bedrock**: Claude Sonnet 4 AI processing
- **DynamoDB**: Analytics and generation history
- **S3 + CloudFront**: README file storage with cache-busting
- **SES**: Email notifications

---

## Error Handling

### Common Error Codes

**400 Bad Request**
- Invalid GitHub URL format
- Missing required parameters
- Malformed JSON request

**401 Unauthorized**
- Missing or invalid API key

**403 Forbidden**
- API key lacks required permissions

**429 Too Many Requests**
- Rate limit exceeded (100 requests/minute)

**500 Internal Server Error**
- Lambda function failure
- Step Functions execution error
- AWS service unavailability

**503 Service Unavailable**
- Temporary service maintenance
- High load conditions

### Error Response Format
```json
{
  "statusCode": 400,
  "body": {
    "success": false,
    "error": "ERROR_CODE",
    "message": "Human-readable error description",
    "timestamp": "2025-07-06T07:00:00Z",
    "request_id": "uuid"
  }
}
```

---

## Rate Limits

- **Generate README**: 10 requests/minute per API key
- **Status Check**: 100 requests/minute per API key
- **History**: 50 requests/minute per API key
- **Direct Lambda**: 5 requests/minute per API key (development only)

---

## Performance Metrics

- **Average Processing Time**: 28.5 seconds
- **Success Rate**: 98.7%
- **Accuracy Rate**: 95%
- **Supported File Types**: 50+ programming languages
- **Maximum Repository Size**: 100MB
- **Maximum Files Analyzed**: 100 files per repository

---

## Examples

### cURL Examples

**Generate README**:
```bash
curl -X POST https://ccki297o82.execute-api.us-east-1.amazonaws.com/prod/generate \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{
    "github_url": "https://github.com/microsoft/calculator",
    "user_email": "developer@example.com"
  }'
```

**Check Status**:
```bash
curl -X GET https://ccki297o82.execute-api.us-east-1.amazonaws.com/prod/status/execution-uuid \
  -H "x-api-key: YOUR_API_KEY"
```

### JavaScript Examples

**Generate README**:
```javascript
const response = await fetch('https://ccki297o82.execute-api.us-east-1.amazonaws.com/prod/generate', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'x-api-key': 'YOUR_API_KEY'
  },
  body: JSON.stringify({
    github_url: 'https://github.com/microsoft/calculator',
    user_email: 'developer@example.com'
  })
});

const result = await response.json();
console.log(result);
```

---

## Support

For API support and questions:
- **Documentation**: This file
- **Live Demo**: [smart-readme-gen.vercel.app](https://smart-readme-gen.vercel.app/)
- **GitHub**: Repository issues and discussions

---

**Last Updated**: June 28, 2025  
**API Version**: 3.2   
**Deployment Region**: us-east-1
