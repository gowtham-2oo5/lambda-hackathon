"""
Simple README Cleaner - Quick 2-second fix for repetitive content
"""

import re
import logging

logger = logging.getLogger(__name__)

def quick_clean_readme(readme_content: str) -> str:
    """
    Quick 2-second cleanup of README content
    Removes obvious repetitive lines after badges
    """
    try:
        lines = readme_content.split('\n')
        cleaned_lines = []
        
        i = 0
        while i < len(lines):
            line = lines[i]
            
            # If this line has badges (either img.shields.io or ![...] pattern), check for repetition
            if 'img.shields.io' in line or (line.startswith('![') and '](https://' in line):
                cleaned_lines.append(line)
                i += 1
                
                # Look ahead for repetitive tech lines (max 5 lines)
                look_ahead = 0
                while i < len(lines) and look_ahead < 5:
                    next_line = lines[i]
                    
                    # Skip if it's a repetitive tech highlight line
                    if _is_repetitive_tech_line(next_line):
                        logger.info(f"🔧 Removed repetitive line: {next_line.strip()}")
                        i += 1
                        look_ahead += 1
                        continue
                    elif next_line.strip() == '':
                        # Skip empty lines but keep looking
                        cleaned_lines.append(next_line)
                        i += 1
                        look_ahead += 1
                        continue
                    else:
                        # Found non-repetitive content, stop looking
                        break
            else:
                cleaned_lines.append(line)
                i += 1
        
        return '\n'.join(cleaned_lines)
        
    except Exception as e:
        logger.error(f"❌ Quick clean failed: {e}")
        return readme_content

def _is_repetitive_tech_line(line: str) -> bool:
    """Quick check if line is repetitive tech highlight"""
    if not line.strip():
        return False
    
    line_lower = line.lower()
    
    # Look for patterns like "### **TypeScript** • **React** • **Secure**"
    if ('###' in line and 
        '**' in line and 
        ('•' in line or '|' in line or ' • ' in line)):
        
        # Check if it contains technology names
        tech_indicators = ['typescript', 'javascript', 'python', 'react', 'next.js', 'django', 'express', 'secure']
        found_techs = sum(1 for tech in tech_indicators if tech in line_lower)
        
        # If it has multiple tech names with formatting, it's likely repetitive
        if found_techs >= 2:
            return True
    
    return False
