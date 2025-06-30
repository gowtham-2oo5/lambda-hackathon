// Debug AWS API endpoints
// Run these in browser console or use Postman

const AWS_API_BASE = 'https://ccki297o82.execute-api.us-east-1.amazonaws.com/prod';

// Test 1: Check if API is accessible
console.log('🔍 Testing AWS API accessibility...');
fetch(`${AWS_API_BASE}/health`)
  .then(response => {
    console.log('Health check response:', response.status, response.statusText);
    return response.text();
  })
  .then(data => console.log('Health check data:', data))
  .catch(error => console.error('Health check failed:', error));

// Test 2: Check history endpoint (replace with your actual user email)
const testUserEmail = 'your-email@example.com'; // REPLACE THIS
console.log('🔍 Testing history endpoint...');
fetch(`${AWS_API_BASE}/history/${encodeURIComponent(testUserEmail)}`)
  .then(response => {
    console.log('History response:', response.status, response.statusText);
    return response.json();
  })
  .then(data => {
    console.log('History data:', data);
    if (data.items && data.items.length > 0) {
      console.log('First history item:', data.items[0]);
      console.log('First item keys:', Object.keys(data.items[0]));
      
      // Check for README content fields
      const firstItem = data.items[0];
      console.log('readmeContent:', firstItem.readmeContent);
      console.log('content:', firstItem.content);
      console.log('readmeS3Url:', firstItem.readmeS3Url);
    }
  })
  .catch(error => console.error('History fetch failed:', error));

// Test 3: Check CloudFront accessibility
const CLOUDFRONT_DOMAIN = 'd3in1w40kamst9.cloudfront.net';
console.log('🔍 Testing CloudFront accessibility...');
fetch(`https://${CLOUDFRONT_DOMAIN}/`)
  .then(response => {
    console.log('CloudFront response:', response.status, response.statusText);
    return response.text();
  })
  .then(data => console.log('CloudFront data length:', data.length))
  .catch(error => console.error('CloudFront failed:', error));

console.log('🔍 Check the console logs above for API responses');
