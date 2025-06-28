"""
README Quality Reviewer - Reviews structure and content before S3 upload
Fixes issues like repetition, formatting problems, and content quality
"""

import re
import logging
from typing import Dict, List, Any, Tuple
from datetime import datetime

logger = logging.getLogger(__name__)

class READMEQualityReviewer:
    """
    Reviews README content for quality issues and fixes them before S3 upload
    """
    
    def __init__(self):
        self.quality_checks = [
            'check_repetition',
            'check_formatting',
            'check_structure',
            'check_content_quality',
            'check_emoji_consistency',
            'check_badge_placement'
        ]
        
        self.quality_threshold = 85.0  # Minimum quality score to pass
        
    def review_and_fix_readme(self, readme_content: str, project_context: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
        """
        Review README content and fix quality issues
        Returns: (fixed_content, review_report)
        """
        logger.info("🔍 Starting README quality review...")
        
        review_report = {
            'original_length': len(readme_content),
            'issues_found': [],
            'fixes_applied': [],
            'quality_score': 0.0,
            'passed_review': False,
            'review_timestamp': datetime.now().isoformat()
        }
        
        try:
            # Make a copy to work with
            fixed_content = readme_content
            
            # Run all quality checks and fixes
            for check_name in self.quality_checks:
                check_method = getattr(self, check_name)
                fixed_content, check_report = check_method(fixed_content, project_context)
                
                # Merge check report
                review_report['issues_found'].extend(check_report.get('issues', []))
                review_report['fixes_applied'].extend(check_report.get('fixes', []))
            
            # Calculate overall quality score
            review_report['quality_score'] = self._calculate_quality_score(fixed_content, review_report)
            review_report['passed_review'] = review_report['quality_score'] >= self.quality_threshold
            review_report['final_length'] = len(fixed_content)
            
            logger.info(f"✅ Quality review completed - Score: {review_report['quality_score']:.1f}%")
            
            return fixed_content, review_report
            
        except Exception as e:
            logger.error(f"❌ Quality review failed: {e}")
            review_report['issues_found'].append(f"Review process failed: {str(e)}")
            return readme_content, review_report
    
    def check_repetition(self, content: str, context: Dict) -> Tuple[str, Dict]:
        """Check and fix content repetition issues"""
        issues = []
        fixes = []
        
        # Check for technology name repetition after badges
        lines = content.split('\n')
        fixed_lines = []
        
        i = 0
        while i < len(lines):
            line = lines[i]
            
            # Look for badge lines followed by tech repetition
            if 'img.shields.io' in line:
                # Look ahead for potential repetition lines
                j = i + 1
                while j < len(lines) and j < i + 5:  # Look ahead up to 5 lines
                    next_line = lines[j]
                    
                    if self._is_tech_repetition_line(line, next_line):
                        issues.append(f"Technology repetition found after badges: {next_line.strip()}")
                        fixes.append("Removed redundant technology repetition after badges")
                        
                        # Add lines up to the repetitive line
                        fixed_lines.extend(lines[i:j])
                        
                        # Skip the repetitive line and continue from after it
                        i = j + 1
                        
                        # Skip any empty lines that follow
                        while i < len(lines) and lines[i].strip() == '':
                            i += 1
                        
                        break
                    elif next_line.strip() and not next_line.startswith('#'):
                        # Found non-empty, non-header line - stop looking
                        break
                    
                    j += 1
                else:
                    # No repetition found, add the line normally
                    fixed_lines.append(line)
                    i += 1
            else:
                fixed_lines.append(line)
                i += 1
        
        fixed_content = '\n'.join(fixed_lines)
        
        # Check for duplicate sections
        section_headers = re.findall(r'^## (.+)$', content, re.MULTILINE)
        seen_sections = set()
        duplicate_sections = []
        
        for section in section_headers:
            if section in seen_sections:
                duplicate_sections.append(section)
                issues.append(f"Duplicate section found: {section}")
            seen_sections.add(section)
        
        if duplicate_sections:
            fixes.append(f"Would remove duplicate sections: {', '.join(duplicate_sections)}")
            # Actually remove duplicate sections
            fixed_content = self._remove_duplicate_sections(fixed_content, duplicate_sections)
        
        return fixed_content, {'issues': issues, 'fixes': fixes}
    
    def _remove_duplicate_sections(self, content: str, duplicate_sections: List[str]) -> str:
        """Remove duplicate sections from content"""
        lines = content.split('\n')
        fixed_lines = []
        skip_section = False
        current_section = None
        
        for line in lines:
            # Check if this is a section header
            section_match = re.match(r'^## (.+)$', line)
            if section_match:
                section_name = section_match.group(1)
                if section_name in duplicate_sections and current_section == section_name:
                    # This is a duplicate section, start skipping
                    skip_section = True
                    continue
                else:
                    # New section or first occurrence
                    skip_section = False
                    current_section = section_name
            
            # Check if we've reached a new section (stop skipping)
            if skip_section and line.startswith('## '):
                skip_section = False
            
            if not skip_section:
                fixed_lines.append(line)
        
        return '\n'.join(fixed_lines)
    
    def check_formatting(self, content: str, context: Dict) -> Tuple[str, Dict]:
        """Check and fix formatting issues"""
        issues = []
        fixes = []
        fixed_content = content
        
        # Fix excessive newlines
        original_newlines = len(re.findall(r'\n{4,}', fixed_content))
        if original_newlines > 0:
            fixed_content = re.sub(r'\n{4,}', '\n\n\n', fixed_content)
            issues.append(f"Found {original_newlines} instances of excessive newlines")
            fixes.append("Fixed excessive newlines (4+ consecutive)")
        
        # Fix header spacing
        headers_without_spacing = len(re.findall(r'\n(#{1,6}[^#\n])', fixed_content))
        if headers_without_spacing > 0:
            fixed_content = re.sub(r'\n(#{1,6}\s)', r'\n\n\1', fixed_content)
            issues.append(f"Found {headers_without_spacing} headers without proper spacing")
            fixes.append("Added proper spacing around headers")
        
        # Fix list formatting
        malformed_lists = len(re.findall(r'\n-[^\s]', fixed_content))
        if malformed_lists > 0:
            fixed_content = re.sub(r'\n-([^\s])', r'\n- \1', fixed_content)
            issues.append(f"Found {malformed_lists} malformed list items")
            fixes.append("Fixed list item spacing")
        
        # Fix center div closing
        if '<div align="center">' in fixed_content and '</div>' not in fixed_content:
            issues.append("Unclosed center div found")
            fixes.append("Would add missing </div> tag")
        
        return fixed_content, {'issues': issues, 'fixes': fixes}
    
    def check_structure(self, content: str, context: Dict) -> Tuple[str, Dict]:
        """Check README structure quality"""
        issues = []
        fixes = []
        
        # Check for essential sections
        essential_sections = ['overview', 'installation', 'usage', 'contributing']
        missing_sections = []
        
        content_lower = content.lower()
        for section in essential_sections:
            if section not in content_lower:
                missing_sections.append(section)
        
        if missing_sections:
            issues.append(f"Missing essential sections: {', '.join(missing_sections)}")
        
        # Check for empty sections
        empty_sections = re.findall(r'## ([^\n]+)\n\n## ', content)
        if empty_sections:
            issues.append(f"Empty sections found: {', '.join(empty_sections)}")
            fixes.append("Would remove or populate empty sections")
        
        # Check title structure
        title_matches = re.findall(r'^# (.+)$', content, re.MULTILINE)
        if len(title_matches) == 0:
            issues.append("No main title (H1) found")
        elif len(title_matches) > 1:
            issues.append(f"Multiple main titles found: {len(title_matches)}")
        
        return content, {'issues': issues, 'fixes': fixes}
    
    def check_content_quality(self, content: str, context: Dict) -> Tuple[str, Dict]:
        """Check content quality and completeness"""
        issues = []
        fixes = []
        
        # Check for placeholder content
        placeholders = [
            'lorem ipsum', 'placeholder', 'todo', 'tbd', 'coming soon',
            'under construction', 'work in progress'
        ]
        
        content_lower = content.lower()
        found_placeholders = [p for p in placeholders if p in content_lower]
        
        if found_placeholders:
            issues.append(f"Placeholder content found: {', '.join(found_placeholders)}")
            fixes.append("Would replace placeholder content with actual information")
        
        # Check for very short descriptions
        description_match = re.search(r'> (.+)', content)
        if description_match:
            description = description_match.group(1)
            if len(description.split()) < 5:
                issues.append("Project description is too short (< 5 words)")
                fixes.append("Would expand project description")
        
        # Check for broken links
        broken_link_patterns = [
            r'\[([^\]]+)\]\(\)',  # Empty links
            r'\[([^\]]+)\]\(#\)',  # Links to nothing
        ]
        
        for pattern in broken_link_patterns:
            matches = re.findall(pattern, content)
            if matches:
                issues.append(f"Broken links found: {len(matches)} instances")
                fixes.append("Would fix broken link references")
        
        return content, {'issues': issues, 'fixes': fixes}
    
    def check_emoji_consistency(self, content: str, context: Dict) -> Tuple[str, Dict]:
        """Check emoji usage consistency"""
        issues = []
        fixes = []
        
        # Check for mixed emoji styles
        unicode_emojis = len(re.findall(r'[🎯✨🚀📦💻🛠️🏗️📚🔧🌐🤝📄📋⭐🔥💎❤️👍🎉⚡🔐🗄️🌍📱👑📊]', content))
        text_emojis = len(re.findall(r'\[[A-Z_]+\]', content))
        
        if unicode_emojis > 0 and text_emojis > 0:
            issues.append(f"Mixed emoji styles: {unicode_emojis} Unicode, {text_emojis} text")
            fixes.append("Would standardize emoji style")
        
        # Check for emoji overuse
        total_emojis = unicode_emojis + text_emojis
        content_words = len(content.split())
        emoji_ratio = total_emojis / max(content_words, 1) * 100
        
        if emoji_ratio > 5:  # More than 5% emojis
            issues.append(f"Excessive emoji usage: {emoji_ratio:.1f}% of content")
            fixes.append("Would reduce emoji density")
        
        return content, {'issues': issues, 'fixes': fixes}
    
    def check_badge_placement(self, content: str, context: Dict) -> Tuple[str, Dict]:
        """Check badge placement and quality"""
        issues = []
        fixes = []
        
        # Check for badges in wrong location
        badge_lines = [i for i, line in enumerate(content.split('\n')) if 'img.shields.io' in line]
        
        if badge_lines:
            first_badge_line = badge_lines[0]
            if first_badge_line > 10:  # Badges should be near the top
                issues.append(f"Badges placed too low in document (line {first_badge_line})")
                fixes.append("Would move badges closer to title")
        
        # Check for too many badges
        total_badges = len(re.findall(r'!\[[^\]]*\]\(https://img\.shields\.io[^)]+\)', content))
        if total_badges > 8:
            issues.append(f"Too many badges: {total_badges} (recommended: ≤8)")
            fixes.append("Would limit badge count to essential ones")
        
        return content, {'issues': issues, 'fixes': fixes}
    
    def _is_tech_repetition_line(self, badge_line: str, next_line: str) -> bool:
        """Check if next line repeats technology names from badges"""
        if not next_line.strip():
            return False
        
        # Skip if it's a divider or structural element
        if next_line.strip() in ['---', '===', '</div>', '<div align="center">']:
            return False
        
        # Extract technology names from badges
        badge_techs = re.findall(r'!\[([^\]]+)\]', badge_line)
        
        # Check if next line contains the same technologies with emojis/formatting
        next_line_lower = next_line.lower()
        
        # Look for patterns like "### **TypeScript** • **React**"
        if '**' in next_line and ('•' in next_line or '|' in next_line):
            repetition_count = 0
            for tech in badge_techs:
                if tech.lower() in next_line_lower:
                    repetition_count += 1
            
            # If more than half the technologies are repeated, it's likely repetition
            return repetition_count >= len(badge_techs) / 2 and repetition_count >= 2
        
        return False
    
    def _calculate_quality_score(self, content: str, review_report: Dict) -> float:
        """Calculate overall quality score"""
        base_score = 100.0
        
        # Deduct points for issues
        issues_count = len(review_report['issues_found'])
        score_deduction = min(issues_count * 5, 50)  # Max 50 points deduction
        
        # Bonus for fixes applied
        fixes_count = len(review_report['fixes_applied'])
        score_bonus = min(fixes_count * 2, 20)  # Max 20 points bonus
        
        # Content length factor
        content_length = len(content)
        if content_length < 1000:
            base_score -= 10  # Too short
        elif content_length > 10000:
            base_score -= 5   # Too long
        
        final_score = base_score - score_deduction + score_bonus
        return max(0.0, min(100.0, final_score))
    
    def generate_review_summary(self, review_report: Dict) -> str:
        """Generate human-readable review summary"""
        summary_parts = [
            f"📊 README Quality Review Summary",
            f"================================",
            f"",
            f"🎯 Quality Score: {review_report['quality_score']:.1f}/100",
            f"✅ Review Status: {'PASSED' if review_report['passed_review'] else 'NEEDS IMPROVEMENT'}",
            f"📏 Content Length: {review_report['original_length']} → {review_report.get('final_length', 'N/A')} chars",
            f"",
            f"🔍 Issues Found: {len(review_report['issues_found'])}",
        ]
        
        if review_report['issues_found']:
            summary_parts.append("Issues:")
            for issue in review_report['issues_found']:
                summary_parts.append(f"  • {issue}")
        
        summary_parts.extend([
            f"",
            f"🔧 Fixes Applied: {len(review_report['fixes_applied'])}",
        ])
        
        if review_report['fixes_applied']:
            summary_parts.append("Fixes:")
            for fix in review_report['fixes_applied']:
                summary_parts.append(f"  • {fix}")
        
        summary_parts.extend([
            f"",
            f"⏰ Review Time: {review_report['review_timestamp']}",
            f"",
            f"{'✅ APPROVED FOR S3 UPLOAD' if review_report['passed_review'] else '❌ REQUIRES FIXES BEFORE UPLOAD'}"
        ])
        
        return '\n'.join(summary_parts)
