import { useState, useCallback } from "react";
import { cognitoAuth } from "../lib/cognito";
import { toast } from "sonner";

// Dynamic AWS SDK imports to avoid build-time issues
let SFNClient, StartExecutionCommand, DescribeExecutionCommand;

const initializeAWS = async () => {
  if (!SFNClient) {
    const awsSdk = await import("@aws-sdk/client-sfn");
    SFNClient = awsSdk.SFNClient;
    StartExecutionCommand = awsSdk.StartExecutionCommand;
    DescribeExecutionCommand = awsSdk.DescribeExecutionCommand;
  }
};

// AWS Configuration - initialized dynamically
let sfnClient;

const initializeSFNClient = async () => {
  if (!sfnClient) {
    await initializeAWS();
    throw new Error(
      "Direct AWS SDK calls should be replaced with API Gateway calls for security"
    );
  }
  return sfnClient;
};

// Phase 3 Complete Workflow ARN with DynamoDB + Email
const PHASE3_WORKFLOW_ARN =
  "arn:aws:states:us-east-1:695221387268:stateMachine:complete-readme-generator-workflow";

// CloudFront CDN URL
const CLOUDFRONT_URL = "https://d3in1w40kamst9.cloudfront.net";

export const useReadmeGeneratorAdvanced = () => {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [progress, setProgress] = useState(null);
  const [executionArn, setExecutionArn] = useState(null);

  const pollForCompletion = useCallback(
    async (arn) => {
      let attempts = 0;
      const maxAttempts = 30; // 2.5 minutes with 5-second intervals

      const poll = async () => {
        try {
          attempts++;

          // Initialize AWS SDK dynamically
          const client = await initializeSFNClient();

          const command = new DescribeExecutionCommand({
            executionArn: arn,
          });

          const result = await client.send(command);

          if (result.status === "SUCCEEDED") {
            const output = JSON.parse(result.output);
            setProgress("✅ README generation completed!");
            setResult(output.body);
            setLoading(false);

            // Show success toast with email and DynamoDB info
            if (output.body?.email_notification?.sent) {
              toast.success("📧 Email sent successfully!", {
                description: "Check your inbox for the README download link",
                duration: 5000,
              });
            }

            if (output.body?.dynamodb_record_id) {
              toast.success("💾 Pipeline tracked successfully!", {
                description: `Record ID: ${output.body.dynamodb_record_id}`,
                duration: 3000,
              });
            }

            return;
          }

          if (result.status === "FAILED") {
            throw new Error("Pipeline execution failed");
          }

          if (attempts >= maxAttempts) {
            throw new Error("Generation timeout - please try again");
          }

          // Enhanced progress tracking for complete pipeline
          if (attempts < 2) {
            setProgress("💾 Creating DynamoDB tracking record...");
          } else if (attempts < 5) {
            setProgress("🧠 Phase 3 AI analyzing repository...");
          } else if (attempts < 8) {
            setProgress("📊 Updating analysis results in database...");
          } else if (attempts < 12) {
            setProgress("🔍 Detecting frameworks and patterns...");
          } else if (attempts < 16) {
            setProgress("📝 Generating professional README...");
          } else if (attempts < 20) {
            setProgress("💾 Storing README results in database...");
          } else if (attempts < 24) {
            setProgress("🎨 Finalizing enhanced documentation...");
          } else if (attempts < 28) {
            setProgress("📧 Preparing email notification...");
          } else {
            setProgress("🏁 Completing pipeline tracking...");
          }

          // Continue polling
          setTimeout(poll, 5000);
        } catch (err) {
          console.error("Polling error:", err);
          setError(err.message);
          setLoading(false);
          toast.error("Pipeline failed", {
            description: err.message,
          });
        }
      };

      poll();
    },
    [setProgress, setError, setLoading, setResult]
  );

  // Start Phase 3 Complete Pipeline with Cognito email + DynamoDB tracking
  const generateREADME = useCallback(
    async (githubUrl) => {
      setLoading(true);
      setError(null);
      setResult(null);
      setProgress("🚀 Starting Phase 3 Ultimate AI Platform...");

      try {
        // Get user email from Cognito
        const userResult = await cognitoAuth.getCurrentUser();
        if (!userResult.success || !userResult.user?.email) {
          throw new Error("Please log in to generate README");
        }

        const userEmail = userResult.user.email;

        // Show Sonner toast for email notification
        toast.success("📧 Email notification enabled!", {
          description: `You'll receive an email at ${userEmail} when your README is ready`,
          duration: 4000,
        });

        // Initialize AWS SDK dynamically
        const client = await initializeSFNClient();

        // Start Step Functions execution with email + DynamoDB tracking
        const command = new StartExecutionCommand({
          stateMachineArn: PHASE3_WORKFLOW_ARN,
          input: JSON.stringify({
            github_url: githubUrl,
            user_email: userEmail,
          }),
        });

        const startResult = await client.send(command);
        setExecutionArn(startResult.executionArn);
        setProgress("💾 Creating DynamoDB tracking record...");

        // Poll for completion
        await pollForCompletion(startResult.executionArn);
      } catch (err) {
        console.error("Phase 3 generation failed:", err);
        setError(err.message || "Generation failed");
        setLoading(false);
        toast.error("Generation failed", {
          description: err.message,
        });
      }
    },
    [pollForCompletion]
  );

  // Poll for execution completion with enhanced progress tracking

  // Get CloudFront URL for README
  const getREADMEUrl = useCallback((s3Key) => {
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
