#!/usr/bin/env python3
"""
Test the README Quality Reviewer
"""

import sys
import os

# Add lambda directory to path
sys.path.append('./lambda')

def test_quality_reviewer():
    """Test the quality reviewer with problematic content"""
    
    print("🔍 Testing README Quality Reviewer")
    print("=" * 40)
    
    try:
        # Import the quality reviewer
        from readme_quality_reviewer import READMEQualityReviewer
        print("✅ Quality reviewer imported successfully")
        
        # Initialize reviewer
        reviewer = READMEQualityReviewer()
        print("✅ Reviewer initialized successfully")
        
        # Create problematic README content (like the EzyBites issue)
        problematic_content = """<div align="center">

# 🚀  EzyBites Super Admin 🚀 

### ⭐  *A comprehensive super admin dashboard* ⭐ 

![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white) ![Next.js](https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white) ![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)

### **🔷 TypeScript** • **⚙️ Next.js • React** • **🔐 Secure**

---
</div>


## 📋 Table of Contents

- [🎯 **Overview**](#overview)
- [✨ **Features**](#features)


## 🎯 Overview

🌍 **Next-Generation Web Application**



## ✨ Features

- 📊 **Admin Dashboard** - Powerful interface
- 🎨 **Modern UI** - Beautiful design


## 🎯 Overview

This is a duplicate section that should be caught.


## 🤝 Contributing

Contributions welcome!

"""
        
        project_context = {
            'project_type': 'Web Application',
            'primary_language': 'TypeScript',
            'frameworks': ['React', 'Next.js']
        }
        
        print(f"📝 Testing with problematic content ({len(problematic_content)} chars)")
        
        # Review the content
        fixed_content, review_report = reviewer.review_and_fix_readme(problematic_content, project_context)
        
        print(f"✅ Quality review completed!")
        print(f"📊 Quality Score: {review_report['quality_score']:.1f}%")
        print(f"✅ Passed Review: {review_report['passed_review']}")
        print(f"🔍 Issues Found: {len(review_report['issues_found'])}")
        print(f"🔧 Fixes Applied: {len(review_report['fixes_applied'])}")
        
        # Show issues found
        if review_report['issues_found']:
            print("\n🔍 Issues Found:")
            for i, issue in enumerate(review_report['issues_found'], 1):
                print(f"  {i}. {issue}")
        
        # Show fixes applied
        if review_report['fixes_applied']:
            print("\n🔧 Fixes Applied:")
            for i, fix in enumerate(review_report['fixes_applied'], 1):
                print(f"  {i}. {fix}")
        
        # Save both versions for comparison
        with open('original_content.md', 'w', encoding='utf-8') as f:
            f.write(problematic_content)
        
        with open('fixed_content.md', 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        
        print(f"\n📄 Files saved:")
        print(f"  • original_content.md ({len(problematic_content)} chars)")
        print(f"  • fixed_content.md ({len(fixed_content)} chars)")
        
        # Generate review summary
        summary = reviewer.generate_review_summary(review_report)
        print(f"\n{summary}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_quality_reviewer()
    if success:
        print("\n🎉 Quality reviewer test PASSED!")
        print("Ready to deploy quality-controlled README generator!")
    else:
        print("\n❌ Quality reviewer test FAILED!")
