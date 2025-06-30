// Test file to verify Cognito authentication
import { cognitoAuth } from './cognito';

export async function testCognitoAuth() {
  console.log('Testing Cognito Authentication...');
  console.log('Config:', cognitoAuth.getConfig());
  
  // Test sign up
  try {
    const signUpResult = await cognitoAuth.signUp('test@example.com', 'TempPass123!', 'Test User');
    console.log('Sign up result:', signUpResult);
  } catch (error) {
    console.error('Sign up error:', error);
  }
}

// Call this function from browser console to test
(window as any).testCognitoAuth = testCognitoAuth;
