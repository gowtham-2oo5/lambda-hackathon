"""
Optimized README Generator Lambda Function with S3 Storage
Lambda 1: Analyzes repository and saves JSON to S3
"""

import json
import boto3
import os
import sys
import base64
import urllib.request
import urllib.parse
from datetime import datetime
from typing import Dict, List, Any, Optional

# Add the services directory to the path
sys.path.append('./services')
sys.path.append('/opt/python/services')
sys.path.append('./agents')
sys.path.append('/opt/python/agents')

# S3 Configuration
S3_BUCKET = 'smart-readme-lambda-31641'
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    """
    Lambda 1: Repository Analysis with S3 Storage
    """
    
    start_time = datetime.now()
    
    try:
        # Extract GitHub URL from event
        github_url = event.get('github_url')
        if not github_url:
            return create_error_response(400, 'GitHub URL is required')
        
        # Parse GitHub URL
        parts = github_url.replace('https://github.com/', '').split('/')
        if len(parts) < 2:
            return create_error_response(400, 'Invalid GitHub URL format')
        
        owner, repo = parts[0], parts[1]
        
        print(f"🚀 Starting README analysis for: {github_url}")
        print(f"   Owner: {owner}, Repo: {repo}")
        
        # Step 1: Perform repository analysis
        repo_analysis = perform_comprehensive_analysis(github_url, owner, repo)
        
        # Step 2: Generate README structure using optimized Bedrock service
        readme_structure = generate_readme_with_bedrock(repo_analysis)
        
        # Step 3: Combine results
        complete_analysis = {
            'repository_analysis': repo_analysis,
            'readme_structure': readme_structure,
            'processing_metadata': {
                'processing_time_seconds': (datetime.now() - start_time).total_seconds(),
                'timestamp': datetime.now().isoformat(),
                'version': 'optimized_v1.0_with_s3',
                'bedrock_enabled': True,
                'inference_profile_used': True,
                'lambda_function': 'Lambda-1-Analysis'
            }
        }
        
        # Step 4: Save to S3
        s3_key = f"readme-analysis/{owner}/{repo}.json"
        s3_url = save_to_s3(complete_analysis, s3_key)
        
        print(f"✅ Analysis saved to S3: {s3_url}")
        
        # Step 5: Return response with S3 location
        result = {
            'analysis_complete': True,
            's3_location': {
                'bucket': S3_BUCKET,
                'key': s3_key,
                'url': s3_url
            },
            'repository_info': {
                'owner': owner,
                'repo': repo,
                'url': github_url
            },
            'analysis_summary': {
                'project_type': repo_analysis.get('project_type', 'Unknown'),
                'primary_language': repo_analysis.get('primary_language', 'Unknown'),
                'frameworks': repo_analysis.get('frameworks', []),
                'features_count': len(repo_analysis.get('features', [])),
                'files_analyzed': len(repo_analysis.get('key_files', [])),
                'security_score': repo_analysis.get('security_analysis', {}).get('security_score', 0)
            },
            'next_step': 'Lambda-2-README-Generation'
        }
        
        print(f"✅ Lambda 1 completed successfully")
        return create_success_response(result)
        
    except Exception as e:
        print(f"❌ Error in Lambda 1: {e}")
        import traceback
        traceback.print_exc()
        return create_error_response(500, f'Lambda 1 error: {str(e)}')

def save_to_s3(data: Dict[str, Any], s3_key: str) -> str:
    """
    Save analysis data to S3
    """
    try:
        # Convert to JSON string
        json_data = json.dumps(data, indent=2, default=str)
        
        # Upload to S3
        s3_client.put_object(
            Bucket=S3_BUCKET,
            Key=s3_key,
            Body=json_data,
            ContentType='application/json',
            Metadata={
                'generated-by': 'smart-readme-generator',
                'lambda-function': 'lambda-1-analysis',
                'timestamp': datetime.now().isoformat()
            }
        )
        
        # Return S3 URL
        s3_url = f"s3://{S3_BUCKET}/{s3_key}"
        print(f"📁 Saved to S3: {s3_url}")
        return s3_url
        
    except Exception as e:
        print(f"❌ Failed to save to S3: {e}")
        raise e

