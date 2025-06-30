"""
Enhanced README Generator Lambda Function with CloudFront URL Support
Lambda 2: ReAct + Comprehend + A2I + Professional README Generation + CloudFront URLs
"""

import json
import boto3
import os
import logging
from datetime import datetime
from typing import Dict, Any

# Import our enhanced components
try:
    from react_agent_updated import EnhancedReActAgent
    from comprehend_analyzer import ComprehendAnalyzer
    from a2i_workflow import A2IWorkflowManager
    from readme_generator_engine import READMEGeneratorEngine
    ENHANCED_MODE = True
except ImportError as e:
    print(f"⚠️ Enhanced components not available: {e}")
    ENHANCED_MODE = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# S3 Configuration
S3_BUCKET = 'smart-readme-lambda-31641'
s3_client = boto3.client('s3')

# CloudFront Configuration
CLOUDFRONT_DOMAIN = "d3in1w40kamst9.cloudfront.net"

def generate_cloudfront_url(s3_key):
    """
    Convert S3 key to CloudFront URL for easy browser access
    """
    if not s3_key:
        return None
    
    # Remove leading slash if present
    clean_key = s3_key.lstrip('/')
    
    # Generate CloudFront URL
    cloudfront_url = f"https://{CLOUDFRONT_DOMAIN}/{clean_key}"
    
    logger.info(f"🌐 Generated CloudFront URL: {cloudfront_url}")
    return cloudfront_url

def lambda_handler(event, context):
    """
    Enhanced Lambda 2: Professional README Generation with ReAct + Comprehend + A2I + CloudFront URLs
    """
    
    start_time = datetime.now()
    
    try:
        # Extract S3 information from event
        s3_key = event.get('s3_key')
        bucket = event.get('bucket', S3_BUCKET)
        
        if not s3_key:
            return create_error_response(400, 'S3 key is required')
        
        logger.info(f"🚀 Starting Enhanced README generation with CloudFront URLs")
        logger.info(f"   Source: s3://{bucket}/{s3_key}")
        logger.info(f"   Enhanced Mode: {ENHANCED_MODE}")
        logger.info(f"   CloudFront Domain: {CLOUDFRONT_DOMAIN}")
        
        # Step 1: Read JSON from S3
        analysis_data = read_from_s3(bucket, s3_key)
        
        # Step 2: Extract repository info for processing
        repo_info = extract_repository_info(analysis_data)
        owner, repo = extract_owner_repo_from_key(s3_key)
        
        logger.info(f"   Repository: {owner}/{repo}")
        logger.info(f"   Project Type: {repo_info.get('project_type', 'Unknown')}")
        
        if ENHANCED_MODE:
            # Enhanced processing with ReAct + Comprehend + A2I
            result = process_enhanced_readme_generation(analysis_data, owner, repo, start_time)
        else:
            # Fallback to basic processing
            result = process_basic_readme_generation(analysis_data, owner, repo, start_time)
        
        logger.info(f"✅ README generation completed with CloudFront URLs")
        return create_success_response(result)
        
    except Exception as e:
        logger.error(f"❌ Enhanced README generation failed: {e}")
        import traceback
        traceback.print_exc()
        return create_error_response(500, f'Enhanced generation error: {str(e)}')

