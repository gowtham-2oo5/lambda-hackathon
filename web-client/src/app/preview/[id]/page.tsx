"use client";

import React, { useState, useEffect, Suspense } from "react";
import { useParams, useSearchParams, useRouter } from "next/navigation";
import { Loader2 } from "lucide-react";
import NaturalReadmePreview from "@/components/NaturalReadmePreview";

interface PreviewData {
  id: string;
  content: string;
  metadata: {
    repoName: string;
    repoUrl: string;
    owner: string;
    generatedAt: string;
    projectType: string;
    primaryLanguage: string;
    frameworks: string[];
    confidence: number;
    processingTime: number;
  };
  stats: {
    characters: number;
    words: number;
    lines: number;
    headings: number;
  };
}

const PreviewPageContent = () => {
  const params = useParams();
  const searchParams = useSearchParams();
  const router = useRouter();

  const [previewData, setPreviewData] = useState<PreviewData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Extract preview ID and source
  const previewId = params.id as string;
  const source = searchParams.get("source") || "history";
  const userEmail = searchParams.get("user") || "";
  const s3Key = searchParams.get("s3Key"); // Keep this for backward compatibility
  const repoUrl = searchParams.get("repo");

  useEffect(() => {
    console.log("🔍 Preview page mounted with params:", {
      previewId,
      source,
      userEmail,
      s3Key,
      repoUrl,
      searchParams: Object.fromEntries(searchParams.entries()),
    });
    fetchPreviewData();
  }, [previewId, source, s3Key, userEmail]);

  const fetchPreviewData = async () => {
    setLoading(true);
    setError(null);

    try {
      let data: PreviewData;

      if (source === "direct" && s3Key) {
        // Fetch directly from S3/CloudFront
        data = await fetchFromS3(s3Key);
      } else if (source === "history") {
        // Fetch from history API
        data = await fetchFromHistory(previewId);
      } else {
        // Try to reconstruct from URL params
        data = await fetchFromParams();
      }

      setPreviewData(data);
    } catch (err) {
      console.error("Error fetching preview data:", err);
      setError(
        err instanceof Error ? err.message : "Failed to load README preview"
      );
    } finally {
      setLoading(false);
    }
  };

  const fetchFromS3 = async (s3Key: string): Promise<PreviewData> => {
    // First try CloudFront
    const cloudFrontUrl = `https://d3in1w40kamst9.cloudfront.net/${s3Key}`;

    try {
      console.log("🔍 Attempting to fetch from CloudFront:", cloudFrontUrl);
      const response = await fetch(cloudFrontUrl, {
        method: "GET",
        headers: {
          Accept: "text/markdown,text/plain,*/*",
          "Cache-Control": "no-cache",
        },
      });

      if (response.ok) {
        const content = await response.text();
        console.log("✅ Successfully fetched from CloudFront");

        return {
          id: previewId,
          content,
          metadata: {
            repoName: searchParams.get("name") || "Unknown Repository",
            repoUrl: repoUrl || "",
            owner: searchParams.get("owner") || "Unknown",
            generatedAt: new Date().toISOString(),
            projectType: searchParams.get("type") || "Unknown",
            primaryLanguage: searchParams.get("lang") || "Unknown",
            frameworks: searchParams.get("frameworks")?.split(",") || [],
            confidence: parseFloat(searchParams.get("confidence") || "0"),
            processingTime: parseFloat(searchParams.get("time") || "0"),
          },
          stats: {
            characters: 0,
            words: 0,
            lines: 0,
            headings: 0,
          },
        };
      } else {
        console.warn(
          `⚠️ CloudFront fetch failed: ${response.status} - ${response.statusText}`
        );
      }
    } catch (error) {
      console.warn("⚠️ CloudFront fetch error:", error);
    }

    // Fallback to mock data for demo purposes
    console.log("🔄 Falling back to mock data for demo");
    const mockResponse = await fetch("/api/mock-readme");
    const mockData = await mockResponse.json();

    return {
      id: previewId,
      content: mockData.content,
      metadata: {
        ...mockData.metadata,
        repoName: searchParams.get("name") || mockData.metadata.repoName,
        repoUrl: repoUrl || mockData.metadata.repoUrl,
        owner: searchParams.get("owner") || mockData.metadata.owner,
        projectType: searchParams.get("type") || mockData.metadata.projectType,
        primaryLanguage:
          searchParams.get("lang") || mockData.metadata.primaryLanguage,
        frameworks:
          searchParams.get("frameworks")?.split(",") ||
          mockData.metadata.frameworks,
        confidence: parseFloat(
          searchParams.get("confidence") || String(mockData.metadata.confidence)
        ),
        processingTime: parseFloat(
          searchParams.get("time") || String(mockData.metadata.processingTime)
        ),
      },
      stats: {
        characters: 0,
        words: 0,
        lines: 0,
        headings: 0,
      },
    };
  };

  const fetchFromHistory = async (id: string): Promise<PreviewData> => {
    try {
      console.log("🔍 Attempting to fetch from history API:", id);
      const response = await fetch(`/api/history/${id}`);

      if (!response.ok) {
        console.warn(`⚠️ History API failed: ${response.status}`);
        throw new Error("Failed to fetch from history");
      }

      const historyItem = await response.json();
      console.log("✅ Successfully fetched history item");

      // Try to fetch the actual README content
      try {
        const contentResponse = await fetch(historyItem.readmeUrl);
        if (contentResponse.ok) {
          const content = await contentResponse.text();

          return {
            id,
            content,
            metadata: {
              repoName: historyItem.repositoryName,
              repoUrl: historyItem.githubUrl,
              owner: historyItem.repositoryOwner,
              generatedAt: historyItem.generatedAt,
              projectType: historyItem.projectType,
              primaryLanguage: historyItem.primaryLanguage,
              frameworks: historyItem.frameworks || [],
              confidence: historyItem.confidence || 0,
              processingTime: historyItem.processingTime || 0,
            },
            stats: {
              characters: 0,
              words: 0,
              lines: 0,
              headings: 0,
            },
          };
        } else {
          console.warn("⚠️ README content fetch failed, using mock data");
        }
      } catch (contentError) {
        console.warn("⚠️ Error fetching README content:", contentError);
      }

      // Fallback to mock data with history metadata
      const mockResponse = await fetch("/api/mock-readme");
      const mockData = await mockResponse.json();

      return {
        id,
        content: mockData.content,
        metadata: {
          repoName: historyItem.repositoryName || mockData.metadata.repoName,
          repoUrl: historyItem.githubUrl || mockData.metadata.repoUrl,
          owner: historyItem.repositoryOwner || mockData.metadata.owner,
          generatedAt: historyItem.generatedAt || mockData.metadata.generatedAt,
          projectType: historyItem.projectType || mockData.metadata.projectType,
          primaryLanguage:
            historyItem.primaryLanguage || mockData.metadata.primaryLanguage,
          frameworks: historyItem.frameworks || mockData.metadata.frameworks,
          confidence: historyItem.confidence || mockData.metadata.confidence,
          processingTime:
            historyItem.processingTime || mockData.metadata.processingTime,
        },
        stats: {
          characters: 0,
          words: 0,
          lines: 0,
          headings: 0,
        },
      };
    } catch (error) {
      console.warn("⚠️ History fetch failed, using mock data:", error);

      // Complete fallback to mock data
      const mockResponse = await fetch("/api/mock-readme");
      const mockData = await mockResponse.json();

      return {
        id,
        content: mockData.content,
        metadata: mockData.metadata,
        stats: {
          characters: 0,
          words: 0,
          lines: 0,
          headings: 0,
        },
      };
    }
  };

  const fetchFromParams = async (): Promise<PreviewData> => {
    // For demo purposes, fetch mock data
    if (previewId.includes("demo") || previewId.includes("example")) {
      const response = await fetch("/api/mock-readme");
      const mockData = await response.json();

      return {
        id: previewId,
        content: mockData.content,
        metadata: mockData.metadata,
        stats: {
          characters: 0,
          words: 0,
          lines: 0,
          headings: 0,
        },
      };
    }

    throw new Error("Invalid preview URL - missing required parameters");
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="h-12 w-12 animate-spin text-blue-600 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-gray-900 mb-2">
            Loading README Preview
          </h2>
          <p className="text-gray-600">Fetching content from our servers...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-red-50 to-pink-100 flex items-center justify-center">
        <div className="text-center max-w-md">
          <div className="h-12 w-12 text-red-500 mx-auto mb-4">❌</div>
          <h2 className="text-xl font-semibold text-red-700 mb-2">
            Failed to Load Preview
          </h2>
          <p className="text-gray-600 mb-4">{error}</p>
          <button
            onClick={() => router.back()}
            className="px-4 py-2 bg-gray-600 text-white rounded hover:bg-gray-700"
          >
            ← Go Back
          </button>
        </div>
      </div>
    );
  }

  if (!previewData) {
    return null;
  }

  return (
    <NaturalReadmePreview
      content={previewData.content}
      metadata={previewData.metadata}
    />
  );
};

const PreviewPage = () => {
  return (
    <Suspense
      fallback={
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
          <Loader2 className="h-8 w-8 animate-spin text-blue-600" />
        </div>
      }
    >
      <PreviewPageContent />
    </Suspense>
  );
};

export default PreviewPage;
