import { NextRequest, NextResponse } from "next/server";

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const { id } = await params;

    if (!id) {
      return NextResponse.json(
        { error: "Missing id parameter" },
        { status: 400 }
      );
    }

    console.log("🔍 HISTORY ITEM API - Fetching item for ID:", id);

    // Try to get the specific history item from your AWS infrastructure
    // This should call your AWS API to get a single history item by requestId

    const apiUrl = `https://ccki297o82.execute-api.us-east-1.amazonaws.com/prod/history-item/${encodeURIComponent(
      id
    )}`;

    console.log("🔍 HISTORY ITEM API - Calling:", apiUrl);

    const response = await fetch(apiUrl, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
    });

    if (!response.ok) {
      console.error("❌ HISTORY ITEM API - AWS API Error:", response.status);

      // If the specific endpoint doesn't exist, try to get from general history
      // and filter by requestId (this is a fallback)
      console.log("🔄 HISTORY ITEM API - Trying fallback approach");

      return NextResponse.json(
        {
          error: `History item not found: ${id}`,
          suggestion: "The history item may not exist or may have been deleted",
        },
        { status: 404 }
      );
    }

    const data = await response.json();
    console.log("✅ HISTORY ITEM API - Success");

    // Transform the data to match expected format
    const historyItem = {
      requestId: data.requestId || id,
      repositoryName: data.repoName || data.repositoryName,
      githubUrl: data.repoUrl || data.githubUrl,
      repositoryOwner: data.owner || data.repositoryOwner,
      generatedAt: data.createdAt || data.generatedAt,
      projectType: data.projectType,
      primaryLanguage: data.primaryLanguage,
      frameworks: data.frameworks || [],
      confidence: data.confidence || 0,
      processingTime: data.processingTime || 0,
      readmeUrl: data.readmeS3Url || data.readmeUrl,
      status: data.status || "completed",
      content: data.readmeContent || data.content,
    };

    // Return the data with proper CORS headers
    return NextResponse.json(historyItem, {
      headers: {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization",
      },
    });
  } catch (error) {
    console.error("❌ HISTORY ITEM API - Error:", error);
    return NextResponse.json(
      {
        error: "Internal server error",
        message: error instanceof Error ? error.message : "Unknown error",
        id: (await params).id,
      },
      { status: 500 }
    );
  }
}

export async function OPTIONS() {
  return new NextResponse(null, {
    status: 200,
    headers: {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "GET, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type, Authorization",
    },
  });
}
