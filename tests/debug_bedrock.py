#!/usr/bin/env python3
"""
Debug Bedrock Access - Find Available Models
"""

import boto3
import json

def debug_bedrock_access():
    """Debug what's actually available in Bedrock"""
    print("🔍 Debugging Bedrock Access")
    print("=" * 30)
    
    try:
        # Check available models
        bedrock = boto3.client('bedrock', region_name='us-east-1')
        
        print("📋 Listing Foundation Models...")
        response = bedrock.list_foundation_models()
        
        claude_models = []
        for model in response['modelSummaries']:
            if 'claude' in model['modelId'].lower():
                claude_models.append({
                    'modelId': model['modelId'],
                    'modelName': model['modelName'],
                    'providerName': model['providerName'],
                    'inputModalities': model.get('inputModalities', []),
                    'outputModalities': model.get('outputModalities', [])
                })
        
        print(f"\n🤖 AVAILABLE CLAUDE MODELS ({len(claude_models)}):")
        for model in claude_models:
            print(f"   • {model['modelId']}")
            print(f"     Name: {model['modelName']}")
            print(f"     Provider: {model['providerName']}")
            print("")
        
        # Test Claude 3 Haiku
        print("🧪 Testing Claude 3 Haiku...")
        test_model('anthropic.claude-3-haiku-20240307-v1:0')
        
        # Test Claude Sonnet 4
        print("\n🧪 Testing Claude Sonnet 4...")
        test_model('anthropic.claude-sonnet-4-20250514-v1:0')
        
        # Test other Claude models
        for model in claude_models:
            if model['modelId'] not in ['anthropic.claude-3-haiku-20240307-v1:0', 'anthropic.claude-sonnet-4-20250514-v1:0']:
                print(f"\n🧪 Testing {model['modelId']}...")
                test_model(model['modelId'])
        
    except Exception as e:
        print(f"❌ Bedrock access failed: {e}")

def test_model(model_id):
    """Test a specific model"""
    try:
        bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-east-1')
        
        response = bedrock_runtime.invoke_model(
            modelId=model_id,
            contentType='application/json',
            accept='application/json',
            body=json.dumps({
                'anthropic_version': 'bedrock-2023-05-31',
                'max_tokens': 50,
                'messages': [{'role': 'user', 'content': 'Hello, test message.'}]
            })
        )
        
        result = json.loads(response['body'].read().decode('utf-8'))
        print(f"   ✅ {model_id} - WORKING!")
        print(f"   Response: {result['content'][0]['text'][:100]}...")
        
        return True
        
    except Exception as e:
        print(f"   ❌ {model_id} - FAILED: {e}")
        return False

def check_lambda_permissions():
    """Check Lambda IAM permissions"""
    print(f"\n🔐 Checking Lambda IAM Permissions")
    print("=" * 35)
    
    try:
        # Get Lambda function details
        lambda_client = boto3.client('lambda', region_name='us-east-1')
        response = lambda_client.get_function(FunctionName='fresh-readme-generator')
        
        role_arn = response['Configuration']['Role']
        print(f"📋 Lambda Role: {role_arn}")
        
        # Check if role has Bedrock permissions
        iam = boto3.client('iam')
        role_name = role_arn.split('/')[-1]
        
        # Get attached policies
        policies = iam.list_attached_role_policies(RoleName=role_name)
        print(f"📄 Attached Policies:")
        for policy in policies['AttachedPolicies']:
            print(f"   • {policy['PolicyName']}")
        
        # Get inline policies
        inline_policies = iam.list_role_policies(RoleName=role_name)
        print(f"📝 Inline Policies:")
        for policy_name in inline_policies['PolicyNames']:
            print(f"   • {policy_name}")
        
    except Exception as e:
        print(f"❌ Permission check failed: {e}")

if __name__ == '__main__':
    debug_bedrock_access()
    check_lambda_permissions()