def perform_comprehensive_analysis(github_url: str, owner: str, repo: str) -> Dict[str, Any]:
    """
    Perform comprehensive repository analysis
    """
    print(f"🔍 Performing comprehensive analysis for {owner}/{repo}")
    
    try:
        # Step 1: Get repository structure
        print("📁 Getting repository structure...")
        repo_structure = get_repository_structure(owner, repo)
        print(f"   Found {len(repo_structure)} files/directories")
        
        # Step 2: Identify key files
        print("🔍 Identifying key files...")
        key_files = identify_key_files(repo_structure)
        print(f"   Identified {len(key_files)} key files")
        
        # Step 3: Analyze key files
        print("📖 Analyzing file contents...")
        file_contents = analyze_key_files(owner, repo, key_files[:15])  # Limit to 15 files
        print(f"   Successfully analyzed {len(file_contents)} files")
        
        # Step 4: Detect project characteristics
        print("🛠️  Detecting project characteristics...")
        project_analysis = detect_project_characteristics(file_contents, repo_structure)
        
        # Step 5: Security analysis
        print("🔒 Performing security analysis...")
        security_analysis = perform_security_analysis(file_contents)
        
        # Combine all analysis
        return {
            'repository_url': github_url,
            'project_type': project_analysis.get('project_type', 'Software Application'),
            'primary_language': project_analysis.get('primary_language', 'Unknown'),
            'frameworks': project_analysis.get('frameworks', []),
            'features': project_analysis.get('features', []),
            'architecture_patterns': project_analysis.get('architecture_patterns', []),
            'key_files': [f['path'] for f in file_contents],
            'file_contents': {f['path']: f.get('content_preview', '') for f in file_contents},
            'security_analysis': security_analysis,
            'repository_stats': {
                'total_files': len(repo_structure),
                'analyzed_files': len(file_contents),
                'languages_detected': list(set([f.get('language', 'unknown') for f in file_contents]))
            }
        }
        
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        # Return minimal analysis
        return {
            'repository_url': github_url,
            'project_type': 'Software Application',
            'primary_language': 'Unknown',
            'frameworks': [],
            'features': ['Code analysis in progress'],
            'architecture_patterns': [],
            'key_files': [],
            'file_contents': {},
            'security_analysis': {'total_issues': 0, 'security_score': 100},
            'repository_stats': {'total_files': 0, 'analyzed_files': 0, 'languages_detected': []},
            'analysis_error': str(e)
        }

