"""
Optimized Bedrock Service for README Generation
Uses inference profiles for maximum accuracy and reliability
"""

import json
import boto3
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ReadmeGenerationRequest:
    """Request structure for README generation"""
    repository_url: str
    project_type: str
    primary_language: str
    frameworks: List[str]
    key_files: List[str]
    file_contents: Dict[str, str]
    features: List[str]
    architecture_patterns: List[str]
    security_analysis: Dict[str, Any]

@dataclass
class ReadmeStructure:
    """Clean JSON structure for README generation"""
    project_overview: Dict[str, str]
    technical_stack: Dict[str, Any]
    features: List[str]
    installation: Dict[str, Any]
    usage: Dict[str, Any]
    architecture: Dict[str, Any]
    api_documentation: Dict[str, Any]
    development: Dict[str, Any]
    deployment: Dict[str, Any]
    contributing: Dict[str, Any]
    license_info: Dict[str, str]

class OptimizedBedrockService:
    """
    Optimized Bedrock service using inference profiles for README generation
    """
    
    def __init__(self, region: str = 'us-east-1'):
        self.region = region
        self.bedrock_runtime = boto3.client('bedrock-runtime', region_name=region)
        
        # Model preferences (in order of preference)
        self.model_preferences = [
            {
                'id': 'us.anthropic.claude-sonnet-4-20250514-v1:0',
                'name': 'Claude Sonnet 4',
                'max_tokens': 4000,
                'temperature': 0.1,
                'use_case': 'High accuracy analysis'
            },
            {
                'id': 'us.anthropic.claude-3-5-haiku-20241022-v1:0', 
                'name': 'Claude 3.5 Haiku',
                'max_tokens': 4000,
                'temperature': 0.1,
                'use_case': 'Fast and reliable'
            },
            {
                'id': 'us.anthropic.claude-3-5-sonnet-20240620-v1:0',
                'name': 'Claude 3.5 Sonnet',
                'max_tokens': 4000,
                'temperature': 0.1,
                'use_case': 'Balanced performance'
            }
        ]
        
        self.active_model = None
        self._initialize_best_model()
    
    def _initialize_best_model(self):
        """Initialize the best available model"""
        logger.info("🔍 Initializing best available Bedrock model...")
        
        for model in self.model_preferences:
            try:
                # Test the model with a simple request
                test_response = self._test_model(model['id'])
                if test_response:
                    self.active_model = model
                    logger.info(f"✅ Using {model['name']} ({model['id']})")
                    return
            except Exception as e:
                logger.warning(f"⚠️ {model['name']} not available: {e}")
                continue
        
        raise Exception("❌ No working Bedrock models found!")
    
    def _test_model(self, model_id: str) -> bool:
        """Test if a model is working"""
        try:
            response = self.bedrock_runtime.invoke_model(
                modelId=model_id,
                contentType='application/json',
                accept='application/json',
                body=json.dumps({
                    'anthropic_version': 'bedrock-2023-05-31',
                    'max_tokens': 50,
                    'temperature': 0.1,
                    'messages': [
                        {
                            'role': 'user',
                            'content': 'Test message. Respond with "OK".'
                        }
                    ]
                })
            )
            
            result = json.loads(response['body'].read().decode('utf-8'))
            return 'content' in result and len(result['content']) > 0
            
        except Exception:
            return False
    
    def generate_readme_structure(self, request: ReadmeGenerationRequest) -> ReadmeStructure:
        """
        Generate clean JSON structure for README using Bedrock
        """
        logger.info(f"🤖 Generating README structure using {self.active_model['name']}")
        
        try:
            # Create comprehensive prompt for README generation
            prompt = self._create_readme_generation_prompt(request)
            
            # Call Bedrock with optimized parameters
            response = self._call_bedrock(prompt)
            
            # Parse and validate the response
            readme_structure = self._parse_readme_response(response)
            
            logger.info("✅ README structure generated successfully")
            return readme_structure
            
        except Exception as e:
            logger.error(f"❌ README generation failed: {e}")
            # Return fallback structure
            return self._create_fallback_structure(request)
    
    def _create_readme_generation_prompt(self, request: ReadmeGenerationRequest) -> str:
        """Create optimized prompt for README generation"""
        
        # Prepare file content summary
        file_summary = []
        for file_path, content in request.file_contents.items():
            file_summary.append(f"FILE: {file_path}")
            file_summary.append(f"CONTENT: {content[:1000]}...")  # Limit content
            file_summary.append("---")
        
        prompt = f"""
You are a senior technical writer and software architect. Analyze this repository and generate a comprehensive JSON structure for a professional README.

REPOSITORY ANALYSIS:
- URL: {request.repository_url}
- Project Type: {request.project_type}
- Primary Language: {request.primary_language}
- Frameworks: {', '.join(request.frameworks)}
- Key Features: {', '.join(request.features)}
- Architecture Patterns: {', '.join(request.architecture_patterns)}

KEY FILES ANALYZED:
{chr(10).join(file_summary[:10])}  # Limit to first 10 files

SECURITY ANALYSIS:
- Total Issues: {request.security_analysis.get('total_issues', 0)}
- Security Score: {request.security_analysis.get('security_score', 100)}

Generate a comprehensive JSON structure that covers all aspects of a professional README. Be specific and accurate based on the actual code analysis.

REQUIRED JSON STRUCTURE:
{{
  "project_overview": {{
    "name": "Extracted from repository or inferred",
    "description": "Comprehensive description based on code analysis",
    "type": "{request.project_type}",
    "primary_purpose": "Main purpose based on code analysis",
    "target_audience": "Who would use this project"
  }},
  "technical_stack": {{
    "primary_language": "{request.primary_language}",
    "frameworks": {json.dumps(request.frameworks)},
    "key_dependencies": ["List from package.json, requirements.txt, etc."],
    "build_tools": ["Identified build tools"],
    "database": "Database type if found",
    "deployment_platforms": ["Platforms supported"]
  }},
  "features": {{
    "core_features": ["Main features from code analysis"],
    "authentication": "Authentication method if found",
    "api_endpoints": ["API endpoints if found"],
    "ui_components": ["UI components identified"],
    "integrations": ["Third-party integrations found"]
  }},
  "installation": {{
    "system_requirements": ["OS, runtime versions"],
    "prerequisites": ["Required software"],
    "installation_steps": ["Step by step installation"],
    "configuration": ["Configuration steps"],
    "verification": ["How to verify installation"]
  }},
  "usage": {{
    "quick_start": ["Basic usage steps"],
    "common_commands": ["Frequently used commands"],
    "examples": ["Code examples if applicable"],
    "configuration_options": ["Available configuration"],
    "troubleshooting": ["Common issues and solutions"]
  }},
  "architecture": {{
    "overview": "Architecture description",
    "patterns": {json.dumps(request.architecture_patterns)},
    "directory_structure": "Key directories explained",
    "data_flow": "How data flows through the system",
    "security_measures": ["Security features implemented"]
  }},
  "api_documentation": {{
    "base_url": "API base URL if found",
    "authentication": "API auth method",
    "endpoints": ["Key endpoints documented"],
    "request_examples": ["Sample requests"],
    "response_formats": ["Response structure"]
  }},
  "development": {{
    "setup": ["Development environment setup"],
    "coding_standards": ["Code style guidelines"],
    "testing": ["How to run tests"],
    "debugging": ["Debugging instructions"],
    "contributing_workflow": ["How to contribute"]
  }},
  "deployment": {{
    "environments": ["Supported environments"],
    "deployment_methods": ["How to deploy"],
    "environment_variables": ["Required env vars"],
    "monitoring": ["Monitoring setup"],
    "scaling": ["Scaling considerations"]
  }},
  "contributing": {{
    "guidelines": ["Contribution guidelines"],
    "code_of_conduct": "Code of conduct info",
    "issue_reporting": "How to report issues",
    "pull_request_process": ["PR process steps"],
    "development_setup": ["Setup for contributors"]
  }},
  "license_info": {{
    "license_type": "License type if found",
    "license_file": "License file location",
    "copyright": "Copyright information",
    "usage_restrictions": "Any usage restrictions"
  }}
}}

IMPORTANT INSTRUCTIONS:
1. Base ALL information on the actual code analysis provided
2. If information is not available from the code, use "Not specified in code analysis"
3. Be specific and avoid generic descriptions
4. Focus on what the code actually does, not what it might do
5. Include actual file names, function names, and specific details where possible
6. Respond with ONLY the JSON structure, no additional text or markdown formatting

Generate the JSON now:
"""
        
        return prompt
    
    def _call_bedrock(self, prompt: str) -> str:
        """Call Bedrock with the optimized prompt"""
        try:
            response = self.bedrock_runtime.invoke_model(
                modelId=self.active_model['id'],
                contentType='application/json',
                accept='application/json',
                body=json.dumps({
                    'anthropic_version': 'bedrock-2023-05-31',
                    'max_tokens': self.active_model['max_tokens'],
                    'temperature': self.active_model['temperature'],
                    'messages': [
                        {
                            'role': 'user',
                            'content': prompt
                        }
                    ]
                })
            )
            
            result = json.loads(response['body'].read().decode('utf-8'))
            return result['content'][0]['text']
            
        except Exception as e:
            logger.error(f"❌ Bedrock API call failed: {e}")
            raise e
    
    def _parse_readme_response(self, response: str) -> ReadmeStructure:
        """Parse and validate the Bedrock response"""
        try:
            # Clean the response (remove markdown formatting if present)
            cleaned_response = response.strip()
            if cleaned_response.startswith('```json'):
                cleaned_response = cleaned_response[7:]
            if cleaned_response.endswith('```'):
                cleaned_response = cleaned_response[:-3]
            
            # Parse JSON
            readme_data = json.loads(cleaned_response.strip())
            
            # Validate required fields
            required_fields = [
                'project_overview', 'technical_stack', 'features', 
                'installation', 'usage', 'architecture'
            ]
            
            for field in required_fields:
                if field not in readme_data:
                    logger.warning(f"⚠️ Missing required field: {field}")
                    readme_data[field] = {}
            
            # Create ReadmeStructure object
            return ReadmeStructure(
                project_overview=readme_data.get('project_overview', {}),
                technical_stack=readme_data.get('technical_stack', {}),
                features=readme_data.get('features', []),
                installation=readme_data.get('installation', {}),
                usage=readme_data.get('usage', {}),
                architecture=readme_data.get('architecture', {}),
                api_documentation=readme_data.get('api_documentation', {}),
                development=readme_data.get('development', {}),
                deployment=readme_data.get('deployment', {}),
                contributing=readme_data.get('contributing', {}),
                license_info=readme_data.get('license_info', {})
            )
            
        except json.JSONDecodeError as e:
            logger.error(f"❌ JSON parsing failed: {e}")
            logger.error(f"Response preview: {response[:500]}...")
            raise e
        except Exception as e:
            logger.error(f"❌ Response parsing failed: {e}")
            raise e
    
    def _create_fallback_structure(self, request: ReadmeGenerationRequest) -> ReadmeStructure:
        """Create fallback README structure when AI generation fails"""
        logger.info("🔄 Creating fallback README structure")
        
        return ReadmeStructure(
            project_overview={
                "name": "Repository Analysis",
                "description": f"A {request.project_type} built with {request.primary_language}",
                "type": request.project_type,
                "primary_purpose": "Software application",
                "target_audience": "Developers"
            },
            technical_stack={
                "primary_language": request.primary_language,
                "frameworks": request.frameworks,
                "key_dependencies": ["Analysis in progress"],
                "build_tools": ["Standard build tools"],
                "database": "Not specified in code analysis",
                "deployment_platforms": ["Standard platforms"]
            },
            features=request.features if request.features else ["Core functionality"],
            installation={
                "system_requirements": [f"{request.primary_language} runtime"],
                "prerequisites": ["Standard development environment"],
                "installation_steps": ["Clone repository", "Install dependencies", "Run application"],
                "configuration": ["Standard configuration"],
                "verification": ["Run tests"]
            },
            usage={
                "quick_start": ["Follow installation steps"],
                "common_commands": ["Standard commands"],
                "examples": ["See documentation"],
                "configuration_options": ["Standard options"],
                "troubleshooting": ["Check logs"]
            },
            architecture={
                "overview": f"{request.project_type} architecture",
                "patterns": request.architecture_patterns,
                "directory_structure": "Standard structure",
                "data_flow": "Standard data flow",
                "security_measures": ["Standard security"]
            },
            api_documentation={
                "base_url": "Not specified in code analysis",
                "authentication": "Not specified in code analysis",
                "endpoints": ["Analysis in progress"],
                "request_examples": ["See documentation"],
                "response_formats": ["JSON"]
            },
            development={
                "setup": ["Standard development setup"],
                "coding_standards": ["Follow best practices"],
                "testing": ["Run test suite"],
                "debugging": ["Use standard debugging tools"],
                "contributing_workflow": ["Standard workflow"]
            },
            deployment={
                "environments": ["Development", "Production"],
                "deployment_methods": ["Standard deployment"],
                "environment_variables": ["See configuration"],
                "monitoring": ["Standard monitoring"],
                "scaling": ["Standard scaling"]
            },
            contributing={
                "guidelines": ["Follow contribution guidelines"],
                "code_of_conduct": "Standard code of conduct",
                "issue_reporting": "Use issue tracker",
                "pull_request_process": ["Standard PR process"],
                "development_setup": ["See development section"]
            },
            license_info={
                "license_type": "Not specified in code analysis",
                "license_file": "LICENSE",
                "copyright": "Repository owner",
                "usage_restrictions": "See license file"
            }
        )
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the active model"""
        return {
            "active_model": self.active_model,
            "region": self.region,
            "timestamp": datetime.now().isoformat()
        }

# Utility function for easy integration
def generate_readme_json(repository_analysis: Dict[str, Any]) -> Dict[str, Any]:
    """
    Utility function to generate README JSON from repository analysis
    """
    service = OptimizedBedrockService()
    
    # Convert analysis to request format
    request = ReadmeGenerationRequest(
        repository_url=repository_analysis.get('repository_url', ''),
        project_type=repository_analysis.get('project_type', 'Software Application'),
        primary_language=repository_analysis.get('primary_language', 'Unknown'),
        frameworks=repository_analysis.get('frameworks', []),
        key_files=repository_analysis.get('key_files', []),
        file_contents=repository_analysis.get('file_contents', {}),
        features=repository_analysis.get('features', []),
        architecture_patterns=repository_analysis.get('architecture_patterns', []),
        security_analysis=repository_analysis.get('security_analysis', {})
    )
    
    # Generate structure
    readme_structure = service.generate_readme_structure(request)
    
    # Convert to dictionary for JSON serialization
    return {
        "project_overview": readme_structure.project_overview,
        "technical_stack": readme_structure.technical_stack,
        "features": readme_structure.features,
        "installation": readme_structure.installation,
        "usage": readme_structure.usage,
        "architecture": readme_structure.architecture,
        "api_documentation": readme_structure.api_documentation,
        "development": readme_structure.development,
        "deployment": readme_structure.deployment,
        "contributing": readme_structure.contributing,
        "license_info": readme_structure.license_info,
        "generation_metadata": {
            "model_used": service.active_model['name'],
            "model_id": service.active_model['id'],
            "generated_at": datetime.now().isoformat(),
            "version": "1.0.0"
        }
    }
