"""
Enhanced README Generator with Extended Bedrock Timeout + Step Functions Format - FULLY FIXED
Takes Smart ReadmeGen analysis and creates stunning, professional READMEs
"""

import json
import boto3
import time
from datetime import datetime
from typing import Dict, Any
from botocore.config import Config

class EnhancedREADMEGenerator:
    def __init__(self):
        # Configure Bedrock client with extended timeout settings
        bedrock_config = Config(
            read_timeout=900,  # 15 minutes read timeout
            connect_timeout=60,  # 1 minute connect timeout
            retries={
                'max_attempts': 3,
                'mode': 'adaptive'
            }
        )
        
        self.bedrock_client = boto3.client(
            'bedrock-runtime', 
            region_name='us-east-1',
            config=bedrock_config
        )
        self.s3_client = boto3.client('s3')
        self.model_id = 'us.anthropic.claude-sonnet-4-20250514-v1:0'
        
    def lambda_handler(self, event, context):
        """🏆 Enhanced README Generator Handler with Extended Timeout + Step Functions Format"""
        try:
            print(f"🚀 Smart ReadmeGen Enhanced README Generator starting with event: {json.dumps(event)}")
            
            # Extract S3 location from event
            if 'analysisData' in event and 'data' in event['analysisData']:
                # From Step Functions
                s3_location = event['analysisData']['data']['s3_location']
                github_url = event['github_url']
            elif 's3_bucket' in event and 's3_key' in event:
                # Direct invocation
                s3_location = {
                    'bucket': event['s3_bucket'],
                    'key': event['s3_key']
                }
                github_url = event.get('github_url', 'Unknown')
            else:
                raise Exception("Missing S3 location in event")
            
            # Load analysis data from S3
            bucket = s3_location['bucket']
            key = s3_location['key']
            
            print(f"📊 Loading analysis from s3://{bucket}/{key}")
            
            try:
                response = self.s3_client.get_object(Bucket=bucket, Key=key)
                analysis_data = json.loads(response['Body'].read().decode('utf-8'))
                print(f"✅ Loaded analysis data: {len(json.dumps(analysis_data))} characters")
            except Exception as e:
                raise Exception(f"Failed to load analysis from S3: {str(e)}")
            
            # Generate enhanced README
            print("🎨 Generating Enhanced README with advanced markdown...")
            readme_content = self._generate_enhanced_readme(analysis_data, github_url)
            
            # Store README in S3
            readme_key = key.replace('.json', '_README.md')
            
            print(f"💾 Storing README at s3://{bucket}/{readme_key}")
            self.s3_client.put_object(
                Bucket=bucket,
                Key=readme_key,
                Body=readme_content.encode('utf-8'),
                ContentType='text/markdown'
            )
            
            # Generate CloudFront URL - Use consistent domain
            cloudfront_url = f"https://d2j9jbqms8047w.cloudfront.net/{readme_key}"
            
            # Return in Step Functions expected format
            success_response = {
                'success': True,
                'readme_content': readme_content,
                'readme_length': len(readme_content),
                's3_location': {
                    'bucket': bucket,
                    'key': readme_key
                },
                'download_url': cloudfront_url,
                'generation_timestamp': datetime.utcnow().isoformat(),
                'message': '🎉 Smart ReadmeGen: Enhanced README generated successfully!'
            }
            
            return {
                'statusCode': 200,
                'body': json.dumps(success_response)  # Step Functions expects this format!
            }
            
        except Exception as e:
            print(f"❌ Enhanced README generation failed: {str(e)}")
            import traceback
            traceback.print_exc()
            
            error_response = {
                'success': False,
                'error': f"Enhanced README generation failed: {str(e)}",
                'message': 'Enhanced README generation failed'
            }
            
            return {
                'statusCode': 500,
                'body': json.dumps(error_response)  # Step Functions expects this format!
            }
    
    def _generate_enhanced_readme(self, analysis_data: Dict[str, Any], github_url: str) -> str:
        """Generate enhanced README using Bedrock with extended timeout"""
        
        # Extract key information
        repo_info = analysis_data.get('repository_info', {})
        analysis_summary = analysis_data.get('analysis_summary', {})
        
        project_name = repo_info.get('name', 'Unknown Project')
        project_type = analysis_summary.get('project_type', 'Software Project')
        primary_language = analysis_summary.get('primary_language', 'Unknown')
        frameworks = analysis_summary.get('frameworks', [])
        
        # Create comprehensive prompt
        prompt = f"""
Create a comprehensive, professional README.md for this {project_type} project:

**Project Details:**
- Name: {project_name}
- Type: {project_type}
- Primary Language: {primary_language}
- Frameworks: {', '.join(frameworks) if frameworks else 'None detected'}
- Repository: {github_url}

**Analysis Data:**
{json.dumps(analysis_summary, indent=2)}

**Requirements:**
1. Create a complete, professional README with proper markdown formatting
2. Include sections: Overview, Features, Installation, Usage, Contributing, License
3. Add appropriate badges and shields
4. Use emojis for visual appeal
5. Include code examples where relevant
6. Make it engaging and comprehensive
7. Ensure proper markdown syntax
8. Add table of contents for long READMEs

Generate a high-quality README that would impress developers and users alike.
"""

        # Call Bedrock with extended timeout configuration
        try:
            print("🤖 Calling Bedrock Claude Sonnet 4 with extended timeout...")
            
            request_body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 4000,
                "temperature": 0.7,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
            
            # This should now use the extended timeout configuration
            response = self.bedrock_client.invoke_model(
                modelId=self.model_id,
                body=json.dumps(request_body)
            )
            
            response_body = json.loads(response['body'].read())
            readme_content = response_body['content'][0]['text']
            
            print(f"✅ Bedrock response received: {len(readme_content)} characters")
            return readme_content
            
        except Exception as e:
            print(f"❌ Bedrock call failed: {str(e)}")
            # Fallback to basic README if Bedrock fails
            return self._generate_fallback_readme(project_name, project_type, primary_language, frameworks, github_url)
    
    def _generate_fallback_readme(self, project_name: str, project_type: str, 
                                primary_language: str, frameworks: list, github_url: str) -> str:
        """Generate a basic README if Bedrock fails"""
        
        frameworks_text = ', '.join(frameworks) if frameworks else 'None'
        
        return f"""# {project_name}

> {project_type} built with {primary_language}

## 🚀 Overview

This is a {project_type.lower()} project developed using {primary_language}.

**Frameworks & Technologies:**
- Primary Language: {primary_language}
- Frameworks: {frameworks_text}

## 📦 Installation

```bash
# Clone the repository
git clone {github_url}
cd {project_name.lower().replace(' ', '-')}

# Install dependencies (adjust based on your project)
npm install  # for Node.js projects
# or
pip install -r requirements.txt  # for Python projects
```

## 🎯 Usage

```bash
# Run the application (adjust based on your project)
npm start  # for Node.js projects
# or
python main.py  # for Python projects
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

---

*Generated by Smart ReadmeGen - AI-Powered README Generation*
"""

# Lambda handler function
def lambda_handler(event, context):
    generator = EnhancedREADMEGenerator()
    return generator.lambda_handler(event, context)
