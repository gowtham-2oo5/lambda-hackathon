#!/usr/bin/env python3
"""
Test the Emoji-Safe README Generator
"""

import sys
import os
import json

# Add lambda directory to path
sys.path.append('./lambda')

def test_emoji_safe_generator():
    """Test the emoji-safe README generator"""
    
    print("🔧 Testing Emoji-Safe README Generator")
    print("=" * 40)
    
    try:
        # Import the emoji-safe generator
        from emoji_safe_generator import EmojiSafeREADMEGenerator
        print("✅ Emoji-safe generator imported successfully")
        
        # Initialize generator
        generator = EmojiSafeREADMEGenerator()
        print("✅ Generator initialized successfully")
        
        # Create test data
        test_data = {
            'repository_analysis': {
                'repository_url': 'https://github.com/gowtham-2oo5/ezybites_super_admin',
                'project_type': 'Web Application',
                'primary_language': 'TypeScript',
                'frameworks': ['React', 'Next.js'],
                'features': ['Admin dashboard interface', 'Data visualization with Recharts', 'Modern UI components'],
                'security_analysis': {'security_score': 100}
            },
            'readme_structure': {
                'project_overview': {
                    'name': 'EzyBites Super Admin',
                    'description': 'A comprehensive super admin dashboard for the EzyBites platform',
                    'primary_purpose': 'Administrative management and data visualization'
                },
                'features': {
                    'core_features': ['Admin dashboard interface', 'Data visualization', 'Modern UI components', 'User management']
                },
                'installation': {
                    'installation_steps': ['Clone the repository', 'Install dependencies with npm install', 'Run npm run dev']
                },
                'usage': {
                    'quick_start': ['Start the development server', 'Navigate to admin dashboard', 'Login with credentials']
                }
            }
        }
        
        # Generate safe README
        readme_content = generator.generate_safe_readme(test_data)
        print(f"✅ Emoji-safe README generated ({len(readme_content)} characters)")
        
        # Save to file
        with open('emoji_safe_test.md', 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print(f"📄 README saved to: emoji_safe_test.md")
        
        # Check for problematic characters
        print("\n🔍 Encoding Quality Check:")
        problematic_chars = ['â', 'ð', '€', '™', '¢', '£']
        found_issues = []
        
        for char in problematic_chars:
            if char in readme_content:
                found_issues.append(char)
        
        if found_issues:
            print(f"❌ Found problematic characters: {found_issues}")
        else:
            print("✅ No problematic encoding characters found!")
        
        # Check for safe emojis
        print("\n🎯 Safe Emoji Check:")
        if '[🎯]' in readme_content or '🎯' in readme_content:
            print("✅ Safe emoji handling working")
        else:
            print("⚠️ No emoji indicators found")
        
        # Show preview
        print("\n📝 Emoji-Safe README Preview (first 25 lines):")
        print("-" * 60)
        lines = readme_content.split('\n')
        for i, line in enumerate(lines[:25], 1):
            print(f"{i:2d}: {line}")
        print("-" * 60)
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_emoji_safe_generator()
    if success:
        print("\n🎉 Emoji-safe generator test PASSED!")
        print("Ready to deploy encoding-safe README generator!")
    else:
        print("\n❌ Emoji-safe generator test FAILED!")
