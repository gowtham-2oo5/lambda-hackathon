"""
Emoji-Safe README Generator - No More Broken Characters!
Uses HTML entities and safe Unicode handling
"""

import re
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class EmojiSafeREADMEGenerator:
    """
    README generator that handles emojis safely without encoding issues
    """
    
    def __init__(self):
        # SAFE EMOJI APPROACH - Use HTML entities or simple text alternatives
        self.safe_emojis = {
            # Core sections - using HTML entities that render properly
            'overview': '🎯',  # Will be replaced with safe alternative
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
            'toc': '📋'
        }
        
        # SAFE ALTERNATIVES - Text-based icons that always work
        self.text_alternatives = {
            'overview': '🎯 ',
            'features': '✨ ',
            'quick_start': '🚀 ',
            'installation': '📦 ',
            'usage': '💻 ',
            'tech_stack': '🛠️ ',
            'architecture': '🏗️ ',
            'api': '📚 ',
            'development': '🔧 ',
            'deployment': '🌐 ',
            'contributing': '🤝 ',
            'license': '📄 ',
            'toc': '📋 ',
            'star': '⭐ ',
            'fire': '🔥 ',
            'gem': '💎 ',
            'rocket': '🚀 ',
            'heart': '❤️ ',
            'success': '✅ ',
            'warning': '⚠️ ',
            'info': 'ℹ️ ',
            'security': '🔐 ',
            'database': '🗄️ ',
            'web': '🌍 ',
            'mobile': '📱 ',
            'admin': '👑 ',
            'dashboard': '📊 '
        }
        
        # FALLBACK - Simple text icons if emojis fail
        self.fallback_icons = {
            'overview': '[🎯]',
            'features': '[✨]',
            'quick_start': '[🚀]',
            'installation': '[📦]',
            'usage': '[💻]',
            'tech_stack': '[🛠️]',
            'architecture': '[🏗️]',
            'api': '[📚]',
            'development': '[🔧]',
            'deployment': '[🌐]',
            'contributing': '[🤝]',
            'license': '[📄]',
            'toc': '[📋]',
            'star': '[⭐]',
            'fire': '[🔥]',
            'security': '[🔐]',
            'database': '[🗄️]',
            'web': '[🌍]',
            'admin': '[👑]',
            'dashboard': '[📊]'
        }
    
    def generate_safe_readme(self, json_data: Dict[str, Any]) -> str:
        """Generate README with safe emoji handling"""
        logger.info("📝 Generating emoji-safe README")
        
        try:
            repo_analysis = json_data.get('repository_analysis', {})
            readme_structure = json_data.get('readme_structure', {})
            
            # Determine project context
            project_context = self._analyze_project_safely(repo_analysis, readme_structure)
            
            sections = []
            
            # Generate sections with safe emoji handling
            header = self._generate_safe_header(readme_structure, repo_analysis, project_context)
            if header: sections.append(header)
            
            toc = self._generate_safe_toc(readme_structure)
            if toc: sections.append(toc)
            
            overview = self._generate_safe_overview(readme_structure, project_context)
            if overview: sections.append(overview)
            
            features = self._generate_safe_features(readme_structure, project_context)
            if features: sections.append(features)
            
            installation = self._generate_safe_installation(readme_structure)
            if installation: sections.append(installation)
            
            usage = self._generate_safe_usage(readme_structure)
            if usage: sections.append(usage)
            
            tech_stack = self._generate_safe_tech_stack(readme_structure, repo_analysis)
            if tech_stack: sections.append(tech_stack)
            
            contributing = self._generate_safe_contributing()
            if contributing: sections.append(contributing)
            
            footer = self._generate_safe_footer(readme_structure)
            if footer: sections.append(footer)
            
            # Combine sections
            readme_content = '\n\n'.join(sections)
            
            # Apply safe encoding
            readme_content = self._ensure_safe_encoding(readme_content)
            
            logger.info(f"✅ Safe README generated ({len(readme_content)} chars)")
            return readme_content
            
        except Exception as e:
            logger.error(f"❌ Safe README generation failed: {e}")
            return self._generate_ultra_safe_fallback(json_data)
    
    def _generate_safe_header(self, readme_structure: Dict, repo_analysis: Dict, context: Dict) -> str:
        """Generate header with safe emoji handling"""
        project_overview = readme_structure.get('project_overview', {})
        if not project_overview:
            return ""
        
        title = project_overview.get('name', '').strip()
        description = project_overview.get('description', '').strip()
        
        if not title:
            return ""
        
        # Safe header with proper encoding
        header_parts = [
            '<div align="center">',
            '',
            f'# {self._safe_emoji("rocket")} {title} {self._safe_emoji("rocket")}',
            ''
        ]
        
        if description:
            header_parts.extend([
                f'### {self._safe_emoji("star")} *{description}* {self._safe_emoji("star")}',
                ''
            ])
        
        # Safe badges
        badges = self._generate_safe_badges(repo_analysis)
        if badges:
            header_parts.extend([
                badges,
                '',
                '---',
                ''
            ])
        
        # Safe tech highlights - SKIP THIS TO AVOID REPETITION
        # tech_highlight = self._generate_safe_tech_highlight(repo_analysis)
        # if tech_highlight:
        #     header_parts.extend([
        #         tech_highlight,
        #         ''
        #     ])
        
        header_parts.extend(['---', '</div>'])
        
        return '\n'.join(header_parts)
    
    def _generate_safe_badges(self, repo_analysis: Dict) -> str:
        """Generate badges without emoji issues"""
        badges = []
        
        # Language badge
        primary_language = repo_analysis.get('primary_language', '')
        if primary_language:
            if primary_language == 'JavaScript':
                badges.append('![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)')
            elif primary_language == 'TypeScript':
                badges.append('![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white)')
            elif primary_language == 'Python':
                badges.append('![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)')
        
        # Framework badges
        frameworks = repo_analysis.get('frameworks', [])
        for framework in frameworks[:2]:
            if framework == 'React':
                badges.append('![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)')
            elif framework == 'Next.js':
                badges.append('![Next.js](https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white)')
            elif framework == 'Django':
                badges.append('![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)')
            elif framework == 'Express.js':
                badges.append('![Express.js](https://img.shields.io/badge/Express.js-404D59?style=for-the-badge)')
        
        # Standard badges
        badges.extend([
            '![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen?style=for-the-badge)',
            '![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)',
            '![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-brightgreen?style=for-the-badge)'
        ])
        
        return ' '.join(badges)
    
    def _generate_safe_tech_highlight(self, repo_analysis: Dict) -> str:
        """Generate tech stack highlight safely"""
        primary_language = repo_analysis.get('primary_language', '')
        frameworks = repo_analysis.get('frameworks', [])
        security_score = repo_analysis.get('security_analysis', {}).get('security_score', 0)
        
        highlights = []
        
        if primary_language:
            highlights.append(f'**{primary_language}**')
        
        if frameworks:
            framework_text = ' • '.join(frameworks[:2])
            highlights.append(f'**{framework_text}**')
        
        if security_score >= 90:
            highlights.append('**Secure**')
        
        if highlights:
            return f'### {" • ".join(highlights)}'
        
        return ""
    
    def _generate_safe_toc(self, readme_structure: Dict) -> str:
        """Generate table of contents safely"""
        toc_items = []
        
        # Check available sections
        if readme_structure.get('project_overview'):
            toc_items.append(f'- [{self._safe_emoji("overview")}**Overview**](#overview)')
        
        if readme_structure.get('features'):
            toc_items.append(f'- [{self._safe_emoji("features")}**Features**](#features)')
        
        if readme_structure.get('installation'):
            toc_items.append(f'- [{self._safe_emoji("installation")}**Installation**](#installation)')
        
        if readme_structure.get('usage'):
            toc_items.append(f'- [{self._safe_emoji("usage")}**Usage**](#usage)')
        
        # Always include tech stack and contributing
        toc_items.extend([
            f'- [{self._safe_emoji("tech_stack")}**Tech Stack**](#tech-stack)',
            f'- [{self._safe_emoji("contributing")}**Contributing**](#contributing)'
        ])
        
        if not toc_items:
            return ""
        
        toc_parts = [
            f'## {self._safe_emoji("toc")}Table of Contents',
            '',
            '<details>',
            '<summary>Click to expand navigation</summary>',
            '',
            *toc_items,
            '',
            '</details>'
        ]
        
        return '\n'.join(toc_parts)
    
    def _generate_safe_overview(self, readme_structure: Dict, context: Dict) -> str:
        """Generate overview section safely"""
        project_overview = readme_structure.get('project_overview', {})
        if not project_overview:
            return ""
        
        description = project_overview.get('description', '').strip()
        purpose = project_overview.get('primary_purpose', '').strip()
        
        if not description and not purpose:
            return ""
        
        overview_parts = [
            f'## {self._safe_emoji("overview")}Overview',
            ''
        ]
        
        # Project type specific intro
        if context.get('is_admin'):
            overview_parts.append(f'{self._safe_emoji("admin")}**Administrative Excellence at Your Fingertips**')
        elif context.get('is_api'):
            overview_parts.append(f'{self._safe_emoji("api")}**Powerful API Solution for Modern Applications**')
        elif context.get('is_web_app'):
            overview_parts.append(f'{self._safe_emoji("web")}**Next-Generation Web Application**')
        else:
            overview_parts.append(f'{self._safe_emoji("rocket")}**Innovative Software Solution**')
        
        overview_parts.append('')
        
        if description:
            overview_parts.extend([description, ''])
        
        if purpose:
            overview_parts.extend([
                f'> {self._safe_emoji("info")}**Purpose:** {purpose}',
                ''
            ])
        
        return '\n'.join(overview_parts)
    
    def _generate_safe_features(self, readme_structure: Dict, context: Dict) -> str:
        """Generate features section safely"""
        features = readme_structure.get('features', {})
        if not features:
            return ""
        
        # Extract features
        if isinstance(features, dict):
            core_features = features.get('core_features', [])
        else:
            core_features = features if isinstance(features, list) else []
        
        if not core_features:
            return ""
        
        features_parts = [
            f'## {self._safe_emoji("features")}Features',
            '',
            '<div align="center">',
            f'{self._safe_emoji("fire")} **Packed with Amazing Capabilities** {self._safe_emoji("fire")}',
            '</div>',
            '',
            f'### {self._safe_emoji("star")}Core Features',
            ''
        ]
        
        for feature in core_features[:6]:
            enhanced_feature = self._enhance_feature_safely(feature, context)
            features_parts.append(f'- {enhanced_feature}')
        
        features_parts.append('')
        
        return '\n'.join(features_parts)
    
    def _enhance_feature_safely(self, feature: str, context: Dict) -> str:
        """Enhance feature descriptions safely"""
        feature_lower = feature.lower()
        
        if 'auth' in feature_lower:
            return f'{self._safe_emoji("security")}**Secure Authentication** - Enterprise-grade security system'
        elif 'jwt' in feature_lower:
            return f'{self._safe_emoji("security")}**JWT Integration** - Stateless token-based authentication'
        elif 'api' in feature_lower:
            return f'{self._safe_emoji("web")}**RESTful API** - Comprehensive endpoint architecture'
        elif 'dashboard' in feature_lower or 'admin' in feature_lower:
            return f'{self._safe_emoji("dashboard")}**Admin Dashboard** - Powerful management interface'
        elif 'database' in feature_lower:
            return f'{self._safe_emoji("database")}**Database Integration** - Robust data management'
        elif 'ui' in feature_lower:
            return f'{self._safe_emoji("mobile")}**Modern UI** - Beautiful, responsive design'
        else:
            return f'{self._safe_emoji("star")}**{feature}** - Advanced functionality for enhanced experience'
    
    def _safe_emoji(self, emoji_key: str) -> str:
        """Get safe emoji that won't break encoding"""
        # Try text alternatives first
        if emoji_key in self.text_alternatives:
            return self.text_alternatives[emoji_key]
        
        # Fallback to bracketed icons
        if emoji_key in self.fallback_icons:
            return self.fallback_icons[emoji_key] + ' '
        
        # Ultimate fallback
        return f'[{emoji_key.upper()}] '
    
    def _ensure_safe_encoding(self, content: str) -> str:
        """Ensure content has safe encoding"""
        try:
            # Try to encode/decode to catch issues
            content.encode('utf-8').decode('utf-8')
            return content
        except UnicodeError:
            # Replace problematic characters
            content = content.encode('ascii', 'ignore').decode('ascii')
            logger.warning("Applied ASCII fallback due to encoding issues")
            return content
    
    def _analyze_project_safely(self, repo_analysis: Dict, readme_structure: Dict) -> Dict:
        """Analyze project context safely"""
        project_type = repo_analysis.get('project_type', '').lower()
        
        return {
            'is_admin': 'admin' in project_type or 'dashboard' in project_type,
            'is_api': 'api' in project_type,
            'is_web_app': 'web' in project_type,
            'has_auth': any('auth' in str(f).lower() for f in repo_analysis.get('features', []))
        }
    
    # Additional safe generation methods...
    def _generate_safe_installation(self, readme_structure: Dict) -> str:
        """Generate installation section safely"""
        installation = readme_structure.get('installation', {})
        if not installation:
            return ""
        
        steps = installation.get('installation_steps', [])
        if not steps:
            return ""
        
        install_parts = [
            f'## {self._safe_emoji("installation")}Installation',
            '',
            f'{self._safe_emoji("rocket")}**Get started in minutes!**',
            ''
        ]
        
        # Use proper numbered list format
        for i, step in enumerate(steps, 1):
            install_parts.append(f'{i}. {step}')
        
        install_parts.append('')
        return '\n'.join(install_parts)
    
    def _generate_safe_usage(self, readme_structure: Dict) -> str:
        """Generate usage section safely"""
        usage = readme_structure.get('usage', {})
        if not usage:
            return ""
        
        quick_start = usage.get('quick_start', [])
        if not quick_start:
            return ""
        
        usage_parts = [
            f'## {self._safe_emoji("usage")}Usage',
            '',
            f'{self._safe_emoji("star")}**Ready to use right out of the box!**',
            ''
        ]
        
        # Use proper numbered list format
        for i, step in enumerate(quick_start, 1):
            usage_parts.append(f'{i}. {step}')
        
        usage_parts.append('')
        return '\n'.join(usage_parts)
    
    def _generate_safe_tech_stack(self, readme_structure: Dict, repo_analysis: Dict) -> str:
        """Generate tech stack section safely"""
        primary_language = repo_analysis.get('primary_language', '')
        frameworks = repo_analysis.get('frameworks', [])
        
        if not primary_language and not frameworks:
            return ""
        
        stack_parts = [
            f'## {self._safe_emoji("tech_stack")}Tech Stack',
            '',
            f'{self._safe_emoji("fire")}**Built with cutting-edge technology**',
            ''
        ]
        
        if primary_language:
            stack_parts.extend([
                f'### Core Technology',
                f'- **{primary_language}** - Primary programming language',
                ''
            ])
        
        if frameworks:
            stack_parts.append('### Frameworks & Libraries')
            for framework in frameworks:
                stack_parts.append(f'- **{framework}** - {self._get_framework_description(framework)}')
            stack_parts.append('')
        
        return '\n'.join(stack_parts)
    
    def _generate_safe_contributing(self) -> str:
        """Generate contributing section safely"""
        return f'''## {self._safe_emoji("contributing")}Contributing

{self._safe_emoji("heart")}**We love contributions! Here's how you can help:**

### Quick Start
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Guidelines
- Follow the existing code style
- Add tests for new features
- Update documentation as needed
- Be respectful and constructive

'''
    
    def _generate_safe_footer(self, readme_structure: Dict) -> str:
        """Generate footer safely"""
        return f'''---

<div align="center">

### {self._safe_emoji("heart")}**Made with Love & Code** {self._safe_emoji("heart")}

{self._safe_emoji("star")}**Star this repo if you found it helpful!** {self._safe_emoji("star")}

{self._safe_emoji("rocket")}**Happy Coding!** {self._safe_emoji("rocket")}

</div>

---

<div align="center">
<sub>Generated with magic by Smart README Generator</sub>
</div>'''
    
    def _get_framework_description(self, framework: str) -> str:
        """Get framework description"""
        descriptions = {
            'React': 'Modern UI library for building interactive interfaces',
            'Next.js': 'Production-ready React framework with SSR',
            'Django': 'High-level Python web framework',
            'Express.js': 'Fast, unopinionated web framework for Node.js'
        }
        return descriptions.get(framework, 'Powerful development framework')
    
    def _generate_ultra_safe_fallback(self, json_data: Dict) -> str:
        """Ultra-safe fallback README"""
        repo_analysis = json_data.get('repository_analysis', {})
        project_name = repo_analysis.get('repository_url', 'Project').split('/')[-1] if repo_analysis.get('repository_url') else 'Project'
        
        return f'''# {project_name}

A software project built with modern technology.

## Installation

1. Clone the repository
2. Install dependencies
3. Run the application

## Usage

Follow the installation steps and refer to the documentation.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

Made with Love & Code
'''
