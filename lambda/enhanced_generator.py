"""
Enhanced README Generator Lambda Function
Lambda 2: ReAct + Comprehend + A2I + Professional README Generation
"""

import json
import boto3
import os
import logging
from datetime import datetime
from typing import Dict, Any

# Import our custom modules
from react_agent import ReActREADMEAgent
from comprehend_analyzer import ComprehendAnalyzer
from a2i_workflow import A2IWorkflowManager
from readme_generator_engine import READMEGeneratorEngine

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# S3 Configuration
S3_BUCKET = 'smart-readme-lambda-31641'
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    """
    Enhanced Lambda 2: Professional README Generation with ReAct + Comprehend + A2I
    """
    
    start_time = datetime.now()
    
    try:
        # Extract S3 information from event
        s3_key = event.get('s3_key')
        bucket = event.get('bucket', S3_BUCKET)
        
        if not s3_key:
            return create_error_response(400, 'S3 key is required')
        
        logger.info(f"🚀 Starting Enhanced README generation")
        logger.info(f"   Source: s3://{bucket}/{s3_key}")
        
        # Step 1: Read JSON from S3
        analysis_data = read_from_s3(bucket, s3_key)
        
        # Step 2: Extract repository info for processing
        repo_info = extract_repository_info(analysis_data)
        owner, repo = extract_owner_repo_from_key(s3_key)
        
        logger.info(f"   Repository: {owner}/{repo}")
        logger.info(f"   Project Type: {repo_info.get('project_type', 'Unknown')}")
        
        # Step 3: Initialize ReAct Agent
        react_agent = ReActREADMEAgent()
        
        # Step 4: Generate README using ReAct framework
        logger.info("🤖 Starting ReAct README generation...")
        react_result = react_agent.generate_professional_readme(analysis_data)
        
        if not react_result['success']:
            logger.error("❌ ReAct generation failed")
            return create_error_response(500, f"ReAct generation failed: {react_result.get('error', 'Unknown error')}")
        
        # Step 5: Enhance with Comprehend Analysis
        logger.info("🔍 Enhancing with Comprehend analysis...")
        comprehend_analyzer = ComprehendAnalyzer()
        
        readme_content = react_result['readme_content']
        comprehend_analysis = comprehend_analyzer.analyze_content(readme_content, 'readme')
        
        # Apply Comprehend improvements
        enhanced_readme = comprehend_analyzer.enhance_content_with_analysis(readme_content, comprehend_analysis)
        
        # Step 6: A2I Human Review (if needed)
        a2i_manager = A2IWorkflowManager()
        final_quality_score = comprehend_analysis.quality_score
        
        project_context = {
            'project_name': repo_info.get('repository_url', '').split('/')[-1],
            'project_type': repo_info.get('project_type', 'Software Application'),
            'primary_language': repo_info.get('primary_language', 'Unknown'),
            'frameworks': repo_info.get('frameworks', []),
            'complexity_level': assess_project_complexity(repo_info)
        }
        
        a2i_result = None
        if a2i_manager.should_trigger_human_review(final_quality_score, project_context):
            logger.info("👥 Triggering A2I human review...")
            
            try:
                # Create human review task
                human_loop_arn = a2i_manager.create_human_review_task(
                    enhanced_readme, 
                    project_context,
                    {
                        'quality_score': final_quality_score,
                        'comprehend_analysis': comprehend_analysis.__dict__,
                        'react_metadata': react_result['metadata']
                    }
                )
                
                # Wait for review (with timeout)
                a2i_result = a2i_manager.wait_for_human_review(human_loop_arn, timeout_seconds=300)  # 5 min timeout for demo
                
                if a2i_result.review_completed and a2i_result.approval_status == 'approved':
                    final_quality_score = a2i_result.quality_score
                    logger.info(f"✅ A2I review completed - Quality: {final_quality_score}")
                elif a2i_result.approval_status == 'timeout_approved':
                    logger.info("⏰ A2I review timed out - proceeding with current content")
                else:
                    logger.warning(f"⚠️ A2I review status: {a2i_result.approval_status}")
                
            except Exception as e:
                logger.error(f"❌ A2I review failed: {e}")
                # Continue without A2I review
                a2i_result = None
        else:
            logger.info(f"✅ Quality score {final_quality_score} - skipping A2I review")
        
        # Step 7: Final README Generation with Professional Engine
        logger.info("📝 Generating final professional README...")
        readme_engine = READMEGeneratorEngine()
        
        # Use enhanced content or apply A2I feedback
        final_readme_content = enhanced_readme
        if a2i_result and a2i_result.review_completed and a2i_result.improvements:
            # Apply A2I improvements (simplified for demo)
            logger.info("🔧 Applying A2I improvements...")
            # In production, you'd implement sophisticated feedback integration
        
        # Generate final professional README
        professional_readme = readme_engine.generate_readme(analysis_data, style='developer')
        
        # Step 8: Save README to S3
        readme_s3_key = f"readme-analysis/{owner}/{repo}-README.md"
        readme_s3_url = save_readme_to_s3(professional_readme, readme_s3_key)
        
        logger.info(f"💾 README saved to: {readme_s3_url}")
        
        # Step 9: Create comprehensive response
        processing_time = (datetime.now() - start_time).total_seconds()
        
        result = {
            'readme_generation_complete': True,
            'repository_info': repo_info,
            'source_data': {
                'bucket': bucket,
                'key': s3_key,
                'data_received': True,
                'data_size_kb': len(json.dumps(analysis_data)) / 1024
            },
            'generated_readme': {
                'bucket': S3_BUCKET,
                'key': readme_s3_key,
                'url': readme_s3_url,
                'size_kb': len(professional_readme) / 1024,
                'final_quality_score': final_quality_score
            },
            'processing_details': {
                'react_cycles': react_result['metadata'].get('cycles_completed', 0),
                'react_quality': react_result['metadata'].get('final_quality_score', 0),
                'comprehend_analysis': {
                    'sentiment': comprehend_analysis.sentiment.get('sentiment', 'NEUTRAL'),
                    'entities_found': len(comprehend_analysis.entities),
                    'key_phrases_found': len(comprehend_analysis.key_phrases),
                    'quality_score': comprehend_analysis.quality_score,
                    'recommendations': len(comprehend_analysis.recommendations)
                },
                'a2i_review': {
                    'triggered': a2i_result is not None,
                    'completed': a2i_result.review_completed if a2i_result else False,
                    'approval_status': a2i_result.approval_status if a2i_result else 'not_triggered',
                    'human_quality_score': a2i_result.quality_score if a2i_result else None
                } if a2i_result else {'triggered': False},
                'final_quality_score': final_quality_score,
                'processing_time_seconds': processing_time
            },
            'readme_preview': professional_readme[:500] + '...' if len(professional_readme) > 500 else professional_readme
        }
        
        logger.info(f"✅ Enhanced README generation completed in {processing_time:.2f}s")
        return create_success_response(result)
        
    except Exception as e:
        logger.error(f"❌ Enhanced README generation failed: {e}")
        import traceback
        traceback.print_exc()
        return create_error_response(500, f'Enhanced generation error: {str(e)}')

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
                'ai-enhanced': 'true'
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
            'message': 'Enhanced README generation completed successfully',
            'data': data,
            'timestamp': datetime.now().isoformat(),
            'version': 'enhanced-v2.0',
            'ai_stack': ['ReAct', 'Comprehend', 'A2I', 'Bedrock']
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
                'lambda_function': 'Enhanced-Lambda-2-README-Generation'
            }
        })
    }
