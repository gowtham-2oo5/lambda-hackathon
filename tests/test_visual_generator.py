#!/usr/bin/env python3
"""
Test the new Visual README Generator
"""

import sys
import os
import json

# Add lambda directory to path
sys.path.append('./lambda')

def test_visual_generator():
    """Test the visual README generator"""
    
    print("🎨 Testing Visual README Generator")
    print("=" * 40)
    
    try:
        # Import the visual generator
        from visual_readme_generator import DynamicVisualREADMEGenerator
        print("✅ Visual generator imported successfully")
        
        # Initialize generator
        generator = DynamicVisualREADMEGenerator()
        print("✅ Generator initialized successfully")
        
        # Create test data for EzyBites Admin (TypeScript/React)
        test_data = {
            'repository_analysis': {
                'repository_url': 'https://github.com/gowtham-2oo5/ezybites_super_admin',
                'project_type': 'Web Application',
                'primary_language': 'TypeScript',
                'frameworks': ['React', 'Next.js'],
                'features': ['Admin dashboard interface', 'Data visualization with Recharts', 'Modern UI components with Radix UI'],
                'security_analysis': {'security_score': 100}
            },
            'readme_structure': {
                'project_overview': {
                    'name': 'EzyBites Super Admin',
                    'description': 'A comprehensive super admin dashboard for the EzyBites platform built with Next.js and TypeScript, featuring modern UI components and administrative management capabilities',
                    'primary_purpose': 'Administrative management and data visualization',
                    'target_audience': 'System administrators and managers'
                },
                'technical_stack': {
                    'primary_language': 'TypeScript',
                    'frameworks': ['React', 'Next.js'],
                    'dependencies': ['Recharts', 'Radix UI', 'Tailwind CSS']
                },
                'features': {
                    'core_features': ['Admin dashboard interface', 'Data visualization with Recharts', 'Modern UI components with Radix UI'],
                    'authentication_features': ['Role-based access control', 'Secure admin authentication'],
                    'api_features': ['RESTful API integration', 'Real-time data updates']
                },
                'installation': {
                    'prerequisites': ['Node.js 18+', 'npm or yarn'],
                    'installation_steps': ['Clone the repository', 'Install dependencies with npm install', 'Configure environment variables', 'Run npm run dev']
                },
                'usage': {
                    'quick_start': ['Start the development server', 'Navigate to admin dashboard', 'Login with admin credentials'],
                    'common_commands': ['npm run dev', 'npm run build', 'npm run start'],
                    'examples': ['Dashboard overview', 'User management', 'Data analytics']
                }
            }
        }
        
        # Generate visual README
        readme_content = generator.generate_stunning_readme(test_data)
        print(f"✅ Visual README generated ({len(readme_content)} characters)")
        
        # Check for proper emojis (should be actual Unicode, not codes)
        print("\n🔍 Emoji Quality Check:")
        if '🎯' in readme_content and '✨' in readme_content and '🚀' in readme_content:
            print("✅ Proper Unicode emojis found!")
        else:
            print("❌ Emoji issues detected")
        
        # Check for visual enhancements
        print("\n🎨 Visual Enhancement Check:")
        if '<div align="center">' in readme_content:
            print("✅ Center alignment found")
        if '---' in readme_content:
            print("✅ Visual dividers found")
        if 'img.shields.io' in readme_content:
            print("✅ Badges found")
        
        # Save to file for inspection
        with open('visual_readme_test.md', 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print(f"\n📄 README saved to: visual_readme_test.md")
        
        # Show preview
        print("\n📝 Visual README Preview (first 30 lines):")
        print("-" * 60)
        lines = readme_content.split('\n')
        for i, line in enumerate(lines[:30], 1):
            print(f"{i:2d}: {line}")
        print("-" * 60)
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_visual_generator()
    if success:
        print("\n🎉 Visual generator test PASSED!")
        print("Ready to deploy enhanced README generator!")
    else:
        print("\n❌ Visual generator test FAILED!")
