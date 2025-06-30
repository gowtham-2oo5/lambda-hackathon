"""
Email Notification Service for README Generator
Sends professional email notifications via SES
"""

import json
import boto3
from datetime import datetime
from typing import Dict, Any

class EmailNotificationService:
    def __init__(self):
        self.ses_client = boto3.client('ses', region_name='us-east-1')
        self.sender_email = 'gowtham.ala.2oo5@gmail.com'  # Correct verified SES email
        
    def lambda_handler(self, event, context):
        """📧 Email Notification Handler"""
        try:
            print(f"📧 Email notification starting with event: {json.dumps(event)}")
            
            # Extract data from Step Functions
            user_email = event.get('user_email') or event.get('email')
            github_url = event.get('github_url', 'Unknown Repository')
            
            # Get analysis and README data
            analysis_data = event.get('analysisData', {}).get('data', {})
            readme_data = event.get('readmeData', {})
            
            if not user_email:
                raise Exception("User email is required")
            
            # Extract repository info
            repo_parts = github_url.replace('https://github.com/', '').split('/')
            repo_owner = repo_parts[0] if len(repo_parts) > 0 else 'Unknown'
            repo_name = repo_parts[1] if len(repo_parts) > 1 else 'Unknown'
            
            # Get analysis summary
            analysis_summary = analysis_data.get('analysis_summary', {})
            project_type = analysis_summary.get('project_type', 'Software Project')
            confidence = analysis_summary.get('project_type_confidence', 0.0)
            frameworks = analysis_summary.get('frameworks', [])
            
            # Get README info
            readme_length = readme_data.get('readme_length', 0)
            s3_location = readme_data.get('s3_location', {})
            
            # Generate CloudFront URLs
            cloudfront_url = f"https://d3in1w40kamst9.cloudfront.net/{s3_location.get('key', '')}"
            dashboard_url = "https://your-dashboard-url.com"  # Update with actual dashboard URL
            
            # Send email notification
            self._send_success_email(
                user_email=user_email,
                repo_owner=repo_owner,
                repo_name=repo_name,
                github_url=github_url,
                project_type=project_type,
                confidence=confidence,
                frameworks=frameworks,
                readme_length=readme_length,
                download_url=cloudfront_url,
                dashboard_url=dashboard_url
            )
            
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'success': True,
                    'message': 'Email notification sent successfully',
                    'recipient': user_email,
                    'notification_type': 'readme_generation_success',
                    'timestamp': datetime.utcnow().isoformat()
                })
            }
            
        except Exception as e:
            print(f"❌ Email notification error: {str(e)}")
            import traceback
            traceback.print_exc()
            
            return {
                'statusCode': 500,
                'body': json.dumps({
                    'success': False,
                    'error': str(e),
                    'message': 'Email notification failed'
                })
            }
    
    def _send_success_email(self, user_email: str, repo_owner: str, repo_name: str, 
                           github_url: str, project_type: str, confidence: float,
                           frameworks: list, readme_length: int, download_url: str, 
                           dashboard_url: str):
        """Send professional success email"""
        
        # Create email subject
        subject = f"🎉 README Generated Successfully for {repo_owner}/{repo_name}"
        
        # Create HTML email body
        html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>README Generation Complete</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
        .content {{ background: #f8f9fa; padding: 30px; border-radius: 0 0 10px 10px; }}
        .success-badge {{ background: #28a745; color: white; padding: 8px 16px; border-radius: 20px; display: inline-block; font-weight: bold; }}
        .stats-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 20px 0; }}
        .stat-card {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .cta-button {{ background: #007bff; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; display: inline-block; font-weight: bold; margin: 10px 5px; }}
        .cta-button:hover {{ background: #0056b3; }}
        .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 14px; }}
        .frameworks {{ background: #e9ecef; padding: 10px; border-radius: 5px; margin: 10px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏆 Phase 3 Ultimate AI Platform</h1>
            <p>Your README has been generated successfully!</p>
            <div class="success-badge">✅ Generation Complete</div>
        </div>
        
        <div class="content">
            <h2>📊 Repository Analysis Results</h2>
            <p><strong>Repository:</strong> <a href="{github_url}" style="color: #007bff;">{repo_owner}/{repo_name}</a></p>
            
            <div class="stats-grid">
                <div class="stat-card">
                    <h3>🎯 Project Analysis</h3>
                    <p><strong>Type:</strong> {project_type}</p>
                    <p><strong>Confidence:</strong> {confidence:.1%}</p>
                </div>
                <div class="stat-card">
                    <h3>📝 README Stats</h3>
                    <p><strong>Length:</strong> {readme_length:,} characters</p>
                    <p><strong>Quality:</strong> Professional Grade</p>
                </div>
            </div>
            
            {f'<div class="frameworks"><strong>🚀 Frameworks Detected:</strong> {", ".join(frameworks)}</div>' if frameworks else ''}
            
            <h3>🎨 Enhanced Features Included:</h3>
            <ul>
                <li>✅ Advanced HTML styling and layout</li>
                <li>✅ Professional badges and shields</li>
                <li>✅ Collapsible sections and tables</li>
                <li>✅ Progress bars and visual indicators</li>
                <li>✅ Mobile-responsive design</li>
                <li>✅ SEO-optimized structure</li>
            </ul>
            
            <div style="text-align: center; margin: 30px 0;">
                <a href="{download_url}" class="cta-button">📥 Download README.md</a>
                <a href="{dashboard_url}" class="cta-button">📊 View Dashboard</a>
            </div>
            
            <div style="background: #d1ecf1; border: 1px solid #bee5eb; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <strong>💡 Pro Tip:</strong> Your README includes advanced markdown and HTML features that will make your repository stand out on GitHub!
            </div>
        </div>
        
        <div class="footer">
            <p>Generated by Phase 3 Ultimate AI Platform</p>
            <p>Powered by AWS Lambda, Bedrock, and Claude Sonnet 4</p>
            <p><small>This email was sent because you requested README generation for {github_url}</small></p>
        </div>
    </div>
</body>
</html>
"""
        
        # Create plain text version
        text_body = f"""
🎉 README Generated Successfully!

Repository: {repo_owner}/{repo_name}
GitHub URL: {github_url}

📊 Analysis Results:
- Project Type: {project_type}
- Confidence: {confidence:.1%}
- Frameworks: {', '.join(frameworks) if frameworks else 'None detected'}

📝 README Stats:
- Length: {readme_length:,} characters
- Quality: Professional Grade with advanced HTML styling

🎨 Enhanced Features:
✅ Advanced HTML styling and layout
✅ Professional badges and shields  
✅ Collapsible sections and tables
✅ Progress bars and visual indicators
✅ Mobile-responsive design
✅ SEO-optimized structure

📥 Download your README: {download_url}
📊 View your dashboard: {dashboard_url}

Generated by Phase 3 Ultimate AI Platform
Powered by AWS Lambda, Bedrock, and Claude Sonnet 4
"""
        
        # Send email via SES
        try:
            response = self.ses_client.send_email(
                Source=self.sender_email,
                Destination={'ToAddresses': [user_email]},
                Message={
                    'Subject': {'Data': subject, 'Charset': 'UTF-8'},
                    'Body': {
                        'Html': {'Data': html_body, 'Charset': 'UTF-8'},
                        'Text': {'Data': text_body, 'Charset': 'UTF-8'}
                    }
                }
            )
            
            print(f"✅ Email sent successfully to {user_email}")
            print(f"SES Message ID: {response['MessageId']}")
            
        except Exception as e:
            print(f"❌ SES email sending failed: {str(e)}")
            raise Exception(f"Failed to send email: {str(e)}")


# Lambda entry point
def lambda_handler(event, context):
    """📧 Email Notification Service Entry Point"""
    service = EmailNotificationService()
    return service.lambda_handler(event, context)