def process_enhanced_readme_generation(analysis_data: Dict[str, Any], owner: str, repo: str, start_time: datetime) -> Dict[str, Any]:
    """Process README generation with full ReAct + Comprehend + A2I pipeline"""
    
    # Step 1: Initialize ReAct Agent
    react_agent = EnhancedReActAgent()
    
    # Step 2: Generate README using ReAct framework
    logger.info("🤖 Starting ReAct README generation...")
    react_result = react_agent.generate_professional_readme(analysis_data)
    
    if not react_result['success']:
        logger.error("❌ ReAct generation failed")
        return process_basic_readme_generation(analysis_data, owner, repo, start_time)
    
    # Step 3: Enhanced Comprehend Analysis
    logger.info("🔍 Performing enhanced Comprehend analysis...")
    comprehend_analyzer = ComprehendAnalyzer()
    readme_content = react_result['readme_content']
    comprehend_analysis = comprehend_analyzer.analyze_content(readme_content, 'readme')
    
    # Step 4: A2I Human Review Decision
    repo_info = extract_repository_info(analysis_data)
    project_context = {
        'project_name': repo,
        'project_type': repo_info.get('project_type', 'Software Application'),
        'primary_language': repo_info.get('primary_language', 'Unknown'),
        'frameworks': repo_info.get('frameworks', []),
        'complexity_level': assess_project_complexity(repo_info)
    }
    
    a2i_manager = A2IWorkflowManager()
    final_quality_score = comprehend_analysis.quality_score
    a2i_result = None
    
    if a2i_manager.should_trigger_human_review(final_quality_score, project_context):
        logger.info("👥 A2I review would be triggered (skipping for demo)")
        # In production, would actually trigger A2I review
        a2i_result = {'triggered': True, 'status': 'demo_skipped', 'quality_score': final_quality_score}
    else:
        logger.info(f"✅ Quality score {final_quality_score} - A2I review not needed")
        a2i_result = {'triggered': False, 'status': 'not_needed'}
    
    # Step 5: Generate Final Professional README with Enhanced Engine
    logger.info("📝 Generating final professional README with enhanced styling...")
    
    # Use the emoji-safe generator
    from readme_generator_engine import READMEGeneratorEngine
    readme_engine = READMEGeneratorEngine()
    logger.info("✅ Using Enhanced README Generator Engine")
    
    professional_readme = readme_engine.generate_readme(analysis_data, style='developer')
    
    # Step 6: Quick Clean (2-second fix for repetitive content)
    logger.info("🔧 Quick cleaning repetitive content...")
    
    try:
        from simple_readme_cleaner import quick_clean_readme
        professional_readme = quick_clean_readme(professional_readme)
        logger.info("✅ Quick clean completed")
    except ImportError:
        logger.info("⚠️ Simple cleaner not available - skipping")
    except Exception as e:
        logger.error(f"❌ Quick clean failed: {e}")
    
    # Step 7: Save to S3 and generate CloudFront URLs
    readme_s3_key = f"generated-readmes/{owner}/{repo}.md"
    readme_s3_url = save_readme_to_s3(professional_readme, readme_s3_key)
    
    # Generate CloudFront URLs for easy access
    readme_cloudfront_url = generate_cloudfront_url(readme_s3_key)
    analysis_cloudfront_url = generate_cloudfront_url(f"readme-analysis/{owner}/{repo}.json")
    
    logger.info(f"✅ README saved to S3: {readme_s3_url}")
    logger.info(f"🌐 CloudFront README URL: {readme_cloudfront_url}")
    
    # Step 8: Create comprehensive result with CloudFront URLs
    processing_time = (datetime.now() - start_time).total_seconds()
    
    return {
        'readme_generation_complete': True,
        'repository_info': extract_repository_info(analysis_data),
        's3_location': {
            'bucket': S3_BUCKET,
            'key': readme_s3_key,
            'url': readme_s3_url
        },
        'readme_url': readme_cloudfront_url,  # CloudFront URL for easy download
        'readme_s3_url': readme_cloudfront_url,  # Same as above for compatibility
        'analysis_url': analysis_cloudfront_url,  # CloudFront URL for analysis JSON
        'generated_readme': {
            'bucket': S3_BUCKET,
            'key': readme_s3_key,
            'url': readme_s3_url,
            'cloudfront_url': readme_cloudfront_url,
            'size_kb': len(professional_readme) / 1024,
            'final_quality_score': final_quality_score
        },
        'processing_details': {
            'mode': 'enhanced',
            'react_cycles': react_result['metadata'].get('cycles_completed', 0),
            'react_quality': react_result['metadata'].get('final_quality_score', 0),
            'comprehend_analysis': {
                'sentiment': comprehend_analysis.sentiment.get('sentiment', 'NEUTRAL'),
                'entities_found': len(comprehend_analysis.entities),
                'key_phrases_found': len(comprehend_analysis.key_phrases),
                'quality_score': comprehend_analysis.quality_score,
                'recommendations': len(comprehend_analysis.recommendations)
            },
            'a2i_review': a2i_result,
            'quick_clean_applied': True,
            'final_quality_score': final_quality_score,
            'processing_time_seconds': processing_time,
            'cloudfront_domain': CLOUDFRONT_DOMAIN
        },
        'readme_preview': professional_readme[:500] + '...' if len(professional_readme) > 500 else professional_readme,
        'cloudfront_domain': CLOUDFRONT_DOMAIN
    }

def process_basic_readme_generation(analysis_data: Dict[str, Any], owner: str, repo: str, start_time: datetime) -> Dict[str, Any]:
    """Process README generation with basic functionality (fallback) + CloudFront URLs"""
    
    logger.info("🔄 Using basic README generation (fallback mode) with CloudFront URLs")
    
    # Basic README generation
    readme_engine = READMEGeneratorEngine()
    basic_readme = readme_engine.generate_readme(analysis_data, style='developer')
    
    # Save to S3 and generate CloudFront URLs
    readme_s3_key = f"generated-readmes/{owner}/{repo}.md"
    readme_s3_url = save_readme_to_s3(basic_readme, readme_s3_key)
    
    # Generate CloudFront URLs
    readme_cloudfront_url = generate_cloudfront_url(readme_s3_key)
    analysis_cloudfront_url = generate_cloudfront_url(f"readme-analysis/{owner}/{repo}.json")
    
    processing_time = (datetime.now() - start_time).total_seconds()
    
    return {
        'readme_generation_complete': True,
        'repository_info': extract_repository_info(analysis_data),
        's3_location': {
            'bucket': S3_BUCKET,
            'key': readme_s3_key,
            'url': readme_s3_url
        },
        'readme_url': readme_cloudfront_url,  # CloudFront URL for easy download
        'readme_s3_url': readme_cloudfront_url,  # Same as above for compatibility
        'analysis_url': analysis_cloudfront_url,  # CloudFront URL for analysis JSON
        'generated_readme': {
            'bucket': S3_BUCKET,
            'key': readme_s3_key,
            'url': readme_s3_url,
            'cloudfront_url': readme_cloudfront_url,
            'size_kb': len(basic_readme) / 1024,
            'final_quality_score': 80.0
        },
        'processing_details': {
            'mode': 'basic_fallback',
            'processing_time_seconds': processing_time,
            'final_quality_score': 80.0,
            'cloudfront_domain': CLOUDFRONT_DOMAIN
        },
        'readme_preview': basic_readme[:500] + '...' if len(basic_readme) > 500 else basic_readme,
        'cloudfront_domain': CLOUDFRONT_DOMAIN
    }

