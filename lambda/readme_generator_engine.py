"""
Professional README Generation Engine
Creates developer-focused, GitHub-standard READMEs with dynamic content
"""

import re
import json
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)

@dataclass
class READMETemplate:
    """README template configuration"""
    style: str  # 'developer', 'user', 'enterprise'
    include_toc: bool
    include_badges: bool
    include_shields: bool
    sections: List[str]

class READMEGeneratorEngine:
    """
    Professional README generation engine with multiple templates and styles
    """
    
    def __init__(self):
        # Badge configurations
        self.badge_configs = {
            'language_badges': {
                'JavaScript': 'https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black',
                'Python': 'https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white',
                'Java': 'https://img.shields.io/badge/Java-ED8B00?style=for-the-badge&logo=java&logoColor=white',
                'TypeScript': 'https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white',
                'Go': 'https://img.shields.io/badge/Go-00ADD8?style=for-the-badge&logo=go&logoColor=white',
                'Rust': 'https://img.shields.io/badge/Rust-000000?style=for-the-badge&logo=rust&logoColor=white'
            },
            'framework_badges': {
                'React': 'https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB',
                'Django': 'https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white',
                'Express.js': 'https://img.shields.io/badge/Express.js-404D59?style=for-the-badge',
                'Next.js': 'https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white',
                'Spring Boot': 'https://img.shields.io/badge/Spring_Boot-6DB33F?style=for-the-badge&logo=spring-boot&logoColor=white',
                'Flask': 'https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white'
            },
            'platform_badges': {
                'AWS': 'https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white',
                'Docker': 'https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white',
                'Kubernetes': 'https://img.shields.io/badge/Kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white'
            }
        }
        
        # Section templates
        self.section_templates = {
            'developer': self._get_developer_templates(),
            'user': self._get_user_templates(),
            'enterprise': self._get_enterprise_templates()
        }
    
    def generate_readme(self, json_data: Dict[str, Any], style: str = 'developer') -> str:
        """
        Generate professional README from structured JSON data
        """
        logger.info(f"📝 Generating {style} README")
        
        try:
            # Try to use the emoji-safe generator first
            try:
                from emoji_safe_generator import EmojiSafeREADMEGenerator
                safe_generator = EmojiSafeREADMEGenerator()
                return safe_generator.generate_safe_readme(json_data)
            except ImportError:
                logger.info("Emoji-safe generator not available, using visual generator")
            
            # Try visual generator as fallback
            try:
                from visual_readme_generator import DynamicVisualREADMEGenerator
                visual_generator = DynamicVisualREADMEGenerator()
                return visual_generator.generate_stunning_readme(json_data)
            except ImportError:
                logger.info("Visual generator not available, using standard generator")
            
            # Standard generation as final fallback
            repo_analysis = json_data.get('repository_analysis', {})
            readme_structure = json_data.get('readme_structure', {})
            
            # Create template configuration
            template = READMETemplate(
                style=style,
                include_toc=True,
                include_badges=True,
                include_shields=True,
                sections=self._get_sections_for_style(style)
            )
            
            # Generate README sections
            sections = []
            
            # Header with title and badges
            sections.append(self._generate_header(readme_structure, repo_analysis, template))
            
            # Table of contents
            if template.include_toc:
                sections.append(self._generate_toc(readme_structure, template))
            
            # Main sections
            for section_name in template.sections:
                section_content = self._generate_section(section_name, readme_structure, repo_analysis, template)
                if section_content:
                    sections.append(section_content)
            
            # Footer
            sections.append(self._generate_footer(readme_structure, repo_analysis))
            
            # Combine all sections
            readme_content = '\n\n'.join(filter(None, sections))
            
            # Post-process for quality
            readme_content = self._post_process_readme(readme_content)
            
            logger.info(f"✅ README generated ({len(readme_content)} characters)")
            return readme_content
            
        except Exception as e:
            logger.error(f"❌ README generation failed: {e}")
            return self._generate_fallback_readme(json_data)
    
    def _generate_header(self, readme_structure: Dict, repo_analysis: Dict, template: READMETemplate) -> str:
        """Generate README header with title, description, and badges"""
        project_overview = readme_structure.get('project_overview', {})
        technical_stack = readme_structure.get('technical_stack', {})
        
        # Project title
        title = project_overview.get('name', 'Project')
        description = project_overview.get('description', 'A software project')
        
        header_parts = [f"# {title}"]
        
        # Add tagline/description
        if description:
            header_parts.append(f"\n> {description}")
        
        # Add badges if enabled
        if template.include_badges:
            badges = self._generate_badges(technical_stack, repo_analysis)
            if badges:
                header_parts.append(f"\n{badges}")
        
        return '\n'.join(header_parts)
    
    def _generate_badges(self, technical_stack: Dict, repo_analysis: Dict) -> str:
        """Generate appropriate badges for the project"""
        badges = []
        
        # Language badge
        primary_language = technical_stack.get('primary_language')
        if primary_language and primary_language in self.badge_configs['language_badges']:
            badge_url = self.badge_configs['language_badges'][primary_language]
            badges.append(f"![{primary_language}]({badge_url})")
        
        # Framework badges
        frameworks = technical_stack.get('frameworks', [])
        for framework in frameworks[:3]:  # Limit to 3 framework badges
            if framework in self.badge_configs['framework_badges']:
                badge_url = self.badge_configs['framework_badges'][framework]
                badges.append(f"![{framework}]({badge_url})")
        
        # License badge (if available)
        license_info = repo_analysis.get('license_info', {})
        license_type = license_info.get('license_type')
        if license_type and license_type != 'Not specified in code analysis':
            license_badge = f"![License](https://img.shields.io/badge/License-{license_type}-blue.svg)"
            badges.append(license_badge)
        
        # Build status badge (generic)
        badges.append("![Build Status](https://img.shields.io/badge/build-passing-brightgreen)")
        
        return ' '.join(badges)
    
    def _generate_toc(self, readme_structure: Dict, template: READMETemplate) -> str:
        """Generate table of contents"""
        toc_items = []
        
        # Standard sections for developer template
        if template.style == 'developer':
            toc_sections = [
                ('🎯 Overview', '#overview'),
                ('🚀 Quick Start', '#quick-start'),
                ('📦 Installation', '#installation'),
                ('💻 Usage', '#usage'),
                ('🏗️ Architecture', '#architecture'),
                ('📚 API Documentation', '#api-documentation'),
                ('🛠️ Development', '#development'),
                ('🚀 Deployment', '#deployment'),
                ('🤝 Contributing', '#contributing'),
                ('📄 License', '#license')
            ]
        else:
            # Generate TOC based on available sections
            toc_sections = [
                ('Overview', '#overview'),
                ('Installation', '#installation'),
                ('Usage', '#usage'),
                ('Contributing', '#contributing'),
                ('License', '#license')
            ]
        
        for title, anchor in toc_sections:
            toc_items.append(f"- [{title}]({anchor})")
        
        return "## 📋 Table of Contents\n\n" + '\n'.join(toc_items)
    
    def _generate_section(self, section_name: str, readme_structure: Dict, repo_analysis: Dict, template: READMETemplate) -> str:
        """Generate a specific README section"""
        try:
            if section_name == 'overview':
                return self._generate_overview_section(readme_structure, repo_analysis)
            elif section_name == 'quick_start':
                return self._generate_quick_start_section(readme_structure, repo_analysis)
            elif section_name == 'installation':
                return self._generate_installation_section(readme_structure)
            elif section_name == 'usage':
                return self._generate_usage_section(readme_structure)
            elif section_name == 'architecture':
                return self._generate_architecture_section(readme_structure)
            elif section_name == 'api_documentation':
                return self._generate_api_section(readme_structure)
            elif section_name == 'development':
                return self._generate_development_section(readme_structure)
            elif section_name == 'deployment':
                return self._generate_deployment_section(readme_structure)
            elif section_name == 'contributing':
                return self._generate_contributing_section(readme_structure)
            elif section_name == 'license':
                return self._generate_license_section(readme_structure)
            else:
                return None
                
        except Exception as e:
            logger.error(f"❌ Failed to generate section {section_name}: {e}")
            return None
    
    def _generate_overview_section(self, readme_structure: Dict, repo_analysis: Dict) -> str:
        """Generate overview section"""
        project_overview = readme_structure.get('project_overview', {})
        technical_stack = readme_structure.get('technical_stack', {})
        features = readme_structure.get('features', {})
        
        content = ["## 🎯 Overview"]
        
        # Project description
        description = project_overview.get('description', '')
        if description:
            content.append(description)
        
        # Key features
        if isinstance(features, dict):
            core_features = features.get('core_features', [])
        else:
            core_features = features if isinstance(features, list) else []
        
        if core_features:
            content.append("### ✨ Key Features")
            for feature in core_features[:6]:  # Limit to 6 features
                enhanced_feature = self._enhance_feature_description(feature)
                content.append(f"- {enhanced_feature}")
        
        # Tech stack highlight
        primary_language = technical_stack.get('primary_language')
        frameworks = technical_stack.get('frameworks', [])
        
        if primary_language or frameworks:
            content.append("### 🛠️ Built With")
            if primary_language:
                content.append(f"- **{primary_language}** - Primary programming language")
            for framework in frameworks[:3]:
                content.append(f"- **{framework}** - Framework/Library")
        
        return '\n\n'.join(content)
    
    def _generate_quick_start_section(self, readme_structure: Dict, repo_analysis: Dict) -> str:
        """Generate quick start section"""
        installation = readme_structure.get('installation', {})
        usage = readme_structure.get('usage', {})
        
        content = ["## 🚀 Quick Start"]
        
        # Prerequisites
        prerequisites = installation.get('prerequisites', [])
        if prerequisites:
            content.append("### Prerequisites")
            for prereq in prerequisites:
                content.append(f"- {prereq}")
        
        # Quick installation
        install_steps = installation.get('installation_steps', [])
        if install_steps:
            content.append("### Installation")
            content.append("```bash")
            for step in install_steps[:3]:  # First 3 steps for quick start
                if 'clone' in step.lower():
                    content.append("git clone <repository-url>")
                elif 'install' in step.lower():
                    content.append("npm install  # or pip install -r requirements.txt")
                elif 'run' in step.lower() or 'start' in step.lower():
                    content.append("npm start    # or python app.py")
                else:
                    content.append(f"# {step}")
            content.append("```")
        
        # Quick usage
        quick_start = usage.get('quick_start', [])
        if quick_start:
            content.append("### Usage")
            for step in quick_start[:2]:  # First 2 usage steps
                content.append(f"1. {step}")
        
        return '\n\n'.join(content)
    
    def _generate_installation_section(self, readme_structure: Dict) -> str:
        """Generate detailed installation section"""
        installation = readme_structure.get('installation', {})
        
        content = ["## 📦 Installation"]
        
        # System requirements
        requirements = installation.get('system_requirements', [])
        if requirements:
            content.append("### System Requirements")
            for req in requirements:
                content.append(f"- {req}")
        
        # Prerequisites
        prerequisites = installation.get('prerequisites', [])
        if prerequisites:
            content.append("### Prerequisites")
            for prereq in prerequisites:
                content.append(f"- {prereq}")
        
        # Installation steps
        steps = installation.get('installation_steps', [])
        if steps:
            content.append("### Installation Steps")
            for i, step in enumerate(steps, 1):
                content.append(f"{i}. {step}")
        
        # Configuration
        config = installation.get('configuration', [])
        if config:
            content.append("### Configuration")
            for conf in config:
                content.append(f"- {conf}")
        
        # Verification
        verification = installation.get('verification', [])
        if verification:
            content.append("### Verify Installation")
            for verify in verification:
                content.append(f"- {verify}")
        
        return '\n\n'.join(content)
    
    def _generate_usage_section(self, readme_structure: Dict) -> str:
        """Generate usage section"""
        usage = readme_structure.get('usage', {})
        
        content = ["## 💻 Usage"]
        
        # Quick start
        quick_start = usage.get('quick_start', [])
        if quick_start:
            content.append("### Quick Start")
            for step in quick_start:
                content.append(f"- {step}")
        
        # Common commands
        commands = usage.get('common_commands', [])
        if commands:
            content.append("### Common Commands")
            content.append("```bash")
            for cmd in commands:
                content.append(cmd)
            content.append("```")
        
        # Examples
        examples = usage.get('examples', [])
        if examples:
            content.append("### Examples")
            for example in examples:
                content.append(f"- {example}")
        
        # Configuration options
        config_options = usage.get('configuration_options', [])
        if config_options:
            content.append("### Configuration Options")
            for option in config_options:
                content.append(f"- {option}")
        
        return '\n\n'.join(content)
    
    def _generate_architecture_section(self, readme_structure: Dict) -> str:
        """Generate architecture section"""
        architecture = readme_structure.get('architecture', {})
        
        content = ["## 🏗️ Architecture"]
        
        # Overview
        overview = architecture.get('overview', '')
        if overview:
            content.append(overview)
        
        # Patterns
        patterns = architecture.get('patterns', [])
        if patterns:
            content.append("### Architecture Patterns")
            for pattern in patterns:
                content.append(f"- **{pattern}**")
        
        # Directory structure
        dir_structure = architecture.get('directory_structure', '')
        if dir_structure:
            content.append("### Project Structure")
            content.append("```")
            content.append(dir_structure)
            content.append("```")
        
        # Data flow
        data_flow = architecture.get('data_flow', '')
        if data_flow:
            content.append("### Data Flow")
            content.append(data_flow)
        
        return '\n\n'.join(content)
    
    def _generate_api_section(self, readme_structure: Dict) -> str:
        """Generate API documentation section"""
        api_docs = readme_structure.get('api_documentation', {})
        
        if not api_docs or api_docs.get('base_url') == 'Not specified in code analysis':
            return None
        
        content = ["## 📚 API Documentation"]
        
        # Base URL
        base_url = api_docs.get('base_url', '')
        if base_url:
            content.append(f"**Base URL:** `{base_url}`")
        
        # Authentication
        auth = api_docs.get('authentication', '')
        if auth and auth != 'Not specified in code analysis':
            content.append(f"**Authentication:** {auth}")
        
        # Endpoints
        endpoints = api_docs.get('endpoints', [])
        if endpoints and endpoints != ['Not specified in code analysis']:
            content.append("### Endpoints")
            for endpoint in endpoints:
                content.append(f"- `{endpoint}`")
        
        return '\n\n'.join(content)
    
    def _generate_development_section(self, readme_structure: Dict) -> str:
        """Generate development section"""
        development = readme_structure.get('development', {})
        
        content = ["## 🛠️ Development"]
        
        # Setup
        setup = development.get('setup', [])
        if setup:
            content.append("### Development Setup")
            for step in setup:
                content.append(f"1. {step}")
        
        # Testing
        testing = development.get('testing', [])
        if testing and testing != ['Not specified in code analysis']:
            content.append("### Testing")
            for test in testing:
                content.append(f"- {test}")
        
        # Debugging
        debugging = development.get('debugging', [])
        if debugging:
            content.append("### Debugging")
            for debug in debugging:
                content.append(f"- {debug}")
        
        return '\n\n'.join(content)
    
    def _generate_deployment_section(self, readme_structure: Dict) -> str:
        """Generate deployment section"""
        deployment = readme_structure.get('deployment', {})
        
        content = ["## 🚀 Deployment"]
        
        # Environments
        environments = deployment.get('environments', [])
        if environments:
            content.append("### Supported Environments")
            for env in environments:
                content.append(f"- {env}")
        
        # Deployment methods
        methods = deployment.get('deployment_methods', [])
        if methods:
            content.append("### Deployment Methods")
            for method in methods:
                content.append(f"- {method}")
        
        # Environment variables
        env_vars = deployment.get('environment_variables', [])
        if env_vars and env_vars != ['Not specified in code analysis']:
            content.append("### Environment Variables")
            for var in env_vars:
                content.append(f"- `{var}`")
        
        return '\n\n'.join(content)
    
    def _generate_contributing_section(self, readme_structure: Dict) -> str:
        """Generate contributing section"""
        contributing = readme_structure.get('contributing', {})
        
        content = ["## 🤝 Contributing"]
        
        content.append("We welcome contributions! Please follow these steps:")
        
        # Guidelines
        guidelines = contributing.get('guidelines', [])
        if guidelines and guidelines != ['Not specified in code analysis']:
            content.append("### Guidelines")
            for guideline in guidelines:
                content.append(f"- {guideline}")
        
        # Standard contribution process
        content.append("### How to Contribute")
        content.append("1. Fork the repository")
        content.append("2. Create a feature branch (`git checkout -b feature/amazing-feature`)")
        content.append("3. Commit your changes (`git commit -m 'Add amazing feature'`)")
        content.append("4. Push to the branch (`git push origin feature/amazing-feature`)")
        content.append("5. Open a Pull Request")
        
        return '\n\n'.join(content)
    
    def _generate_license_section(self, readme_structure: Dict) -> str:
        """Generate license section"""
        license_info = readme_structure.get('license_info', {})
        
        content = ["## 📄 License"]
        
        license_type = license_info.get('license_type', 'Not specified')
        if license_type and license_type != 'Not specified in code analysis':
            content.append(f"This project is licensed under the {license_type} License.")
            
            license_file = license_info.get('license_file', 'LICENSE')
            if license_file:
                content.append(f"See the [{license_file}]({license_file}) file for details.")
        else:
            content.append("License information not specified. Please check the repository for license details.")
        
        return '\n\n'.join(content)
    
    def _generate_footer(self, readme_structure: Dict, repo_analysis: Dict) -> str:
        """Generate README footer"""
        generation_metadata = readme_structure.get('generation_metadata', {})
        
        footer_parts = ["---"]
        
        # Generation info
        model_used = generation_metadata.get('model_used', 'AI')
        footer_parts.append(f"*Generated with ❤️ by {model_used}*")
        
        # Timestamp
        generated_at = generation_metadata.get('generated_at', '')
        if generated_at:
            try:
                # Parse and format timestamp
                dt = datetime.fromisoformat(generated_at.replace('Z', '+00:00'))
                formatted_date = dt.strftime('%B %d, %Y')
                footer_parts.append(f"*Last updated: {formatted_date}*")
            except:
                pass
        
        return '\n\n'.join(footer_parts)
    
    def _post_process_readme(self, content: str) -> str:
        """Post-process README for quality improvements and fix encoding"""
        # Fix Unicode encoding issues first
        try:
            content = content.encode('utf-8').decode('utf-8')
        except:
            pass
        
        # Fix broken emoji encoding with safe replacements
        # Remove problematic Unicode characters and replace with proper emojis
        content = re.sub(r'ð[^a-zA-Z0-9\s]{1,3}', '', content)  # Remove broken emoji sequences
        content = re.sub(r'â[^a-zA-Z0-9\s]{1,3}', '', content)   # Remove broken special chars
        
        # Ensure proper emojis are in place for key sections
        content = re.sub(r'## Table of Contents', '## 📋 Table of Contents', content)
        content = re.sub(r'## Overview', '## 🎯 Overview', content)
        content = re.sub(r'## Quick Start', '## 🚀 Quick Start', content)
        content = re.sub(r'## Installation', '## 📦 Installation', content)
        content = re.sub(r'## Usage', '## 💻 Usage', content)
        content = re.sub(r'## Architecture', '## 🏗️ Architecture', content)
        content = re.sub(r'## API Documentation', '## 📚 API Documentation', content)
        content = re.sub(r'## Development', '## 🛠️ Development', content)
        content = re.sub(r'## Deployment', '## 🚀 Deployment', content)
        content = re.sub(r'## Contributing', '## 🤝 Contributing', content)
        content = re.sub(r'## License', '## 📄 License', content)
        
        # Fix multiple consecutive newlines
        content = re.sub(r'\n{4,}', '\n\n\n', content)
        
        # Ensure proper spacing around headers
        content = re.sub(r'\n(#{1,6}\s)', r'\n\n\1', content)
        
        # Fix list formatting
        content = re.sub(r'\n-\s', r'\n- ', content)
        content = re.sub(r'\n\d+\.\s', lambda m: f'\n{m.group().strip()} ', content)
        
        # Clean up extra spaces
        content = re.sub(r' +', ' ', content)
        
        return content.strip()
    
    def _enhance_feature_description(self, feature: str) -> str:
        """Enhance feature descriptions with more engaging language"""
        feature_lower = feature.lower()
        
        # Enhanced feature descriptions
        if 'authentication' in feature_lower or 'auth' in feature_lower:
            return '🔐 **Secure Authentication** - Enterprise-grade user authentication system'
        elif 'jwt' in feature_lower:
            return '🎫 **JWT Tokens** - Stateless authentication with JSON Web Tokens'
        elif 'api' in feature_lower:
            return '🌐 **RESTful API** - Comprehensive API endpoints for seamless integration'
        elif 'database' in feature_lower:
            return '💾 **Database Integration** - Robust data persistence and management'
        elif 'testing' in feature_lower:
            return '🧪 **Testing Suite** - Comprehensive test coverage for reliability'
        elif 'authorization' in feature_lower:
            return '🛡️ **Role-Based Access** - Granular permission control system'
        else:
            return f'🚀 **{feature}** - Advanced functionality for enhanced user experience'
    
    def _generate_fallback_readme(self, json_data: Dict[str, Any]) -> str:
        """Generate fallback README when main generation fails"""
        repo_analysis = json_data.get('repository_analysis', {})
        
        project_name = repo_analysis.get('repository_url', 'Project').split('/')[-1] if repo_analysis.get('repository_url') else 'Project'
        project_type = repo_analysis.get('project_type', 'Software Application')
        primary_language = repo_analysis.get('primary_language', 'Unknown')
        
        return f"""# {project_name}

> A {project_type} built with {primary_language}

## Overview

This project is a {project_type} that provides core functionality for users and developers.

## Installation

1. Clone the repository
2. Install dependencies
3. Run the application

## Usage

Follow the installation steps and refer to the documentation for usage instructions.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

Please check the repository for license information.

---

*Generated by Smart README Generator*
"""
    
    def _get_sections_for_style(self, style: str) -> List[str]:
        """Get sections list for specific style"""
        if style == 'developer':
            return ['overview', 'quick_start', 'installation', 'usage', 'architecture', 
                   'api_documentation', 'development', 'deployment', 'contributing', 'license']
        elif style == 'user':
            return ['overview', 'installation', 'usage', 'contributing', 'license']
        elif style == 'enterprise':
            return ['overview', 'architecture', 'installation', 'deployment', 
                   'api_documentation', 'development', 'contributing', 'license']
        else:
            return ['overview', 'installation', 'usage', 'contributing', 'license']
    
    def _get_developer_templates(self) -> Dict[str, str]:
        """Get developer-focused templates"""
        return {
            'header_style': 'comprehensive',
            'code_examples': 'detailed',
            'technical_depth': 'high'
        }
    
    def _get_user_templates(self) -> Dict[str, str]:
        """Get user-focused templates"""
        return {
            'header_style': 'simple',
            'code_examples': 'basic',
            'technical_depth': 'low'
        }
    
    def _get_enterprise_templates(self) -> Dict[str, str]:
        """Get enterprise-focused templates"""
        return {
            'header_style': 'professional',
            'code_examples': 'comprehensive',
            'technical_depth': 'high'
        }
