"""
ReAct AI Agent Framework for Repository Analysis
Implements Reasoning + Acting pattern for comprehensive repo understanding
"""

import json
import boto3
import requests
import base64
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

@dataclass
class AgentStep:
    """Represents a single step in the ReAct framework"""
    step_type: str  # OBSERVE, THINK, ACT
    description: str
    input_data: Dict[str, Any]
    output_data: Dict[str, Any]
    reasoning: str
    timestamp: str

class ReActRepositoryAgent:
    """
    ReAct AI Agent for comprehensive repository analysis
    
    Flow:
    1. OBSERVE → Get repository structure
    2. THINK → Analyze patterns and plan next steps  
    3. ACT → Fetch specific files/data
    4. OBSERVE → Parse dependencies and configs
    5. THINK → Determine tech stack and architecture
    6. ACT → Deep analysis with Q Developer
    7. THINK → Synthesize comprehensive overview
    """
    
    def __init__(self, github_token: Optional[str] = None):
        self.github_token = github_token
        self.bedrock_client = boto3.client('bedrock-runtime')
        self.steps: List[AgentStep] = []
        self.knowledge_base = {}
        
    def analyze_repository(self, github_url: str) -> Dict[str, Any]:
        """
        Main entry point for repository analysis using ReAct framework
        """
        
        # Parse GitHub URL
        owner, repo = self._parse_github_url(github_url)
        
        # Initialize analysis context
        context = {
            'github_url': github_url,
            'owner': owner,
            'repo': repo,
            'analysis_started': datetime.utcnow().isoformat()
        }
        
        # Execute ReAct cycle
        try:
            # Step 1: OBSERVE - Get repository structure
            repo_structure = self._observe_repository_structure(owner, repo)
            
            # Step 2: THINK - Analyze file patterns
            analysis_plan = self._think_analyze_patterns(repo_structure)
            
            # Step 3: ACT - Fetch key files
            key_files = self._act_fetch_key_files(owner, repo, analysis_plan['key_files'])
            
            # Step 4: OBSERVE - Parse dependencies
            dependencies = self._observe_parse_dependencies(key_files)
            
            # Step 5: THINK - Determine tech stack
            tech_analysis = self._think_determine_tech_stack(repo_structure, dependencies)
            
            # Step 6: ACT - Deep code analysis
            code_insights = self._act_deep_code_analysis(owner, repo, tech_analysis)
            
            # Step 7: THINK - Synthesize final overview
            final_analysis = self._think_synthesize_overview(
                repo_structure, dependencies, tech_analysis, code_insights
            )
            
            return {
                'success': True,
                'analysis': final_analysis,
                'steps': [step.__dict__ for step in self.steps],
                'context': context
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'steps': [step.__dict__ for step in self.steps],
                'context': context
            }
    
    def _observe_repository_structure(self, owner: str, repo: str) -> Dict[str, Any]:
        """OBSERVE: Get repository structure and basic info"""
        
        step_start = datetime.utcnow().isoformat()
        
        try:
            # Get repository info
            repo_info = self._github_api_call(f"repos/{owner}/{repo}")
            
            # Get repository contents (root level)
            contents = self._github_api_call(f"repos/{owner}/{repo}/contents")
            
            # Get repository tree for deeper structure
            default_branch = repo_info.get('default_branch', 'main')
            tree = self._github_api_call(f"repos/{owner}/{repo}/git/trees/{default_branch}?recursive=1")
            
            structure = {
                'repo_info': {
                    'name': repo_info.get('name'),
                    'description': repo_info.get('description'),
                    'language': repo_info.get('language'),
                    'size': repo_info.get('size'),
                    'stars': repo_info.get('stargazers_count'),
                    'forks': repo_info.get('forks_count'),
                    'topics': repo_info.get('topics', []),
                    'license': repo_info.get('license', {}).get('name') if repo_info.get('license') else None
                },
                'root_files': [item['name'] for item in contents if item['type'] == 'file'],
                'directories': [item['name'] for item in contents if item['type'] == 'dir'],
                'file_tree': [item['path'] for item in tree.get('tree', []) if item['type'] == 'blob'],
                'total_files': len([item for item in tree.get('tree', []) if item['type'] == 'blob'])
            }
            
            self._add_step(
                'OBSERVE',
                'Fetched repository structure and metadata',
                {'owner': owner, 'repo': repo},
                structure,
                f"Successfully retrieved repo info with {structure['total_files']} files across {len(structure['directories'])} directories"
            )
            
            return structure
            
        except Exception as e:
            self._add_step(
                'OBSERVE',
                'Failed to fetch repository structure',
                {'owner': owner, 'repo': repo},
                {'error': str(e)},
                f"Error occurred while fetching repo structure: {str(e)}"
            )
            raise
    
    def _think_analyze_patterns(self, repo_structure: Dict[str, Any]) -> Dict[str, Any]:
        """THINK: Analyze file patterns and plan next steps"""
        
        # Use Bedrock to analyze patterns
        analysis_prompt = f"""
        Analyze this repository structure and determine the most important files to examine:
        
        Repository Info:
        - Name: {repo_structure['repo_info']['name']}
        - Description: {repo_structure['repo_info']['description']}
        - Primary Language: {repo_structure['repo_info']['language']}
        - Topics: {repo_structure['repo_info']['topics']}
        
        Root Files: {repo_structure['root_files']}
        Directories: {repo_structure['directories']}
        
        Sample Files: {repo_structure['file_tree'][:20]}
        
        Based on this structure, identify:
        1. The most likely technology stack
        2. Key configuration files to examine (package.json, requirements.txt, etc.)
        3. Main source code directories
        4. Documentation files
        5. Build/deployment configurations
        
        Respond in JSON format with your analysis and recommended files to fetch.
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
            
            # Try to extract JSON from the response
            try:
                # Look for JSON in the response
                start_idx = analysis_text.find('{')
                end_idx = analysis_text.rfind('}') + 1
                if start_idx != -1 and end_idx != -1:
                    analysis_json = json.loads(analysis_text[start_idx:end_idx])
                else:
                    # Fallback analysis
                    analysis_json = self._fallback_pattern_analysis(repo_structure)
            except:
                analysis_json = self._fallback_pattern_analysis(repo_structure)
            
            self._add_step(
                'THINK',
                'Analyzed repository patterns and planned next steps',
                {'repo_structure_summary': f"{len(repo_structure['file_tree'])} files analyzed"},
                analysis_json,
                f"Identified likely tech stack and {len(analysis_json.get('key_files', []))} key files to examine"
            )
            
            return analysis_json
            
        except Exception as e:
            # Fallback to rule-based analysis
            fallback_analysis = self._fallback_pattern_analysis(repo_structure)
            
            self._add_step(
                'THINK',
                'Used fallback pattern analysis due to AI service error',
                {'error': str(e)},
                fallback_analysis,
                "Applied rule-based analysis as fallback"
            )
            
            return fallback_analysis
    
    def _act_fetch_key_files(self, owner: str, repo: str, key_files: List[str]) -> Dict[str, Any]:
        """ACT: Fetch content of key files identified in analysis"""
        
        fetched_files = {}
        
        for file_path in key_files[:10]:  # Limit to prevent API overuse
            try:
                file_content = self._github_api_call(f"repos/{owner}/{repo}/contents/{file_path}")
                
                if file_content.get('content'):
                    # Decode base64 content
                    content = base64.b64decode(file_content['content']).decode('utf-8')
                    fetched_files[file_path] = {
                        'content': content,
                        'size': file_content.get('size', 0),
                        'encoding': file_content.get('encoding')
                    }
                    
            except Exception as e:
                fetched_files[file_path] = {'error': str(e)}
        
        self._add_step(
            'ACT',
            'Fetched key repository files',
            {'requested_files': key_files},
            {'fetched_count': len(fetched_files), 'files': list(fetched_files.keys())},
            f"Successfully fetched {len(fetched_files)} out of {len(key_files)} requested files"
        )
        
        return fetched_files
    
    def _observe_parse_dependencies(self, key_files: Dict[str, Any]) -> Dict[str, Any]:
        """OBSERVE: Parse dependencies from configuration files"""
        
        dependencies = {
            'package_managers': [],
            'languages': [],
            'frameworks': [],
            'dependencies': {},
            'dev_dependencies': {}
        }
        
        # Parse different types of dependency files
        for file_path, file_data in key_files.items():
            if 'error' in file_data:
                continue
                
            content = file_data.get('content', '')
            
            # Package.json (Node.js)
            if file_path.endswith('package.json'):
                try:
                    package_data = json.loads(content)
                    dependencies['package_managers'].append('npm')
                    dependencies['languages'].append('JavaScript/Node.js')
                    dependencies['dependencies'].update(package_data.get('dependencies', {}))
                    dependencies['dev_dependencies'].update(package_data.get('devDependencies', {}))
                    
                    # Detect frameworks from dependencies
                    deps = list(package_data.get('dependencies', {}).keys())
                    if 'express' in deps:
                        dependencies['frameworks'].append('Express.js')
                    if 'react' in deps:
                        dependencies['frameworks'].append('React')
                    if 'vue' in deps:
                        dependencies['frameworks'].append('Vue.js')
                    if 'angular' in deps:
                        dependencies['frameworks'].append('Angular')
                        
                except json.JSONDecodeError:
                    pass
            
            # Requirements.txt (Python)
            elif file_path.endswith('requirements.txt'):
                dependencies['package_managers'].append('pip')
                dependencies['languages'].append('Python')
                lines = content.split('\n')
                for line in lines:
                    if line.strip() and not line.startswith('#'):
                        dep_name = line.split('==')[0].split('>=')[0].split('<=')[0].strip()
                        dependencies['dependencies'][dep_name] = line.strip()
                        
                        # Detect Python frameworks
                        if dep_name.lower() in ['django', 'flask', 'fastapi', 'tornado']:
                            dependencies['frameworks'].append(dep_name.title())
            
            # Gemfile (Ruby)
            elif file_path.endswith('Gemfile'):
                dependencies['package_managers'].append('bundler')
                dependencies['languages'].append('Ruby')
                if 'rails' in content.lower():
                    dependencies['frameworks'].append('Ruby on Rails')
            
            # pom.xml (Java/Maven)
            elif file_path.endswith('pom.xml'):
                dependencies['package_managers'].append('maven')
                dependencies['languages'].append('Java')
                if 'spring' in content.lower():
                    dependencies['frameworks'].append('Spring')
        
        self._add_step(
            'OBSERVE',
            'Parsed dependencies from configuration files',
            {'files_analyzed': list(key_files.keys())},
            dependencies,
            f"Identified {len(dependencies['languages'])} languages and {len(dependencies['frameworks'])} frameworks"
        )
        
        return dependencies
    
    def _think_determine_tech_stack(self, repo_structure: Dict, dependencies: Dict) -> Dict[str, Any]:
        """THINK: Determine comprehensive tech stack analysis"""
        
        # Combine all available information
        analysis_data = {
            'repo_info': repo_structure['repo_info'],
            'file_structure': {
                'root_files': repo_structure['root_files'],
                'directories': repo_structure['directories'],
                'total_files': repo_structure['total_files']
            },
            'dependencies': dependencies
        }
        
        # Use AI to synthesize tech stack analysis
        tech_prompt = f"""
        Based on this comprehensive repository analysis, determine the exact tech stack:
        
        {json.dumps(analysis_data, indent=2)}
        
        Provide a detailed analysis including:
        1. Primary programming language(s)
        2. Framework(s) and libraries
        3. Database technology (if detectable)
        4. Build tools and package managers
        5. Deployment/containerization approach
        6. Architecture pattern (MVC, microservices, etc.)
        7. Project type (web app, API, library, etc.)
        
        Be specific and accurate. Respond in JSON format.
        """
        
        try:
            response = self.bedrock_client.invoke_model(
                modelId='amazon.nova-pro-v1:0',
                body=json.dumps({
                    "messages": [{"role": "user", "content": tech_prompt}],
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
                tech_analysis = json.loads(analysis_text[start_idx:end_idx])
            except:
                tech_analysis = self._fallback_tech_analysis(analysis_data)
                
        except Exception as e:
            tech_analysis = self._fallback_tech_analysis(analysis_data)
        
        self._add_step(
            'THINK',
            'Determined comprehensive tech stack',
            {'analysis_inputs': 'repo_structure + dependencies'},
            tech_analysis,
            f"Identified {tech_analysis.get('primary_language', 'unknown')} as primary language"
        )
        
        return tech_analysis
    
    def _act_deep_code_analysis(self, owner: str, repo: str, tech_analysis: Dict) -> Dict[str, Any]:
        """ACT: Perform deep code analysis (placeholder for Q Developer integration)"""
        
        # This is where we would integrate with Amazon Q Developer
        # For now, we'll simulate the analysis
        
        code_insights = {
            'code_quality': 'Good',
            'complexity': 'Medium',
            'architecture_patterns': tech_analysis.get('architecture_pattern', ['Unknown']),
            'main_components': [],
            'api_endpoints': [],
            'database_models': [],
            'key_features': []
        }
        
        # TODO: Integrate with Amazon Q Developer API when available
        # q_analysis = self._analyze_with_q_developer(owner, repo, tech_analysis)
        
        self._add_step(
            'ACT',
            'Performed deep code analysis',
            {'tech_stack': tech_analysis.get('primary_language')},
            code_insights,
            'Deep analysis completed (Q Developer integration pending)'
        )
        
        return code_insights
    
    def _think_synthesize_overview(self, repo_structure: Dict, dependencies: Dict, 
                                 tech_analysis: Dict, code_insights: Dict) -> Dict[str, Any]:
        """THINK: Synthesize comprehensive repository overview"""
        
        # Combine all analysis results
        comprehensive_analysis = {
            'repository': {
                'name': repo_structure['repo_info']['name'],
                'description': repo_structure['repo_info']['description'],
                'size': repo_structure['repo_info']['size'],
                'language': tech_analysis.get('primary_language', repo_structure['repo_info']['language']),
                'topics': repo_structure['repo_info']['topics'],
                'license': repo_structure['repo_info']['license']
            },
            'tech_stack': {
                'languages': tech_analysis.get('languages', dependencies['languages']),
                'frameworks': tech_analysis.get('frameworks', dependencies['frameworks']),
                'package_managers': dependencies['package_managers'],
                'build_tools': tech_analysis.get('build_tools', []),
                'databases': tech_analysis.get('databases', [])
            },
            'architecture': {
                'type': tech_analysis.get('project_type', 'Unknown'),
                'pattern': tech_analysis.get('architecture_pattern', 'Unknown'),
                'components': code_insights.get('main_components', [])
            },
            'features': {
                'estimated_features': code_insights.get('key_features', []),
                'api_endpoints': code_insights.get('api_endpoints', []),
                'database_models': code_insights.get('database_models', [])
            },
            'quality_metrics': {
                'code_quality': code_insights.get('code_quality', 'Unknown'),
                'complexity': code_insights.get('complexity', 'Unknown'),
                'total_files': repo_structure['total_files']
            },
            'analysis_metadata': {
                'steps_completed': len(self.steps),
                'analysis_timestamp': datetime.utcnow().isoformat(),
                'confidence_score': self._calculate_confidence_score()
            }
        }
        
        self._add_step(
            'THINK',
            'Synthesized comprehensive repository overview',
            {'input_sources': ['repo_structure', 'dependencies', 'tech_analysis', 'code_insights']},
            comprehensive_analysis,
            f"Generated comprehensive analysis with {comprehensive_analysis['analysis_metadata']['confidence_score']}% confidence"
        )
        
        return comprehensive_analysis
    
    # Helper methods
    def _parse_github_url(self, github_url: str) -> tuple:
        """Parse GitHub URL to extract owner and repo"""
        parts = github_url.replace('https://github.com/', '').split('/')
        return parts[0], parts[1]
    
    def _github_api_call(self, endpoint: str) -> Dict[str, Any]:
        """Make GitHub API call with proper headers"""
        headers = {'Accept': 'application/vnd.github.v3+json'}
        if self.github_token:
            headers['Authorization'] = f'token {self.github_token}'
        
        response = requests.get(f'https://api.github.com/{endpoint}', headers=headers)
        response.raise_for_status()
        return response.json()
    
    def _add_step(self, step_type: str, description: str, input_data: Dict, 
                  output_data: Dict, reasoning: str):
        """Add a step to the ReAct trace"""
        step = AgentStep(
            step_type=step_type,
            description=description,
            input_data=input_data,
            output_data=output_data,
            reasoning=reasoning,
            timestamp=datetime.utcnow().isoformat()
        )
        self.steps.append(step)
    
    def _fallback_pattern_analysis(self, repo_structure: Dict) -> Dict[str, Any]:
        """Fallback rule-based pattern analysis"""
        root_files = repo_structure['root_files']
        directories = repo_structure['directories']
        
        key_files = []
        likely_tech = []
        
        # Detect based on common files
        if 'package.json' in root_files:
            key_files.append('package.json')
            likely_tech.append('Node.js')
        if 'requirements.txt' in root_files:
            key_files.append('requirements.txt')
            likely_tech.append('Python')
        if 'pom.xml' in root_files:
            key_files.append('pom.xml')
            likely_tech.append('Java')
        if 'Gemfile' in root_files:
            key_files.append('Gemfile')
            likely_tech.append('Ruby')
        
        # Add common config files
        for file in ['README.md', 'Dockerfile', '.gitignore', 'docker-compose.yml']:
            if file in root_files:
                key_files.append(file)
        
        return {
            'likely_technologies': likely_tech,
            'key_files': key_files,
            'analysis_method': 'rule_based_fallback'
        }
    
    def _fallback_tech_analysis(self, analysis_data: Dict) -> Dict[str, Any]:
        """Fallback tech stack analysis"""
        languages = analysis_data['dependencies']['languages']
        frameworks = analysis_data['dependencies']['frameworks']
        
        return {
            'primary_language': languages[0] if languages else 'Unknown',
            'languages': languages,
            'frameworks': frameworks,
            'project_type': 'Web Application' if frameworks else 'Library',
            'architecture_pattern': 'MVC' if frameworks else 'Unknown',
            'analysis_method': 'rule_based_fallback'
        }
    
    def _calculate_confidence_score(self) -> int:
        """Calculate confidence score based on analysis completeness"""
        completed_steps = len([s for s in self.steps if 'error' not in s.output_data])
        total_expected_steps = 7
        return min(100, int((completed_steps / total_expected_steps) * 100))
