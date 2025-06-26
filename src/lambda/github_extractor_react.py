"""
Enhanced GitHub Extractor with ReAct AI Agent
Replaces hardcoded analysis with intelligent ReAct framework
"""

import json
import boto3
import os
import sys
from datetime import datetime

# Add the agents directory to the path
sys.path.append('/opt/python/agents')
sys.path.append('./agents')

try:
    from react_agent import ReActRepositoryAgent
except ImportError:
    # Fallback if import fails
    print("Warning: ReAct agent not available, using fallback analysis")
    ReActRepositoryAgent = None

def lambda_handler(event, context):
    """
    Enhanced GitHub Repository Data Extractor using ReAct AI Agent
    """
    
    try:
        # Extract GitHub URL from event
        github_url = event.get('github_url')
        if not github_url:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'GitHub URL is required'})
            }
        
        # Parse GitHub URL
        parts = github_url.replace('https://github.com/', '').split('/')
        if len(parts) < 2:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Invalid GitHub URL format'})
            }
        
        owner, repo = parts[0], parts[1]
        
        # Try to use ReAct Agent if available
        if ReActRepositoryAgent:
            try:
                # Initialize ReAct Agent
                github_token = os.environ.get('GITHUB_TOKEN')
                agent = ReActRepositoryAgent(github_token=github_token)
                
                # Perform comprehensive analysis using ReAct framework
                print(f"Starting ReAct analysis for: {github_url}")
                analysis_result = agent.analyze_repository(github_url)
                
                if analysis_result['success']:
                    repo_info = create_enhanced_repo_info(analysis_result, owner, repo, github_url)
                else:
                    print(f"ReAct analysis failed: {analysis_result.get('error')}")
                    repo_info = create_fallback_repo_info(owner, repo, github_url)
                    
            except Exception as e:
                print(f"ReAct agent error: {str(e)}")
                repo_info = create_fallback_repo_info(owner, repo, github_url)
        else:
            # Use enhanced fallback analysis
            repo_info = create_enhanced_fallback_repo_info(owner, repo, github_url)
        
        # Store in S3 for processing pipeline
        s3_client = boto3.client('s3')
        bucket_name = 'humane-ai-readme-generator-695221387268'
        key = f"extractions/{owner}-{repo}-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}.json"
        
        s3_client.put_object(
            Bucket=bucket_name,
            Key=key,
            Body=json.dumps(repo_info, indent=2),
            ContentType='application/json'
        )
        
        # Store metadata in DynamoDB
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('readme-generator-projects')
        
        project_id = f"{owner}-{repo}-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        
        table.put_item(
            Item={
                'project_id': project_id,
                'github_url': github_url,
                'owner': owner,
                'repo': repo,
                'project_type': repo_info['project_type'],
                'language': repo_info['language'],
                'primary_framework': repo_info.get('tech_stack', {}).get('frameworks', ['None'])[0],
                'confidence_score': repo_info.get('analysis_metadata', {}).get('confidence_score', 0),
                'analysis_method': repo_info.get('analysis_metadata', {}).get('method', 'fallback'),
                'status': 'extracted',
                'created_at': datetime.utcnow().isoformat(),
                's3_key': key
            }
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': f'Repository analyzed successfully',
                'project_id': project_id,
                's3_key': key,
                'analysis_summary': {
                    'project_type': repo_info['project_type'],
                    'primary_language': repo_info['language'],
                    'frameworks': repo_info.get('tech_stack', {}).get('frameworks', []),
                    'confidence_score': f"{repo_info.get('analysis_metadata', {}).get('confidence_score', 0)}%",
                    'analysis_method': repo_info.get('analysis_metadata', {}).get('method', 'fallback')
                }
            }, indent=2)
        }
        
    except Exception as e:
        print(f"Error in repository analysis: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e),
                'message': 'Repository analysis failed'
            })
        }

