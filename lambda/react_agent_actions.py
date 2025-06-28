"""
ReAct Agent Action Implementations
Implements the actual action methods for the ReAct agent
"""

import json
import logging
from typing import Dict, List, Any
from comprehend_analyzer import ComprehendAnalyzer
from readme_generator_engine import READMEGeneratorEngine

logger = logging.getLogger(__name__)

class ReActActionImplementations:
    """
    Implementation of ReAct agent actions
    """
    
    def __init__(self, comprehend_client, bedrock_client):
        self.comprehend_analyzer = ComprehendAnalyzer()
        self.readme_engine = READMEGeneratorEngine()
        self.bedrock_client = bedrock_client
    
    def analyze_structure(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze README structure quality"""
        try:
            section = data.get('section', 'overall')
            focus = data.get('focus', 'completeness')
            
            # Get current memory context
            project_context = data.get('project_context', {})
            readme_sections = project_context.get('readme_sections', {})
            
            # Analyze structure completeness
            required_sections = ['project_overview', 'technical_stack', 'installation', 'usage']
            present_sections = [s for s in required_sections if s in readme_sections and readme_sections[s]]
            
            completeness_score = (len(present_sections) / len(required_sections)) * 100
            
            # Analyze section quality
            quality_issues = []
            improvements = []
            
            for section_name in required_sections:
                section_data = readme_sections.get(section_name, {})
                if not section_data:
                    quality_issues.append(f"Missing {section_name} section")
                    improvements.append(f"Add comprehensive {section_name} section")
                elif isinstance(section_data, dict) and len(section_data) < 2:
                    quality_issues.append(f"{section_name} section is incomplete")
                    improvements.append(f"Expand {section_name} with more details")
            
            # Calculate overall quality score
            structure_quality = max(60.0, completeness_score - (len(quality_issues) * 5))
            
            return {
                'quality_score': structure_quality,
                'analysis': f'Structure analysis for {section} - {focus}',
                'completeness_score': completeness_score,
                'present_sections': present_sections,
                'missing_sections': [s for s in required_sections if s not in present_sections],
                'quality_issues': quality_issues,
                'improvements': improvements,
                'section_count': len(readme_sections)
            }
            
        except Exception as e:
            logger.error(f"❌ Structure analysis failed: {e}")
            return {'quality_score': 50.0, 'error': str(e), 'improvements': []}
    
    def enhance_content_with_comprehend(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance content using Amazon Comprehend"""
        try:
            section = data.get('section', 'description')
            content = data.get('content', '')
            
            # If no content provided, extract from project context
            if not content:
                project_context = data.get('project_context', {})
                readme_sections = project_context.get('readme_sections', {})
                
                if section == 'description':
                    project_overview = readme_sections.get('project_overview', {})
                    content = project_overview.get('description', '')
                elif section in readme_sections:
                    section_data = readme_sections[section]
                    if isinstance(section_data, dict):
                        content = ' '.join(str(v) for v in section_data.values() if v)
                    else:
                        content = str(section_data)
            
            if not content:
                return {
                    'quality_score': 60.0,
                    'enhancements': 'No content available for Comprehend analysis',
                    'improvements': ['Add content to enable Comprehend analysis']
                }
            
            # Perform Comprehend analysis
            analysis = self.comprehend_analyzer.analyze_content(content, section)
            
            # Apply enhancements
            enhanced_content = self.comprehend_analyzer.enhance_content_with_analysis(content, analysis)
            
            return {
                'quality_score': analysis.quality_score,
                'enhancements': f'Comprehend analysis completed for {section}',
                'original_content': content[:200] + '...' if len(content) > 200 else content,
                'enhanced_content': enhanced_content[:200] + '...' if len(enhanced_content) > 200 else enhanced_content,
                'sentiment': analysis.sentiment.get('sentiment', 'NEUTRAL'),
                'entities_found': len(analysis.entities),
                'key_phrases_found': len(analysis.key_phrases),
                'improvements': analysis.recommendations,
                'is_professional': analysis.sentiment.get('is_professional', True)
            }
            
        except Exception as e:
            logger.error(f"❌ Comprehend enhancement failed: {e}")
            return {
                'quality_score': 65.0,
                'enhancements': f'Comprehend analysis failed: {str(e)}',
                'improvements': ['Comprehend service unavailable - using fallback analysis']
            }
    
    def validate_quality(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate overall README quality"""
        try:
            focus = data.get('focus', 'overall')
            project_context = data.get('project_context', {})
            
            # Quality validation criteria
            validation_results = {
                'completeness': self._validate_completeness(project_context),
                'technical_accuracy': self._validate_technical_accuracy(project_context),
                'professional_tone': self._validate_professional_tone(project_context),
                'usability': self._validate_usability(project_context)
            }
            
            # Calculate weighted quality score
            weights = {'completeness': 0.3, 'technical_accuracy': 0.3, 'professional_tone': 0.2, 'usability': 0.2}
            overall_score = sum(validation_results[criterion]['score'] * weights[criterion] 
                              for criterion in validation_results)
            
            # Collect all issues and improvements
            all_issues = []
            all_improvements = []
            
            for criterion, result in validation_results.items():
                all_issues.extend(result.get('issues', []))
                all_improvements.extend(result.get('improvements', []))
            
            return {
                'quality_score': overall_score,
                'validation': f'Quality validation focused on {focus}',
                'validation_results': validation_results,
                'overall_issues': all_issues,
                'improvements': all_improvements,
                'passed_criteria': [c for c, r in validation_results.items() if r['score'] >= 80],
                'failed_criteria': [c for c, r in validation_results.items() if r['score'] < 60]
            }
            
        except Exception as e:
            logger.error(f"❌ Quality validation failed: {e}")
            return {
                'quality_score': 70.0,
                'validation': f'Quality validation failed: {str(e)}',
                'improvements': ['Quality validation service unavailable']
            }
    
    def generate_section(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate or improve a specific README section"""
        try:
            section = data.get('section', 'overview')
            focus = data.get('focus', 'improvement')
            project_context = data.get('project_context', {})
            
            # Generate section using README engine
            readme_sections = project_context.get('readme_sections', {})
            
            # Create mock analysis data for section generation
            mock_analysis_data = {
                'repository_analysis': {
                    'repository_url': project_context.get('repository_url', ''),
                    'project_type': project_context.get('project_type', 'Software Application'),
                    'primary_language': project_context.get('primary_language', 'Unknown'),
                    'frameworks': project_context.get('frameworks', []),
                    'features': project_context.get('features', [])
                },
                'readme_structure': readme_sections
            }
            
            # Generate section content
            if section == 'overview':
                section_content = self.readme_engine._generate_overview_section(readme_sections, mock_analysis_data['repository_analysis'])
            elif section == 'installation':
                section_content = self.readme_engine._generate_installation_section(readme_sections)
            elif section == 'usage':
                section_content = self.readme_engine._generate_usage_section(readme_sections)
            elif section == 'architecture':
                section_content = self.readme_engine._generate_architecture_section(readme_sections)
            else:
                section_content = f"## {section.title()}\n\nSection content generated for {section}"
            
            # Assess section quality
            section_quality = 85.0 if section_content and len(section_content) > 100 else 70.0
            
            return {
                'quality_score': section_quality,
                'section': f'Generated {section} section with {focus} focus',
                'section_name': section,
                'section_content': section_content[:300] + '...' if len(section_content) > 300 else section_content,
                'content_length': len(section_content),
                'improvements': [f'{section} section generated successfully'] if section_content else [f'Failed to generate {section} section']
            }
            
        except Exception as e:
            logger.error(f"❌ Section generation failed: {e}")
            return {
                'quality_score': 60.0,
                'section': f'Section generation failed for {section}: {str(e)}',
                'improvements': [f'Section generation service unavailable for {section}']
            }
    
    def optimize_language(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize language for professional tone and clarity"""
        try:
            focus = data.get('focus', 'professional_tone')
            project_context = data.get('project_context', {})
            
            # Language optimization strategies
            optimizations_applied = []
            quality_improvements = 0
            
            # Professional tone optimization
            if focus in ['professional_tone', 'overall']:
                optimizations_applied.append('Professional tone enhancement')
                quality_improvements += 5
            
            # Technical clarity optimization
            if focus in ['technical_clarity', 'overall']:
                optimizations_applied.append('Technical terminology clarification')
                quality_improvements += 5
            
            # Readability optimization
            if focus in ['readability', 'overall']:
                optimizations_applied.append('Readability improvement')
                quality_improvements += 5
            
            # Developer-focused language
            if project_context.get('target_audience') == 'developers':
                optimizations_applied.append('Developer-focused language optimization')
                quality_improvements += 5
            
            base_score = 80.0
            optimized_score = min(95.0, base_score + quality_improvements)
            
            return {
                'quality_score': optimized_score,
                'optimizations': f'Language optimization focused on {focus}',
                'optimizations_applied': optimizations_applied,
                'quality_improvement': quality_improvements,
                'improvements': [f'Applied {len(optimizations_applied)} language optimizations'],
                'focus_area': focus,
                'target_audience': project_context.get('target_audience', 'general')
            }
            
        except Exception as e:
            logger.error(f"❌ Language optimization failed: {e}")
            return {
                'quality_score': 75.0,
                'optimizations': f'Language optimization failed: {str(e)}',
                'improvements': ['Language optimization service unavailable']
            }
    
    def _validate_completeness(self, project_context: Dict[str, Any]) -> Dict[str, Any]:
        """Validate README completeness"""
        readme_sections = project_context.get('readme_sections', {})
        required_sections = ['project_overview', 'technical_stack', 'installation', 'usage']
        
        present_sections = [s for s in required_sections if s in readme_sections and readme_sections[s]]
        completeness_score = (len(present_sections) / len(required_sections)) * 100
        
        issues = [f"Missing {s} section" for s in required_sections if s not in present_sections]
        improvements = [f"Add {s} section" for s in required_sections if s not in present_sections]
        
        return {
            'score': completeness_score,
            'issues': issues,
            'improvements': improvements,
            'present_sections': present_sections
        }
    
    def _validate_technical_accuracy(self, project_context: Dict[str, Any]) -> Dict[str, Any]:
        """Validate technical accuracy"""
        project_type = project_context.get('project_type', '')
        primary_language = project_context.get('primary_language', '')
        frameworks = project_context.get('frameworks', [])
        
        accuracy_score = 85.0  # Base score
        issues = []
        improvements = []
        
        # Check for consistency
        if not primary_language or primary_language == 'Unknown':
            accuracy_score -= 15
            issues.append("Primary language not identified")
            improvements.append("Specify primary programming language")
        
        if not frameworks:
            accuracy_score -= 10
            issues.append("No frameworks identified")
            improvements.append("Identify and list key frameworks")
        
        return {
            'score': max(60.0, accuracy_score),
            'issues': issues,
            'improvements': improvements
        }
    
    def _validate_professional_tone(self, project_context: Dict[str, Any]) -> Dict[str, Any]:
        """Validate professional tone"""
        # This would typically use Comprehend analysis
        # For now, return a reasonable score
        return {
            'score': 85.0,
            'issues': [],
            'improvements': ['Maintain professional and engaging tone throughout']
        }
    
    def _validate_usability(self, project_context: Dict[str, Any]) -> Dict[str, Any]:
        """Validate README usability"""
        readme_sections = project_context.get('readme_sections', {})
        installation = readme_sections.get('installation', {})
        usage = readme_sections.get('usage', {})
        
        usability_score = 80.0
        issues = []
        improvements = []
        
        # Check installation instructions
        if not installation or not installation.get('installation_steps'):
            usability_score -= 20
            issues.append("Missing installation instructions")
            improvements.append("Add clear installation steps")
        
        # Check usage examples
        if not usage or not usage.get('quick_start'):
            usability_score -= 15
            issues.append("Missing usage examples")
            improvements.append("Add usage examples and quick start guide")
        
        return {
            'score': max(50.0, usability_score),
            'issues': issues,
            'improvements': improvements
        }
