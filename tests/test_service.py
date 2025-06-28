#!/usr/bin/env python3
"""
Test the Optimized Bedrock Service for README Generation
"""

import json
import sys
import os
from datetime import datetime

# Add the services directory to the path
sys.path.append('./src/services')

def test_optimized_bedrock_service():
    """Test the optimized Bedrock service"""
    
    print("🧪 Testing Optimized Bedrock Service for README Generation")
    print("=" * 60)
    
    try:
        # Import the service
        from optimized_bedrock_service import OptimizedBedrockService, ReadmeGenerationRequest
        
        print("✅ Successfully imported OptimizedBedrockService")
        
        # Initialize the service
        print("\n🔧 Initializing Bedrock service...")
        service = OptimizedBedrockService()
        
        # Get model info
        model_info = service.get_model_info()
        print(f"✅ Active Model: {model_info['active_model']['name']}")
        print(f"   Model ID: {model_info['active_model']['id']}")
        print(f"   Use Case: {model_info['active_model']['use_case']}")
        
        # Create a test request
        print("\n📝 Creating test README generation request...")
        test_request = ReadmeGenerationRequest(
            repository_url="https://github.com/test/sample-react-app",
            project_type="Web Application",
            primary_language="JavaScript",
            frameworks=["React", "Next.js", "Node.js"],
            key_files=["package.json", "next.config.js", "pages/index.js", "components/Header.js"],
            file_contents={
                "package.json": '{"name": "sample-app", "dependencies": {"react": "^18.0.0", "next": "^13.0.0"}}',
                "next.config.js": "module.exports = { reactStrictMode: true }",
                "pages/index.js": "import React from 'react'; export default function Home() { return <div>Hello World</div>; }",
                "components/Header.js": "import React from 'react'; export default function Header() { return <header>My App</header>; }"
            },
            features=["Authentication", "API Integration", "Responsive Design"],
            architecture_patterns=["Component-Based", "Server-Side Rendering"],
            security_analysis={"total_issues": 0, "security_score": 95}
        )
        
        print("✅ Test request created successfully")
        
        # Generate README structure
        print("\n🤖 Generating README structure with Bedrock...")
        start_time = datetime.now()
        
        readme_structure = service.generate_readme_structure(test_request)
        
        generation_time = (datetime.now() - start_time).total_seconds()
        print(f"✅ README structure generated in {generation_time:.2f} seconds")
        
        # Convert to dictionary for display
        readme_dict = {
            "project_overview": readme_structure.project_overview,
            "technical_stack": readme_structure.technical_stack,
            "features": readme_structure.features,
            "installation": readme_structure.installation,
            "usage": readme_structure.usage,
            "architecture": readme_structure.architecture,
            "api_documentation": readme_structure.api_documentation,
            "development": readme_structure.development,
            "deployment": readme_structure.deployment,
            "contributing": readme_structure.contributing,
            "license_info": readme_structure.license_info
        }
        
        # Display results
        print("\n📋 Generated README Structure:")
        print("=" * 40)
        
        # Show key sections
        print(f"📖 Project Overview:")
        print(f"   Name: {readme_structure.project_overview.get('name', 'N/A')}")
        print(f"   Type: {readme_structure.project_overview.get('type', 'N/A')}")
        print(f"   Description: {readme_structure.project_overview.get('description', 'N/A')[:100]}...")
        
        print(f"\n🛠️  Technical Stack:")
        print(f"   Primary Language: {readme_structure.technical_stack.get('primary_language', 'N/A')}")
        print(f"   Frameworks: {readme_structure.technical_stack.get('frameworks', [])}")
        print(f"   Dependencies: {len(readme_structure.technical_stack.get('key_dependencies', []))} identified")
        
        print(f"\n⚡ Features:")
        features = readme_structure.features
        if isinstance(features, dict):
            print(f"   Core Features: {features.get('core_features', [])}")
        else:
            print(f"   Features: {features}")
        
        print(f"\n📦 Installation:")
        installation = readme_structure.installation
        print(f"   Requirements: {len(installation.get('system_requirements', []))} items")
        print(f"   Steps: {len(installation.get('installation_steps', []))} steps")
        
        # Save full structure to file
        output_file = "test_readme_structure.json"
        with open(output_file, 'w') as f:
            json.dump(readme_dict, f, indent=2)
        
        print(f"\n💾 Full structure saved to: {output_file}")
        
        # Test the utility function
        print("\n🔧 Testing utility function...")
        from optimized_bedrock_service import generate_readme_json
        
        test_analysis = {
            'repository_url': 'https://github.com/test/sample-app',
            'project_type': 'Web Application',
            'primary_language': 'JavaScript',
            'frameworks': ['React', 'Next.js'],
            'features': ['Authentication', 'API Integration'],
            'architecture_patterns': ['Component-Based'],
            'key_files': ['package.json', 'next.config.js'],
            'file_contents': {'package.json': '{"name": "test"}'},
            'security_analysis': {'total_issues': 0, 'security_score': 100}
        }
        
        utility_result = generate_readme_json(test_analysis)
        print(f"✅ Utility function test successful")
        print(f"   Generated sections: {len(utility_result)} sections")
        print(f"   Model used: {utility_result.get('generation_metadata', {}).get('model_used', 'Unknown')}")
        
        print(f"\n🎉 ALL TESTS PASSED!")
        print(f"   Service is ready for production use")
        print(f"   Model: {model_info['active_model']['name']}")
        print(f"   Generation time: {generation_time:.2f}s")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        print("   Make sure the optimized_bedrock_service.py is in the correct location")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_fallback_behavior():
    """Test fallback behavior when Bedrock is not available"""
    
    print("\n🔄 Testing Fallback Behavior")
    print("=" * 30)
    
    try:
        # Test the Lambda function's fallback
        sys.path.append('./src/lambda')
        from optimized_readme_generator import create_fallback_readme_structure
        
        test_analysis = {
            'project_type': 'Web Application',
            'primary_language': 'JavaScript',
            'frameworks': ['React'],
            'features': ['Authentication'],
            'architecture_patterns': ['MVC']
        }
        
        fallback_structure = create_fallback_readme_structure(test_analysis)
        
        print("✅ Fallback structure generated successfully")
        print(f"   Project Type: {fallback_structure['project_overview']['type']}")
        print(f"   Primary Language: {fallback_structure['technical_stack']['primary_language']}")
        print(f"   Features: {len(fallback_structure['features'])} features")
        
        return True
        
    except Exception as e:
        print(f"❌ Fallback test failed: {e}")
        return False

if __name__ == '__main__':
    print("🚀 Starting Optimized Bedrock Service Tests")
    print("=" * 50)
    
    # Test main service
    main_test_passed = test_optimized_bedrock_service()
    
    # Test fallback
    fallback_test_passed = test_fallback_behavior()
    
    print(f"\n📊 TEST SUMMARY:")
    print(f"   Main Service: {'✅ PASSED' if main_test_passed else '❌ FAILED'}")
    print(f"   Fallback: {'✅ PASSED' if fallback_test_passed else '❌ FAILED'}")
    
    if main_test_passed and fallback_test_passed:
        print(f"\n🎉 ALL TESTS PASSED - Service is ready for deployment!")
    else:
        print(f"\n⚠️  Some tests failed - check the logs above")
        sys.exit(1)