def create_enhanced_repo_info(analysis_result, owner, repo, github_url):
    """Create repo info from ReAct analysis results"""
    
    comprehensive_analysis = analysis_result['analysis']
    
    return {
        'owner': owner,
        'repo': repo,
        'url': github_url,
        'extracted_at': datetime.utcnow().isoformat(),
        
        # Enhanced with ReAct analysis
        'project_type': comprehensive_analysis['architecture']['type'],
        'language': comprehensive_analysis['repository']['language'],
        'description': comprehensive_analysis['repository']['description'] or f"AI-analyzed {comprehensive_analysis['architecture']['type']}",
        
        # Comprehensive tech stack
        'tech_stack': comprehensive_analysis['tech_stack'],
        'architecture': comprehensive_analysis['architecture'],
        'features': comprehensive_analysis['features'],
        'quality_metrics': comprehensive_analysis['quality_metrics'],
        
        # ReAct analysis metadata
        'analysis_metadata': {
            'method': 'ReAct_AI_Agent',
            'steps_completed': comprehensive_analysis['analysis_metadata']['steps_completed'],
            'confidence_score': comprehensive_analysis['analysis_metadata']['confidence_score'],
            'analysis_timestamp': comprehensive_analysis['analysis_metadata']['analysis_timestamp']
        },
        
        # Detailed insights for README generation
        'readme_insights': {
            'estimated_features': comprehensive_analysis['features']['estimated_features'],
            'tech_stack_summary': {
                'primary_language': comprehensive_analysis['tech_stack']['languages'][0] if comprehensive_analysis['tech_stack']['languages'] else 'Unknown',
                'frameworks': comprehensive_analysis['tech_stack']['frameworks'],
                'databases': comprehensive_analysis['tech_stack']['databases'],
                'build_tools': comprehensive_analysis['tech_stack']['build_tools']
            },
            'architecture_insights': {
                'pattern': comprehensive_analysis['architecture']['pattern'],
                'components': comprehensive_analysis['architecture']['components']
            }
        },
        
        # Store ReAct steps for transparency
        'react_steps': analysis_result['steps']
    }

def create_enhanced_fallback_repo_info(owner, repo, github_url):
    """Enhanced fallback analysis using basic GitHub API calls"""
    
    try:
        import requests
        
        # Make basic GitHub API call
        headers = {'Accept': 'application/vnd.github.v3+json'}
        response = requests.get(f'https://api.github.com/repos/{owner}/{repo}', headers=headers)
        
        if response.status_code == 200:
            repo_data = response.json()
            
            # Enhanced analysis based on repo data
            language = repo_data.get('language', 'Unknown')
            topics = repo_data.get('topics', [])
            
            # Determine project type from language and topics
            project_type = determine_project_type(language, topics, repo)
            frameworks = determine_frameworks(language, topics)
            
            return {
                'owner': owner,
                'repo': repo,
                'url': github_url,
                'extracted_at': datetime.utcnow().isoformat(),
                'project_type': project_type,
                'language': language,
                'description': repo_data.get('description', f'{project_type} built with {language}'),
                'tech_stack': {
                    'languages': [language] if language != 'Unknown' else [],
                    'frameworks': frameworks,
                    'package_managers': determine_package_managers(language),
                    'build_tools': [],
                    'databases': []
                },
                'architecture': {
                    'type': project_type,
                    'pattern': 'Unknown',
                    'components': []
                },
                'features': {
                    'estimated_features': generate_estimated_features(project_type, language),
                    'api_endpoints': [],
                    'database_models': []
                },
                'quality_metrics': {
                    'code_quality': 'Unknown',
                    'complexity': 'Unknown',
                    'total_files': 0
                },
                'analysis_metadata': {
                    'method': 'Enhanced_GitHub_API',
                    'confidence_score': 70,
                    'analysis_timestamp': datetime.utcnow().isoformat()
                }
            }
        else:
            return create_fallback_repo_info(owner, repo, github_url)
            
    except Exception as e:
        print(f"Enhanced fallback failed: {str(e)}")
        return create_fallback_repo_info(owner, repo, github_url)

