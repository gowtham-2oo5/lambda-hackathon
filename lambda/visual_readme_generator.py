"""
Dynamic Visual README Generator with Proper Emojis and Eye-Catching Styling
Uses Claude Sonnet 4 for dynamic content enhancement
"""

import re
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class DynamicVisualREADMEGenerator:
    """
    Dynamic README generator with proper emojis, stunning visuals, and Claude-powered enhancements
    """
    
    def __init__(self):
        # PROPER EMOJI MAP - Real Unicode emojis, not codes!
        self.emojis = {
            # Core sections
            'overview': '🎯',
            'features': '✨', 
            'quick_start': '🚀',
            'installation': '📦',
            'usage': '💻',
            'tech_stack': '🛠️',
            'architecture': '🏗️',
            'api': '📚',
            'development': '🔧',
            'deployment': '🌐',
            'contributing': '🤝',
            'license': '📄',
            'toc': '📋',
            
            # Technology specific
            'javascript': '🟨',
            'typescript': '🔷',
            'python': '🐍',
            'react': '⚛️',
            'nextjs': '▲',
            'django': '🎸',
            'express': '🚂',
            'database': '🗄️',
            'api_endpoint': '🔗',
            'security': '🔐',
            'auth': '🛡️',
            'jwt': '🎫',
            'admin': '👑',
            'dashboard': '📊',
            'ui': '🎨',
            'mobile': '📱',
            'web': '🌍',
            'cloud': '☁️',
            'docker': '🐳',
            'testing': '🧪',
            'performance': '⚡',
            'monitoring': '📈',
            
            # Status & Actions
            'success': '✅',
            'warning': '⚠️',
            'error': '❌',
            'info': 'ℹ️',
            'star': '⭐',
            'fire': '🔥',
            'gem': '💎',
            'trophy': '🏆',
            'rocket': '🚀',
            'magic': '✨',
            'heart': '❤️',
            'thumbs_up': '👍',
            'party': '🎉',
            'target': '🎯',
            'lightning': '⚡',
            'sparkles': '✨',
            'gear': '⚙️',
            'package': '📦',
            'terminal': '💻',
            'docs': '📖',
            'code': '💻'
        }
        
        # Dynamic badge system
        self.badge_templates = {
            'language': 'https://img.shields.io/badge/{name}-{color}?style=for-the-badge&logo={logo}&logoColor=white',
            'framework': 'https://img.shields.io/badge/{name}-{color}?style=for-the-badge&logo={logo}&logoColor=white',
            'status': 'https://img.shields.io/badge/{name}-{status}-{color}?style=for-the-badge',
            'custom': 'https://img.shields.io/badge/{name}-{value}-{color}?style=for-the-badge&logo={logo}'
        }
        
        # Color schemes for different project types
        self.color_schemes = {
            'web_application': {'primary': '#4CAF50', 'secondary': '#2196F3', 'accent': '#FF9800'},
            'api_service': {'primary': '#2196F3', 'secondary': '#00BCD4', 'accent': '#4CAF50'},
            'admin_dashboard': {'primary': '#9C27B0', 'secondary': '#673AB7', 'accent': '#3F51B5'},
            'mobile_app': {'primary': '#FF5722', 'secondary': '#FF9800', 'accent': '#FFC107'},
            'library': {'primary': '#607D8B', 'secondary': '#795548', 'accent': '#8BC34A'}
        }
    
    def generate_stunning_readme(self, json_data: Dict[str, Any]) -> str:
        """Generate a visually stunning, dynamic README"""
        logger.info(f"{self.emojis['rocket']} Generating dynamic visual README")
        
        try:
            repo_analysis = json_data.get('repository_analysis', {})
            readme_structure = json_data.get('readme_structure', {})
            
            # Determine project context for dynamic styling
            project_context = self._analyze_project_context(repo_analysis, readme_structure)
            
            sections = []
            
            # Generate sections only if they have content
            header = self._generate_dynamic_header(readme_structure, repo_analysis, project_context)
            if header: sections.append(header)
            
            toc = self._generate_dynamic_toc(readme_structure, project_context)
            if toc: sections.append(toc)
            
            overview = self._generate_dynamic_overview(readme_structure, repo_analysis, project_context)
            if overview: sections.append(overview)
            
            features = self._generate_dynamic_features(readme_structure, project_context)
            if features: sections.append(features)
            
            quick_start = self._generate_dynamic_quick_start(readme_structure, project_context)
            if quick_start: sections.append(quick_start)
            
            installation = self._generate_dynamic_installation(readme_structure, project_context)
            if installation: sections.append(installation)
            
            usage = self._generate_dynamic_usage(readme_structure, project_context)
            if usage: sections.append(usage)
            
            tech_stack = self._generate_dynamic_tech_stack(readme_structure, repo_analysis, project_context)
            if tech_stack: sections.append(tech_stack)
            
            api_docs = self._generate_dynamic_api_docs(readme_structure, project_context)
            if api_docs: sections.append(api_docs)
            
            contributing = self._generate_dynamic_contributing(readme_structure, project_context)
            if contributing: sections.append(contributing)
            
            footer = self._generate_dynamic_footer(readme_structure, repo_analysis, project_context)
            if footer: sections.append(footer)
            
            # Combine with beautiful spacing
            readme_content = '\n\n'.join(sections)
            
            # Apply final visual polish
            readme_content = self._apply_visual_enhancements(readme_content, project_context)
            
            logger.info(f"{self.emojis['success']} Dynamic README generated ({len(readme_content)} chars)")
            return readme_content
            
        except Exception as e:
            logger.error(f"{self.emojis['error']} Dynamic README generation failed: {e}")
            return self._generate_minimal_fallback(json_data)
    
    def _analyze_project_context(self, repo_analysis: Dict, readme_structure: Dict) -> Dict:
        """Analyze project to determine dynamic styling context"""
        project_type = repo_analysis.get('project_type', '').lower()
        primary_language = repo_analysis.get('primary_language', '').lower()
        frameworks = [f.lower() for f in repo_analysis.get('frameworks', [])]
        
        context = {
            'project_type': project_type,
            'primary_language': primary_language,
            'frameworks': frameworks,
            'is_web_app': 'web' in project_type or 'react' in frameworks or 'next' in str(frameworks),
            'is_api': 'api' in project_type or 'express' in frameworks or 'django' in frameworks,
            'is_admin': 'admin' in project_type or 'dashboard' in project_type,
            'is_mobile': 'mobile' in project_type or 'react native' in str(frameworks),
            'has_auth': any('auth' in str(f) for f in repo_analysis.get('features', [])),
            'has_database': any('database' in str(f).lower() for f in repo_analysis.get('features', [])),
            'complexity': self._assess_visual_complexity(repo_analysis)
        }
        
        # Determine color scheme
        if context['is_admin']:
            context['color_scheme'] = self.color_schemes['admin_dashboard']
        elif context['is_api']:
            context['color_scheme'] = self.color_schemes['api_service']
        elif context['is_mobile']:
            context['color_scheme'] = self.color_schemes['mobile_app']
        else:
            context['color_scheme'] = self.color_schemes['web_application']
        
        return context
    
    def _generate_dynamic_header(self, readme_structure: Dict, repo_analysis: Dict, context: Dict) -> str:
        """Generate dynamic header with context-aware styling"""
        project_overview = readme_structure.get('project_overview', {})
        if not project_overview:
            return ""
        
        title = project_overview.get('name', '').strip()
        description = project_overview.get('description', '').strip()
        
        if not title:
            return ""
        
        # Dynamic emoji selection based on project type
        title_emoji = self._get_dynamic_emoji_for_project(context)
        
        header_parts = [
            '<div align="center">',
            '',
            f'# {title_emoji} {title} {title_emoji}',
            ''
        ]
        
        if description:
            header_parts.extend([
                f'### {self.emojis["sparkles"]} *{description}* {self.emojis["sparkles"]}',
                ''
            ])
        
        # Dynamic badges
        badges = self._generate_dynamic_badges(repo_analysis, context)
        if badges:
            header_parts.extend([
                badges,
                '',
                '---',
                ''
            ])
        
        # Project stats if meaningful
        stats = self._generate_dynamic_stats(repo_analysis, context)
        if stats:
            header_parts.extend([
                stats,
                ''
            ])
        
        header_parts.extend(['---', '</div>'])
        
        return '\n'.join(header_parts)
    
    def _get_dynamic_emoji_for_project(self, context: Dict) -> str:
        """Get appropriate emoji based on project context"""
        if context['is_admin']:
            return self.emojis['admin']
        elif context['is_api']:
            return self.emojis['api_endpoint']
        elif context['is_mobile']:
            return self.emojis['mobile']
        elif context['is_web_app']:
            return self.emojis['web']
        elif 'python' in context['primary_language']:
            return self.emojis['python']
        elif 'typescript' in context['primary_language']:
            return self.emojis['typescript']
        elif 'javascript' in context['primary_language']:
            return self.emojis['javascript']
        else:
            return self.emojis['rocket']
    
    def _generate_dynamic_badges(self, repo_analysis: Dict, context: Dict) -> str:
        """Generate context-aware badges"""
        badges = []
        
        # Language badge
        primary_language = repo_analysis.get('primary_language', '')
        if primary_language:
            lang_config = self._get_language_badge_config(primary_language)
            if lang_config:
                badges.append(f"![{primary_language}]({lang_config})")
        
        # Framework badges
        frameworks = repo_analysis.get('frameworks', [])
        for framework in frameworks[:2]:  # Limit to 2
            framework_config = self._get_framework_badge_config(framework)
            if framework_config:
                badges.append(f"![{framework}]({framework_config})")
        
        # Dynamic status badges based on context
        if context['has_auth']:
            badges.append('![Security](https://img.shields.io/badge/Security-Enterprise-brightgreen?style=for-the-badge&logo=shield)')
        
        if context['complexity'] == 'high':
            badges.append('![Complexity](https://img.shields.io/badge/Complexity-Advanced-orange?style=for-the-badge)')
        
        # Standard badges
        badges.extend([
            '![Build](https://img.shields.io/badge/Build-Passing-brightgreen?style=for-the-badge&logo=github-actions)',
            '![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)',
            '![PRs](https://img.shields.io/badge/PRs-Welcome-brightgreen?style=for-the-badge&logo=github)'
        ])
        
        return ' '.join(badges)
    
    def _generate_dynamic_overview(self, readme_structure: Dict, repo_analysis: Dict, context: Dict) -> str:
        """Generate dynamic overview section"""
        project_overview = readme_structure.get('project_overview', {})
        if not project_overview:
            return ""
        
        description = project_overview.get('description', '').strip()
        purpose = project_overview.get('primary_purpose', '').strip()
        
        if not description and not purpose:
            return ""
        
        overview_parts = [
            f'## {self.emojis["overview"]} Overview',
            ''
        ]
        
        # Dynamic intro based on project type
        if context['is_admin']:
            overview_parts.append(f'{self.emojis["admin"]} **Administrative Excellence at Your Fingertips**')
        elif context['is_api']:
            overview_parts.append(f'{self.emojis["api"]} **Powerful API Solution for Modern Applications**')
        elif context['is_web_app']:
            overview_parts.append(f'{self.emojis["web"]} **Next-Generation Web Application**')
        else:
            overview_parts.append(f'{self.emojis["rocket"]} **Innovative Software Solution**')
        
        overview_parts.append('')
        
        if description:
            overview_parts.extend([
                f'{description}',
                ''
            ])
        
        if purpose:
            overview_parts.extend([
                f'> {self.emojis["target"]} **Purpose:** {purpose}',
                ''
            ])
        
        # Add dynamic highlights
        target_audience = project_overview.get('target_audience', '').strip()
        if target_audience:
            overview_parts.extend([
                f'> {self.emojis["star"]} **Built for:** {target_audience}',
                ''
            ])
        
        return '\n'.join(overview_parts)
    
    def _generate_dynamic_features(self, readme_structure: Dict, context: Dict) -> str:
        """Generate dynamic features section with visual enhancements"""
        features = readme_structure.get('features', {})
        if not features:
            return ""
        
        # Extract features based on structure
        if isinstance(features, dict):
            core_features = features.get('core_features', [])
            auth_features = features.get('authentication_features', [])
            api_features = features.get('api_features', [])
        else:
            core_features = features if isinstance(features, list) else []
            auth_features = []
            api_features = []
        
        if not core_features and not auth_features and not api_features:
            return ""
        
        features_parts = [
            f'## {self.emojis["features"]} Features',
            '',
            '<div align="center">',
            f'{self.emojis["fire"]} **Packed with Amazing Capabilities** {self.emojis["fire"]}',
            '</div>',
            ''
        ]
        
        # Core features with dynamic enhancement
        if core_features:
            features_parts.extend([
                f'### {self.emojis["star"]} Core Features',
                ''
            ])
            
            for feature in core_features[:6]:
                enhanced = self._enhance_feature_dynamically(feature, context)
                features_parts.append(f'- {enhanced}')
            
            features_parts.append('')
        
        # Authentication features if present
        if auth_features and context['has_auth']:
            features_parts.extend([
                f'### {self.emojis["security"]} Security & Authentication',
                ''
            ])
            
            for feature in auth_features[:4]:
                features_parts.append(f'- {self.emojis["auth"]} **{feature}**')
            
            features_parts.append('')
        
        # API features if present
        if api_features and context['is_api']:
            features_parts.extend([
                f'### {self.emojis["api"]} API Capabilities',
                ''
            ])
            
            for feature in api_features[:4]:
                features_parts.append(f'- {self.emojis["api_endpoint"]} **{feature}**')
            
            features_parts.append('')
        
        return '\n'.join(features_parts)
    
    def _enhance_feature_dynamically(self, feature: str, context: Dict) -> str:
        """Dynamically enhance feature descriptions based on context"""
        feature_lower = feature.lower()
        
        # Context-aware feature enhancement
        if 'auth' in feature_lower:
            return f'{self.emojis["security"]} **Secure Authentication** - Enterprise-grade security system'
        elif 'jwt' in feature_lower:
            return f'{self.emojis["jwt"]} **JWT Integration** - Stateless token-based authentication'
        elif 'api' in feature_lower:
            return f'{self.emojis["api_endpoint"]} **RESTful API** - Comprehensive endpoint architecture'
        elif 'dashboard' in feature_lower or 'admin' in feature_lower:
            return f'{self.emojis["dashboard"]} **Admin Dashboard** - Powerful management interface'
        elif 'database' in feature_lower:
            return f'{self.emojis["database"]} **Database Integration** - Robust data management'
        elif 'ui' in feature_lower or 'interface' in feature_lower:
            return f'{self.emojis["ui"]} **Modern UI** - Beautiful, responsive design'
        elif 'test' in feature_lower:
            return f'{self.emojis["testing"]} **Testing Suite** - Comprehensive quality assurance'
        elif 'performance' in feature_lower:
            return f'{self.emojis["performance"]} **High Performance** - Optimized for speed'
        elif 'monitoring' in feature_lower:
            return f'{self.emojis["monitoring"]} **Monitoring** - Real-time system insights'
        else:
            # Dynamic emoji selection based on context
            if context['is_admin']:
                emoji = self.emojis['admin']
            elif context['is_api']:
                emoji = self.emojis['api_endpoint']
            else:
                emoji = self.emojis['star']
            
            return f'{emoji} **{feature}** - Advanced functionality for enhanced experience'
    
    def _generate_dynamic_toc(self, readme_structure: Dict, context: Dict) -> str:
        """Generate dynamic table of contents based on available sections"""
        available_sections = []
        
        # Check which sections have content
        if readme_structure.get('project_overview'):
            available_sections.append(f'- [{self.emojis["overview"]} **Overview**](#-overview)')
        
        if readme_structure.get('features'):
            available_sections.append(f'- [{self.emojis["features"]} **Features**](#-features)')
        
        if readme_structure.get('installation'):
            available_sections.append(f'- [{self.emojis["installation"]} **Installation**](#-installation)')
        
        if readme_structure.get('usage'):
            available_sections.append(f'- [{self.emojis["usage"]} **Usage**](#-usage)')
        
        # Always include tech stack if we have repo analysis
        available_sections.append(f'- [{self.emojis["tech_stack"]} **Tech Stack**](#-tech-stack)')
        
        if readme_structure.get('api_documentation', {}).get('endpoints'):
            available_sections.append(f'- [{self.emojis["api"]} **API Documentation**](#-api-documentation)')
        
        # Always include contributing
        available_sections.append(f'- [{self.emojis["contributing"]} **Contributing**](#-contributing)')
        
        if not available_sections:
            return ""
        
        toc_parts = [
            f'## {self.emojis["toc"]} Table of Contents',
            '',
            '<details>',
            '<summary>📖 Click to expand navigation</summary>',
            '',
            *available_sections,
            '',
            '</details>'
        ]
        
        return '\n'.join(toc_parts)
    
    def _generate_dynamic_installation(self, readme_structure: Dict, context: Dict) -> str:
        """Generate installation section only if content exists"""
        installation = readme_structure.get('installation', {})
        if not installation:
            return ""
        
        steps = installation.get('installation_steps', [])
        prerequisites = installation.get('prerequisites', [])
        
        if not steps and not prerequisites:
            return ""
        
        install_parts = [
            f'## {self.emojis["installation"]} Installation',
            '',
            f'{self.emojis["rocket"]} **Get started in minutes!**',
            ''
        ]
        
        if prerequisites:
            install_parts.extend([
                f'### {self.emojis["warning"]} Prerequisites',
                ''
            ])
            for prereq in prerequisites:
                install_parts.append(f'- {prereq}')
            install_parts.append('')
        
        if steps:
            install_parts.extend([
                f'### {self.emojis["gear"]} Installation Steps',
                ''
            ])
            for i, step in enumerate(steps, 1):
                install_parts.append(f'**{i}.** {step}')
            install_parts.append('')
        
        return '\n'.join(install_parts)
    
    def _generate_dynamic_usage(self, readme_structure: Dict, context: Dict) -> str:
        """Generate usage section only if content exists"""
        usage = readme_structure.get('usage', {})
        if not usage:
            return ""
        
        quick_start = usage.get('quick_start', [])
        examples = usage.get('examples', [])
        commands = usage.get('common_commands', [])
        
        if not quick_start and not examples and not commands:
            return ""
        
        usage_parts = [
            f'## {self.emojis["usage"]} Usage',
            '',
            f'{self.emojis["lightning"]} **Ready to use right out of the box!**',
            ''
        ]
        
        if quick_start:
            usage_parts.extend([
                f'### {self.emojis["rocket"]} Quick Start',
                ''
            ])
            for step in quick_start:
                usage_parts.append(f'1. {step}')
            usage_parts.append('')
        
        if commands:
            usage_parts.extend([
                f'### {self.emojis["terminal"]} Common Commands',
                '',
                '```bash'
            ])
            for cmd in commands:
                usage_parts.append(cmd)
            usage_parts.extend(['```', ''])
        
        if examples:
            usage_parts.extend([
                f'### {self.emojis["star"]} Examples',
                ''
            ])
            for example in examples:
                usage_parts.append(f'- {example}')
            usage_parts.append('')
        
        return '\n'.join(usage_parts)
    
    def _generate_dynamic_quick_start(self, readme_structure: Dict, context: Dict) -> str:
        """Generate quick start section only if content exists"""
        usage = readme_structure.get('usage', {})
        installation = readme_structure.get('installation', {})
        
        quick_start_steps = usage.get('quick_start', [])
        install_steps = installation.get('installation_steps', [])
        
        if not quick_start_steps and not install_steps:
            return ""
        
        quick_parts = [
            f'## {self.emojis["quick_start"]} Quick Start',
            '',
            f'{self.emojis["lightning"]} **Get up and running in minutes!**',
            ''
        ]
        
        # Use installation steps if no quick start available
        steps_to_use = quick_start_steps if quick_start_steps else install_steps[:3]
        
        if steps_to_use:
            for i, step in enumerate(steps_to_use, 1):
                quick_parts.append(f'**{i}.** {step}')
            quick_parts.append('')
        
        return '\n'.join(quick_parts)
    
    def _generate_dynamic_tech_stack(self, readme_structure: Dict, repo_analysis: Dict, context: Dict) -> str:
        """Generate dynamic tech stack section"""
        tech_stack = readme_structure.get('technical_stack', {})
        primary_language = repo_analysis.get('primary_language', '')
        frameworks = repo_analysis.get('frameworks', [])
        
        if not primary_language and not frameworks and not tech_stack:
            return ""
        
        stack_parts = [
            f'## {self.emojis["tech_stack"]} Tech Stack',
            '',
            f'{self.emojis["fire"]} **Built with cutting-edge technology**',
            ''
        ]
        
        # Create visual tech stack
        if primary_language:
            lang_emoji = self._get_language_emoji(primary_language)
            stack_parts.append(f'### {lang_emoji} Core Technology')
            stack_parts.append(f'- **{primary_language}** - Primary programming language')
            stack_parts.append('')
        
        if frameworks:
            stack_parts.append(f'### {self.emojis["gear"]} Frameworks & Libraries')
            for framework in frameworks:
                framework_emoji = self._get_framework_emoji(framework)
                stack_parts.append(f'- {framework_emoji} **{framework}** - {self._get_framework_description(framework)}')
            stack_parts.append('')
        
        # Additional tech from analysis
        dependencies = tech_stack.get('dependencies', []) if tech_stack else []
        if dependencies:
            stack_parts.append(f'### {self.emojis["package"]} Key Dependencies')
            for dep in dependencies[:5]:  # Limit to 5
                stack_parts.append(f'- {self.emojis["star"]} {dep}')
            stack_parts.append('')
        
        return '\n'.join(stack_parts)
    
    def _generate_dynamic_api_docs(self, readme_structure: Dict, context: Dict) -> str:
        """Generate API documentation section only if content exists"""
        api_docs = readme_structure.get('api_documentation', {})
        if not api_docs or not context['is_api']:
            return ""
        
        endpoints = api_docs.get('endpoints', [])
        base_url = api_docs.get('base_url', '')
        
        if not endpoints and not base_url:
            return ""
        
        api_parts = [
            f'## {self.emojis["api"]} API Documentation',
            '',
            f'{self.emojis["web"]} **Comprehensive API for seamless integration**',
            ''
        ]
        
        if base_url and base_url != 'Not specified in code analysis':
            api_parts.extend([
                f'### {self.emojis["link"]} Base URL',
                f'```',
                base_url,
                f'```',
                ''
            ])
        
        if endpoints and endpoints != ['Not specified in code analysis']:
            api_parts.extend([
                f'### {self.emojis["api_endpoint"]} Available Endpoints',
                ''
            ])
            for endpoint in endpoints[:8]:  # Limit to 8
                api_parts.append(f'- `{endpoint}`')
            api_parts.append('')
        
        return '\n'.join(api_parts)
    
    def _generate_dynamic_contributing(self, readme_structure: Dict, context: Dict) -> str:
        """Generate contributing section"""
        contributing_parts = [
            f'## {self.emojis["contributing"]} Contributing',
            '',
            f'{self.emojis["heart"]} **We love contributions! Here\'s how you can help:**',
            '',
            f'### {self.emojis["rocket"]} Quick Start',
            '1. 🍴 Fork the repository',
            '2. 🌟 Create your feature branch (`git checkout -b feature/amazing-feature`)',
            '3. 💫 Commit your changes (`git commit -m \'Add amazing feature\'`)',
            '4. 🚀 Push to the branch (`git push origin feature/amazing-feature`)',
            '5. 🎉 Open a Pull Request',
            '',
            f'### {self.emojis["star"]} Guidelines',
            f'- {self.emojis["thumbs_up"]} Follow the existing code style',
            f'- {self.emojis["testing"]} Add tests for new features',
            f'- {self.emojis["docs"]} Update documentation as needed',
            f'- {self.emojis["heart"]} Be respectful and constructive',
            ''
        ]
        
        return '\n'.join(contributing_parts)
    
    def _generate_dynamic_footer(self, readme_structure: Dict, repo_analysis: Dict, context: Dict) -> str:
        """Generate dynamic footer"""
        footer_parts = [
            '---',
            '',
            '<div align="center">',
            '',
            f'### {self.emojis["heart"]} Made with Love & Code {self.emojis["heart"]}',
            '',
            f'{self.emojis["star"]} **Star this repo if you found it helpful!** {self.emojis["star"]}',
            '',
            f'{self.emojis["rocket"]} **Happy Coding!** {self.emojis["rocket"]}',
            '',
            '</div>',
            '',
            '---',
            '',
            f'<div align="center">',
            f'<sub>Generated with {self.emojis["magic"]} by Smart README Generator</sub>',
            f'</div>'
        ]
        
        return '\n'.join(footer_parts)
    
    # Helper methods
    def _get_language_emoji(self, language: str) -> str:
        """Get emoji for programming language"""
        lang_lower = language.lower()
        if 'javascript' in lang_lower:
            return self.emojis['javascript']
        elif 'typescript' in lang_lower:
            return self.emojis['typescript']
        elif 'python' in lang_lower:
            return self.emojis['python']
        else:
            return self.emojis['code']
    
    def _get_framework_emoji(self, framework: str) -> str:
        """Get emoji for framework"""
        framework_lower = framework.lower()
        if 'react' in framework_lower:
            return self.emojis['react']
        elif 'next' in framework_lower:
            return self.emojis['nextjs']
        elif 'django' in framework_lower:
            return self.emojis['django']
        elif 'express' in framework_lower:
            return self.emojis['express']
        else:
            return self.emojis['gear']
    
    def _get_framework_description(self, framework: str) -> str:
        """Get description for framework"""
        descriptions = {
            'React': 'Modern UI library for building interactive interfaces',
            'Next.js': 'Production-ready React framework with SSR',
            'Django': 'High-level Python web framework',
            'Express.js': 'Fast, unopinionated web framework for Node.js',
            'Spring Boot': 'Enterprise Java framework',
            'Flask': 'Lightweight Python web framework'
        }
        return descriptions.get(framework, 'Powerful development framework')
    
    def _get_language_badge_config(self, language: str) -> str:
        """Get badge configuration for language"""
        configs = {
            'JavaScript': 'https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black',
            'TypeScript': 'https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white',
            'Python': 'https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white'
        }
        return configs.get(language, '')
    
    def _get_framework_badge_config(self, framework: str) -> str:
        """Get badge configuration for framework"""
        configs = {
            'React': 'https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB',
            'Next.js': 'https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white',
            'Django': 'https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white',
            'Express.js': 'https://img.shields.io/badge/Express.js-404D59?style=for-the-badge'
        }
        return configs.get(framework, '')
    
    def _assess_visual_complexity(self, repo_analysis: Dict) -> str:
        """Assess project complexity for visual styling"""
        frameworks_count = len(repo_analysis.get('frameworks', []))
        features_count = len(repo_analysis.get('features', []))
        
        if frameworks_count >= 3 or features_count >= 8:
            return 'high'
        elif frameworks_count >= 2 or features_count >= 4:
            return 'medium'
        else:
            return 'low'
    
    def _apply_visual_enhancements(self, content: str, context: Dict) -> str:
        """Apply final visual enhancements"""
        # Ensure proper spacing
        content = re.sub(r'\n{4,}', '\n\n\n', content)
        
        # Fix any remaining formatting issues
        content = re.sub(r'\n(#{1,6}\s)', r'\n\n\1', content)
        
        return content.strip()
    
    def _generate_dynamic_stats(self, repo_analysis: Dict, context: Dict) -> str:
        """Generate dynamic project statistics"""
        stats_data = []
        
        primary_language = repo_analysis.get('primary_language')
        if primary_language:
            lang_emoji = self._get_language_emoji(primary_language)
            stats_data.append(f'**{lang_emoji} {primary_language}**')
        
        frameworks = repo_analysis.get('frameworks', [])
        if frameworks:
            framework_text = ' • '.join(frameworks[:2])
            stats_data.append(f'**{self.emojis["gear"]} {framework_text}**')
        
        security_score = repo_analysis.get('security_analysis', {}).get('security_score', 0)
        if security_score >= 90:
            stats_data.append(f'**{self.emojis["security"]} Secure**')
        
        if not stats_data:
            return ""
        
        return f'### {" • ".join(stats_data)}'
    
    def _generate_minimal_fallback(self, json_data: Dict) -> str:
        """Generate minimal fallback README"""
        repo_analysis = json_data.get('repository_analysis', {})
        project_name = repo_analysis.get('repository_url', 'Project').split('/')[-1] if repo_analysis.get('repository_url') else 'Project'
        
        return f"""# {self.emojis['rocket']} {project_name}

{self.emojis['star']} A software project built with modern technology.

## {self.emojis['installation']} Installation

1. Clone the repository
2. Install dependencies  
3. Run the application

## {self.emojis['contributing']} Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

<div align="center">
{self.emojis['heart']} Made with Love & Code {self.emojis['heart']}
</div>"""
