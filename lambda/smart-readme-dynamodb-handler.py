import json
import boto3
import uuid
from datetime import datetime, timezone
from decimal import Decimal
import logging

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

# FIXED: Use the correct table name
TABLE_NAME = 'readme-records'
table = dynamodb.Table(TABLE_NAME)

def decimal_default(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

def lambda_handler(event, context):
    """
    Enhanced DynamoDB handler supporting both API Gateway events and Step Functions direct invocations
    """
    try:
        logger.info(f"Received event: {json.dumps(event, default=str)}")
        
        # Determine if this is an API Gateway event or Step Functions direct invocation
        is_api_gateway = 'httpMethod' in event
        
        if is_api_gateway:
            return handle_api_gateway_event(event, context)
        else:
            return handle_step_functions_event(event, context)
            
    except Exception as e:
        logger.error(f"Error in lambda_handler: {str(e)}")
        error_response = {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
            },
            'body': json.dumps({
                'success': False,
                'error': f'Internal server error: {str(e)}'
            })
        }
        
        if is_api_gateway:
            return error_response
        else:
            return error_response

def handle_api_gateway_event(event, context):
    """Handle API Gateway events (GET requests for history)"""
    try:
        http_method = event.get('httpMethod', '')
        
        if http_method == 'GET':
            return handle_get_history(event)
        elif http_method == 'POST':
            return handle_post_data(event)
        else:
            return {
                'statusCode': 405,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
                },
                'body': json.dumps({
                    'success': False,
                    'error': 'Method not allowed'
                })
            }
            
    except Exception as e:
        logger.error(f"Error in handle_api_gateway_event: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
            },
            'body': json.dumps({
                'success': False,
                'error': f'Internal server error: {str(e)}'
            })
        }

def handle_get_history(event):
    """Handle GET requests to retrieve user history"""
    try:
        # Extract userId from query parameters
        query_params = event.get('queryStringParameters') or {}
        user_id = query_params.get('userId')
        
        if not user_id:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
                },
                'body': json.dumps({
                    'success': False,
                    'error': 'Missing userId parameter'
                })
            }
        
        logger.info(f"Fetching history for user: {user_id}")
        
        # FIXED: Use UpdatedAtIndex instead of UserIndex
        # Query using the correct index structure
        response = table.query(
            IndexName='UpdatedAtIndex',
            KeyConditionExpression='userId = :userId',
            ExpressionAttributeValues={
                ':userId': user_id
            },
            ScanIndexForward=False,  # Sort by updatedAt in descending order (newest first)
            Limit=50  # Limit to 50 most recent items
        )
        
        items = response.get('Items', [])
        logger.info(f"Found {len(items)} history items for user {user_id}")
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
            },
            'body': json.dumps({
                'success': True,
                'data': {
                    'records': items,
                    'count': len(items)
                }
            }, default=decimal_default)
        }
        
    except Exception as e:
        logger.error(f"Error in handle_get_history: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
            },
            'body': json.dumps({
                'success': False,
                'error': f'Internal server error: {str(e)}'
            })
        }

def handle_post_data(event):
    """Handle POST requests to store new data"""
    try:
        # Parse request body
        body = json.loads(event.get('body', '{}'))
        
        # Extract required fields
        user_email = body.get('user_email')
        github_url = body.get('github_url')
        
        if not user_email or not github_url:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
                },
                'body': json.dumps({
                    'success': False,
                    'error': 'Missing required fields: user_email and github_url'
                })
            }
        
        return store_readme_data(user_email, github_url, body)
        
    except Exception as e:
        logger.error(f"Error in handle_post_data: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
            },
            'body': json.dumps({
                'success': False,
                'error': f'Internal server error: {str(e)}'
            })
        }

def handle_step_functions_event(event, context):
    """Handle Step Functions direct invocations"""
    try:
        # Extract data from Step Functions event
        user_email = event.get('user_email')
        github_url = event.get('github_url')
        analysis_data = event.get('analysisData', {})
        
        if not user_email or not github_url:
            raise ValueError("Missing required fields: user_email and github_url")
        
        # Store the data and return the result
        result = store_readme_data(user_email, github_url, analysis_data)
        
        # For Step Functions, return the parsed body content
        if result['statusCode'] == 200:
            return json.loads(result['body'])
        else:
            raise Exception(f"Failed to store data: {result['body']}")
            
    except Exception as e:
        logger.error(f"Error in handle_step_functions_event: {str(e)}")
        raise e

def store_readme_data(user_email, github_url, data):
    """Store README generation data in DynamoDB"""
    try:
        # Generate unique ID
        item_id = str(uuid.uuid4())
        current_time = datetime.now(timezone.utc).isoformat()
        
        # Extract repository information from GitHub URL
        repo_parts = github_url.replace('https://github.com/', '').split('/')
        repo_owner = repo_parts[0] if len(repo_parts) > 0 else 'unknown'
        repo_name = repo_parts[1] if len(repo_parts) > 1 else 'unknown'
        repo_id = f"{repo_owner}/{repo_name}"
        
        # Extract analysis data if available
        analysis_info = data.get('data', {}) if isinstance(data, dict) else {}
        
        # Prepare item for DynamoDB
        item = {
            'userId': user_email,
            'repoId': repo_id,
            'requestId': item_id,
            'repoName': repo_name,
            'repoOwner': repo_owner,
            'repoUrl': github_url,
            'status': 'completed',
            'createdAt': current_time,
            'updatedAt': current_time,
            'completedAt': current_time
        }
        
        # Add analysis data if available
        if analysis_info:
            if 'readme_content' in analysis_info:
                item['readmeContent'] = analysis_info['readme_content'][:1000]  # Truncate for storage
                item['readmeLength'] = analysis_info.get('readme_length', len(analysis_info['readme_content']))
            
            if 'download_url' in analysis_info:
                item['readmeUrl'] = analysis_info['download_url']
            
            if 's3_location' in analysis_info:
                item['s3Location'] = analysis_info['s3_location']
            
            if 'processing_time' in analysis_info:
                item['processingTime'] = Decimal(str(analysis_info['processing_time']))
            
            if 'files_analyzed' in analysis_info:
                item['filesAnalyzedCount'] = analysis_info['files_analyzed']
            
            if 'primary_language' in analysis_info:
                item['primaryLanguage'] = analysis_info['primary_language']
            
            if 'project_type' in analysis_info:
                item['projectType'] = analysis_info['project_type']
            
            if 'tech_stack' in analysis_info:
                item['techStack'] = analysis_info['tech_stack']
            
            if 'frameworks' in analysis_info:
                item['frameworks'] = analysis_info['frameworks']
            
            if 'analysis_method' in analysis_info:
                item['analysisMethod'] = analysis_info['analysis_method']
            
            if 'version' in analysis_info:
                item['version'] = analysis_info['version']
            
            if 'branch_used' in analysis_info:
                item['branchUsed'] = analysis_info['branch_used']
        
        # Store in DynamoDB
        logger.info(f"Storing item in DynamoDB: {json.dumps(item, default=str)}")
        table.put_item(Item=item)
        
        logger.info(f"Successfully stored README data for {user_email} - {repo_id}")
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
            },
            'body': json.dumps({
                'success': True,
                'message': 'README data stored successfully',
                'itemId': item_id,
                'userId': user_email,
                'repoId': repo_id
            })
        }
        
    except Exception as e:
        logger.error(f"Error storing README data: {str(e)}")
        raise e
