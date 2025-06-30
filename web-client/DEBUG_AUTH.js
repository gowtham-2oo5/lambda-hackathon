// Quick debug script to check authentication state
// Run this in browser console to see what's stored

console.log('🔍 DEBUG: Checking authentication state...');

console.log('📦 localStorage contents:');
console.log('- cognito_tokens:', localStorage.getItem('cognito_tokens'));
console.log('- auth_token:', localStorage.getItem('auth_token'));
console.log('- user_data:', localStorage.getItem('user_data'));

try {
  const tokens = JSON.parse(localStorage.getItem('cognito_tokens') || '{}');
  console.log('🔑 Parsed tokens:', tokens);
  
  const userData = JSON.parse(localStorage.getItem('user_data') || '{}');
  console.log('👤 Parsed user data:', userData);
  
  if (userData.sub) {
    console.log('✅ User ID found:', userData.sub);
  } else {
    console.log('❌ No user ID found');
  }
  
  if (tokens.accessToken) {
    console.log('✅ Access token found (length):', tokens.accessToken.length);
  } else {
    console.log('❌ No access token found');
  }
  
} catch (error) {
  console.error('❌ Error parsing stored data:', error);
}

console.log('🔍 DEBUG: Authentication check complete');
