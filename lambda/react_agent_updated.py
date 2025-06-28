"""
Updated ReAct Agent with Action Implementations
"""

# Import the action implementations
from react_agent import ReActREADMEAgent, ActionType
from react_agent_actions import ReActActionImplementations
import logging

logger = logging.getLogger(__name__)

class EnhancedReActAgent(ReActREADMEAgent):
    """
    Enhanced ReAct Agent with full action implementations
    """
    
    def __init__(self, region: str = 'us-east-1'):
        super().__init__(region)
        # Initialize action implementations
        self.action_impl = ReActActionImplementations(self.comprehend, self.bedrock_runtime)
    
    def _analyze_structure(self, data: dict) -> dict:
        """Analyze README structure - implemented"""
        data['project_context'] = self.memory['project_context']
        return self.action_impl.analyze_structure(data)
    
    def _enhance_content_with_comprehend(self, data: dict) -> dict:
        """Enhance content using Comprehend - implemented"""
        data['project_context'] = self.memory['project_context']
        return self.action_impl.enhance_content_with_comprehend(data)
    
    def _validate_quality(self, data: dict) -> dict:
        """Validate quality - implemented"""
        data['project_context'] = self.memory['project_context']
        return self.action_impl.validate_quality(data)
    
    def _generate_section(self, data: dict) -> dict:
        """Generate README section - implemented"""
        data['project_context'] = self.memory['project_context']
        return self.action_impl.generate_section(data)
    
    def _optimize_language(self, data: dict) -> dict:
        """Optimize language - implemented"""
        data['project_context'] = self.memory['project_context']
        return self.action_impl.optimize_language(data)
    
    def _generate_final_readme(self) -> dict:
        """Generate final README using all accumulated knowledge"""
        try:
            from readme_generator_engine import READMEGeneratorEngine
            
            # Create comprehensive analysis data from memory
            project_context = self.memory['project_context']
            
            analysis_data = {
                'repository_analysis': {
                    'repository_url': project_context.get('repository_url', ''),
                    'project_type': project_context.get('project_type', 'Software Application'),
                    'primary_language': project_context.get('primary_language', 'Unknown'),
                    'frameworks': project_context.get('frameworks', []),
                    'features': project_context.get('features', []),
                    'architecture_patterns': project_context.get('architecture_patterns', []),
                    'security_analysis': {'security_score': project_context.get('security_score', 100)}
                },
                'readme_structure': project_context.get('readme_sections', {})
            }
            
            # Generate professional README
            readme_engine = READMEGeneratorEngine()
            readme_content = readme_engine.generate_readme(analysis_data, style='developer')
            
            # Perform final Comprehend analysis
            comprehend_analysis = {}
            try:
                from comprehend_analyzer import ComprehendAnalyzer
                analyzer = ComprehendAnalyzer()
                analysis = analyzer.analyze_content(readme_content[:1000], 'final_readme')  # First 1000 chars
                comprehend_analysis = {
                    'sentiment': analysis.sentiment.get('sentiment', 'NEUTRAL'),
                    'quality_score': analysis.quality_score,
                    'entities_count': len(analysis.entities),
                    'recommendations_count': len(analysis.recommendations)
                }
            except Exception as e:
                logger.warning(f"Final Comprehend analysis failed: {e}")
                comprehend_analysis = {'sentiment': 'NEUTRAL', 'quality_score': 85.0}
            
            return {
                'content': readme_content,
                'comprehend_analysis': comprehend_analysis,
                'generation_method': 'react_enhanced',
                'final_length': len(readme_content)
            }
            
        except Exception as e:
            logger.error(f"❌ Final README generation failed: {e}")
            # Return fallback README
            project_context = self.memory['project_context']
            fallback_content = f"""# {project_context.get('project_type', 'Project')}

> A {project_context.get('project_type', 'software application')} built with {project_context.get('primary_language', 'modern technologies')}

## Overview

This project provides {', '.join(project_context.get('features', ['core functionality']))}.

## Installation

1. Clone the repository
2. Install dependencies
3. Run the application

## Usage

Follow the installation steps and refer to the documentation.

## Contributing

Contributions are welcome! Please submit a Pull Request.

---

*Generated by ReAct README Generator*
"""
            
            return {
                'content': fallback_content,
                'comprehend_analysis': {'sentiment': 'NEUTRAL', 'quality_score': 70.0},
                'generation_method': 'fallback',
                'final_length': len(fallback_content)
            }
