import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  try {
    console.log('🧪 TEST API - Testing history proxy');
    
    // Test with a known user email
    const testUserId = 'test@example.com';
    
    // Call our proxy API
    const proxyUrl = `${request.nextUrl.origin}/api/history?userId=${encodeURIComponent(testUserId)}`;
    console.log('🧪 TEST API - Calling proxy:', proxyUrl);
    
    const response = await fetch(proxyUrl);
    const data = await response.json();
    
    return NextResponse.json({
      success: true,
      proxyResponse: data,
      message: 'Proxy test completed'
    });
    
  } catch (error) {
    console.error('❌ TEST API - Error:', error);
    return NextResponse.json(
      { error: 'Test failed', message: error instanceof Error ? error.message : 'Unknown error' },
      { status: 500 }
    );
  }
}
