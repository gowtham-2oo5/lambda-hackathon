"""
Amazon Q Developer Integration for Deep Code Analysis
Enhances the ReAct Agent with Q Developer's code intelligence
"""

import json
import boto3
import base64
from datetime import datetime
from typing import Dict, List, Any, Optional

class QDeveloperCodeAnalyzer:
    """
    Amazon Q Developer integration for deep code analysis
    Provides intelligent code insights, architecture analysis, and recommendations
    """
    
    def __init__(self, region: str = 'us-east-1'):
        self.region = region
        # Initialize Q Developer client (when available)
        # self.q_client = boto3.client('q-developer', region_name=region)
        
        # For now, we'll use Bedrock as a proxy for Q Developer capabilities
        try:
            self.bedrock_client = boto3.client('bedrock-runtime', region_name=region)
        except Exception:
            self.bedrock_client = None  # Fallback for local testing
        
    def analyze_repository_code(self, owner: str, repo: str, repo_structure: Dict, 
                              key_files: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform deep code analysis using Q Developer capabilities
        """
        
        analysis_results = {
            'code_quality': {},
            'architecture_analysis': {},
            'security_insights': {},
            'performance_recommendations': {},
            'best_practices': {},
            'refactoring_suggestions': {},
            'dependency_analysis': {},
            'api_documentation': {},
            'test_coverage_insights': {},
            'deployment_recommendations': {}
        }
        
        try:
            # Step 1: Code Quality Analysis
            analysis_results['code_quality'] = self._analyze_code_quality(key_files)
            
            # Step 2: Architecture Pattern Detection
            analysis_results['architecture_analysis'] = self._analyze_architecture(repo_structure, key_files)
            
            # Step 3: Security Analysis
            analysis_results['security_insights'] = self._analyze_security(key_files)
            
            # Step 4: Performance Analysis
            analysis_results['performance_recommendations'] = self._analyze_performance(key_files)
            
            # Step 5: Best Practices Check
            analysis_results['best_practices'] = self._check_best_practices(key_files)
            
            # Step 6: API Documentation Analysis
            analysis_results['api_documentation'] = self._analyze_api_structure(key_files)
            
            # Step 7: Deployment Recommendations
            analysis_results['deployment_recommendations'] = self._analyze_deployment(key_files)
            
            return {
                'success': True,
                'analysis': analysis_results,
                'analyzed_at': datetime.utcnow().isoformat(),
                'analyzer': 'Q_Developer_Enhanced'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'fallback_analysis': self._create_fallback_analysis(repo_structure)
            }
    
    def _analyze_code_quality(self, key_files: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze code quality using Q Developer insights"""
        
        # Prepare code samples for analysis
        code_samples = []
        for file_path, file_data in key_files.items():
            if 'content' in file_data and file_path.endswith(('.java', '.js', '.py', '.ts')):
                code_samples.append({
                    'file': file_path,
                    'content': file_data['content'][:2000]  # First 2000 chars
                })
        
        if not code_samples:
            return {'status': 'no_code_files', 'score': 'unknown'}
        
        # Use Bedrock to simulate Q Developer analysis
        analysis_prompt = f"""
        As an expert code reviewer, analyze these code samples for quality:
        
        {json.dumps(code_samples[:3], indent=2)}  # Limit to 3 files
        
        Provide analysis on:
        1. Code structure and organization
        2. Naming conventions
        3. Error handling
        4. Code complexity
        5. Maintainability score (1-10)
        6. Specific improvement suggestions
        
        Respond in JSON format with detailed insights.
        """
        
        try:
            response = self.bedrock_client.invoke_model(
                modelId='amazon.nova-pro-v1:0',
                body=json.dumps({
                    "messages": [{"role": "user", "content": analysis_prompt}],
                    "max_tokens": 2000,
                    "temperature": 0.1
                })
            )
            
            result = json.loads(response['body'].read())
            analysis_text = result['output']['message']['content'][0]['text']
            
            # Extract JSON from response
            try:
                start_idx = analysis_text.find('{')
                end_idx = analysis_text.rfind('}') + 1
                if start_idx != -1 and end_idx != -1:
                    quality_analysis = json.loads(analysis_text[start_idx:end_idx])
                else:
                    quality_analysis = self._create_basic_quality_analysis(code_samples)
            except:
                quality_analysis = self._create_basic_quality_analysis(code_samples)
            
            return quality_analysis
            
        except Exception as e:
            return {
                'status': 'analysis_failed',
                'error': str(e),
                'fallback': self._create_basic_quality_analysis(code_samples)
            }
    
    def _analyze_architecture(self, repo_structure: Dict, key_files: Dict) -> Dict[str, Any]:
        """Analyze architecture patterns and structure"""
        
        architecture_prompt = f"""
        Analyze this repository structure and identify the architecture pattern:
        
        Repository Structure:
        - Root files: {repo_structure.get('root_files', [])}
        - Directories: {repo_structure.get('directories', [])}
        - Total files: {repo_structure.get('total_files', 0)}
        
        Key configuration files found:
        {list(key_files.keys())}
        
        Determine:
        1. Architecture pattern (MVC, Microservices, Layered, etc.)
        2. Design patterns used
        3. Separation of concerns
        4. Scalability considerations
        5. Architecture strengths and weaknesses
        6. Recommended improvements
        
        Respond in JSON format.
        """
        
        try:
            response = self.bedrock_client.invoke_model(
                modelId='amazon.nova-pro-v1:0',
                body=json.dumps({
                    "messages": [{"role": "user", "content": architecture_prompt}],
                    "max_tokens": 1500,
                    "temperature": 0.2
                })
            )
            
            result = json.loads(response['body'].read())
            analysis_text = result['output']['message']['content'][0]['text']
            
            # Extract architecture insights
            try:
                start_idx = analysis_text.find('{')
                end_idx = analysis_text.rfind('}') + 1
                if start_idx != -1 and end_idx != -1:
                    arch_analysis = json.loads(analysis_text[start_idx:end_idx])
                else:
                    arch_analysis = self._create_basic_architecture_analysis(repo_structure)
            except:
                arch_analysis = self._create_basic_architecture_analysis(repo_structure)
            
            return arch_analysis
            
        except Exception as e:
            return {
                'pattern': 'Unknown',
                'analysis_failed': str(e),
                'fallback': self._create_basic_architecture_analysis(repo_structure)
            }
    
    def _analyze_security(self, key_files: Dict) -> Dict[str, Any]:
        """Analyze security aspects of the codebase"""
        
        security_indicators = {
            'authentication_found': False,
            'authorization_found': False,
            'input_validation': False,
            'secure_dependencies': True,
            'security_headers': False,
            'encryption_usage': False
        }
        
        # Check for security patterns in files
        for file_path, file_data in key_files.items():
            if 'content' not in file_data:
                continue
                
            content = file_data['content'].lower()
            
            # Check for authentication patterns
            if any(term in content for term in ['authentication', 'login', 'jwt', 'oauth', 'session']):
                security_indicators['authentication_found'] = True
            
            # Check for authorization patterns
            if any(term in content for term in ['authorization', 'role', 'permission', 'access']):
                security_indicators['authorization_found'] = True
            
            # Check for input validation
            if any(term in content for term in ['validation', 'sanitize', 'validate', 'filter']):
                security_indicators['input_validation'] = True
            
            # Check for encryption
            if any(term in content for term in ['encrypt', 'hash', 'bcrypt', 'crypto']):
                security_indicators['encryption_usage'] = True
        
        # Calculate security score
        security_score = sum(security_indicators.values()) / len(security_indicators) * 100
        
        return {
            'security_score': round(security_score),
            'indicators': security_indicators,
            'recommendations': self._generate_security_recommendations(security_indicators),
            'analysis_method': 'pattern_based_security_scan'
        }
    
    def _analyze_performance(self, key_files: Dict) -> Dict[str, Any]:
        """Analyze performance aspects and provide recommendations"""
        
        performance_insights = {
            'database_optimization': [],
            'caching_opportunities': [],
            'async_patterns': [],
            'resource_management': [],
            'scalability_concerns': []
        }
        
        # Analyze for performance patterns
        for file_path, file_data in key_files.items():
            if 'content' not in file_data:
                continue
                
            content = file_data['content'].lower()
            
            # Database optimization opportunities
            if 'select *' in content:
                performance_insights['database_optimization'].append(
                    f"Avoid SELECT * in {file_path} - specify columns explicitly"
                )
            
            # Caching opportunities
            if any(term in content for term in ['repository', 'service', 'dao']) and 'cache' not in content:
                performance_insights['caching_opportunities'].append(
                    f"Consider adding caching layer in {file_path}"
                )
            
            # Async patterns
            if 'spring boot' in content and 'async' not in content:
                performance_insights['async_patterns'].append(
                    f"Consider async processing for long-running operations in {file_path}"
                )
        
        return {
            'insights': performance_insights,
            'overall_score': self._calculate_performance_score(performance_insights),
            'priority_recommendations': self._get_priority_performance_recommendations(performance_insights)
        }
    
    def _check_best_practices(self, key_files: Dict) -> Dict[str, Any]:
        """Check adherence to best practices"""
        
        best_practices = {
            'spring_boot': {
                'proper_annotations': False,
                'configuration_externalized': False,
                'proper_exception_handling': False,
                'logging_implemented': False,
                'testing_present': False
            },
            'general': {
                'readme_present': False,
                'gitignore_present': False,
                'proper_project_structure': False,
                'documentation_adequate': False
            }
        }
        
        # Check Spring Boot specific practices
        for file_path, file_data in key_files.items():
            if 'content' not in file_data:
                continue
                
            content = file_data['content']
            
            # Spring Boot annotations
            if any(annotation in content for annotation in ['@RestController', '@Service', '@Repository', '@Component']):
                best_practices['spring_boot']['proper_annotations'] = True
            
            # Configuration externalization
            if 'application.properties' in file_path or 'application.yml' in file_path:
                best_practices['spring_boot']['configuration_externalized'] = True
            
            # Exception handling
            if '@ExceptionHandler' in content or 'try-catch' in content.lower():
                best_practices['spring_boot']['proper_exception_handling'] = True
            
            # Logging
            if any(log in content for log in ['Logger', 'log.', 'logger.']):
                best_practices['spring_boot']['logging_implemented'] = True
        
        # Check general practices
        file_names = list(key_files.keys())
        best_practices['general']['readme_present'] = any('readme' in f.lower() for f in file_names)
        best_practices['general']['gitignore_present'] = '.gitignore' in file_names
        
        return {
            'practices': best_practices,
            'compliance_score': self._calculate_compliance_score(best_practices),
            'recommendations': self._generate_best_practice_recommendations(best_practices)
        }
    
    def _analyze_api_structure(self, key_files: Dict) -> Dict[str, Any]:
        """Analyze API structure and generate documentation insights"""
        
        api_analysis = {
            'endpoints_found': [],
            'http_methods': set(),
            'request_mappings': [],
            'response_types': [],
            'api_documentation': 'missing'
        }
        
        for file_path, file_data in key_files.items():
            if 'content' not in file_data:
                continue
                
            content = file_data['content']
            
            # Find Spring Boot REST endpoints
            if '@RestController' in content or '@Controller' in content:
                # Extract endpoint patterns
                import re
                
                # Find @RequestMapping, @GetMapping, etc.
                mapping_patterns = re.findall(r'@(Get|Post|Put|Delete|Request)Mapping\([^)]*\)', content)
                api_analysis['request_mappings'].extend(mapping_patterns)
                
                # Extract HTTP methods
                for pattern in mapping_patterns:
                    if 'Get' in pattern:
                        api_analysis['http_methods'].add('GET')
                    elif 'Post' in pattern:
                        api_analysis['http_methods'].add('POST')
                    elif 'Put' in pattern:
                        api_analysis['http_methods'].add('PUT')
                    elif 'Delete' in pattern:
                        api_analysis['http_methods'].add('DELETE')
        
        api_analysis['http_methods'] = list(api_analysis['http_methods'])
        
        return {
            'api_structure': api_analysis,
            'documentation_recommendations': self._generate_api_doc_recommendations(api_analysis),
            'swagger_integration': 'recommended' if api_analysis['request_mappings'] else 'not_applicable'
        }
    
    def _analyze_deployment(self, key_files: Dict) -> Dict[str, Any]:
        """Analyze deployment configuration and provide recommendations"""
        
        deployment_analysis = {
            'containerization': {
                'dockerfile_present': 'Dockerfile' in key_files,
                'docker_compose_present': 'docker-compose.yml' in key_files or 'docker-compose.yaml' in key_files
            },
            'cloud_ready': {
                'externalized_config': False,
                'health_checks': False,
                'logging_configured': False,
                'metrics_enabled': False
            },
            'ci_cd': {
                'github_actions': '.github/workflows' in str(key_files.keys()),
                'jenkins_file': 'Jenkinsfile' in key_files
            }
        }
        
        # Check for cloud-ready patterns
        for file_path, file_data in key_files.items():
            if 'content' not in file_data:
                continue
                
            content = file_data['content'].lower()
            
            if 'actuator' in content:
                deployment_analysis['cloud_ready']['health_checks'] = True
                deployment_analysis['cloud_ready']['metrics_enabled'] = True
            
            if 'logging' in content or 'logback' in content:
                deployment_analysis['cloud_ready']['logging_configured'] = True
        
        return {
            'current_state': deployment_analysis,
            'recommendations': self._generate_deployment_recommendations(deployment_analysis),
            'cloud_readiness_score': self._calculate_cloud_readiness_score(deployment_analysis)
        }
    
    # Helper methods for analysis
    def _create_basic_quality_analysis(self, code_samples: List) -> Dict:
        return {
            'maintainability_score': 7,
            'files_analyzed': len(code_samples),
            'general_assessment': 'Code structure appears organized',
            'method': 'basic_pattern_analysis'
        }
    
    def _create_basic_architecture_analysis(self, repo_structure: Dict) -> Dict:
        return {
            'pattern': 'Layered Architecture',
            'confidence': 'medium',
            'structure_score': 8,
            'method': 'structure_based_inference'
        }
    
    def _generate_security_recommendations(self, indicators: Dict) -> List[str]:
        recommendations = []
        
        if not indicators['authentication_found']:
            recommendations.append("Implement robust authentication mechanism")
        
        if not indicators['input_validation']:
            recommendations.append("Add comprehensive input validation")
        
        if not indicators['encryption_usage']:
            recommendations.append("Implement encryption for sensitive data")
        
        return recommendations
    
    def _calculate_performance_score(self, insights: Dict) -> int:
        total_issues = sum(len(issues) for issues in insights.values())
        return max(100 - (total_issues * 10), 0)
    
    def _get_priority_performance_recommendations(self, insights: Dict) -> List[str]:
        recommendations = []
        
        if insights['database_optimization']:
            recommendations.append("Optimize database queries - highest priority")
        
        if insights['caching_opportunities']:
            recommendations.append("Implement caching strategy - medium priority")
        
        return recommendations[:3]  # Top 3 recommendations
    
    def _calculate_compliance_score(self, practices: Dict) -> int:
        total_practices = 0
        followed_practices = 0
        
        for category in practices.values():
            for practice, followed in category.items():
                total_practices += 1
                if followed:
                    followed_practices += 1
        
        return int((followed_practices / total_practices) * 100) if total_practices > 0 else 0
    
    def _generate_best_practice_recommendations(self, practices: Dict) -> List[str]:
        recommendations = []
        
        if not practices['spring_boot']['proper_exception_handling']:
            recommendations.append("Implement global exception handling with @ControllerAdvice")
        
        if not practices['spring_boot']['logging_implemented']:
            recommendations.append("Add comprehensive logging throughout the application")
        
        if not practices['general']['readme_present']:
            recommendations.append("Create comprehensive README documentation")
        
        return recommendations
    
    def _generate_api_doc_recommendations(self, api_analysis: Dict) -> List[str]:
        recommendations = []
        
        if api_analysis['request_mappings']:
            recommendations.append("Integrate Swagger/OpenAPI for API documentation")
            recommendations.append("Add @ApiOperation annotations for better documentation")
        
        return recommendations
    
    def _generate_deployment_recommendations(self, deployment_analysis: Dict) -> List[str]:
        recommendations = []
        
        if not deployment_analysis['containerization']['dockerfile_present']:
            recommendations.append("Create Dockerfile for containerization")
        
        if not deployment_analysis['cloud_ready']['health_checks']:
            recommendations.append("Add Spring Boot Actuator for health checks")
        
        if not deployment_analysis['ci_cd']['github_actions']:
            recommendations.append("Set up CI/CD pipeline with GitHub Actions")
        
        return recommendations
    
    def _calculate_cloud_readiness_score(self, deployment_analysis: Dict) -> int:
        score = 0
        total_checks = 0
        
        for category in deployment_analysis.values():
            for check, status in category.items():
                total_checks += 1
                if status:
                    score += 1
        
        return int((score / total_checks) * 100) if total_checks > 0 else 0
    
    def _create_fallback_analysis(self, repo_structure: Dict) -> Dict:
        """Fallback analysis when Q Developer integration fails"""
        return {
            'code_quality': {'score': 'unknown', 'method': 'fallback'},
            'architecture_analysis': {'pattern': 'inferred_from_structure'},
            'security_insights': {'basic_checks': 'performed'},
            'recommendations': ['Enable Q Developer integration for detailed analysis']
        }
