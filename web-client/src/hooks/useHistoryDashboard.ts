import { useState, useEffect, useCallback } from "react";
import { toast } from "sonner";

export interface ReadmeHistoryItem {
  requestId: string;
  repoName: string;
  repoUrl: string;
  status: "processing" | "completed" | "failed";
  createdAt: string;
  completedAt?: string;
  processingTime?: number;
  projectType?: string;
  primaryLanguage?: string;
  frameworks?: string[];
  confidence?: number;
  readmeLength?: number;
  readmeS3Url?: string;
  error?: string;
  content?: string;
  userId?: string;
  generationTimestamp?: string;
  analysisMethod?: string;
  frameworkConfidence?: Record<string, number>;
  emailSent?: boolean;
  pipelineVersion?: string;
}

export const useHistoryDashboard = (userEmail: string) => {
  const [historyItems, setHistoryItems] = useState<ReadmeHistoryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [progress] = useState<string | null>(null);

  function processUrl(s3Url: string): string {
    if (s3Url.includes("d2j9jbqms8047w.cloudfront.net")) {
      s3Url = s3Url.replace(
        "d2j9jbqms8047w.cloudfront.net",
        "d3in1w40kamst9.cloudfront.net"
      );
    }

    console.log("changed Url: ", s3Url);
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

      console.log("🔍 FIXED DASHBOARD - Fetching history for user:", userEmail);

      // Use the Next.js API proxy to avoid CORS issues - FIXED
      const apiUrl = `/api/history?userId=${encodeURIComponent(userEmail)}`;
      console.log("🔍 FIXED DASHBOARD - API URL:", apiUrl);

      const response = await fetch(apiUrl, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
          "Cache-Control": "no-cache",
        },
      });

      console.log("🔍 FIXED DASHBOARD - Response status:", response.status);

      if (!response.ok) {
        const errorText = await response.text();
        console.error("❌ FIXED DASHBOARD - API Error:", errorText);
        throw new Error(
          `Failed to fetch history: ${response.status} - ${errorText}`
        );
      }

      const data = await response.json();
      console.log("🔍 FIXED DASHBOARD - Response data:", data);

      const items = data.items || [];
      console.log("🔍 FIXED DASHBOARD - History items count:", items.length);

      const transformedItems: ReadmeHistoryItem[] = items.map((item: any) => {
        console.log("🔍 FIXED DASHBOARD - Transforming item:", item);

        return {
          requestId: item.requestId,
          repoName: item.repoName,
          repoUrl: item.repoUrl,
          status: item.status || "completed",
          createdAt: item.createdAt,
          completedAt: item.completedAt || item.generationTimestamp,
          processingTime: item.processingTime,
          projectType: item.projectType,
          primaryLanguage: item.primaryLanguage,
          frameworks: Array.isArray(item.frameworks) ? item.frameworks : [],
          confidence:
            typeof item.confidence === "object"
              ? item.confidence.projectType || item.confidence.language || 0
              : item.confidence || 0,
          readmeLength: item.readmeLength,
          readmeS3Url: processUrl(item.readmeS3Url),
          error: item.error,
          userId: item.userId,
          generationTimestamp: item.generationTimestamp,
          analysisMethod: item.analysisMethod,
          frameworkConfidence: item.frameworkConfidence || {},
          emailSent: item.emailSent,
          pipelineVersion: item.pipelineVersion,
        };
      });

      // Sort by creation date (newest first)
      transformedItems.sort(
        (a, b) =>
          new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
      );

      setHistoryItems(transformedItems);
      console.log(
        "✅ FIXED DASHBOARD - Successfully loaded history items:",
        transformedItems.length
      );

      if (transformedItems.length === 0) {
        console.log("ℹ️ FIXED DASHBOARD - No history items found for user");
      }
    } catch (err) {
      console.error("❌ FIXED DASHBOARD - Error fetching history:", err);
      setError(err instanceof Error ? err.message : "Failed to fetch history");
      toast.error("Failed to load history");
    } finally {
      setLoading(false);
    }
  }, [userEmail]);

  const deleteHistoryItem = async (requestId: string) => {
    try {
      console.log("🗑️ FIXED DASHBOARD - Deleting history item:", requestId);

      // TODO: Implement actual deletion API call
      // For now, just remove from local state
      setHistoryItems((prev) =>
        prev.filter((item) => item.requestId !== requestId)
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

  // Refresh history every 30 seconds to catch new completions
  useEffect(() => {
    if (!userEmail) return;

    fetchHistory();

    const interval = setInterval(() => {
      console.log("🔄 FIXED DASHBOARD - Auto-refreshing history");
      fetchHistory();
    }, 30000); // 30 seconds

    return () => clearInterval(interval);
  }, [userEmail, fetchHistory]);

  return {
    historyItems,
    loading,
    error,
    progress,
    refetch: fetchHistory,
    deleteHistoryItem,
    copyToClipboard,
    downloadReadme,
  };
};
