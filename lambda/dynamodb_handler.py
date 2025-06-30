import json
import boto3
import logging
from datetime import datetime
from decimal import Decimal
from botocore.exceptions import ClientError

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize DynamoDB client with CORRECT TABLE NAME
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('smart-readme-gen-records')  # CORRECT TABLE NAME

def lambda_handler(event, context):
    """
    DynamoDB handler for Smart README Generator
    Uses table: smart-readme-gen-records
    """
    
    logger.info(f"🔍 DynamoDB Handler received event: {json.dumps(event, default=str)}")
    
    try:
        # Handle different event sources
        if 'Records' in event:
            # Handle Step Functions via EventBridge/SQS
            return handle_step_functions_records(event['Records'])
        elif 'httpMethod' in event:
            # Handle direct API Gateway calls
            return handle_api_gateway_request(event)
        elif 'user_email' in event and 'github_url' in event:
            # Handle direct Step Functions completion event
            return handle_step_functions_completion(event)
        else:
            # Handle raw Step Functions data
            return handle_step_functions_completion(event)
            
    except Exception as e:
        logger.error(f"❌ Error in DynamoDB handler: {str(e)}")
        return {
            'statusCode': 500,
            'headers': get_cors_headers(),
            'body': json.dumps({
                'error': 'Internal server error',
                'message': str(e)
            })
        }

def handle_step_functions_completion(event_data):
    """Handle Step Functions completion event and save to DynamoDB"""
    
    logger.info(f"🔍 Processing Step Functions completion: {json.dumps(event_data, default=str)}")
    
    try:
        # Extract required fields from Step Functions output
        user_email = event_data.get('user_email')
        github_url = event_data.get('github_url')
        request_id = event_data.get('request_id')
        
        if not all([user_email, github_url, request_id]):
            logger.error(f"❌ Missing required fields: user_email={user_email}, github_url={github_url}, request_id={request_id}")
            return {'error': 'Missing required fields: user_email, github_url, request_id'}
        
        # Check for duplicate repo URL first
        if check_duplicate_repo(github_url):
            logger.warning(f"⚠️ Duplicate repo URL detected: {github_url}")
            return {
                'statusCode': 409,
                'message': 'Repository already processed',
                'duplicate': True
            }
        
        # Extract analysis data
        analysis_data = event_data.get('ai_analysis', {})
        readme_data = event_data.get('readme_generation', {})
        
        # Build the DynamoDB item
        current_time = datetime.utcnow().isoformat()
        
        item = {
            'userId': user_email,
            'requestId': request_id,
            'repoUrl': github_url,
            'repoName': extract_repo_name(github_url),
            'status': 'completed',
            'createdAt': current_time,
            'completedAt': current_time,
            'generationTimestamp': current_time,
            
            # Analysis data
            'projectType': analysis_data.get('project_type', 'Unknown'),
            'primaryLanguage': analysis_data.get('primary_language', 'Unknown'),
            'frameworks': analysis_data.get('frameworks', []),
            'confidence': {
                'projectType': Decimal(str(analysis_data.get('confidence', 0.0))),
                'language': Decimal(str(analysis_data.get('language_confidence', 0.0)))
            },
            'frameworkConfidence': {
                fw: Decimal(str(conf)) for fw, conf in analysis_data.get('framework_confidence', {}).items()
            },
            'processingTime': Decimal(str(analysis_data.get('processing_time', 0.0))),
            'analysisMethod': analysis_data.get('analysis_method', 'AI Analysis'),
            'filesAnalyzed': analysis_data.get('files_analyzed', 0),
            
            # README data
            'readmeLength': readme_data.get('content_length', 0),
            'readmeS3Url': readme_data.get('s3_url', ''),
            
            # Additional metadata
            'emailSent': event_data.get('email_notification', {}).get('sent', False),
            'pipelineVersion': event_data.get('pipeline_version', '1.0')
        }
        
        logger.info(f"💾 Saving item to smart-readme-gen-records: {json.dumps(item, default=str)}")
        
        # Save to DynamoDB
        table.put_item(Item=item)
        
        logger.info(f"✅ Successfully saved history record for {github_url} to smart-readme-gen-records")
        
        return {
            'statusCode': 200,
            'message': 'History record saved successfully to smart-readme-gen-records',
            'requestId': request_id,
            'repoUrl': github_url,
            'tableName': 'smart-readme-gen-records'
        }
        
    except Exception as e:
        logger.error(f"❌ Error saving to DynamoDB: {str(e)}")
        raise e

