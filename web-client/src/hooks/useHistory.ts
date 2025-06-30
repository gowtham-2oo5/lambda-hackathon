import { useState, useEffect, useCallback } from "react";
import { toast } from "sonner";

export interface ReadmeHistoryItem {
  requestId: string;
  repoId: string;
  repoName: string;
  repoUrl: string;
  repoOwner: string;
  status: "processing" | "completed" | "failed";
  createdAt: string;
  updatedAt: string;
  completedAt?: string;
  processingTime?: number;
  projectType?: string;
  primaryLanguage?: string;
  frameworks?: string[];
  techStack?: string[];
  confidence?: number;
  confidenceScore?: number;
  accuracyPercentage?: number;
  accuracyLevel?: string;
  readmeLength?: number;
  readmeS3Url?: string; // Keep for backward compatibility
  readmeUrl?: string; // New field name
  readmeContent?: string;
  readmePreview?: string;
  error?: string;
  content?: string;
  userId?: string;
  generationTimestamp?: string;
  analysisMethod?: string;
  generationMethod?: string;
  frameworkConfidence?: Record<string, number>;
  emailSent?: boolean;
  pipelineVersion?: string;
  version?: string;
  branchUsed?: string;
  filesAnalyzedCount?: number;
  sourceFilesAnalyzed?: string[];
  analysisComplete?: boolean;
  realContentAnalyzed?: boolean;
  hallucinationPrevented?: boolean;
  qualityScore?: string;
  accuracyBreakdown?: any;
  performanceMetrics?: any;
  s3Location?: {
    bucket: string;
    key: string;
  };
  ttl?: number;
  lastAccessedAt?: string;
}

