import json
import boto3
import logging
from datetime import datetime
from decimal import Decimal
from botocore.exceptions import ClientError
import uuid
import urllib.parse

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('smart-readme-gen-records')

def lambda_handler(event, context):
    """
    FIXED DynamoDB handler with proper email URL decoding
    """
    
    logger.info(f"🔍 EVENT RECEIVED: {json.dumps(event, default=str)}")
    
    try:
        # Handle different event sources
        if 'httpMethod' in event:
            # Handle API Gateway requests
            return handle_api_gateway_request(event)
        else:
            # Handle Step Functions completion
            return handle_step_functions_data(event)
            
    except Exception as e:
        logger.error(f"❌ CRITICAL ERROR in DynamoDB handler: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': 'DynamoDB handler failed',
                'message': str(e),
                'success': False
            })
        }

def handle_step_functions_data(step_functions_event):
    """Handle Step Functions completion data"""
    
    logger.info(f"🔍 PROCESSING STEP FUNCTIONS DATA")
    
    try:
        # Extract data from Step Functions event structure
        user_email = step_functions_event.get('user_email')
        github_url = step_functions_event.get('github_url')
        
        # Extract analysis data from the nested structure
        analysis_data = step_functions_event.get('analysisData', {})
        if isinstance(analysis_data, dict) and 'data' in analysis_data:
            analysis_info = analysis_data['data']
        else:
            analysis_info = analysis_data
            
        # Extract README data
        readme_data = step_functions_event.get('readmeData', {})
        
        logger.info(f"🔍 EXTRACTED: user_email={user_email}, github_url={github_url}")
        
        if not user_email or not github_url:
            logger.error(f"❌ MISSING REQUIRED FIELDS")
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'Missing required fields',
                    'success': False
                })
            }
        
        # Generate request ID if not provided
        request_id = step_functions_event.get('requestId') or str(uuid.uuid4())
        
        # Extract repository info
        repo_info = analysis_info.get('repository_info', {}) if analysis_info else {}
        repo_name = repo_info.get('name', extract_repo_name_from_url(github_url))
        
        # Extract analysis summary
        analysis_summary = analysis_info.get('analysis_summary', {}) if analysis_info else {}
        
        # Build DynamoDB item
        current_time = datetime.utcnow().isoformat()
        
        item = {
            'userId': user_email,  # Keep email as primary key but fix URL handling
            'requestId': request_id,
            'repoUrl': github_url,
            'repoName': repo_name,
            'status': 'completed',
            'createdAt': current_time,
            'completedAt': current_time,
            'generationTimestamp': current_time,
            
            # Analysis data from Step Functions
            'projectType': analysis_summary.get('project_type', 'Unknown'),
            'primaryLanguage': analysis_summary.get('primary_language', 'Unknown'),
            'frameworks': analysis_summary.get('frameworks', []),
            'confidence': {
                'projectType': Decimal(str(analysis_summary.get('project_type_confidence', 0.0))),
                'language': Decimal(str(analysis_summary.get('language_confidence', 0.0)))
            },
            'frameworkConfidence': {
                fw: Decimal(str(conf)) for fw, conf in analysis_summary.get('framework_confidence', {}).items()
            },
            'processingTime': Decimal(str(analysis_summary.get('processing_time_seconds', 0.0))),
            'analysisMethod': analysis_summary.get('analysis_method', 'Step Functions Analysis'),
            'filesAnalyzed': analysis_summary.get('files_analyzed', 0),
            
            # README data from Step Functions
            'readmeLength': readme_data.get('readme_length', 0),
            'readmeS3Url': readme_data.get('download_url', ''),
            'readmeContent': readme_data.get('readme_content', '')[:1000] if readme_data.get('readme_content') else '',
            
            # Step Functions metadata
            'executionArn': step_functions_event.get('executionArn', ''),
            'workflowVersion': step_functions_event.get('version', '1.0'),
            'emailSent': True,
            'source': 'step-functions-workflow'
        }
        
        logger.info(f"💾 SAVING TO DYNAMODB: userId={item['userId']}, requestId={item['requestId']}")
        
        # Save to DynamoDB
        table.put_item(Item=item)
        
        logger.info(f"✅ SUCCESS: Step Functions data saved!")
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'success': True,
                'message': 'Step Functions data saved successfully',
                'userId': user_email,
                'requestId': request_id,
                'repoUrl': github_url,
                'tableName': 'smart-readme-gen-records'
            })
        }
        
    except Exception as e:
        logger.error(f"❌ ERROR saving Step Functions data: {str(e)}")
        raise e

def handle_api_gateway_request(event):
    """Handle API Gateway requests with FIXED email URL decoding"""
    
    method = event['httpMethod']
    path = event['path']
    
    logger.info(f"🔍 API Gateway request: {method} {path}")
    
    if method == 'GET' and '/history/' in path:
        # Get user history - DECODE the email properly
        encoded_user_id = event['pathParameters']['userId']
        
        # DECODE URL-encoded email
        user_email = urllib.parse.unquote(encoded_user_id)
        
        logger.info(f"🔍 DECODED EMAIL: '{encoded_user_id}' -> '{user_email}'")
        
        return get_user_history(user_email)
    else:
        return {
            'statusCode': 404,
            'headers': get_cors_headers(),
            'body': json.dumps({'error': 'Not found'})
        }

def get_user_history(user_email):
    """Get history records for a user by email - FIXED"""
    
    try:
        logger.info(f"🔍 Getting history for email: '{user_email}'")
        
        # Use scan with email filter (works reliably)
        response = table.scan(
            FilterExpression='userId = :email',
            ExpressionAttributeValues={':email': user_email},
            Limit=50
        )
        
        items = response.get('Items', [])
        items = convert_decimals_to_float(items)
        
        # Sort by createdAt descending (newest first)
        items.sort(key=lambda x: x.get('createdAt', ''), reverse=True)
        
        logger.info(f"✅ Found {len(items)} history records for email '{user_email}'")
        
        return {
            'statusCode': 200,
            'headers': get_cors_headers(),
            'body': json.dumps({
                'items': items,
                'count': len(items),
                'tableName': 'smart-readme-gen-records',
                'userEmail': user_email,
                'method': 'email-scan-filter'
            })
        }
        
    except Exception as e:
        logger.error(f"❌ Error getting user history: {str(e)}")
        return {
            'statusCode': 500,
            'headers': get_cors_headers(),
            'body': json.dumps({'error': str(e)})
        }

def extract_repo_name_from_url(github_url):
    """Extract repository name from GitHub URL"""
    try:
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