def generate_readme_with_bedrock(repo_analysis: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate README structure using optimized Bedrock service
    """
    print(f"🤖 Generating README structure with Bedrock...")
    
    try:
        # Import the optimized service
        from optimized_bedrock_service import generate_readme_json
        
        # Generate README structure
        readme_structure = generate_readme_json(repo_analysis)
        
        print(f"✅ README structure generated successfully")
        return readme_structure
        
    except ImportError as e:
        print(f"⚠️ Optimized Bedrock service not available: {e}")
        return create_fallback_readme_structure(repo_analysis)
    except Exception as e:
        print(f"⚠️ Bedrock generation failed: {e}")
        return create_fallback_readme_structure(repo_analysis)

def create_fallback_readme_structure(repo_analysis: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create fallback README structure when Bedrock is not available
    """
    print("🔄 Creating fallback README structure...")
    
    return {
        "project_overview": {
            "name": "Repository Analysis",
            "description": f"A {repo_analysis.get('project_type', 'software application')} built with {repo_analysis.get('primary_language', 'multiple technologies')}",
            "type": repo_analysis.get('project_type', 'Software Application'),
            "primary_purpose": "Software development project",
            "target_audience": "Developers and users"
        },
        "technical_stack": {
            "primary_language": repo_analysis.get('primary_language', 'Unknown'),
            "frameworks": repo_analysis.get('frameworks', []),
            "key_dependencies": ["Analysis in progress"],
            "build_tools": ["Standard build tools"],
            "database": "Not specified in code analysis",
            "deployment_platforms": ["Standard platforms"]
        },
        "features": repo_analysis.get('features', ["Core functionality"]),
        "generation_metadata": {
            "model_used": "Fallback Generator",
            "model_id": "fallback",
            "generated_at": datetime.now().isoformat(),
            "version": "fallback_1.0.0"
        }
    }

# Include all the helper functions from the previous version
def get_repository_structure(owner: str, repo: str) -> List[Dict[str, Any]]:
    """Get repository file structure"""
    try:
        url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/HEAD?recursive=1"
        headers = {}
        github_token = os.environ.get('GITHUB_TOKEN')
        if github_token:
            headers['Authorization'] = f'token {github_token}'
        
        request = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(request) as response:
            data = json.loads(response.read().decode())
            return data.get('tree', [])
            
    except Exception as e:
        print(f"❌ Failed to get repository structure: {e}")
        return []

def identify_key_files(repo_structure: List[Dict[str, Any]]) -> List[str]:
    """Identify key files for analysis"""
    key_files = []
    
    # Priority files
    priority_patterns = [
        'README.md', 'package.json', 'requirements.txt', 'pom.xml',
        'build.gradle', 'AndroidManifest.xml', 'Dockerfile', 'docker-compose.yml',
        'next.config.js', 'tsconfig.json', 'webpack.config.js'
    ]
    
    # Code file extensions
    code_extensions = ['.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.kt', '.go', '.rs', '.php', '.rb']
    
    for item in repo_structure:
        if item.get('type') == 'blob':
            path = item.get('path', '')
            
            # Add priority files first
            if any(pattern in path for pattern in priority_patterns):
                key_files.insert(0, path)
            # Add code files
            elif any(path.endswith(ext) for ext in code_extensions):
                key_files.append(path)
    
    return key_files

def analyze_key_files(owner: str, repo: str, file_paths: List[str]) -> List[Dict[str, Any]]:
    """Analyze key files"""
    analyzed_files = []
    
    for file_path in file_paths:
        try:
            file_analysis = analyze_single_file(owner, repo, file_path)
            if file_analysis:
                analyzed_files.append(file_analysis)
        except Exception as e:
            print(f"⚠️ Failed to analyze {file_path}: {e}")
            continue
    
    return analyzed_files

def analyze_single_file(owner: str, repo: str, file_path: str) -> Optional[Dict[str, Any]]:
    """Analyze a single file"""
    try:
        url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"
        headers = {}
        github_token = os.environ.get('GITHUB_TOKEN')
        if github_token:
            headers['Authorization'] = f'token {github_token}'
        
        request = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(request) as response:
            data = json.loads(response.read().decode())
            
            if data.get('content'):
                content = base64.b64decode(data['content']).decode('utf-8', errors='ignore')
                
                return {
                    'path': file_path,
                    'size': len(content),
                    'language': detect_language(file_path),
                    'content_preview': content[:2000] + ('...' if len(content) > 2000 else ''),
                    'imports': extract_imports(content, detect_language(file_path))
                }
    except Exception:
        return None

def detect_project_characteristics(file_contents: List[Dict[str, Any]], repo_structure: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Detect project characteristics"""
    
    # Language detection
    language_counts = {}
    for file_data in file_contents:
        lang = file_data.get('language', 'unknown')
        if lang != 'unknown':
            language_counts[lang] = language_counts.get(lang, 0) + 1
    
    primary_language = max(language_counts, key=language_counts.get) if language_counts else 'Unknown'
    
    # Framework detection
    frameworks = []
    features = []
    architecture_patterns = []
    
    for file_data in file_contents:
        content = file_data.get('content_preview', '').lower()
        path = file_data.get('path', '').lower()
        
        # Framework detection
        if 'react' in content or 'jsx' in path:
            frameworks.append('React')
        if 'next' in content or 'next.config' in path:
            frameworks.append('Next.js')
        if 'android' in content or 'androidmanifest' in path:
            frameworks.append('Android SDK')
        if 'spring' in content:
            frameworks.append('Spring Boot')
        if 'django' in content:
            frameworks.append('Django')
        if 'flask' in content:
            frameworks.append('Flask')
        
        # Feature detection
        if 'auth' in content:
            features.append('Authentication')
        if 'api' in content:
            features.append('API Integration')
        if 'database' in content or 'db' in content:
            features.append('Database Integration')
        if 'test' in content:
            features.append('Testing')
        
        # Architecture patterns
        if 'mvc' in content:
            architecture_patterns.append('MVC')
        if 'microservice' in content:
            architecture_patterns.append('Microservices')
        if 'rest' in content:
            architecture_patterns.append('REST API')
    
    # Project type detection
    project_type = 'Software Application'
    if 'android' in ' '.join(frameworks).lower():
        project_type = 'Mobile Application'
    elif any(fw in ['React', 'Next.js', 'Vue.js'] for fw in frameworks):
        project_type = 'Web Application'
    elif any(fw in ['Spring Boot', 'Django', 'Flask'] for fw in frameworks):
        project_type = 'Web Service'
    
    return {
        'project_type': project_type,
        'primary_language': primary_language,
        'frameworks': list(set(frameworks)),
        'features': list(set(features)),
        'architecture_patterns': list(set(architecture_patterns))
    }

def detect_language(file_path: str) -> str:
    """Detect programming language from file extension"""
    extension_map = {
        '.py': 'Python',
        '.js': 'JavaScript',
        '.ts': 'TypeScript',
        '.jsx': 'JavaScript',
        '.tsx': 'TypeScript',
        '.java': 'Java',
        '.kt': 'Kotlin',
        '.go': 'Go',
        '.rs': 'Rust',
        '.php': 'PHP',
        '.rb': 'Ruby',
        '.xml': 'XML',
        '.json': 'JSON'
    }
    
    for ext, lang in extension_map.items():
        if file_path.endswith(ext):
            return lang
    
    return 'Unknown'

def extract_imports(content: str, language: str) -> List[str]:
    """Extract imports/dependencies from code"""
    imports = []
    
    if language in ['Python']:
        import re
        python_imports = re.findall(r'(?:from\s+(\S+)\s+import|import\s+(\S+))', content)
        for match in python_imports:
            imports.extend([imp for imp in match if imp])
    
    elif language in ['JavaScript', 'TypeScript']:
        import re
        js_imports = re.findall(r'import.*?from\s+["\']([^"\']+)["\']', content)
        imports.extend(js_imports)
    
    return list(set(imports))

def perform_security_analysis(file_contents: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Perform basic security analysis"""
    total_issues = 0
    issues = []
    
    security_patterns = {
        'hardcoded_password': r'password\s*=\s*["\'][^"\']+["\']',
        'hardcoded_api_key': r'api_key\s*=\s*["\'][^"\']+["\']',
        'sql_injection': r'SELECT.*FROM.*WHERE.*\+'
    }
    
    for file_data in file_contents:
        content = file_data.get('content_preview', '')
        
        for issue_type, pattern in security_patterns.items():
            import re
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                total_issues += 1
                issues.append({
                    'type': issue_type,
                    'file': file_data['path'],
                    'severity': 'HIGH'
                })
    
    security_score = max(0, 100 - (total_issues * 10))
    
    return {
        'total_issues': total_issues,
        'issues': issues,
        'security_score': security_score
    }

def create_success_response(data: Any) -> Dict[str, Any]:
    """Create standardized success response"""
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
        },
        'body': json.dumps({
            'success': True,
            'message': 'Lambda 1: Repository analysis completed and saved to S3',
            'data': data,
            'timestamp': datetime.now().isoformat()
        }, indent=2)
    }

def create_error_response(status_code: int, error_message: str) -> Dict[str, Any]:
    """Create standardized error response"""
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            'success': False,
            'error': {
                'message': error_message,
                'timestamp': datetime.now().isoformat(),
                'lambda_function': 'Lambda-1-Analysis'
            }
        })
    }
