import { useState, useCallback } from "react";
import { cognitoAuth } from "../lib/cognito";
import { toast } from "sonner";

// SECURE: Use API Gateway endpoints instead of direct AWS SDK
const API_BASE_URL =
  "https://ccki297o82.execute-api.us-east-1.amazonaws.com/prod";

export const useReadmeGenerator = () => {
  const [loading, setLoading] = useState<boolean>(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [progress, setProgress] = useState<string | null>(null);
  const [executionArn, setExecutionArn] = useState<string | null>(null);

  // Get auth headers for API calls
  const getAuthHeaders = useCallback(async (): Promise<
    Record<string, string>
  > => {
    try {
      const tokens = JSON.parse(localStorage.getItem("cognito_tokens") || "{}");
      if (!tokens?.accessToken) {
        throw new Error("No access token found");
      }

      return {
        "Content-Type": "application/json",
        Authorization: `Bearer ${tokens.accessToken}`,
        Accept: "application/json",
      };
    } catch (error) {
      console.error("Auth headers error:", error);
      throw new Error("Authentication required");
    }
  }, []);

  // Create initial DynamoDB record for processing tracking
  const createInitialRecord = useCallback(
    async (githubUrl: string, userEmail: string, executionArn: string) => {
      try {
        const headers = await getAuthHeaders();
        const repoName = githubUrl.split("/").slice(-2).join("/");
        const requestId =
          executionArn.split(":").pop() || Date.now().toString();

        const initialRecord = {
          userId: userEmail,
          requestId: requestId,
          repoName: repoName,
          repoUrl: githubUrl,
          status: "processing",
          createdAt: new Date().toISOString(),
          executionArn: executionArn,
          pipelineVersion: "ultimate_enterprise_v1.0",
        };

        console.log("🔧 Creating initial DynamoDB record:", initialRecord);

        const response = await fetch(`${API_BASE_URL}/history`, {
          method: "POST",
          headers,
          body: JSON.stringify(initialRecord),
        });

        if (!response.ok) {
          console.warn("⚠️ Failed to create initial record, continuing anyway");
        } else {
          console.log("✅ Initial processing record created successfully");
        }
      } catch (error) {
        console.warn("⚠️ Error creating initial record:", error);
        // Don't throw - this is not critical for the generation process
      }
    },
    [getAuthHeaders]
  );

  // SECURE: Poll for completion using API Gateway
  const pollForCompletion = useCallback(
    async (arn: string) => {
      let attempts = 0;
      const maxAttempts = 60; // 5 minutes with 5-second intervals

      console.log("🔧 Starting polling for execution ARN:", arn);

      const poll = async () => {
        try {
          attempts++;
          setProgress(`🔄 Processing... (${attempts}/${maxAttempts})`);

          // SECURE: Use API Gateway status endpoint with executionArn in path
          const headers = await getAuthHeaders();

          // FIXED: No encoding needed - API Gateway handles ARN directly
          const statusUrl = `${API_BASE_URL}/status/${arn}`;

          console.log("🔧 Original ARN:", arn);
          console.log("🔧 Polling status URL:", statusUrl);

          const statusResponse = await fetch(statusUrl, {
            method: "GET",
            headers,
          });

          console.log("🔧 Status response status:", statusResponse.status);
          console.log(
            "🔧 Status response headers:",
            Object.fromEntries(statusResponse.headers.entries())
          );

          if (!statusResponse.ok) {
            const errorText = await statusResponse.text();
            console.error("🔧 Status response error:", errorText);
            throw new Error(
              `Status check failed: ${statusResponse.status} - ${errorText}`
            );
          }

          const statusData = await statusResponse.json();
          console.log("🔧 Status check result:", statusData);

          // Handle different response structures
          if (statusData.status === "FAILED" || statusData.cause) {
            // Handle Step Functions execution failures
            console.error("🚨 Step Functions execution failed:", statusData);

            // Extract error message from the nested structure
            const errorMessage =
              statusData.cause || statusData.error || "Unknown workflow error";

            // Parse the error to provide user-friendly messages
            if (errorMessage.includes("JSONPath")) {
              throw new Error(
                "Internal workflow configuration error. The backend service needs to be updated."
              );
            } else if (errorMessage.includes("Lambda")) {
              throw new Error(
                "Service temporarily unavailable. Please try again in a few moments."
              );
            } else if (errorMessage.includes("States.Runtime")) {
              throw new Error(
                "Workflow execution error. Please try again or contact support."
              );
            } else {
              throw new Error(`README generation failed: ${errorMessage}`);
            }
          }

          if (statusData.status === "SUCCEEDED") {
            let output;
            try {
              // Handle both string and object outputs
              if (typeof statusData.output === "string") {
                output = JSON.parse(statusData.output);
              } else {
                output = statusData.output;
              }

              // If output has a body field, extract it
              if (output && output.body && typeof output.body === "object") {
                output = output.body;
              }

              console.log("🔧 Parsed output:", output);
            } catch (parseError) {
              console.log(
                "🔧 Output parsing failed, using as-is:",
                statusData.output
              );
              output = statusData;
            }

            setProgress("✅ README generation completed!");
            setResult(output);
            setLoading(false);

            toast.success("🎉 README Generated Successfully!", {
              description: `Analysis completed successfully`,
            });
          } else if (statusData.status === "FAILED") {
            const errorMessage =
              statusData.error || "Step Functions execution failed";
            setError(errorMessage);
            setLoading(false);
            toast.error("Generation failed", {
              description: errorMessage,
            });
          } else if (
            (statusData.status === "RUNNING" ||
              statusData.status === "EXECUTING") &&
            attempts < maxAttempts
          ) {
            console.log(`🔧 Still running, attempt ${attempts}/${maxAttempts}`);
            setTimeout(poll, 5000);
          } else if (attempts >= maxAttempts) {
            setError("Execution timeout - process took too long to complete");
            setLoading(false);
            toast.error("Generation timeout", {
              description: "Process took too long to complete (5 minutes)",
            });
          } else {
            console.log("🔧 Unknown status:", statusData.status);
            setError(`Unknown execution status: ${statusData.status}`);
            setLoading(false);
            toast.error("Unknown status", {
              description: `Execution status: ${statusData.status}`,
            });
          }
        } catch (err: any) {
          console.error("🔧 Polling error:", err);

          // If it's an authentication error, don't retry
          if (
            err.message.includes("Authentication") ||
            err.message.includes("401") ||
            err.message.includes("403")
          ) {
            setError("Authentication failed - please sign in again");
            setLoading(false);
            toast.error("Authentication failed", {
              description: "Please sign in again",
            });
            return;
          }

          // For other errors, retry a few times before giving up
          if (attempts < 3) {
            console.log(
              `🔧 Retrying after error (attempt ${attempts}/3):`,
              err.message
            );
            setTimeout(poll, 20000); // Wait 10 seconds before retry
          } else {
            setError(err.message);
            setLoading(false);
            toast.error("Status check failed", {
              description: err.message,
            });
          }
        }
      };

      // Start polling immediately
      poll();
    },
    [getAuthHeaders]
  );

  // SECURE: Generate README using API Gateway
  const generateREADME = useCallback(
    async (githubUrl: string) => {
      setLoading(true);
      setError(null);
      setResult(null);
      setProgress("🚀 Starting README generation...");

      console.log("🔧 Starting README generation for:", githubUrl);

      try {
        // Get user email from Cognito if available
        let userEmail = "demo@smartreadmegen.com";
        try {
          const user = cognitoAuth.getStoredUser();
          if (user?.email) {
            userEmail = user.email;
            console.log("🔧 Using user email:", userEmail);
          }
        } catch {
          console.log("🔧 No Cognito user found, using demo email");
        }

        // SECURE: Use API Gateway instead of direct AWS SDK
        const headers = await getAuthHeaders();
        console.log("🔧 Auth headers prepared");

        setProgress("🎯 Initializing enterprise analysis pipeline...");

        const requestBody = {
          github_url: githubUrl,
          user_email: userEmail,
          phase: 3,
          version: "ultimate_enterprise_v1.0",
          features: [
            "real_time_learning",
            "pattern_intelligence",
            "multi_model_consensus",
            "predictive_analysis",
            "enterprise_validation",
          ],
        };

        console.log("🔧 Request body:", requestBody);
        console.log("🔧 Making request to:", `${API_BASE_URL}/generate`);

        // SECURE: Call API Gateway generate endpoint
        const response = await fetch(`${API_BASE_URL}/generate`, {
          method: "POST",
          headers,
          body: JSON.stringify(requestBody),
        });

        console.log("🔧 Generate response status:", response.status);
        console.log(
          "🔧 Generate response headers:",
          Object.fromEntries(response.headers.entries())
        );

        if (!response.ok) {
          const errorText = await response.text();
          console.error("🔧 Generate response error:", errorText);

          let errorMessage;
          try {
            const errorData = JSON.parse(errorText);
            errorMessage =
              errorData.message ||
              errorData.error ||
              `API request failed: ${response.status}`;
          } catch {
            errorMessage = `API request failed: ${response.status} - ${errorText}`;
          }

          throw new Error(errorMessage);
        }

        const data = await response.json();
        console.log("🔧 Generate API response:", data);

        if (data.executionArn) {
          setExecutionArn(data.executionArn);
          setProgress("🚀 Generation started - creating tracking record...");
          console.log(
            "🔧 Starting polling for execution ARN:",
            data.executionArn
          );

          // Create initial DynamoDB record with processing status
          await createInitialRecord(githubUrl, userEmail, data.executionArn);

          // Poll for completion using secure API Gateway
          await pollForCompletion(data.executionArn);
        } else {
          console.error("🔧 No execution ARN in response:", data);
          throw new Error(
            "No execution ARN returned from API - generation may not have started properly"
          );
        }
      } catch (err: any) {
        console.error("🔧 Generation error:", err);
        setError(err.message || "Generation failed");
        setLoading(false);
        toast.error("Generation failed", {
          description: err.message,
        });
      }
    },
    [pollForCompletion, getAuthHeaders, createInitialRecord]
  );

  // Get README URL via CloudFront (public CDN)
  const getREADMEUrl = useCallback((s3Key: string) => {
    if (!s3Key) return null;
    return `https://d3in1w40kamst9.cloudfront.net/${s3Key}`;
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
