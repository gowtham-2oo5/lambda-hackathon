import { useState, useCallback } from "react";
import { toast } from "sonner";

// SECURE API INTEGRATION - NO AWS CREDENTIALS IN FRONTEND
const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_GATEWAY_URL ||
  "https://ccki297o82.execute-api.us-east-1.amazonaws.com/prod";
const CLOUDFRONT_URL =
  process.env.NEXT_PUBLIC_CLOUDFRONT_URL ||
  "https://d3in1w40kamst9.cloudfront.net";

export const useReadmeGeneratorSecure = () => {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [progress, setProgress] = useState(null);
  const [executionArn, setExecutionArn] = useState(null);

  // SECURE: Use API Gateway instead of direct AWS SDK calls
  const generateREADME = useCallback(async (githubUrl) => {
    setLoading(true);
    setError(null);
    setResult(null);
    setProgress("Starting analysis...");

    try {
      // Step 1: Start generation via API Gateway (SECURE)
      const response = await fetch(`${API_BASE_URL}/generate`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
        body: JSON.stringify({
          github_url: githubUrl,
          user_email: "demo@smartreadmegen.com", // You can get this from Cognito auth
        }),
      });

      if (!response.ok) {
        throw new Error(`API request failed: ${response.status}`);
      }

      const data = await response.json();
      setExecutionArn(data.executionArn);
      setProgress("Analysis started, monitoring progress...");

      // Step 2: Poll for completion (SECURE)
      await pollExecutionStatus(data.executionArn);
    } catch (err) {
      console.error("Generation error:", err);
      setError(err.message);
      toast.error("Generation failed", {
        description: err.message,
      });
    } finally {
      setLoading(false);
    }
  }, []);

  // SECURE: Poll execution status via API Gateway
  const pollExecutionStatus = async (executionArn) => {
    const maxAttempts = 60; // 5 minutes max
    let attempts = 0;

    const poll = async () => {
      try {
        attempts++;
        setProgress(`Checking progress... (${attempts}/${maxAttempts})`);

        // Use API Gateway status endpoint (SECURE)
        const statusResponse = await fetch(
          `${API_BASE_URL}/status/${encodeURIComponent(executionArn)}`,
          {
            method: "GET",
            headers: {
              Accept: "application/json",
            },
          }
        );

        if (!statusResponse.ok) {
          throw new Error(`Status check failed: ${statusResponse.status}`);
        }

        const statusData = await statusResponse.json();

        if (statusData.status === "SUCCEEDED") {
          const output = JSON.parse(statusData.output);
          setResult(output.body);
          setProgress("Analysis completed successfully!");
          toast.success("README analysis completed!");
          return;
        } else if (statusData.status === "FAILED") {
          throw new Error("Step Functions execution failed");
        } else if (statusData.status === "RUNNING" && attempts < maxAttempts) {
          // Continue polling
          setTimeout(poll, 5000); // Poll every 5 seconds
        } else {
          throw new Error("Execution timeout or unknown status");
        }
      } catch (err) {
        setError(err.message);
        toast.error("Status check failed", {
          description: err.message,
        });
      }
    };

    poll();
  };

  // SECURE: Get README URL via CloudFront (public CDN)
  const getREADMEUrl = useCallback((s3Key) => {
    if (!s3Key) return null;
    return `${CLOUDFRONT_URL}/${s3Key}`;
  }, []);

  // Reset state
  const reset = useCallback(() => {
    setLoading(false);
    setResult(null);
    setError(null);
    setProgress(null);
    setExecutionArn(null);
  }, []);

  return {
    generateREADME,
    getREADMEUrl,
    loading,
    result,
    error,
    progress,
    executionArn,
    reset,
  };
};
