import { useState, useCallback } from 'react';
import { toast } from 'sonner';
import { cognitoAuth } from '../lib/cognito-fixed';

const API_BASE_URL = 'https://ccki297o82.execute-api.us-east-1.amazonaws.com/prod';

export const useReadmeGeneratorSimple = () => {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [progress, setProgress] = useState(null);

  // Get user email from Cognito
  const getUserEmail = useCallback(async () => {
    try {
      // Method 1: Try getCurrentUser
      const userResult = await cognitoAuth.getCurrentUser();
      if (userResult.success && userResult.user?.email) {
        return userResult.user.email;
      }
    } catch {
      // Silent fallback
    }

    try {
      // Method 2: Try getStoredUser
      const storedUser = cognitoAuth.getStoredUser();
      if (storedUser?.email) {
        return storedUser.email;
      }
    } catch {
      // Silent fallback
    }

    try {
      // Method 3: Try localStorage
      const userData = localStorage.getItem('user_data');
      if (userData) {
        const user = JSON.parse(userData);
        if (user?.email) {
          return user.email;
        }
      }
    } catch {
      // Silent fallback
    }

    // Fallback to demo email only if nothing else works
    return 'demo@smartreadmegen.com';
  }, []);

  // Simple polling function
  const pollForCompletion = useCallback(async (executionArn: string) => {
    let attempts = 0;
    const maxAttempts = 60; // 5 minutes

    const poll = async () => {
      try {
        attempts++;
        setProgress(`🔄 Processing... (${attempts}/${maxAttempts})`);

        // FIXED: No encoding needed - API Gateway handles ARN directly
        const response = await fetch(`${API_BASE_URL}/status/${executionArn}`);
        
        if (!response.ok) {
          throw new Error(`Status check failed: ${response.status}`);
        }

        const data = await response.json();

        if (data.status === 'SUCCEEDED') {
          setProgress('✅ README generation completed!');
          setResult(data);
          setLoading(false);
          
          toast.success('🎉 README Generated Successfully!');
          
        } else if (data.status === 'FAILED') {
          setError('Generation failed');
          setLoading(false);
          toast.error('Generation failed');
          
        } else if (data.status === 'RUNNING' && attempts < maxAttempts) {
          setTimeout(poll, 5000); // Check again in 5 seconds
          
        } else {
          setError('Generation timeout');
          setLoading(false);
          toast.error('Generation timeout');
        }
        
      } catch (err: any) {
        console.error('Polling error:', err);
        if (attempts < 3) {
          setTimeout(poll, 10000); // Retry after 10 seconds
        } else {
          setError(err.message);
          setLoading(false);
          toast.error('Status check failed');
        }
      }
    };

    poll();
  }, []);

  const generateREADME = useCallback(async (githubUrl: string) => {
    setLoading(true);
    setError(null);
    setResult(null);
    setProgress('🚀 Starting README generation...');

    try {
      // FIXED: Get actual user email from Cognito
      const userEmail = await getUserEmail();
      console.log('🔧 Using user email:', userEmail);

      // Simple POST request to start generation
      const response = await fetch(`${API_BASE_URL}/generate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          github_url: githubUrl,
          user_email: userEmail // ✅ Now uses real Cognito email
        }),
      });

      if (!response.ok) {
        throw new Error(`Generation failed: ${response.status}`);
      }

      const data = await response.json();
      
      if (data.executionArn) {
        setProgress('💾 Generation started, checking status...');
        // Now poll for completion
        await pollForCompletion(data.executionArn);
      } else {
        // Fallback if no executionArn
        setProgress('✅ Generation started successfully!');
        setResult(data);
        setLoading(false);
        toast.success('🎉 README Generation Started!');
      }

    } catch (err: any) {
      setError(err.message);
      setLoading(false);
      toast.error('Generation failed', {
        description: err.message,
      });
    }
  }, [pollForCompletion, getUserEmail]);

  const reset = useCallback(() => {
    setLoading(false);
    setResult(null);
    setError(null);
    setProgress(null);
  }, []);

  return {
    generateREADME,
    loading,
    result,
    error,
    progress,
    reset,
  };
};
