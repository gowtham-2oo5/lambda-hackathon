"""
Enhanced ReAct Agent with Amazon Q Developer Integration
Complete implementation of the 7-step ReAct framework with deep code analysis
"""

import json
import boto3
import urllib.request
import urllib.parse
import base64
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

# Import Q Developer integration
from q_developer_integration import QDeveloperCodeAnalyzer

@dataclass
class EnhancedAgentStep:
    """Enhanced step in the ReAct framework with Q Developer insights"""
    step_type: str  # OBSERVE, THINK, ACT
    description: str
    input_data: Dict[str, Any]
    output_data: Dict[str, Any]
    reasoning: str
    q_insights: Optional[Dict[str, Any]]
    timestamp: str

class EnhancedReActRepositoryAgent:
    """
    Enhanced ReAct AI Agent with Amazon Q Developer Integration
    
    Complete Flow:
    1. OBSERVE → Get repository structure
    2. THINK → Analyze patterns with AI
    3. ACT → Fetch specific files
    4. OBSERVE → Parse dependencies and configs
    5. THINK → Determine tech stack with AI
    6. ACT → Deep code analysis with Q Developer ⭐ NEW!
    7. THINK → Synthesize comprehensive overview with Q insights
    """
    
    def __init__(self, github_token: Optional[str] = None, region: str = 'us-east-1'):
        self.github_token = github_token
        self.region = region
        try:
            self.bedrock_client = boto3.client('bedrock-runtime', region_name=region)
        except Exception:
            self.bedrock_client = None  # Fallback for local testing
        self.q_analyzer = QDeveloperCodeAnalyzer(region=region)  # Q Developer integration
        self.steps: List[EnhancedAgentStep] = []
        self.knowledge_base = {}
        
    def analyze_repository_with_q_developer(self, github_url: str) -> Dict[str, Any]:
        """
        Main entry point for enhanced repository analysis with Q Developer
        """
        
        # Parse GitHub URL
        owner, repo = self._parse_github_url(github_url)
        
        # Initialize analysis context
        context = {
            'github_url': github_url,
            'owner': owner,
            'repo': repo,
            'analysis_started': datetime.utcnow().isoformat(),
            'q_developer_enabled': True
        }
        
        # Execute Enhanced ReAct cycle with Q Developer
        try:
            # Step 1: OBSERVE - Get repository structure
            repo_structure = self._observe_repository_structure(owner, repo)
            
            # Step 2: THINK - Analyze file patterns with AI
            analysis_plan = self._think_analyze_patterns_enhanced(repo_structure)
            
            # Step 3: ACT - Fetch key files for analysis
            key_files = self._act_fetch_key_files_enhanced(owner, repo, analysis_plan['key_files'])
            
            # Step 4: OBSERVE - Parse dependencies and configurations
            dependencies = self._observe_parse_dependencies_enhanced(key_files)
            
            # Step 5: THINK - Determine comprehensive tech stack
            tech_analysis = self._think_determine_tech_stack_enhanced(repo_structure, dependencies)
            
            # Step 6: ACT - Deep code analysis with Q Developer ⭐ NEW STEP!
            q_code_insights = self._act_q_developer_deep_analysis(owner, repo, repo_structure, key_files)
            
            # Step 7: THINK - Synthesize comprehensive overview with Q insights
            final_analysis = self._think_synthesize_with_q_insights(
                repo_structure, dependencies, tech_analysis, q_code_insights
            )
            
            return {
                'success': True,
                'analysis': final_analysis,
                'steps': [step.__dict__ for step in self.steps],
                'q_developer_enabled': True
            }
            
        except Exception as e:
            print(f"Enhanced ReAct + Q Developer analysis error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'q_developer_enabled': False
            }
            
            # Step 7: THINK - Synthesize comprehensive overview with Q insights
            final_analysis = self._think_synthesize_with_q_insights(
                repo_structure, dependencies, tech_analysis, q_code_insights
            )
            
            return {
                'success': True,
                'analysis': final_analysis,
                'steps': [step.__dict__ for step in self.steps],
                'q_developer_enabled': True
            }
            
        except Exception as e:
            print(f"Enhanced ReAct + Q Developer analysis error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'q_developer_enabled': False
            }
    
    def _observe_parse_dependencies_enhanced(self, key_files: Dict[str, Any]) -> Dict[str, Any]:
        """Enhanced dependency parsing with comprehensive analysis"""
        dependencies = {
            'package_managers': [],
            'dependencies': [],
            'dev_dependencies': [],
            'frameworks': [],
            'build_tools': []
        }
        
        try:
            # Parse package.json (both root and client)
            package_files = ['package.json', 'client/package.json']
            for pkg_file in package_files:
                if pkg_file in key_files and key_files[pkg_file]:
                    try:
                        # Handle different content formats
                        file_data = key_files[pkg_file]
                        if isinstance(file_data, dict) and 'content' in file_data:
                            # File content is in {'content': '...', 'size': ...} format
                            content = file_data['content']
                        elif isinstance(file_data, str):
                            # File content is direct string
                            content = file_data
                        else:
                            # File content is already parsed dict
                            package_data = file_data
                            content = None
                        
                        # Parse JSON content if needed
                        if content:
                            package_data = json.loads(content)
                            
                        dependencies['package_managers'].append('npm')
                        if 'dependencies' in package_data:
                            dependencies['dependencies'].extend(list(package_data['dependencies'].keys()))
                        if 'devDependencies' in package_data:
                            dependencies['dev_dependencies'].extend(list(package_data['devDependencies'].keys()))
                        
                        # Detect frameworks from package.json
                        all_deps = list(package_data.get('dependencies', {}).keys()) + list(package_data.get('devDependencies', {}).keys())
                        for dep in all_deps:
                            if 'next' in dep.lower():
                                dependencies['frameworks'].append('Next.js')
                            elif 'react' in dep.lower():
                                dependencies['frameworks'].append('React')
                            elif 'tailwind' in dep.lower():
                                dependencies['frameworks'].append('Tailwind CSS')
                    except (json.JSONDecodeError, TypeError, KeyError) as e:
                        print(f"Error parsing {pkg_file}: {e}")
            
            # Parse requirements.txt
            if 'requirements.txt' in key_files:
                dependencies['package_managers'].append('pip')
                deps = [line.split('==')[0].split('>=')[0].strip() 
                       for line in key_files['requirements.txt'].split('\n') if line.strip()]
                dependencies['dependencies'].extend(deps)
            
            # Parse pom.xml
            if 'pom.xml' in key_files:
                dependencies['package_managers'].append('maven')
                dependencies['build_tools'].append('Maven')
            
            # Parse build.gradle
            if 'build.gradle' in key_files or 'build.gradle.kts' in key_files:
                dependencies['package_managers'].append('gradle')
                dependencies['build_tools'].append('Gradle')
                
        except Exception as e:
            print(f"Error parsing dependencies: {e}")
            
        return dependencies
    
    def _think_determine_tech_stack_enhanced(self, repo_structure: Dict, dependencies: Dict) -> Dict[str, Any]:
        """Enhanced tech stack determination with AI insights"""
        tech_stack = {
            'primary_language': None,
            'frameworks': [],
            'databases': [],
            'cloud_services': [],
            'deployment_tools': []
        }
        
        # Determine primary language from file extensions
        file_extensions = {}
        for file_path in repo_structure.get('files', []):
            ext = file_path.split('.')[-1] if '.' in file_path else 'no_ext'
            file_extensions[ext] = file_extensions.get(ext, 0) + 1
        
        # Map extensions to languages
        lang_mapping = {
            'js': 'JavaScript', 'ts': 'TypeScript', 'py': 'Python',
            'java': 'Java', 'kt': 'Kotlin', 'go': 'Go',
            'rb': 'Ruby', 'php': 'PHP', 'cs': 'C#'
        }
        
        if file_extensions:
            primary_ext = max(file_extensions, key=file_extensions.get)
            tech_stack['primary_language'] = lang_mapping.get(primary_ext, primary_ext)
        
        # Enhanced framework detection from dependencies and file patterns
        framework_mapping = {
            'express': 'Express.js', 'react': 'React', 'vue': 'Vue.js',
            'angular': 'Angular', 'django': 'Django', 'flask': 'Flask',
            'spring-boot': 'Spring Boot', 'spring': 'Spring Framework',
            'next': 'Next.js', 'nuxt': 'Nuxt.js', 'gatsby': 'Gatsby',
            'tailwindcss': 'Tailwind CSS', 'bootstrap': 'Bootstrap',
            'shadcn': 'shadcn/ui', '@radix-ui': 'Radix UI'
        }
        
        for dep in dependencies.get('dependencies', []):
            for key, framework in framework_mapping.items():
                if key in dep.lower():
                    if framework not in tech_stack['frameworks']:
                        tech_stack['frameworks'].append(framework)
        
        # Detect frameworks from file patterns
        file_pattern_frameworks = {
            'next.config': 'Next.js',
            'tailwind.config': 'Tailwind CSS',
            'components.json': 'shadcn/ui',
            'app/layout.tsx': 'Next.js App Router',
            'pages/_app': 'Next.js Pages Router'
        }
        
        for pattern, framework in file_pattern_frameworks.items():
            if any(pattern in str(file) for file in repo_structure.get('files', [])):
                if framework not in tech_stack['frameworks']:
                    tech_stack['frameworks'].append(framework)
        
        return tech_stack
    
    def _extract_features_from_structure(self, repo_structure: Dict, key_files: Dict) -> List[str]:
        """Extract features from repository structure and files"""
        features = []
        
        # Extract features from directory structure
        directories = repo_structure.get('directories', [])
        files = repo_structure.get('files', [])
        file_tree = repo_structure.get('file_tree', [])
        
        # Admin/Dashboard features
        admin_patterns = ['admin', 'dashboard', 'management', 'panel']
        if any(pattern in str(file_tree).lower() for pattern in admin_patterns):
            features.extend([
                'Admin Dashboard',
                'User Management',
                'Administrative Controls'
            ])
        
        # Authentication features
        auth_patterns = ['auth', 'login', 'signin', 'signup', 'register']
        if any(pattern in str(file_tree).lower() for pattern in auth_patterns):
            features.extend([
                'User Authentication',
                'Login System',
                'Access Control'
            ])
        
        # Restaurant/Food features (specific to ezybites)
        restaurant_patterns = ['restaurant', 'food', 'menu', 'order', 'review']
        if any(pattern in str(file_tree).lower() for pattern in restaurant_patterns):
            features.extend([
                'Restaurant Management',
                'Review System',
                'Food Service Platform'
            ])
        
        # Analytics features
        analytics_patterns = ['analytics', 'chart', 'metrics', 'stats', 'report']
        if any(pattern in str(file_tree).lower() for pattern in analytics_patterns):
            features.extend([
                'Analytics Dashboard',
                'Data Visualization',
                'Performance Metrics'
            ])
        
        # UI/Component features
        ui_patterns = ['components/ui', 'button', 'card', 'table', 'form']
        if any(pattern in str(file_tree).lower() for pattern in ui_patterns):
            features.extend([
                'Modern UI Components',
                'Responsive Design',
                'Interactive Interface'
            ])
        
        # Settings features
        settings_patterns = ['settings', 'config', 'preferences']
        if any(pattern in str(file_tree).lower() for pattern in settings_patterns):
            features.extend([
                'Settings Management',
                'Configuration Panel',
                'User Preferences'
            ])
        
        return list(set(features))  # Remove duplicates
    
    def _observe_repository_structure(self, owner: str, repo: str) -> Dict[str, Any]:
        """OBSERVE: Enhanced repository structure analysis"""
        
        try:
            # Get repository info using urllib
            repo_url = f'https://api.github.com/repos/{owner}/{repo}'
            req = urllib.request.Request(repo_url)
            req.add_header('Accept', 'application/vnd.github.v3+json')
            
            with urllib.request.urlopen(req) as response:
                repo_info = json.loads(response.read().decode())
            
            # Get repository contents (root level)
            contents_url = f'https://api.github.com/repos/{owner}/{repo}/contents'
            req = urllib.request.Request(contents_url)
            req.add_header('Accept', 'application/vnd.github.v3+json')
            
            with urllib.request.urlopen(req) as response:
                contents = json.loads(response.read().decode())
            
            # Get repository tree for deeper structure
            default_branch = repo_info.get('default_branch', 'main')
            tree_url = f'https://api.github.com/repos/{owner}/{repo}/git/trees/{default_branch}?recursive=1'
            req = urllib.request.Request(tree_url)
            req.add_header('Accept', 'application/vnd.github.v3+json')
            
            try:
                with urllib.request.urlopen(req) as response:
                    tree = json.loads(response.read().decode())
            except:
                tree = {'tree': []}
            
            structure = {
                'repo_info': {
                    'name': repo_info.get('name'),
                    'description': repo_info.get('description'),
                    'language': repo_info.get('language'),
                    'size': repo_info.get('size'),
                    'stars': repo_info.get('stargazers_count'),
                    'forks': repo_info.get('forks_count'),
                    'topics': repo_info.get('topics', []),
                    'license': repo_info.get('license', {}).get('name') if repo_info.get('license') else None,
                    'created_at': repo_info.get('created_at'),
                    'updated_at': repo_info.get('updated_at')
                },
                'root_files': [item['name'] for item in contents if item['type'] == 'file'],
                'directories': [item['name'] for item in contents if item['type'] == 'dir'],
                'file_tree': [item['path'] for item in tree.get('tree', []) if item['type'] == 'blob'],
                'total_files': len([item for item in tree.get('tree', []) if item['type'] == 'blob']),
                'directory_structure': self._analyze_directory_structure(tree.get('tree', []))
            }
            
            self._add_enhanced_step(
                'OBSERVE',
                'Enhanced repository structure analysis',
                {'owner': owner, 'repo': repo},
                structure,
                f"Successfully retrieved comprehensive repo info with {structure['total_files']} files",
                None
            )
            
            return structure
            
        except Exception as e:
            self._add_enhanced_step(
                'OBSERVE',
                'Failed to fetch repository structure',
                {'owner': owner, 'repo': repo},
                {'error': str(e)},
                f"Error occurred while fetching repo structure: {str(e)}",
                None
            )
            raise
    
    def _think_analyze_patterns_enhanced(self, repo_structure: Dict[str, Any]) -> Dict[str, Any]:
        """THINK: Enhanced pattern analysis with deeper insights"""
        
        # Enhanced analysis prompt for better pattern recognition
        analysis_prompt = f"""
        Analyze this repository structure for comprehensive insights:
        
        Repository Info:
        - Name: {repo_structure['repo_info']['name']}
        - Description: {repo_structure['repo_info']['description']}
        - Primary Language: {repo_structure['repo_info']['language']}
        - Topics: {repo_structure['repo_info']['topics']}
        - Size: {repo_structure['repo_info']['size']} KB
        - Stars: {repo_structure['repo_info']['stars']}
        
        Structure Analysis:
        - Root Files: {repo_structure['root_files']}
        - Directories: {repo_structure['directories']}
        - Total Files: {repo_structure['total_files']}
        - Directory Structure: {repo_structure['directory_structure']}
        
        Provide comprehensive analysis including:
        1. Technology stack identification
        2. Architecture pattern recognition
        3. Project complexity assessment
        4. Key files to examine for deep analysis
        5. Potential code quality indicators
        6. Security considerations
        7. Performance optimization opportunities
        8. Best practices adherence
        
        Focus on files that would provide the most insights for Q Developer analysis.
        Respond in JSON format with detailed recommendations.
        """
        
        try:
            response = self.bedrock_client.invoke_model(
                modelId='amazon.nova-pro-v1:0',
                body=json.dumps({
                    "messages": [{"role": "user", "content": analysis_prompt}],
                    "temperature": 0.1,
                    "top_p": 0.9
                })
            )
            
            result = json.loads(response['body'].read())
            analysis_text = result['output']['message']['content'][0]['text']
            
            # Extract JSON from the response
            try:
                start_idx = analysis_text.find('{')
                end_idx = analysis_text.rfind('}') + 1
                if start_idx != -1 and end_idx != -1:
                    analysis_json = json.loads(analysis_text[start_idx:end_idx])
                else:
                    analysis_json = self._fallback_enhanced_pattern_analysis(repo_structure)
            except:
                analysis_json = self._fallback_enhanced_pattern_analysis(repo_structure)
            
            self._add_enhanced_step(
                'THINK',
                'Enhanced pattern analysis with AI insights',
                {'repo_structure_summary': f"{len(repo_structure['file_tree'])} files analyzed"},
                analysis_json,
                f"Identified comprehensive tech stack and {len(analysis_json.get('key_files', []))} priority files for Q Developer analysis",
                None
            )
            
            return analysis_json
            
        except Exception as e:
            fallback_analysis = self._fallback_enhanced_pattern_analysis(repo_structure)
            
            self._add_enhanced_step(
                'THINK',
                'Used enhanced fallback pattern analysis',
                {'error': str(e)},
                fallback_analysis,
                "Applied enhanced rule-based analysis as fallback",
                None
            )
            
            return fallback_analysis
    
    def _act_fetch_key_files_enhanced(self, owner: str, repo: str, key_files: List[str]) -> Dict[str, Any]:
        """ACT: Enhanced file fetching with content analysis"""
        
        fetched_files = {}
        
        # Prioritize files for Q Developer analysis
        priority_files = []
        config_files = []
        code_files = []
        
        for file_path in key_files[:15]:  # Increased limit for better analysis
            if file_path.endswith(('.java', '.js', '.py', '.ts', '.jsx', '.tsx')):
                code_files.append(file_path)
            elif file_path.endswith(('.json', '.xml', '.yml', '.yaml', '.properties')):
                config_files.append(file_path)
            else:
                priority_files.append(file_path)
        
        # Fetch files in priority order
        all_files = priority_files + config_files + code_files
        
        for file_path in all_files:
            try:
                file_url = f'https://api.github.com/repos/{owner}/{repo}/contents/{file_path}'
                req = urllib.request.Request(file_url)
                req.add_header('Accept', 'application/vnd.github.v3+json')
                
                with urllib.request.urlopen(req) as response:
                    file_content = json.loads(response.read().decode())
                
                if file_content.get('content'):
                    # Decode base64 content
                    content = base64.b64decode(file_content['content']).decode('utf-8')
                    fetched_files[file_path] = {
                        'content': content,
                        'size': file_content.get('size', 0),
                        'encoding': file_content.get('encoding'),
                        'type': self._classify_file_type(file_path, content),
                        'analysis_priority': self._get_analysis_priority(file_path, content)
                    }
                    
            except Exception as e:
                fetched_files[file_path] = {'error': str(e)}
        
        self._add_enhanced_step(
            'ACT',
            'Enhanced key file fetching with content classification',
            {'requested_files': key_files},
            {
                'fetched_count': len(fetched_files), 
                'files': list(fetched_files.keys()),
                'code_files': len(code_files),
                'config_files': len(config_files)
            },
            f"Successfully fetched {len(fetched_files)} files with enhanced content analysis",
            None
        )
        
        return fetched_files
    
    def _act_q_developer_deep_analysis(self, owner: str, repo: str, repo_structure: Dict, 
                                     key_files: Dict[str, Any]) -> Dict[str, Any]:
        """ACT: Deep code analysis using Q Developer integration ⭐ NEW STEP!"""
        
        print(f"🔍 Starting Q Developer deep code analysis for {owner}/{repo}")
        
        try:
            # Use Q Developer analyzer for comprehensive code analysis
            q_analysis = self.q_analyzer.analyze_repository_code(
                owner, repo, repo_structure, key_files
            )
            
            if q_analysis['success']:
                q_insights = q_analysis['analysis']
                
                # Extract key insights for README generation
                readme_insights = {
                    'code_quality_score': q_insights['code_quality'].get('maintainability_score', 'unknown'),
                    'architecture_pattern': q_insights['architecture_analysis'].get('pattern', 'unknown'),
                    'security_score': q_insights['security_insights'].get('security_score', 'unknown'),
                    'performance_recommendations': q_insights['performance_recommendations'].get('priority_recommendations', []),
                    'best_practices_score': q_insights['best_practices'].get('compliance_score', 'unknown'),
                    'api_endpoints': q_insights['api_documentation'].get('api_structure', {}).get('endpoints_found', []),
                    'deployment_readiness': q_insights['deployment_recommendations'].get('cloud_readiness_score', 'unknown'),
                    'key_features_detected': self._extract_features_from_q_analysis(q_insights, repo_structure, key_files)
                }
                
                self._add_enhanced_step(
                    'ACT',
                    'Q Developer deep code analysis completed',
                    {'files_analyzed': len(key_files)},
                    readme_insights,
                    f"Q Developer analyzed {len(key_files)} files with comprehensive insights",
                    q_insights  # Store full Q insights
                )
                
                return {
                    'success': True,
                    'q_insights': q_insights,
                    'readme_insights': readme_insights,
                    'analysis_depth': 'comprehensive'
                }
            else:
                # Fallback analysis
                fallback_insights = self._create_fallback_q_analysis(repo_structure, key_files)
                
                self._add_enhanced_step(
                    'ACT',
                    'Q Developer analysis failed, using enhanced fallback',
                    {'error': q_analysis.get('error', 'unknown')},
                    fallback_insights,
                    "Used enhanced pattern-based analysis as Q Developer fallback",
                    None
                )
                
                return {
                    'success': False,
                    'fallback_insights': fallback_insights,
                    'analysis_depth': 'basic'
                }
                
        except Exception as e:
            print(f"❌ Q Developer analysis error: {str(e)}")
            
            fallback_insights = self._create_fallback_q_analysis(repo_structure, key_files)
            
            self._add_enhanced_step(
                'ACT',
                'Q Developer analysis exception, using fallback',
                {'error': str(e)},
                fallback_insights,
                f"Exception in Q Developer analysis: {str(e)}",
                None
            )
            
            return {
                'success': False,
                'error': str(e),
                'fallback_insights': fallback_insights,
                'analysis_depth': 'minimal'
            }
    
    def _think_synthesize_with_q_insights(self, repo_structure: Dict, dependencies: Dict, 
                                        tech_analysis: Dict, q_code_insights: Dict) -> Dict[str, Any]:
        """THINK: Synthesize comprehensive overview with Q Developer insights"""
        
        # Combine all analysis results with Q Developer insights
        comprehensive_analysis = {
            'repository': {
                'name': repo_structure['repo_info']['name'],
                'description': repo_structure['repo_info']['description'],
                'size': repo_structure['repo_info']['size'],
                'language': tech_analysis.get('primary_language', repo_structure['repo_info']['language']),
                'topics': repo_structure['repo_info']['topics'],
                'license': repo_structure['repo_info']['license'],
                'stars': repo_structure['repo_info']['stars'],
                'created_at': repo_structure['repo_info']['created_at']
            },
            'tech_stack': {
                'languages': [tech_analysis.get('primary_language')] if tech_analysis.get('primary_language') else [],
                'frameworks': tech_analysis.get('frameworks', []),
                'package_managers': dependencies.get('package_managers', []),
                'build_tools': tech_analysis.get('build_tools', []),
                'databases': tech_analysis.get('databases', [])
            },
            'architecture': {
                'type': tech_analysis.get('project_type', 'Unknown'),
                'pattern': q_code_insights.get('readme_insights', {}).get('architecture_pattern', 'Unknown'),
                'components': tech_analysis.get('components', [])
            },
            'features': {
                'estimated_features': q_code_insights.get('readme_insights', {}).get('key_features_detected', []),
                'api_endpoints': q_code_insights.get('readme_insights', {}).get('api_endpoints', []),
                'database_models': []  # Would need deeper analysis
            },
            'quality_metrics': {
                'code_quality': q_code_insights.get('readme_insights', {}).get('code_quality_score', 'Unknown'),
                'security_score': q_code_insights.get('readme_insights', {}).get('security_score', 'Unknown'),
                'performance_score': 'Good' if q_code_insights.get('readme_insights', {}).get('performance_recommendations') else 'Unknown',
                'best_practices_score': q_code_insights.get('readme_insights', {}).get('best_practices_score', 'Unknown'),
                'total_files': repo_structure['total_files']
            },
            'deployment': {
                'cloud_readiness': q_code_insights.get('readme_insights', {}).get('deployment_readiness', 'Unknown'),
                'containerization': 'Recommended',
                'ci_cd': 'GitHub Actions recommended'
            },
            'analysis_metadata': {
                'steps_completed': len(self.steps),
                'analysis_timestamp': datetime.utcnow().isoformat(),
                'confidence_score': self._calculate_enhanced_confidence_score(q_code_insights),
                'q_developer_enabled': q_code_insights.get('success', False),
                'analysis_depth': q_code_insights.get('analysis_depth', 'basic')
            }
        }
        
        self._add_enhanced_step(
            'THINK',
            'Synthesized comprehensive repository overview with Q Developer insights',
            {'input_sources': ['repo_structure', 'dependencies', 'tech_analysis', 'q_code_insights']},
            comprehensive_analysis,
            f"Generated comprehensive analysis with {comprehensive_analysis['analysis_metadata']['confidence_score']}% confidence using Q Developer insights",
            q_code_insights.get('q_insights')
        )
        
        return comprehensive_analysis
    
    # Enhanced helper methods
    def _analyze_directory_structure(self, tree_items: List) -> Dict[str, List[str]]:
        """Analyze directory structure for better insights"""
        structure = {}
        
        for item in tree_items:
            if item['type'] == 'blob':  # file
                path_parts = item['path'].split('/')
                if len(path_parts) > 1:
                    directory = '/'.join(path_parts[:-1])
                    if directory not in structure:
                        structure[directory] = []
                    structure[directory].append(path_parts[-1])
        
        return structure
    
    def _classify_file_type(self, file_path: str, content: str) -> str:
        """Classify file type for analysis priority"""
        if file_path.endswith(('.java', '.js', '.py', '.ts')):
            return 'source_code'
        elif file_path.endswith(('.json', '.xml', '.yml', '.yaml')):
            return 'configuration'
        elif file_path.endswith(('.md', '.txt', '.rst')):
            return 'documentation'
        elif file_path.endswith(('.sql', '.db')):
            return 'database'
        else:
            return 'other'
    
    def _get_analysis_priority(self, file_path: str, content: str) -> int:
        """Get analysis priority (1-10, 10 being highest)"""
        if 'main' in file_path.lower() or 'app' in file_path.lower():
            return 10
        elif file_path.endswith('.java') and ('controller' in content.lower() or '@restcontroller' in content.lower()):
            return 9
        elif file_path.endswith(('.json', '.xml')) and ('dependencies' in content.lower() or 'spring' in content.lower()):
            return 8
        elif file_path.endswith(('.java', '.js', '.py', '.ts')):
            return 7
        else:
            return 5
    
    def _extract_features_from_q_analysis(self, q_insights: Dict, repo_structure: Dict = None, key_files: Dict = None) -> List[str]:
        """Extract key features from Q Developer analysis"""
        features = []
        
        # From API analysis
        api_structure = q_insights.get('api_documentation', {}).get('api_structure', {})
        if api_structure.get('request_mappings'):
            features.append('RESTful API endpoints')
        
        # From security analysis
        security = q_insights.get('security_insights', {}).get('indicators', {})
        if security.get('authentication_found'):
            features.append('Authentication system')
        if security.get('authorization_found'):
            features.append('Authorization and access control')
        
        # From best practices
        practices = q_insights.get('best_practices', {}).get('practices', {})
        spring_practices = practices.get('spring_boot', {})
        if spring_practices.get('proper_annotations'):
            features.append('Spring Boot annotations and dependency injection')
        if spring_practices.get('configuration_externalized'):
            features.append('Externalized configuration management')
        
        # From performance analysis
        performance = q_insights.get('performance_recommendations', {}).get('insights', {})
        if performance.get('caching_opportunities'):
            features.append('Caching layer implementation')
        
        # Extract features from repository structure if provided
        if repo_structure and key_files:
            extracted_features = self._extract_features_from_structure(repo_structure, key_files)
            if extracted_features:
                features.extend(extracted_features)
        
        return features if features else ['Core application functionality']
    
    def _create_fallback_q_analysis(self, repo_structure: Dict, key_files: Dict) -> Dict[str, Any]:
        """Create fallback analysis when Q Developer is not available"""
        return {
            'code_quality_score': 7,
            'architecture_pattern': 'Layered Architecture',
            'security_score': 70,
            'performance_recommendations': ['Consider implementing caching', 'Optimize database queries'],
            'best_practices_score': 75,
            'api_endpoints': ['Detected REST endpoints'],
            'deployment_readiness': 80,
            'key_features_detected': [
                'Spring Boot application',
                'RESTful API',
                'Database integration',
                'Configuration management'
            ]
        }
    
    def _calculate_enhanced_confidence_score(self, q_code_insights: Dict) -> int:
        """Calculate enhanced confidence score with Q Developer insights"""
        base_score = min(100, int((len(self.steps) / 7) * 100))
        
        if q_code_insights.get('success'):
            # Q Developer analysis successful - high confidence
            return min(100, base_score + 20)
        elif q_code_insights.get('fallback_insights'):
            # Fallback analysis - medium confidence
            return min(100, base_score + 10)
        else:
            # Basic analysis only
            return base_score
    
    def _fallback_enhanced_pattern_analysis(self, repo_structure: Dict) -> Dict[str, Any]:
        """Enhanced fallback pattern analysis"""
        root_files = repo_structure['root_files']
        directories = repo_structure['directories']
        file_tree = repo_structure.get('file_tree', [])  # Add this line!
        
        key_files = []
        likely_tech = []
        
        # Enhanced detection based on files and structure
        if 'pom.xml' in root_files:
            key_files.extend(['pom.xml', 'src/main/java', 'src/main/resources/application.properties'])
            likely_tech.append('Java/Spring Boot')
        if 'build.gradle' in root_files:
            key_files.extend(['build.gradle', 'src/main/java'])
            likely_tech.append('Java/Gradle')
        if 'package.json' in root_files:
            key_files.append('package.json')
            likely_tech.append('Node.js')
        if 'requirements.txt' in root_files:
            key_files.append('requirements.txt')
            likely_tech.append('Python')
        
        # Add common files for analysis
        priority_files = [
            'README.md', 'package.json', 'package-lock.json',
            'next.config.ts', 'next.config.js', 'tailwind.config.ts', 'tailwind.config.js',
            'tsconfig.json', 'components.json', 'Dockerfile', '.gitignore', 
            'docker-compose.yml', 'app/layout.tsx', 'app/page.tsx'
        ]
        
        for file in priority_files:
            if file in root_files:
                key_files.append(file)
        
        # Add client directory files for Next.js projects
        client_priority_files = [
            'client/package.json', 'client/next.config.ts', 'client/tailwind.config.ts',
            'client/tsconfig.json', 'client/components.json', 'client/app/layout.tsx',
            'client/app/page.tsx', 'client/app/(dashboard)/layout.tsx'
        ]
        
        for file in client_priority_files:
            if any(f.endswith(file.split('/')[-1]) for f in file_tree):
                key_files.append(file)
        
        return {
            'likely_technologies': likely_tech,
            'key_files': key_files,
            'complexity_assessment': 'Medium' if len(directories) > 5 else 'Low',
            'analysis_method': 'enhanced_rule_based_fallback'
        }
    
    def _add_enhanced_step(self, step_type: str, description: str, input_data: Dict, 
                         output_data: Dict, reasoning: str, q_insights: Optional[Dict]):
        """Add an enhanced step to the ReAct trace with Q insights"""
        step = EnhancedAgentStep(
            step_type=step_type,
            description=description,
            input_data=input_data,
            output_data=output_data,
            reasoning=reasoning,
            q_insights=q_insights,
            timestamp=datetime.utcnow().isoformat()
        )
        self.steps.append(step)
    
    def _parse_github_url(self, github_url: str) -> tuple:
        """Parse GitHub URL to extract owner and repo"""
        parts = github_url.replace('https://github.com/', '').split('/')
        return parts[0], parts[1]
