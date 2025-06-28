#!/usr/bin/env python3
"""
Simple test to identify Lambda 2 issues
"""

import sys
import os
import json

# Add lambda directory to path
sys.path.append('./lambda')

def test_simple_generation():
    """Test simple README generation"""
    
    print("🧪 Testing Simple README Generation")
    print("=" * 40)
    
    try:
        # Test basic imports
        from readme_generator_engine import READMEGeneratorEngine
        print("✅ READMEGeneratorEngine imported successfully")
        
        # Initialize engine
        engine = READMEGeneratorEngine()
        print("✅ Engine initialized successfully")
        
        # Create simple test data
        test_data = {
            'repository_analysis': {
                'repository_url': 'https://github.com/test/sample',
                'project_type': 'Web Application',
                'primary_language': 'JavaScript',
                'frameworks': ['Express.js'],
                'features': ['JWT authentication', 'API integration'],
                'security_analysis': {'security_score': 95}
            },
            'readme_structure': {
                'project_overview': {
                    'name': 'Test Project',
                    'description': 'A test project for README generation',
                    'type': 'Web Application'
                },
                'technical_stack': {
                    'primary_language': 'JavaScript',
                    'frameworks': ['Express.js']
                },
                'features': {
                    'core_features': ['JWT authentication', 'API integration', 'User management']
                }
            }
        }
        
        # Generate README
        readme_content = engine.generate_readme(test_data, style='developer')
        print(f"✅ README generated successfully ({len(readme_content)} characters)")
        
        # Check for emoji issues
        if 'ð' in readme_content:
            print("⚠️ Found broken emoji encoding")
            # Count occurrences
            broken_count = readme_content.count('ð')
            print(f"   Found {broken_count} broken emoji characters")
        else:
            print("✅ No broken emoji encoding found")
        
        # Show preview
        print("\n📝 README Preview (first 500 chars):")
        print("-" * 50)
        print(readme_content[:500])
        print("-" * 50)
        
        # Test the enhancement method
        if hasattr(engine, '_enhance_feature_description'):
            enhanced = engine._enhance_feature_description('JWT authentication')
            print(f"\n✅ Feature enhancement working: {enhanced}")
        else:
            print("\n⚠️ Feature enhancement method not found")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_simple_generation()
    if success:
        print("\n🎉 Simple generation test PASSED!")
    else:
        print("\n❌ Simple generation test FAILED!")
