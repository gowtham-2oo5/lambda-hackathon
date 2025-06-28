"""
ReAct Agent for Professional README Generation
Combines Reasoning, Acting, and Observing with AWS AI services
"""

import json
import boto3
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ActionType(Enum):
    ANALYZE_STRUCTURE = "analyze_structure"
    ENHANCE_CONTENT = "enhance_content"
    VALIDATE_QUALITY = "validate_quality"
    GENERATE_SECTION = "generate_section"
    OPTIMIZE_LANGUAGE = "optimize_language"

@dataclass
class ReasoningResult:
    """Result of reasoning phase"""
    analysis: str
    action_plan: List[Dict[str, Any]]
    confidence: float
    context: Dict[str, Any]

@dataclass
class ActionResult:
    """Result of action execution"""
    action_type: ActionType
    success: bool
    data: Dict[str, Any]
    quality_score: float
    execution_time: float

@dataclass
class ObservationResult:
    """Result of observation phase"""
    quality_score: float
    issues_found: List[str]
    improvements: List[str]
    should_continue: bool
    next_focus: Optional[str]

class ReActREADMEAgent:
    """
    ReAct Agent for Professional README Generation
    Implements Reasoning, Acting, and Observing cycles
    """
    
    def __init__(self, region: str = 'us-east-1'):
        self.region = region
        self.comprehend = boto3.client('comprehend', region_name=region)
        self.bedrock_runtime = boto3.client('bedrock-runtime', region_name=region)
        self.s3_client = boto3.client('s3', region_name=region)
        
        # Agent configuration
        self.max_cycles = 4
        self.quality_threshold = 85.0
        self.target_quality = 95.0
        
        # Memory system
        self.memory = {
            'project_context': {},
            'reasoning_history': [],
            'action_results': [],
            'quality_progression': [],
            'learned_patterns': {}
        }
        
        # Bedrock model configuration
        self.bedrock_model = 'us.anthropic.claude-sonnet-4-20250514-v1:0'
        
    def generate_professional_readme(self, json_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main entry point for README generation using ReAct framework
        """
        logger.info("🤖 Starting ReAct README generation process")
        start_time = datetime.now()
        
        try:
            # Initialize memory with project context
            self._initialize_memory(json_data)
            
            # ReAct cycles
            for cycle in range(1, self.max_cycles + 1):
                logger.info(f"🔄 ReAct Cycle {cycle}/{self.max_cycles}")
                
                # REASON: Analyze current state and plan actions
                reasoning_result = self._reason(cycle)
                
                # ACT: Execute planned actions
                action_results = self._act(reasoning_result.action_plan)
                
                # OBSERVE: Evaluate results and determine next steps
                observation_result = self._observe(action_results)
                
                # Update memory
                self._update_memory(reasoning_result, action_results, observation_result)
                
                # Check if we've reached target quality
                if observation_result.quality_score >= self.target_quality:
                    logger.info(f"✅ Target quality achieved: {observation_result.quality_score}%")
                    break
                    
                # Check if we should continue
                if not observation_result.should_continue:
                    logger.info("🛑 Agent decided to stop iterations")
                    break
            
            # Generate final README
            final_readme = self._generate_final_readme()
            
            # Calculate processing time
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return {
                'success': True,
                'readme_content': final_readme['content'],
                'metadata': {
                    'cycles_completed': cycle,
                    'final_quality_score': observation_result.quality_score,
                    'processing_time_seconds': processing_time,
                    'react_enabled': True,
                    'comprehend_analysis': final_readme['comprehend_analysis'],
                    'quality_progression': self.memory['quality_progression']
                }
            }
            
        except Exception as e:
            logger.error(f"❌ ReAct generation failed: {e}")
            return self._handle_failure(str(e))
    
    def _initialize_memory(self, json_data: Dict[str, Any]):
        """Initialize agent memory with project context"""
        repo_analysis = json_data.get('repository_analysis', {})
        readme_structure = json_data.get('readme_structure', {})
        
        self.memory['project_context'] = {
            'repository_url': repo_analysis.get('repository_url', ''),
            'project_type': repo_analysis.get('project_type', 'Software Application'),
            'primary_language': repo_analysis.get('primary_language', 'Unknown'),
            'frameworks': repo_analysis.get('frameworks', []),
            'features': repo_analysis.get('features', []),
            'architecture_patterns': repo_analysis.get('architecture_patterns', []),
            'security_score': repo_analysis.get('security_analysis', {}).get('security_score', 0),
            'readme_sections': readme_structure,
            'target_audience': 'developers',
            'complexity_level': self._assess_complexity(repo_analysis)
        }
        
        logger.info(f"📝 Initialized memory for {self.memory['project_context']['project_type']} project")
    
    def _reason(self, cycle: int) -> ReasoningResult:
        """
        REASONING phase: Analyze current state and plan actions
        """
        logger.info(f"🧠 Reasoning - Cycle {cycle}")
        
        # Get current context
        context = self.memory['project_context']
        previous_results = self.memory['action_results']
        quality_history = self.memory['quality_progression']
        
        # Create reasoning prompt
        reasoning_prompt = self._create_reasoning_prompt(cycle, context, previous_results, quality_history)
        
        # Call Bedrock for reasoning
        reasoning_response = self._call_bedrock_for_reasoning(reasoning_prompt)
        
        # Parse reasoning result
        analysis = reasoning_response.get('analysis', '')
        action_plan = reasoning_response.get('action_plan', [])
        confidence = reasoning_response.get('confidence', 0.7)
        
        result = ReasoningResult(
            analysis=analysis,
            action_plan=action_plan,
            confidence=confidence,
            context=context
        )
        
        logger.info(f"🎯 Reasoning complete - {len(action_plan)} actions planned")
        return result
    
    def _act(self, action_plan: List[Dict[str, Any]]) -> List[ActionResult]:
        """
        ACTING phase: Execute planned actions
        """
        logger.info(f"⚡ Acting - Executing {len(action_plan)} actions")
        
        results = []
        
        for action in action_plan:
            action_type = ActionType(action.get('type'))
            action_data = action.get('data', {})
            
            start_time = datetime.now()
            
            try:
                if action_type == ActionType.ANALYZE_STRUCTURE:
                    result_data = self._analyze_structure(action_data)
                elif action_type == ActionType.ENHANCE_CONTENT:
                    result_data = self._enhance_content_with_comprehend(action_data)
                elif action_type == ActionType.VALIDATE_QUALITY:
                    result_data = self._validate_quality(action_data)
                elif action_type == ActionType.GENERATE_SECTION:
                    result_data = self._generate_section(action_data)
                elif action_type == ActionType.OPTIMIZE_LANGUAGE:
                    result_data = self._optimize_language(action_data)
                else:
                    result_data = {'error': f'Unknown action type: {action_type}'}
                
                execution_time = (datetime.now() - start_time).total_seconds()
                
                action_result = ActionResult(
                    action_type=action_type,
                    success=True,
                    data=result_data,
                    quality_score=result_data.get('quality_score', 0.0),
                    execution_time=execution_time
                )
                
                results.append(action_result)
                logger.info(f"✅ Action {action_type.value} completed in {execution_time:.2f}s")
                
            except Exception as e:
                logger.error(f"❌ Action {action_type.value} failed: {e}")
                action_result = ActionResult(
                    action_type=action_type,
                    success=False,
                    data={'error': str(e)},
                    quality_score=0.0,
                    execution_time=(datetime.now() - start_time).total_seconds()
                )
                results.append(action_result)
        
        return results
    
    def _observe(self, action_results: List[ActionResult]) -> ObservationResult:
        """
        OBSERVING phase: Evaluate results and determine next steps
        """
        logger.info("👁️ Observing - Evaluating action results")
        
        # Calculate overall quality score
        successful_actions = [r for r in action_results if r.success]
        if successful_actions:
            quality_score = sum(r.quality_score for r in successful_actions) / len(successful_actions)
        else:
            quality_score = 0.0
        
        # Identify issues and improvements
        issues_found = []
        improvements = []
        
        for result in action_results:
            if not result.success:
                issues_found.append(f"{result.action_type.value}: {result.data.get('error', 'Unknown error')}")
            else:
                if 'improvements' in result.data:
                    improvements.extend(result.data['improvements'])
        
        # Determine if we should continue
        should_continue = (
            quality_score < self.target_quality and 
            len(issues_found) < 3 and  # Don't continue if too many failures
            quality_score > 0  # Don't continue if no progress
        )
        
        # Determine next focus area
        next_focus = None
        if should_continue:
            if quality_score < 70:
                next_focus = "content_structure"
            elif quality_score < 85:
                next_focus = "language_optimization"
            else:
                next_focus = "final_polish"
        
        result = ObservationResult(
            quality_score=quality_score,
            issues_found=issues_found,
            improvements=improvements,
            should_continue=should_continue,
            next_focus=next_focus
        )
        
        logger.info(f"📊 Observation complete - Quality: {quality_score:.1f}%, Continue: {should_continue}")
        return result
    
    def _update_memory(self, reasoning: ReasoningResult, actions: List[ActionResult], observation: ObservationResult):
        """Update agent memory with cycle results"""
        self.memory['reasoning_history'].append({
            'analysis': reasoning.analysis,
            'confidence': reasoning.confidence,
            'timestamp': datetime.now().isoformat()
        })
        
        self.memory['action_results'].extend(actions)
        self.memory['quality_progression'].append(observation.quality_score)
        
        # Learn patterns for future cycles
        if observation.quality_score > 80:
            successful_actions = [a.action_type.value for a in actions if a.success]
            self.memory['learned_patterns']['successful_actions'] = successful_actions
    
    def _assess_complexity(self, repo_analysis: Dict[str, Any]) -> str:
        """Assess project complexity level"""
        frameworks = len(repo_analysis.get('frameworks', []))
        features = len(repo_analysis.get('features', []))
        files_analyzed = len(repo_analysis.get('key_files', []))
        
        complexity_score = frameworks + features + (files_analyzed / 5)
        
        if complexity_score < 5:
            return 'simple'
        elif complexity_score < 15:
            return 'moderate'
        else:
            return 'complex'
    
    def _create_reasoning_prompt(self, cycle: int, context: Dict, previous_results: List, quality_history: List) -> str:
        """Create enhanced reasoning prompt for engaging content"""
        from enhanced_react_prompts import create_enhanced_reasoning_prompt
        return create_enhanced_reasoning_prompt(cycle, context, previous_results, quality_history)
    
    def _call_bedrock_for_reasoning(self, prompt: str) -> Dict[str, Any]:
        """Call Bedrock for reasoning analysis"""
        try:
            response = self.bedrock_runtime.invoke_model(
                modelId=self.bedrock_model,
                contentType='application/json',
                accept='application/json',
                body=json.dumps({
                    'anthropic_version': 'bedrock-2023-05-31',
                    'max_tokens': 2000,
                    'temperature': 0.3,
                    'messages': [{'role': 'user', 'content': prompt}]
                })
            )
            
            result = json.loads(response['body'].read().decode('utf-8'))
            response_text = result['content'][0]['text']
            
            # Parse JSON response
            try:
                return json.loads(response_text)
            except json.JSONDecodeError:
                # Extract JSON from response if wrapped in markdown
                import re
                json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())
                else:
                    return {
                        'analysis': 'Failed to parse reasoning response',
                        'action_plan': [{'type': 'validate_quality', 'priority': 1, 'data': {}}],
                        'confidence': 0.5
                    }
                    
        except Exception as e:
            logger.error(f"❌ Bedrock reasoning failed: {e}")
            return {
                'analysis': f'Reasoning failed: {str(e)}',
                'action_plan': [{'type': 'validate_quality', 'priority': 1, 'data': {}}],
                'confidence': 0.3
            }
    
    def _handle_failure(self, error_message: str) -> Dict[str, Any]:
        """Handle generation failure"""
        return {
            'success': False,
            'error': error_message,
            'fallback_attempted': False,
            'timestamp': datetime.now().isoformat()
        }
    
    # Placeholder methods for action implementations (to be implemented in next phases)
    def _analyze_structure(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze README structure - placeholder"""
        return {'quality_score': 75.0, 'analysis': 'Structure analysis placeholder'}
    
    def _enhance_content_with_comprehend(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance content using Comprehend - placeholder"""
        return {'quality_score': 80.0, 'enhancements': 'Comprehend analysis placeholder'}
    
    def _validate_quality(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate quality - placeholder"""
        return {'quality_score': 85.0, 'validation': 'Quality validation placeholder'}
    
    def _generate_section(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate README section - placeholder"""
        return {'quality_score': 82.0, 'section': 'Generated section placeholder'}
    
    def _optimize_language(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize language - placeholder"""
        return {'quality_score': 88.0, 'optimizations': 'Language optimization placeholder'}
    
    def _generate_final_readme(self) -> Dict[str, Any]:
        """Generate final README - placeholder"""
        return {
            'content': '# Placeholder README\n\nGenerated by ReAct Agent',
            'comprehend_analysis': {'sentiment': 'POSITIVE', 'entities': []}
        }