def create_fallback_repo_info(owner, repo, github_url):
    """Basic fallback repo info"""
    
    # Analyze repo name for clues
    repo_lower = repo.lower()
    
    if 'server' in repo_lower or 'api' in repo_lower or 'backend' in repo_lower:
        project_type = 'Backend Server'
        language = 'Node.js/JavaScript'  # Common assumption
        frameworks = ['Express.js']
    elif 'frontend' in repo_lower or 'ui' in repo_lower or 'app' in repo_lower:
        project_type = 'Frontend Application'
        language = 'JavaScript'
        frameworks = ['React']
    elif 'portal' in repo_lower:
        project_type = 'Web Portal'
        language = 'Node.js/JavaScript'
        frameworks = ['Express.js']
    else:
        project_type = 'Application'
        language = 'Unknown'
        frameworks = []
    
    return {
        'owner': owner,
        'repo': repo,
        'url': github_url,
        'extracted_at': datetime.utcnow().isoformat(),
        'project_type': project_type,
        'language': language,
        'description': f'{project_type} - {repo}',
        'tech_stack': {
            'languages': [language] if language != 'Unknown' else [],
            'frameworks': frameworks,
            'package_managers': ['npm'] if 'JavaScript' in language else [],
            'build_tools': [],
            'databases': []
        },
        'analysis_metadata': {
            'method': 'Basic_Fallback',
            'confidence_score': 30,
            'analysis_timestamp': datetime.utcnow().isoformat()
        }
    }

def determine_project_type(language, topics, repo_name):
    """Determine project type from language and topics"""
    
    repo_lower = repo_name.lower()
    topics_str = ' '.join(topics).lower()
    
    if 'api' in topics_str or 'server' in repo_lower or 'backend' in topics_str:
        return 'Backend Server'
    elif 'frontend' in topics_str or 'react' in topics_str or 'vue' in topics_str:
        return 'Frontend Application'
    elif 'web' in topics_str or 'webapp' in topics_str:
        return 'Web Application'
    elif 'library' in topics_str or 'package' in topics_str:
        return 'Library'
    elif 'cli' in topics_str or 'tool' in topics_str:
        return 'CLI Tool'
    elif language == 'Python':
        return 'Python Application'
    elif language == 'JavaScript':
        return 'JavaScript Application'
    else:
        return 'Application'

def determine_frameworks(language, topics):
    """Determine likely frameworks from language and topics"""
    
    frameworks = []
    topics_str = ' '.join(topics).lower()
    
    if language == 'JavaScript':
        if 'react' in topics_str:
            frameworks.append('React')
        if 'vue' in topics_str:
            frameworks.append('Vue.js')
        if 'angular' in topics_str:
            frameworks.append('Angular')
        if 'express' in topics_str or 'node' in topics_str:
            frameworks.append('Express.js')
        if 'next' in topics_str:
            frameworks.append('Next.js')
    elif language == 'Python':
        if 'django' in topics_str:
            frameworks.append('Django')
        if 'flask' in topics_str:
            frameworks.append('Flask')
        if 'fastapi' in topics_str:
            frameworks.append('FastAPI')
    elif language == 'Java':
        if 'spring' in topics_str:
            frameworks.append('Spring')
    elif language == 'Ruby':
        if 'rails' in topics_str:
            frameworks.append('Ruby on Rails')
    
    return frameworks

def determine_package_managers(language):
    """Determine package managers from language"""
    
    if language in ['JavaScript', 'Node.js/JavaScript']:
        return ['npm']
    elif language == 'Python':
        return ['pip']
    elif language == 'Java':
        return ['maven']
    elif language == 'Ruby':
        return ['bundler']
    else:
        return []

def generate_estimated_features(project_type, language):
    """Generate estimated features based on project type"""
    
    features = []
    
    if 'Backend' in project_type or 'Server' in project_type:
        features = [
            'RESTful API endpoints',
            'Database integration',
            'Authentication system',
            'Request/Response handling',
            'Error handling and logging'
        ]
    elif 'Frontend' in project_type:
        features = [
            'User interface components',
            'State management',
            'API integration',
            'Responsive design',
            'User interaction handling'
        ]
    elif 'Web' in project_type:
        features = [
            'Web interface',
            'User authentication',
            'Data management',
            'Interactive features'
        ]
    else:
        features = [
            'Core functionality',
            'Configuration management',
            'Error handling'
        ]
    
    return features
