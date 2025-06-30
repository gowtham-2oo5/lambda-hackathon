import { useState, useCallback } from "react";
import { toast } from "sonner";

// FIXED: Use the secure API Gateway approach instead of direct AWS SDK
const API_BASE_URL =
  "https://ccki297o82.execute-api.us-east-1.amazonaws.com/prod";
const CLOUDFRONT_URL = "https://d3in1w40kamst9.cloudfront.net";

export const useReadmeGeneratorFixed = () => {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [progress, setProgress] = useState(null);
  const [executionArn, setExecutionArn] = useState(null);

  // FIXED: Declare pollForCompletion FIRST before using it
  const pollForCompletion = useCallback(async (arn) => {
    let attempts = 0;
    const maxAttempts = 60; // 5 minutes with 5-second intervals

    const poll = async () => {
      try {
        attempts++;
        setProgress(`🔄 Processing... (${attempts}/${maxAttempts})`);

        // Use API Gateway status endpoint (SECURE)
        const statusResponse = await fetch(
          `${API_BASE_URL}/status/${encodeURIComponent(arn)}`,
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
          setProgress("✅ README generation completed!");
          setResult(output.body);
          setLoading(false);

          toast.success("🎉 README Generated Successfully!", {
            description: `Analysis completed with high confidence`,
          });
        } else if (statusData.status === "FAILED") {
          setError("Step Functions execution failed");
          setLoading(false);
          toast.error("Generation failed", {
            description: "Step Functions workflow failed",
          });
        } else if (statusData.status === "RUNNING" && attempts < maxAttempts) {
          setTimeout(poll, 5000); // Poll every 5 seconds
        } else {
          setError("Execution timeout or unknown status");
          setLoading(false);
          toast.error("Generation timeout", {
            description: "Process took too long to complete",
          });
        }
      } catch (err) {
        console.error("Polling error:", err);
        setError(err.message);
        setLoading(false);
        toast.error("Status check failed", {
          description: err.message,
        });
      }
    };

    poll();
  }, []);

  // FIXED: Now generateREADME can use pollForCompletion since it's declared above
  const generateREADME = useCallback(
    async (githubUrl) => {
      setLoading(true);
      setError(null);
      setResult(null);
      setProgress("🚀 Starting README generation...");

      try {
        // Use API Gateway instead of direct AWS SDK (SECURE)
        const response = await fetch(`${API_BASE_URL}/generate`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
          },
          body: JSON.stringify({
            github_url: githubUrl,
            user_email: "demo@smartreadmegen.com",
          }),
        });

        if (!response.ok) {
          throw new Error(`API request failed: ${response.status}`);
        }

        const data = await response.json();
        setExecutionArn(data.executionArn);
        setProgress("Analysis started, monitoring progress...");

        // Poll for completion - NOW this will work since pollForCompletion is declared above
        await pollForCompletion(data.executionArn);
      } catch (err) {
        console.error("Generation error:", err);
        setError(err.message || "Generation failed");
        setLoading(false);
        toast.error("Generation failed", {
          description: err.message,
        });
      }
    },
    [pollForCompletion]
  ); // Now this dependency is valid

  // Get README URL via CloudFront (public CDN)
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
