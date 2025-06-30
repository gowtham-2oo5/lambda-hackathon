// Simple test script to verify the API is working
const testUserId = "gowtham.ala.2oo5@gmail.com";

async function testAPI() {
  console.log("🧪 Testing API endpoints...");
  
  try {
    // Test the Next.js API route
    console.log("\n1. Testing Next.js API route:");
    const response = await fetch(`http://localhost:3000/api/history?userId=${encodeURIComponent(testUserId)}`);
    console.log("Status:", response.status);
    
    if (response.ok) {
      const data = await response.json();
      console.log("Response:", JSON.stringify(data, null, 2));
    } else {
      const errorText = await response.text();
      console.log("Error:", errorText);
    }
    
  } catch (error) {
    console.error("Test failed:", error);
  }
}

// Run the test if this is executed directly
if (typeof window === 'undefined') {
  testAPI();
}

module.exports = { testAPI };
