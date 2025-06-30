import json
import boto3
import urllib.request
import urllib.parse
import base64
import os
import time
import uuid
from datetime import datetime
from typing import Dict, List, Optional
from botocore.config import Config

class CacheBustingGenerator:
    def __init__(self):
        self.bedrock_client = boto3.client(
            'bedrock-runtime',
            region_name='us-east-1',
            config=Config(read_timeout=180, connect_timeout=30)
        )
        self.s3_client = boto3.client('s3')
        self.cloudfront_client = boto3.client('cloudfront')
        self.bucket_name = 'smart-readme-lambda-31641'
        self.github_token = os.environ.get('GITHUB_TOKEN')
        self.cloudfront_domain = 'd3in1w40kamst9.cloudfront.net'
        self.cloudfront_distribution_id = 'E2SGUO2RBNJDS5'

    def lambda_handler(self, event, context):
        try:
            print(f"🚀 ENHANCED CACHE-BUSTING README Generation Started")
            start_time = time.time()
            
            github_url = event.get('github_url', '')
            user_email = event.get('user_email', '')
            
            if not github_url:
                return self._error_response("GitHub URL is required")
            
            repo_info = self._parse_github_url(github_url)
            if not repo_info:
                return self._error_response("Invalid GitHub URL format")
            
            print(f"🔍 Processing: {repo_info['owner']}/{repo_info['repo']}")
            
            default_branch = self._get_default_branch(repo_info)
            print(f"📋 Using branch: {default_branch}")
            
            repo_structure = self._explore_repository_structure(repo_info, default_branch)
            
            source_files = self._fetch_comprehensive_source_files(repo_info, repo_structure, default_branch)
            
            if not self._validate_analysis_completeness(source_files):
                additional_files = self._fetch_additional_files(repo_info, repo_structure, default_branch)
                source_files.update(additional_files)
            
            readme_content = self._generate_readme_from_code_analysis(repo_info, source_files, github_url)
            
            # Extract metadata from README content
            metadata = self._extract_metadata_from_readme(readme_content)
            clean_readme = self._clean_readme_content(readme_content)
            
            s3_key = f"readmes/{repo_info['owner']}-{repo_info['repo']}-{int(time.time())}.md"
            
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=s3_key,
                Body=clean_readme.encode('utf-8'),
                ContentType='text/markdown',
                CacheControl='no-cache, no-store, must-revalidate',
                Expires=datetime.utcnow(),
                Metadata={
                    'generated-at': datetime.utcnow().isoformat(),
                    'repo-url': github_url,
                    'cache-buster': str(uuid.uuid4())
                }
            )
            
            cloudfront_url = f"https://{self.cloudfront_domain}/{s3_key}"
            
            try:
                self.cloudfront_client.create_invalidation(
                    DistributionId=self.cloudfront_distribution_id,
                    InvalidationBatch={
                        'Paths': {
                            'Quantity': 1,
                            'Items': [f'/{s3_key}']
                        },
                        'CallerReference': str(uuid.uuid4())
                    }
                )
                print(f"🔄 CloudFront invalidation created for: {s3_key}")
            except Exception as e:
                print(f"⚠️ CloudFront invalidation failed: {e}")
            
            processing_time = round(time.time() - start_time, 2)
            
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Cache-Control': 'no-cache, no-store, must-revalidate',
                    'Pragma': 'no-cache',
                    'Expires': '0'
                },
                'body': json.dumps({
                    'success': True,
                    'data': {
                        'readme_content': clean_readme,
                        'readme_length': len(clean_readme),
                        'download_url': cloudfront_url,
                        's3_location': {
                            'bucket': self.bucket_name,
                            'key': s3_key
                        },
                        'processing_time': processing_time,
                        'files_analyzed': len(source_files),
                        'analysis_method': 'enhanced_code_analysis_with_metadata',
                        'version': 'v3.3_metadata_enhanced',
                        'branch_used': default_branch,
                        # 🔥 NEW: Include extracted metadata
                        'metadata': metadata,
                        'primary_language': metadata.get('primaryLanguage', 'Unknown'),
                        'project_type': metadata.get('projectType', 'software_project'),
                        'tech_stack': metadata.get('techStack', []),
                        'frameworks': metadata.get('frameworks', [])
                    }
                })
            }
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return self._error_response(f"Processing failed: {str(e)}")

    def _extract_metadata_from_readme(self, readme_content: str) -> Dict[str, any]:
        """Extract metadata from README content"""
        try:
            # Look for metadata section
            if '---METADATA---' in readme_content and '---END_METADATA---' in readme_content:
                metadata_start = readme_content.find('---METADATA---') + len('---METADATA---')
                metadata_end = readme_content.find('---END_METADATA---')
                metadata_section = readme_content[metadata_start:metadata_end].strip()
                
                metadata = {}
                for line in metadata_section.split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        key = key.strip()
                        value = value.strip()
                        
                        if key == 'PRIMARY_LANGUAGE':
                            metadata['primaryLanguage'] = value
                        elif key == 'PROJECT_TYPE':
                            metadata['projectType'] = value
                        elif key == 'TECH_STACK':
                            metadata['techStack'] = [tech.strip() for tech in value.split(',') if tech.strip()]
                        elif key == 'FRAMEWORKS':
                            metadata['frameworks'] = [fw.strip() for fw in value.split(',') if fw.strip()]
                
                return metadata
            
            # Fallback to defaults if no metadata found
            return {
                'primaryLanguage': 'Unknown',
                'projectType': 'software_project',
                'techStack': [],
                'frameworks': []
            }
            
        except Exception as e:
            print(f"❌ Error extracting metadata: {e}")
            return {
                'primaryLanguage': 'Unknown',
                'projectType': 'software_project',
                'techStack': [],
                'frameworks': []
            }

    def _clean_readme_content(self, readme_content: str) -> str:
        """Remove metadata section from README content"""
        if '---METADATA---' in readme_content:
            return readme_content[:readme_content.find('---METADATA---')].strip()
        return readme_content

    def _parse_github_url(self, github_url: str) -> Optional[Dict[str, str]]:
        try:
            if 'github.com' not in github_url:
                return None
            
            parts = github_url.replace('https://github.com/', '').replace('http://github.com/', '').split('/')
            if len(parts) >= 2:
                return {
                    'owner': parts[0],
                    'repo': parts[1].replace('.git', '')
                }
            return None
        except:
            return None

    def _get_default_branch(self, repo_info: Dict) -> str:
        try:
            owner, repo = repo_info['owner'], repo_info['repo']
            url = f"https://api.github.com/repos/{owner}/{repo}"
            
            req = urllib.request.Request(url)
            if self.github_token:
                req.add_header('Authorization', f'token {self.github_token}')
            
            with urllib.request.urlopen(req, timeout=30) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode('utf-8'))
                    return data.get('default_branch', 'main')
        except Exception as e:
            print(f"❌ Failed to get default branch: {e}")
        
        return 'main'

    def _explore_repository_structure(self, repo_info: Dict, branch: str) -> List[Dict]:
        try:
            owner, repo = repo_info['owner'], repo_info['repo']
            url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
            
            req = urllib.request.Request(url)
            if self.github_token:
                req.add_header('Authorization', f'token {self.github_token}')
            
            with urllib.request.urlopen(req, timeout=30) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode('utf-8'))
                    return data.get('tree', [])
        except Exception as e:
            print(f"❌ Failed to explore repository: {e}")
        
        return []

    def _fetch_comprehensive_source_files(self, repo_info: Dict, repo_structure: List[Dict], branch: str) -> Dict:
        print("🔍 Fetching comprehensive source files")
        
        owner, repo = repo_info['owner'], repo_info['repo']
        source_files = {}
        
        priority_files = [
            'package.json', 'requirements.txt', 'Cargo.toml', 'go.mod', 'pom.xml',
            'composer.json', 'Gemfile', 'setup.py', 'pyproject.toml', 'Dockerfile',
            'docker-compose.yml', 'README.md', 'README.txt', 'README'
        ]
        
        code_extensions = ['.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.go', '.rs', '.php', '.rb', '.cpp', '.c', '.h', '.cs', '.swift', '.kt']
        
        files_to_fetch = []
        
        for file_info in repo_structure:
            file_path = file_info.get('path', '')
            file_name = os.path.basename(file_path)
            
            if any(skip in file_path.lower() for skip in ['.git', 'node_modules', 'vendor', '__pycache__', '.next', 'dist', 'build']):
                continue
            
            if file_name in priority_files:
                files_to_fetch.insert(0, file_path)
            elif any(file_path.endswith(ext) for ext in code_extensions):
                files_to_fetch.append(file_path)
        
        files_to_fetch = files_to_fetch[:30]
        
        for file_path in files_to_fetch:
            try:
                url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}?ref={branch}"
                req = urllib.request.Request(url)
                if self.github_token:
                    req.add_header('Authorization', f'token {self.github_token}')
                
                with urllib.request.urlopen(req, timeout=30) as response:
                    if response.status == 200:
                        data = json.loads(response.read().decode('utf-8'))
                        
                        if data.get('content') and data.get('size', 0) < 100000:
                            content = base64.b64decode(data['content']).decode('utf-8', errors='ignore')
                            source_files[file_path] = content
                            print(f"✅ Fetched: {file_path} ({len(content)} chars)")
                        else:
                            print(f"⚠️ Skipped large file: {file_path}")
                            
            except Exception as e:
                print(f"❌ Failed to fetch {file_path}: {e}")
        
        return source_files

    def _validate_analysis_completeness(self, source_files: Dict) -> bool:
        if len(source_files) < 2:
            print(f"❌ Insufficient files: {len(source_files)} < 2")
            return False
        
        print(f"✅ Analysis complete: {len(source_files)} files")
        return True

    def _fetch_additional_files(self, repo_info: Dict, repo_structure: List[Dict], branch: str) -> Dict:
        print("🔍 Fetching additional files for complete analysis")
        
        owner, repo = repo_info['owner'], repo_info['repo']
        source_files = {}
        
        files_to_fetch = []
        for file_info in repo_structure[:25]:
            file_path = file_info.get('path', '')
            if not any(skip in file_path.lower() for skip in ['.git', 'node_modules', 'vendor']):
                files_to_fetch.append(file_path)
        
        for file_path in files_to_fetch:
            try:
                url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}?ref={branch}"
                req = urllib.request.Request(url)
                if self.github_token:
                    req.add_header('Authorization', f'token {self.github_token}')
                
                with urllib.request.urlopen(req, timeout=30) as response:
                    if response.status == 200:
                        data = json.loads(response.read().decode('utf-8'))
                        
                        if data.get('content') and data.get('size', 0) < 50000:
                            content = base64.b64decode(data['content']).decode('utf-8', errors='ignore')
                            source_files[file_path] = content
                            
            except Exception as e:
                continue
        
        return source_files

    def _generate_readme_from_code_analysis(self, repo_info: Dict, source_files: Dict, github_url: str) -> str:
        if not source_files:
            return self._create_fallback_readme(repo_info['repo'], github_url)
        
        project_name = repo_info['repo']
        
        file_contents = ""
        existing_readme_content = ""
        
        for file_path, content in source_files.items():
            file_name = os.path.basename(file_path)
            
            if file_name.lower() in ['readme.md', 'readme.txt', 'readme']:
                existing_readme_content = content[:2000]
                continue
            
            file_contents += f"\n=== FILE: {file_path} ===\n"
            file_contents += content[:3000]
            file_contents += "\n"
        
        ai_prompt = f"""You are a technical documentation expert analyzing source code to create professional README documentation.

PROJECT: {project_name}
REPOSITORY: {github_url}

SOURCE CODE AND PROJECT FILES FOR ANALYSIS:
{file_contents}

EXISTING README (FOR REFERENCE ONLY - DO NOT COPY):
{existing_readme_content[:500] if existing_readme_content else "No existing README found"}

MANDATORY TASK: Create a comprehensive README.md by analyzing the SOURCE CODE above.

CRITICAL REQUIREMENTS:
1. ANALYZE THE SOURCE CODE FILES - do not rely on existing README
2. Identify the ACTUAL project purpose from the code structure and implementation
3. Document REAL features found in the source code
4. List ACTUAL technologies and dependencies from package files
5. Create ACCURATE installation and usage instructions based on the code
6. Document REAL API endpoints, functions, and capabilities found in source
7. DO NOT make assumptions - only document what you can verify from the code
8. If existing README exists, use it only for reference - create fresh documentation
9. Focus on what the code actually does, not what a README claims it does
10. Make it comprehensive and professional based on CODE ANALYSIS
11. Imagine yourself as the project owner, the voice of content should be narrative. dont include terms like based on anaysis or based source code
12. Make sure to not mix up NextJS and React frameworks. 
13. And if you are to find multiple radix ui components in package.json Then it's probably cuz of shadcn ui or other UI component library. Be sure to conclude properly.

IMPORTANT: After generating the README, add a metadata section at the very end in this EXACT format:

---METADATA---
PRIMARY_LANGUAGE: [detected primary programming language like Python, JavaScript, TypeScript, Java, Go, etc.]
PROJECT_TYPE: [web_app|mobile_app|api|library|cli_tool|desktop_app|data_science|game|other]
TECH_STACK: [comma-separated list of main technologies/frameworks like React, Node.js, Express, MongoDB, etc.]
FRAMEWORKS: [comma-separated list of frameworks detected like Next.js, Django, Flask, Spring Boot, etc.]
---END_METADATA---

Generate a detailed, accurate README that represents what this project actually does based on thorough source code analysis."""

        try:
            print(f"🤖 Generating README with metadata from code analysis ({len(ai_prompt)} chars)")
            
            response = self.bedrock_client.invoke_model(
                modelId='us.anthropic.claude-sonnet-4-20250514-v1:0',
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 4000,
                    "messages": [
                        {
                            "role": "user",
                            "content": ai_prompt
                        }
                    ]
                })
            )
            
            response_body = json.loads(response['body'].read())
            generated_readme = response_body['content'][0]['text']
            
            print(f"✅ Generated README with metadata from code analysis: {len(generated_readme)} characters")
            return generated_readme
            
        except Exception as e:
            print(f"❌ AI generation failed: {e}")
            return self._create_fallback_readme(project_name, github_url)

    def _create_fallback_readme(self, project_name: str, github_url: str) -> str:
        return f"""# {project_name}

A project hosted at {github_url}

## About
This project requires further analysis to generate comprehensive documentation.

## Repository
- **Source**: {github_url}
- **Analysis**: Basic fallback documentation

## Next Steps
Please ensure the repository contains analyzable source code files for better documentation generation.

---METADATA---
PRIMARY_LANGUAGE: Unknown
PROJECT_TYPE: other
TECH_STACK: 
FRAMEWORKS: 
---END_METADATA---
"""

    def _error_response(self, message: str):
        return {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'success': False,
                'error': message
            })
        }

def lambda_handler(event, context):
    generator = CacheBustingGenerator()
    return generator.lambda_handler(event, context)