def handle_api_gateway_request(event):
    """Handle direct API Gateway requests"""
    
    method = event['httpMethod']
    path = event['path']
    
    logger.info(f"🔍 API Gateway request: {method} {path}")
    
    if method == 'GET' and '/history/' in path:
        # Get user history
        user_id = event['pathParameters']['userId']
        return get_user_history(user_id)
    elif method == 'POST' and path == '/history':
        # Create new history record
        body = json.loads(event['body'])
        return handle_step_functions_completion(body)
    elif method == 'PUT' and path == '/history':
        # Update existing record
        body = json.loads(event['body'])
        return update_history_record(body)
    else:
        return {
            'statusCode': 404,
            'headers': get_cors_headers(),
            'body': json.dumps({'error': 'Not found'})
        }

def get_user_history(user_id):
    """Get history records for a user from smart-readme-gen-records"""
    
    try:
        logger.info(f"🔍 Getting history for user: {user_id} from smart-readme-gen-records")
        
        # Query using the UserTimeIndex to get records sorted by time
        response = table.query(
            IndexName='UserTimeIndex',
            KeyConditionExpression='userId = :userId',
            ExpressionAttributeValues={':userId': user_id},
            ScanIndexForward=False,  # Sort by createdAt descending (newest first)
            Limit=50  # Limit to last 50 records
        )
        
        items = response.get('Items', [])
        
        # Convert Decimal to float for JSON serialization
        items = convert_decimals_to_float(items)
        
        logger.info(f"✅ Found {len(items)} history records for user {user_id} in smart-readme-gen-records")
        
        return {
            'statusCode': 200,
            'headers': get_cors_headers(),
            'body': json.dumps({
                'items': items,
                'count': len(items),
                'tableName': 'smart-readme-gen-records'
            })
        }
        
    except Exception as e:
        logger.error(f"❌ Error getting user history: {str(e)}")
        return {
            'statusCode': 500,
            'headers': get_cors_headers(),
            'body': json.dumps({'error': str(e)})
        }

def check_duplicate_repo(repo_url):
    """Check if repo URL already exists in smart-readme-gen-records"""
    
    try:
        response = table.query(
            IndexName='RepoUrlIndex',
            KeyConditionExpression='repoUrl = :repoUrl',
            ExpressionAttributeValues={':repoUrl': repo_url},
            Limit=1
        )
        
        return len(response.get('Items', [])) > 0
        
    except Exception as e:
        logger.error(f"❌ Error checking duplicate repo: {str(e)}")
        return False

def update_history_record(data):
    """Update an existing history record in smart-readme-gen-records"""
    
    try:
        user_id = data.get('userId')
        request_id = data.get('requestId')
        
        if not user_id or not request_id:
            return {
                'statusCode': 400,
                'headers': get_cors_headers(),
                'body': json.dumps({'error': 'Missing userId or requestId'})
            }
        
        # Update the record
        update_expression = "SET #status = :status, completedAt = :completedAt"
        expression_values = {
            ':status': data.get('status', 'completed'),
            ':completedAt': datetime.utcnow().isoformat()
        }
        expression_names = {'#status': 'status'}
        
        # Add other fields if provided
        if 'readmeS3Url' in data:
            update_expression += ", readmeS3Url = :readmeS3Url"
            expression_values[':readmeS3Url'] = data['readmeS3Url']
        
        if 'readmeLength' in data:
            update_expression += ", readmeLength = :readmeLength"
            expression_values[':readmeLength'] = data['readmeLength']
        
        table.update_item(
            Key={'userId': user_id, 'requestId': request_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_values,
            ExpressionAttributeNames=expression_names
        )
        
        logger.info(f"✅ Updated history record: {user_id}/{request_id} in smart-readme-gen-records")
        
        return {
            'statusCode': 200,
            'headers': get_cors_headers(),
            'body': json.dumps({
                'message': 'Record updated successfully in smart-readme-gen-records',
                'tableName': 'smart-readme-gen-records'
            })
        }
        
    except Exception as e:
        logger.error(f"❌ Error updating record: {str(e)}")
        return {
            'statusCode': 500,
            'headers': get_cors_headers(),
            'body': json.dumps({'error': str(e)})
        }

def extract_repo_name(github_url):
    """Extract repository name from GitHub URL"""
    try:
        # Extract owner/repo from URL like https://github.com/owner/repo
        parts = github_url.rstrip('/').split('/')
        if len(parts) >= 2:
            return f"{parts[-2]}/{parts[-1]}"
        return github_url
    except:
        return github_url

def convert_decimals_to_float(obj):
    """Convert DynamoDB Decimal objects to float for JSON serialization"""
    if isinstance(obj, list):
        return [convert_decimals_to_float(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: convert_decimals_to_float(value) for key, value in obj.items()}
    elif isinstance(obj, Decimal):
        return float(obj)
    else:
        return obj

def get_cors_headers():
    """Get CORS headers for API responses"""
    return {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
        'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
    }