export const useHistory = (userEmail: string, shouldPoll: boolean = false) => {
  const [historyItems, setHistoryItems] = useState<ReadmeHistoryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [progress] = useState<string | null>(null);
  const [initialLoadComplete, setInitialLoadComplete] = useState(false);

  function processUrl(s3Url: string): string {
    if (s3Url.includes("d2j9jbqms8047w.cloudfront.net")) {
      s3Url = s3Url.replace(
        "d2j9jbqms8047w.cloudfront.net",
        "d3in1w40kamst9.cloudfront.net"
      );
    } else console.log("NO NEED ");
    return s3Url;
  }

  const fetchHistory = useCallback(async () => {
    if (!userEmail) {
      setLoading(false);
      return;
    }

    try {
      setLoading(true);
      setError(null);

      console.log("🔍 HISTORY HOOK - Fetching history for user:", userEmail);

      // Use the Next.js API proxy to avoid CORS issues
      const apiUrl = `/api/history?userId=${encodeURIComponent(userEmail)}`;
      console.log("🔍 HISTORY HOOK - API URL:", apiUrl);

      const response = await fetch(apiUrl, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
          "Cache-Control": "no-cache",
        },
      });

      console.log("🔍 HISTORY HOOK - Response status:", response.status);

      if (!response.ok) {
        const errorText = await response.text();
        console.error("❌ HISTORY HOOK - API Error:", errorText);
        throw new Error(
          `Failed to fetch history: ${response.status} - ${errorText}`
        );
      }

      const data = await response.json();
      console.log("🔍 HISTORY HOOK - Response data:", data);
      console.log("🔍 HISTORY HOOK - data.data:", data?.data);
      console.log("🔍 HISTORY HOOK - data.data.records:", data?.data?.records);
      console.log("🔍 HISTORY HOOK - data.data.history:", data?.data?.history);

      // Handle the correct API response structure: data.data.records (not history)
      const items = data?.data?.records || data?.data?.history || [];
      console.log("🔍 HISTORY HOOK - History items count:", items.length);

      const transformedItems: ReadmeHistoryItem[] = items.map((item: any) => {
        console.log("🔍 HISTORY HOOK - Transforming item:", item);

        return {
          // Primary identifiers - API already provides these correctly
          requestId: item.requestId || item.repoId,
          repoId: item.repoId,
          repoName: item.repoName,
          repoUrl: item.repoUrl,
          repoOwner: item.repoOwner,
          
          // Status and timing
          status: item.status || "completed",
          createdAt: item.createdAt,
          updatedAt: item.updatedAt,
          completedAt: item.updatedAt || item.createdAt,
          processingTime: Number(item.processingTime || 0),
          
          // Project analysis
          projectType: item.projectType || "software_project",
          primaryLanguage: item.primaryLanguage || "Mixed",
          frameworks: Array.isArray(item.frameworks) ? item.frameworks : [],
          techStack: Array.isArray(item.techStack) ? item.techStack : [],
          
          // Quality metrics
          confidence: Number(item.confidence || item.confidenceScore || 0),
          confidenceScore: Number(item.confidenceScore || item.confidence || 0),
          accuracyPercentage: Number(item.accuracyPercentage || 0),
          accuracyLevel: item.accuracyLevel || "basic",
          qualityScore: item.qualityScore || "basic",
          
          // README content - API provides readmeUrl directly
          readmeLength: Number(item.readmeLength || 0),
          readmeS3Url: processUrl(item.readmeUrl || ""), // For backward compatibility
          readmeUrl: item.readmeUrl || "",
          readmeContent: item.readmeContent,
          readmePreview: item.readmePreview,
          
          // Analysis details
          analysisMethod: item.analysisMethod || item.generationMethod,
          generationMethod: item.generationMethod || item.analysisMethod,
          filesAnalyzedCount: Number(item.filesAnalyzedCount || 0),
          sourceFilesAnalyzed: Array.isArray(item.sourceFilesAnalyzed) ? item.sourceFilesAnalyzed : [],
          analysisComplete: item.analysisComplete || false,
          realContentAnalyzed: item.realContentAnalyzed || false,
          hallucinationPrevented: item.hallucinationPrevented || false,
          
          // System metadata
          userId: item.userId,
          version: item.version,
          branchUsed: item.branchUsed || "main",
          pipelineVersion: item.pipelineVersion,
          
          // Complex objects
          accuracyBreakdown: item.accuracyBreakdown,
          performanceMetrics: item.performanceMetrics,
          s3Location: item.s3Location,
          frameworkConfidence: item.frameworkConfidence || {},
          
          // Additional fields
          error: item.error,
          emailSent: item.emailSent,
          ttl: item.ttl,
          lastAccessedAt: item.lastAccessedAt,
          
          // Legacy fields for backward compatibility
          generationTimestamp: item.updatedAt || item.createdAt,
        };
      });

      // Sort by creation date (newest first)
      transformedItems.sort(
        (a, b) =>
          new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
      );

      setHistoryItems(transformedItems);
      setInitialLoadComplete(true);
      console.log(
        "✅ HISTORY HOOK - Successfully loaded history items:",
        transformedItems.length
      );

      if (transformedItems.length === 0) {
        console.log("ℹ️ HISTORY HOOK - No history items found for user");
      }
    } catch (err) {
      console.error("❌ HISTORY HOOK - Error fetching history:", err);
      setError(err instanceof Error ? err.message : "Failed to fetch history");
      toast.error("Failed to load history");
    } finally {
      setLoading(false);
    }
  }, [userEmail]);

  const deleteHistoryItem = async (identifier: string) => {
    try {
      console.log("🗑️ HISTORY HOOK - Deleting history item:", identifier);

      // TODO: Implement actual deletion API call
      // For now, just remove from local state using either repoId or requestId
      setHistoryItems((prev) =>
        prev.filter((item) => 
          item.repoId !== identifier && 
          item.requestId !== identifier
        )
      );
      toast.success("History item deleted");
    } catch (err) {
      console.error("❌ Error deleting history item:", err);
      toast.error("Failed to delete history item");
    }
  };

  const copyToClipboard = async (content: string) => {
    try {
      await navigator.clipboard.writeText(content);
      toast.success("Copied to clipboard!");
    } catch (err) {
      console.error("❌ Error copying to clipboard:", err);
      toast.error("Failed to copy to clipboard");
    }
  };

  const downloadReadme = (content: string, repoName: string) => {
    try {
      const blob = new Blob([content], { type: "text/markdown" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `${repoName.replace("/", "-")}-README.md`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
      toast.success("README downloaded!");
    } catch (err) {
      console.error("❌ Error downloading README:", err);
      toast.error("Failed to download README");
    }
  };

  // Smart polling logic: only poll when needed
  useEffect(() => {
    if (!userEmail) return;

    // Always fetch on initial load
    if (!initialLoadComplete) {
      console.log("🚀 HISTORY HOOK - Initial load for user:", userEmail);
      fetchHistory();
      return;
    }

    // Only set up polling if shouldPoll is true (during generation)
    if (shouldPoll) {
      console.log("🔄 HISTORY HOOK - Starting polling (generation in progress)");
      
      const interval = setInterval(() => {
        console.log("🔄 HISTORY HOOK - Polling for updates during generation");
        fetchHistory();
      }, 10000); // Poll every 10 seconds during generation

      return () => {
        console.log("🛑 HISTORY HOOK - Stopping polling (generation completed)");
        clearInterval(interval);
      };
    } else {
      console.log("ℹ️ HISTORY HOOK - No polling needed (no active generation)");
    }
  }, [userEmail, fetchHistory, shouldPoll, initialLoadComplete]);

  return {
    historyItems,
    loading,
    error,
    progress,
    refetch: fetchHistory,
    deleteHistoryItem,
    copyToClipboard,
    downloadReadme,
    initialLoadComplete,
  };
};
