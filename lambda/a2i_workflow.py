"""
Amazon A2I (Augmented AI) Integration for Human-in-the-Loop README Review
Provides quality validation and human feedback for professional standards
"""

import boto3
import json
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)

@dataclass
class A2IReviewResult:
    """Result of A2I human review process"""
    review_completed: bool
    quality_score: float
    human_feedback: Dict[str, Any]
    improvements: List[str]
    approval_status: str  # 'approved', 'needs_revision', 'rejected'
    review_time_seconds: float
    reviewer_confidence: float

class A2IWorkflowManager:
    """
    Amazon A2I integration for human-in-the-loop README quality review
    """
    
    def __init__(self, region: str = 'us-east-1'):
        self.region = region
        self.sagemaker_a2i = boto3.client('sagemaker-a2i-runtime', region_name=region)
        self.sagemaker = boto3.client('sagemaker', region_name=region)
        self.s3_client = boto3.client('s3', region_name=region)
        
        # A2I Configuration
        self.flow_definition_name = 'readme-quality-review-flow'
        self.human_task_ui_name = 'readme-review-ui'
        self.workteam_arn = None  # Will be set during initialization
        
        # Quality thresholds
        self.quality_threshold = 85.0  # Trigger human review below this
        self.auto_approve_threshold = 95.0  # Auto-approve above this
        
        # Review criteria
        self.review_criteria = {
            'completeness': 'All necessary sections present and well-structured',
            'clarity': 'Clear, concise, and easy to understand',
            'technical_accuracy': 'Technical information is accurate and up-to-date',
            'professional_tone': 'Professional, engaging, and appropriate tone',
            'formatting': 'Proper markdown formatting and visual appeal',
            'usability': 'Easy to follow installation and usage instructions'
        }
    
    def should_trigger_human_review(self, quality_score: float, project_context: Dict[str, Any]) -> bool:
        """
        Determine if human review should be triggered
        """
        # Always review if below threshold
        if quality_score < self.quality_threshold:
            logger.info(f"🔍 Triggering A2I review - Quality score {quality_score} below threshold {self.quality_threshold}")
            return True
        
        # Auto-approve if very high quality
        if quality_score >= self.auto_approve_threshold:
            logger.info(f"✅ Auto-approving - Quality score {quality_score} above auto-approve threshold")
            return False
        
        # Consider project complexity for borderline cases
        complexity = project_context.get('complexity_level', 'simple')
        if complexity == 'complex' and quality_score < 90:
            logger.info(f"🔍 Triggering A2I review - Complex project with quality score {quality_score}")
            return True
        
        return False
    
    def create_human_review_task(self, readme_content: str, project_context: Dict[str, Any], 
                                quality_analysis: Dict[str, Any]) -> str:
        """
        Create A2I human review task
        """
        logger.info("👥 Creating A2I human review task")
        
        try:
            # Generate unique task name
            task_name = f"readme-review-{uuid.uuid4().hex[:8]}"
            
            # Prepare input data for human reviewers
            human_task_input = {
                'readme_content': readme_content,
                'project_info': {
                    'name': project_context.get('project_name', 'Unknown Project'),
                    'type': project_context.get('project_type', 'Software Application'),
                    'language': project_context.get('primary_language', 'Unknown'),
                    'frameworks': project_context.get('frameworks', []),
                    'complexity': project_context.get('complexity_level', 'simple')
                },
                'quality_analysis': {
                    'ai_quality_score': quality_analysis.get('quality_score', 0),
                    'comprehend_analysis': quality_analysis.get('comprehend_analysis', {}),
                    'identified_issues': quality_analysis.get('issues', []),
                    'suggested_improvements': quality_analysis.get('improvements', [])
                },
                'review_criteria': self.review_criteria,
                'instructions': self._generate_review_instructions(project_context)
            }
            
            # Create human loop
            response = self.sagemaker_a2i.start_human_loop(
                HumanLoopName=task_name,
                FlowDefinitionArn=self._get_flow_definition_arn(),
                HumanLoopInput={
                    'InputContent': json.dumps(human_task_input)
                }
            )
            
            human_loop_arn = response['HumanLoopArn']
            logger.info(f"✅ A2I task created: {human_loop_arn}")
            
            return human_loop_arn
            
        except Exception as e:
            logger.error(f"❌ Failed to create A2I task: {e}")
            raise e
    
    def wait_for_human_review(self, human_loop_arn: str, timeout_seconds: int = 3600) -> A2IReviewResult:
        """
        Wait for human review completion (with timeout)
        """
        logger.info(f"⏳ Waiting for human review completion (timeout: {timeout_seconds}s)")
        
        start_time = datetime.now()
        
        try:
            while True:
                # Check review status
                response = self.sagemaker_a2i.describe_human_loop(
                    HumanLoopName=human_loop_arn.split('/')[-1]
                )
                
                status = response['HumanLoopStatus']
                
                if status == 'Completed':
                    # Review completed - get results
                    return self._process_human_review_results(response)
                
                elif status == 'Failed':
                    logger.error("❌ Human review failed")
                    return self._create_failed_review_result("Human review failed")
                
                elif status == 'Stopped':
                    logger.warning("⚠️ Human review was stopped")
                    return self._create_failed_review_result("Human review was stopped")
                
                # Check timeout
                elapsed = (datetime.now() - start_time).total_seconds()
                if elapsed > timeout_seconds:
                    logger.warning(f"⏰ Human review timeout after {elapsed}s")
                    return self._create_timeout_review_result(elapsed)
                
                # Wait before next check
                import time
                time.sleep(30)  # Check every 30 seconds
                
        except Exception as e:
            logger.error(f"❌ Error waiting for human review: {e}")
            return self._create_failed_review_result(str(e))
    
    def _process_human_review_results(self, describe_response: Dict[str, Any]) -> A2IReviewResult:
        """
        Process completed human review results
        """
        try:
            # Get human review output
            output_s3_uri = describe_response['HumanLoopOutput']['OutputS3Uri']
            review_data = self._read_s3_review_output(output_s3_uri)
            
            # Parse human feedback
            human_answers = review_data.get('humanAnswers', [])
            
            if not human_answers:
                return self._create_failed_review_result("No human answers found")
            
            # Process the first (and typically only) human answer
            answer = human_answers[0]
            answer_content = json.loads(answer.get('answerContent', '{}'))
            
            # Extract review results
            quality_scores = answer_content.get('quality_scores', {})
            overall_score = sum(quality_scores.values()) / len(quality_scores) if quality_scores else 0
            
            feedback = answer_content.get('feedback', {})
            improvements = answer_content.get('improvements', [])
            approval_status = answer_content.get('approval_status', 'needs_revision')
            
            # Calculate review time
            creation_time = describe_response.get('CreationTime')
            completion_time = describe_response.get('HumanLoopOutput', {}).get('OutputS3Uri')  # Approximate
            review_time = 0  # Would need more precise timing from A2I
            
            return A2IReviewResult(
                review_completed=True,
                quality_score=overall_score * 20,  # Convert to 0-100 scale
                human_feedback=feedback,
                improvements=improvements,
                approval_status=approval_status,
                review_time_seconds=review_time,
                reviewer_confidence=answer_content.get('confidence', 0.8)
            )
            
        except Exception as e:
            logger.error(f"❌ Error processing human review results: {e}")
            return self._create_failed_review_result(str(e))
    
    def _read_s3_review_output(self, s3_uri: str) -> Dict[str, Any]:
        """
        Read human review output from S3
        """
        try:
            # Parse S3 URI
            parts = s3_uri.replace('s3://', '').split('/')
            bucket = parts[0]
            key = '/'.join(parts[1:])
            
            # Read from S3
            response = self.s3_client.get_object(Bucket=bucket, Key=key)
            content = response['Body'].read().decode('utf-8')
            
            return json.loads(content)
            
        except Exception as e:
            logger.error(f"❌ Failed to read S3 review output: {e}")
            return {}
    
    def _get_flow_definition_arn(self) -> str:
        """
        Get or create A2I flow definition ARN
        """
        try:
            # Try to describe existing flow definition
            response = self.sagemaker.describe_flow_definition(
                FlowDefinitionName=self.flow_definition_name
            )
            return response['FlowDefinitionArn']
            
        except self.sagemaker.exceptions.ResourceNotFound:
            # Create new flow definition
            return self._create_flow_definition()
        except Exception as e:
            logger.error(f"❌ Error getting flow definition: {e}")
            # Return a mock ARN for development
            return f"arn:aws:sagemaker:{self.region}:123456789012:flow-definition/{self.flow_definition_name}"
    
    def _create_flow_definition(self) -> str:
        """
        Create A2I flow definition for README review
        """
        logger.info("🔧 Creating A2I flow definition")
        
        try:
            # Create human task UI first
            human_task_ui_arn = self._create_human_task_ui()
            
            # Create flow definition
            response = self.sagemaker.create_flow_definition(
                FlowDefinitionName=self.flow_definition_name,
                HumanLoopRequestSource={
                    'AwsManagedHumanLoopRequestSource': 'AWS/Textract/AnalyzeDocument/Forms/V1'
                },
                HumanLoopActivationConfig={
                    'HumanLoopActivationConditionsConfig': {
                        'HumanLoopActivationConditions': json.dumps({
                            "conditions": [
                                {
                                    "ConditionType": "Sampling",
                                    "ConditionParameters": {
                                        "RandomSamplingPercentage": 100
                                    }
                                }
                            ]
                        })
                    }
                },
                HumanLoopConfig={
                    'WorkteamArn': self._get_workteam_arn(),
                    'HumanTaskUiArn': human_task_ui_arn,
                    'TaskTitle': 'README Quality Review',
                    'TaskDescription': 'Review and validate the quality of AI-generated README documentation',
                    'TaskCount': 1,
                    'TaskAvailabilityLifetimeInSeconds': 3600,  # 1 hour
                    'TaskTimeLimitInSeconds': 1800,  # 30 minutes per task
                    'TaskKeywords': ['readme', 'documentation', 'quality', 'review']
                },
                OutputConfig={
                    'S3OutputPath': f's3://smart-readme-lambda-31641/a2i-output/'
                },
                RoleArn=self._get_execution_role_arn()
            )
            
            flow_definition_arn = response['FlowDefinitionArn']
            logger.info(f"✅ Flow definition created: {flow_definition_arn}")
            
            return flow_definition_arn
            
        except Exception as e:
            logger.error(f"❌ Failed to create flow definition: {e}")
            # Return mock ARN for development
            return f"arn:aws:sagemaker:{self.region}:123456789012:flow-definition/{self.flow_definition_name}"
    
    def _create_human_task_ui(self) -> str:
        """
        Create human task UI for README review
        """
        ui_template = self._get_readme_review_ui_template()
        
        try:
            response = self.sagemaker.create_human_task_ui(
                HumanTaskUiName=self.human_task_ui_name,
                UiTemplate={
                    'Content': ui_template
                }
            )
            
            return response['HumanTaskUiArn']
            
        except Exception as e:
            logger.error(f"❌ Failed to create human task UI: {e}")
            # Return mock ARN for development
            return f"arn:aws:sagemaker:{self.region}:123456789012:human-task-ui/{self.human_task_ui_name}"
    
    def _get_readme_review_ui_template(self) -> str:
        """
        Get HTML template for README review UI
        """
        return """
        <script src="https://assets.crowd.aws/crowd-html-elements.js"></script>
        
        <crowd-form>
            <crowd-instructions link-text="View full instructions" link-type="button">
                <short-summary>
                    Review the AI-generated README for quality, completeness, and professional standards.
                </short-summary>
                <detailed-instructions>
                    <h3>README Quality Review</h3>
                    <p>Please evaluate the README documentation based on the following criteria:</p>
                    <ul>
                        <li><strong>Completeness:</strong> All necessary sections are present</li>
                        <li><strong>Clarity:</strong> Information is clear and easy to understand</li>
                        <li><strong>Technical Accuracy:</strong> Technical details are correct</li>
                        <li><strong>Professional Tone:</strong> Language is professional and engaging</li>
                        <li><strong>Formatting:</strong> Proper markdown and visual appeal</li>
                        <li><strong>Usability:</strong> Instructions are easy to follow</li>
                    </ul>
                </detailed-instructions>
            </crowd-instructions>
            
            <div>
                <h2>Project Information</h2>
                <p><strong>Project:</strong> {{ task.input.project_info.name }}</p>
                <p><strong>Type:</strong> {{ task.input.project_info.type }}</p>
                <p><strong>Language:</strong> {{ task.input.project_info.language }}</p>
                <p><strong>AI Quality Score:</strong> {{ task.input.quality_analysis.ai_quality_score }}%</p>
            </div>
            
            <div>
                <h2>README Content</h2>
                <crowd-text-area name="readme_content" rows="20" readonly>
                    {{ task.input.readme_content }}
                </crowd-text-area>
            </div>
            
            <div>
                <h2>Quality Assessment</h2>
                <p>Rate each aspect from 1 (Poor) to 5 (Excellent):</p>
                
                <crowd-radio-group>
                    <crowd-radio-button name="completeness" value="1">1 - Poor</crowd-radio-button>
                    <crowd-radio-button name="completeness" value="2">2 - Fair</crowd-radio-button>
                    <crowd-radio-button name="completeness" value="3">3 - Good</crowd-radio-button>
                    <crowd-radio-button name="completeness" value="4">4 - Very Good</crowd-radio-button>
                    <crowd-radio-button name="completeness" value="5">5 - Excellent</crowd-radio-button>
                </crowd-radio-group>
                
                <!-- Similar radio groups for other criteria -->
            </div>
            
            <div>
                <h2>Overall Decision</h2>
                <crowd-radio-group>
                    <crowd-radio-button name="approval_status" value="approved">Approve - Ready for use</crowd-radio-button>
                    <crowd-radio-button name="approval_status" value="needs_revision">Needs Revision</crowd-radio-button>
                    <crowd-radio-button name="approval_status" value="rejected">Reject - Major issues</crowd-radio-button>
                </crowd-radio-group>
            </div>
            
            <div>
                <h2>Feedback and Improvements</h2>
                <crowd-text-area name="feedback" placeholder="Provide specific feedback and suggestions for improvement..."></crowd-text-area>
            </div>
        </crowd-form>
        """
    
    def _get_workteam_arn(self) -> str:
        """Get workteam ARN (would be configured in real deployment)"""
        # In real deployment, this would be a configured workteam
        return f"arn:aws:sagemaker:{self.region}:123456789012:workteam/private-crowd/readme-reviewers"
    
    def _get_execution_role_arn(self) -> str:
        """Get execution role ARN for A2I"""
        # In real deployment, this would be a configured IAM role
        return f"arn:aws:iam::123456789012:role/A2IExecutionRole"
    
    def _generate_review_instructions(self, project_context: Dict[str, Any]) -> str:
        """Generate specific review instructions based on project context"""
        project_type = project_context.get('project_type', 'Software Application')
        complexity = project_context.get('complexity_level', 'simple')
        
        instructions = f"""
        Review Instructions for {project_type}:
        
        1. Verify that the README accurately represents a {project_type}
        2. Check that installation instructions are appropriate for the technology stack
        3. Ensure usage examples are relevant and helpful
        4. Validate that the technical information is accurate
        
        Project Complexity: {complexity.title()}
        """
        
        if complexity == 'complex':
            instructions += """
        
        Additional considerations for complex projects:
        - Architecture documentation should be comprehensive
        - API documentation should be detailed
        - Deployment instructions should cover multiple scenarios
        """
        
        return instructions
    
    def _create_failed_review_result(self, error_message: str) -> A2IReviewResult:
        """Create failed review result"""
        return A2IReviewResult(
            review_completed=False,
            quality_score=0.0,
            human_feedback={'error': error_message},
            improvements=[],
            approval_status='failed',
            review_time_seconds=0.0,
            reviewer_confidence=0.0
        )
    
    def _create_timeout_review_result(self, elapsed_time: float) -> A2IReviewResult:
        """Create timeout review result"""
        return A2IReviewResult(
            review_completed=False,
            quality_score=75.0,  # Assume reasonable quality on timeout
            human_feedback={'timeout': f'Review timed out after {elapsed_time}s'},
            improvements=['Human review timed out - proceeding with AI-generated content'],
            approval_status='timeout_approved',
            review_time_seconds=elapsed_time,
            reviewer_confidence=0.6
        )
