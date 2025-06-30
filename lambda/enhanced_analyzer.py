"""
Enhanced README Analyzer Lambda Function - Phase 1 Improvements
Integrates improved file selection and project classification
"""

import json
import boto3
import requests
import base64
import time
from typing import Dict, List, Optional
from enhanced_file_selector import EnhancedFileSelector
from project_classifier import ProjectClassifier

class EnhancedREADMEAnalyzer:
    def __init__(self):
        self.s3_client = boto3.client('s3')
        self.bedrock_client = boto3.client('bedrock-runtime', region_name='us-east-1')
        self.file_selector = EnhancedFileSelector()
        self.classifier = ProjectClassifier()
        
        # Configuration
        self.bucket_name = 'smart-readme-lambda-31641'
        self.github_token = None  # Will be set from environment
        self.max_files_to_analyze = 25
        self.max_file_size = 50000  # 50KB max per file

    def lambda_handler(self, event, context):
        """🏆 HACKATHON-GRADE Phase 3 Ultimate Lambda handler"""
        try:
            # Extract GitHub URL
            github_url = event.get('github_url', '')
            if not github_url:
                return self._error_response("GitHub URL is required")
            
            print(f"🚀 Starting PHASE 3 ULTIMATE analysis for: {github_url}")
            start_time = time.time()
            
            # Parse repository info
            repo_info = self._parse_github_url(github_url)
            if not repo_info:
                return self._error_response("Invalid GitHub URL format")
            
            # 🏆 PHASE 3: Try ultimate AI platform first
            try:
                from phase3_orchestrator import Phase3UltimateOrchestrator
                print("🔥 HACKATHON MODE: Using Phase 3 Ultimate AI Platform")
                
                phase3_orchestrator = Phase3UltimateOrchestrator()
                # Use Phase 3's lambda_handler directly
                return phase3_orchestrator.lambda_handler(event, context)
                
            except ImportError as e:
                print(f"⚠️ Phase 3 modules not available: {e}")
                print("📉 Falling back to Phase 2")
            
            # 🎯 PHASE 2: Try advanced multi-pass analysis
            try:
                from phase2_analyzer import Phase2READMEAnalyzer
                print("🔥 Using Phase 2 Multi-Pass AI Orchestration")
                
                phase2_analyzer = Phase2READMEAnalyzer()
                # Use Phase 2's lambda_handler directly
                return phase2_analyzer.lambda_handler(event, context)
                
            except ImportError as e:
                print(f"⚠️ Phase 2 modules not available: {e}")
                print("📉 Falling back to Phase 1 (still enhanced)")
            
            # Phase 1 fallback (still enhanced)
            # Get repository files with improved selection
            files_data = self._get_repository_files_enhanced(repo_info)
            if not files_data:
                return self._error_response("Could not fetch repository files")
            
            print(f"📁 Selected {len(files_data)} priority files for analysis")
            
            # Enhanced project classification
            classification_result = self.classifier.analyze_project(
                files_data['file_contents'], 
                files_data.get('package_json')
            )
            
            print(f"🔍 Classification: {classification_result['project_type']} - {classification_result['primary_language']}")
            print(f"🛠️ Frameworks: {classification_result['frameworks']}")
            
            # Generate enhanced analysis with Bedrock
            analysis_result = self._generate_enhanced_analysis(files_data, classification_result)
            
            # Store results in S3
            s3_key = f"readme-analysis/{repo_info['owner']}/{repo_info['name']}.json"
            self._store_analysis_result(analysis_result, s3_key)
            
            processing_time = time.time() - start_time
            
            # Return enhanced response
            return {
                'statusCode': 200,
                'body': {
                    'success': True,
                    'message': 'Enhanced analysis completed successfully',
                    'analysis_summary': {
                        'project_type': classification_result['project_type'],
                        'primary_language': classification_result['primary_language'],
                        'frameworks': classification_result['frameworks'],
                        'confidence_scores': classification_result['confidence_scores'],
                        'files_analyzed': len(files_data['file_contents']),
                        'accuracy_improvements': 'Phase 1 - Enhanced file selection and classification'
                    },
                    'processing_time': processing_time,
                    'github_url': github_url,
                    's3_location': {
                        'bucket': self.bucket_name,
                        'key': s3_key,
                        'url': f"s3://{self.bucket_name}/{s3_key}"
                    },
                    'analysis_url': f"https://d3in1w40kamst9.cloudfront.net/{s3_key}",
                    'timestamp': time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
                }
            }
            
        except Exception as e:
            print(f"❌ Error in enhanced analysis: {str(e)}")
            return self._error_response(f"Analysis failed: {str(e)}")

    def _get_repository_files_enhanced(self, repo_info: Dict) -> Optional[Dict]:
        """Get repository files with enhanced selection logic"""
        try:
            # Get repository tree
            tree_url = f"https://api.github.com/repos/{repo_info['owner']}/{repo_info['name']}/git/trees/main?recursive=1"
            headers = {'Authorization': f'token {self.github_token}'} if self.github_token else {}
            
            response = requests.get(tree_url, headers=headers)
            if response.status_code != 200:
                print(f"❌ Failed to get repository tree: {response.status_code}")
                return None
            
            tree_data = response.json()
            all_files = [item['path'] for item in tree_data.get('tree', []) if item['type'] == 'blob']
            
            print(f"📊 Repository has {len(all_files)} total files")
            
            # Use enhanced file selector
            selected_files = self.file_selector.select_priority_files(all_files, self.max_files_to_analyze)
            selection_summary = self.file_selector.get_selection_summary(selected_files)
            
            print(f"🎯 File selection summary: {selection_summary}")
            
            # Fetch content for selected files
            file_contents = {}
            package_json = None
            
            for file_info in selected_files:
                file_path = file_info['path']
                content = self._get_file_content(repo_info, file_path)
                
                if content and len(content) <= self.max_file_size:
                    file_contents[file_path] = content
                    
                    # Extract package.json for dependency analysis
                    if file_path == 'package.json':
                        try:
                            package_json = json.loads(content)
                        except json.JSONDecodeError:
                            print(f"⚠️ Could not parse package.json")
                
                # Rate limiting
                time.sleep(0.1)
            
            return {
                'file_contents': file_contents,
                'package_json': package_json,
                'selection_summary': selection_summary,
                'total_repository_files': len(all_files)
            }
            
        except Exception as e:
            print(f"❌ Error fetching repository files: {str(e)}")
            return None

    def _generate_enhanced_analysis(self, files_data: Dict, classification_result: Dict) -> Dict:
        """Generate enhanced analysis using Bedrock with improved prompts"""
        
        # Create enhanced prompt with classification context
        enhanced_prompt = f"""
You are analyzing a {classification_result['project_type']} written primarily in {classification_result['primary_language']}.

DETECTED FRAMEWORKS: {', '.join(classification_result['frameworks']) if classification_result['frameworks'] else 'None detected'}

CONFIDENCE SCORES: {classification_result['confidence_scores']}

IMPORTANT CONTEXT:
- This is a {classification_result['project_type']}, not a generic web application
- Primary language is {classification_result['primary_language']}
- {len(files_data['file_contents'])} carefully selected files were analyzed (not just test files)

FILES ANALYZED:
{json.dumps(list(files_data['file_contents'].keys()), indent=2)}

FILE CONTENTS:
{json.dumps(files_data['file_contents'], indent=2)}

Based on this enhanced analysis, generate a comprehensive README structure that:

1. ACCURATELY reflects the project type ({classification_result['project_type']})
2. Correctly identifies the primary language ({classification_result['primary_language']})
3. Properly recognizes the frameworks: {classification_result['frameworks']}
4. Focuses on the actual functionality, not just testing infrastructure
5. Uses professional, technical language (minimal emojis)

Generate a detailed JSON structure for README generation with accurate project classification.
"""

        try:
            # Call Bedrock with enhanced prompt
            response = self.bedrock_client.invoke_model(
                modelId='us.anthropic.claude-sonnet-4-20250514-v1:0',
                body=json.dumps({
                    'anthropic_version': 'bedrock-2023-05-31',
                    'max_tokens': 4000,
                    'messages': [
                        {
                            'role': 'user',
                            'content': enhanced_prompt
                        }
                    ]
                })
            )
            
            response_body = json.loads(response['body'].read())
            ai_analysis = response_body['content'][0]['text']
            
            # Parse AI response and combine with classification results
            try:
                ai_json = json.loads(ai_analysis)
            except json.JSONDecodeError:
                # Fallback if AI doesn't return valid JSON
                ai_json = {'ai_analysis': ai_analysis}
            
            # Combine results
            enhanced_analysis = {
                'repository_analysis': {
                    'repository_url': files_data.get('github_url', ''),
                    'project_type': classification_result['project_type'],
                    'primary_language': classification_result['primary_language'],
                    'frameworks': classification_result['frameworks'],
                    'confidence_scores': classification_result['confidence_scores'],
                    'analysis_details': classification_result['analysis_details'],
                    'files_analyzed': len(files_data['file_contents']),
                    'selection_summary': files_data.get('selection_summary', {}),
                    'total_repository_files': files_data.get('total_repository_files', 0)
                },
                'ai_analysis': ai_json,
                'processing_metadata': {
                    'version': 'enhanced_v1.0_phase1',
                    'improvements': [
                        'Enhanced file selection prioritizing important files',
                        'Improved project type classification',
                        'Framework detection with confidence scoring',
                        'Language detection excluding test files',
                        'Balanced file category selection'
                    ],
                    'timestamp': time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
                }
            }
            
            return enhanced_analysis
            
        except Exception as e:
            print(f"❌ Error generating enhanced analysis: {str(e)}")
            # Return classification results even if AI analysis fails
            return {
                'repository_analysis': {
                    'project_type': classification_result['project_type'],
                    'primary_language': classification_result['primary_language'],
                    'frameworks': classification_result['frameworks'],
                    'confidence_scores': classification_result['confidence_scores']
                },
                'error': f"AI analysis failed: {str(e)}"
            }

    def _parse_github_url(self, github_url: str) -> Optional[Dict]:
        """Parse GitHub URL to extract owner and repo name"""
        import re
        pattern = r'github\.com/([^/]+)/([^/]+?)(?:\.git)?/?$'
        match = re.search(pattern, github_url)
        
        if match:
            return {
                'owner': match.group(1),
                'name': match.group(2)
            }
        return None

    def _get_file_content(self, repo_info: Dict, file_path: str) -> Optional[str]:
        """Get content of a specific file from GitHub"""
        try:
            url = f"https://api.github.com/repos/{repo_info['owner']}/{repo_info['name']}/contents/{file_path}"
            headers = {'Authorization': f'token {self.github_token}'} if self.github_token else {}
            
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                content_data = response.json()
                if content_data.get('encoding') == 'base64':
                    return base64.b64decode(content_data['content']).decode('utf-8')
            
            return None
            
        except Exception as e:
            print(f"⚠️ Error fetching {file_path}: {str(e)}")
            return None

    def _store_analysis_result(self, analysis_result: Dict, s3_key: str):
        """Store analysis result in S3"""
        try:
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=s3_key,
                Body=json.dumps(analysis_result, indent=2),
                ContentType='application/json'
            )
            print(f"✅ Analysis stored at s3://{self.bucket_name}/{s3_key}")
        except Exception as e:
            print(f"❌ Error storing analysis: {str(e)}")

    def _error_response(self, message: str) -> Dict:
        """Return standardized error response"""
        return {
            'statusCode': 400,
            'body': {
                'success': False,
                'error': message,
                'version': 'enhanced_v1.0_phase1'
            }
        }

# Lambda entry point
def lambda_handler(event, context):
    analyzer = EnhancedREADMEAnalyzer()
    return analyzer.lambda_handler(event, context)