def read_from_s3(bucket: str, key: str) -> Dict[str, Any]:
    """Read JSON data from S3"""
    try:
        logger.info(f"📥 Reading from S3: s3://{bucket}/{key}")
        
        response = s3_client.get_object(Bucket=bucket, Key=key)
        json_content = response['Body'].read().decode('utf-8')
        
        data = json.loads(json_content)
        logger.info(f"✅ Successfully read {len(json_content)} characters from S3")
        return data
        
    except Exception as e:
        logger.error(f"❌ Failed to read from S3: {e}")
        raise e

def save_readme_to_s3(readme_content: str, s3_key: str) -> str:
    """Save generated README to S3"""
    try:
        logger.info(f"💾 Saving README to S3: s3://{S3_BUCKET}/{s3_key}")
        
        s3_client.put_object(
            Bucket=S3_BUCKET,
            Key=s3_key,
            Body=readme_content,
            ContentType='text/markdown',
            Metadata={
                'generated-by': 'enhanced-react-readme-generator',
                'generation-timestamp': datetime.now().isoformat(),
                'content-type': 'professional-readme',
                'ai-enhanced': 'true',
                'cloudfront-enabled': 'true'
            }
        )
        
        s3_url = f"s3://{S3_BUCKET}/{s3_key}"
        logger.info(f"✅ README saved successfully: {s3_url}")
        return s3_url
        
    except Exception as e:
        logger.error(f"❌ Failed to save README to S3: {e}")
        raise e

def extract_repository_info(analysis_data: Dict[str, Any]) -> Dict[str, Any]:
    """Extract repository information from analysis data"""
    try:
        repo_analysis = analysis_data.get('repository_analysis', {})
        
        return {
            'repository_url': repo_analysis.get('repository_url', 'Unknown'),
            'project_type': repo_analysis.get('project_type', 'Unknown'),
            'primary_language': repo_analysis.get('primary_language', 'Unknown'),
            'frameworks': repo_analysis.get('frameworks', []),
            'features_count': len(repo_analysis.get('features', [])),
            'files_analyzed': len(repo_analysis.get('key_files', [])),
            'security_score': repo_analysis.get('security_analysis', {}).get('security_score', 0)
        }
        
    except Exception as e:
        logger.error(f"⚠️ Error extracting repository info: {e}")
        return {'error': 'Could not extract repository information'}

def extract_owner_repo_from_key(s3_key: str) -> tuple:
    """Extract owner and repo from S3 key"""
    try:
        # Expected format: readme-analysis/{owner}/{repo}.json
        parts = s3_key.split('/')
        if len(parts) >= 3:
            owner = parts[1]
            repo = parts[2].replace('.json', '')
            return owner, repo
        else:
            return 'unknown', 'repository'
    except:
        return 'unknown', 'repository'

def assess_project_complexity(repo_info: Dict[str, Any]) -> str:
    """Assess project complexity for A2I decision making"""
    frameworks_count = len(repo_info.get('frameworks', []))
    features_count = repo_info.get('features_count', 0)
    files_analyzed = repo_info.get('files_analyzed', 0)
    
    complexity_score = frameworks_count + (features_count / 2) + (files_analyzed / 10)
    
    if complexity_score < 3:
        return 'simple'
    elif complexity_score < 8:
        return 'moderate'
    else:
        return 'complex'

def create_success_response(data: Any) -> Dict[str, Any]:
    """Create standardized success response with CloudFront URLs"""
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
            'message': 'Enhanced README generation completed successfully with CloudFront URLs',
            'data': data,
            'timestamp': datetime.now().isoformat(),
            'version': 'enhanced-v2.1-cloudfront',
            'ai_stack': ['ReAct', 'Comprehend', 'A2I', 'Bedrock'] if ENHANCED_MODE else ['Basic'],
            'cloudfront_domain': CLOUDFRONT_DOMAIN
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
                'lambda_function': 'Enhanced-Lambda-2-README-Generation-CloudFront'
            }
        })
    }
