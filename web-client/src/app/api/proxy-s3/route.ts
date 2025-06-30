import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const s3Url = searchParams.get('url');
    
    if (!s3Url) {
      return NextResponse.json(
        { error: 'Missing url parameter' },
        { status: 400 }
      );
    }

    console.log('🔍 S3 PROXY - Fetching from:', s3Url);
    
    // Fetch from S3/CloudFront without CORS restrictions (server-side)
    const response = await fetch(s3Url, {
      method: 'GET',
      headers: {
        'Accept': 'text/markdown,text/plain,*/*',
        'User-Agent': 'SmartReadmeGen-Proxy/1.0'
      }
    });

    if (!response.ok) {
      console.error('❌ S3 PROXY - Fetch failed:', response.status, response.statusText);
      return NextResponse.json(
        { 
          error: `Failed to fetch from S3: ${response.status} ${response.statusText}`,
          url: s3Url
        },
        { status: response.status }
      );
    }

    const content = await response.text();
    console.log('✅ S3 PROXY - Successfully fetched content, length:', content.length);
    
    // Return the content with proper CORS headers
    return NextResponse.json({ 
      content,
      source: 'proxy',
      url: s3Url
    }, {
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
      }
    });
    
  } catch (error) {
    console.error('❌ S3 PROXY - Error:', error);
    return NextResponse.json(
      { 
        error: 'Internal server error', 
        message: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
}

export async function OPTIONS() {
  return new NextResponse(null, {
    status: 200,
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    },
  });
}
