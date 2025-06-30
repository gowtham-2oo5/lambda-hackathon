"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { cognitoAuth } from "@/lib/cognito";

export function DebugInfo() {
  const [debugInfo, setDebugInfo] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const checkAuth = async () => {
    setLoading(true);
    try {
      const isAuth = cognitoAuth.isAuthenticated();
      const userResult = await cognitoAuth.getCurrentUser();
      
      setDebugInfo({
        isAuthenticated: isAuth,
        userResult: userResult,
        timestamp: new Date().toISOString()
      });
    } catch (error) {
      setDebugInfo({
        error: error instanceof Error ? error.message : 'Unknown error',
        timestamp: new Date().toISOString()
      });
    } finally {
      setLoading(false);
    }
  };

  const testAPI = async () => {
    setLoading(true);
    try {
      const userResult = await cognitoAuth.getCurrentUser();
      
      if (!userResult.success) {
        throw new Error('Not authenticated');
      }

      // Try to get auth headers using the same method as the hook
      const response = await fetch(`https://ccki297o82.execute-api.us-east-1.amazonaws.com/prod/history/${userResult.user?.sub}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          // Note: We can't access the private getStoredTokens method here
          // This is just for testing the endpoint structure
        },
      });

      const result = {
        status: response.status,
        statusText: response.statusText,
        headers: Object.fromEntries(response.headers.entries()),
        body: response.ok ? await response.json() : await response.text(),
      };

      setDebugInfo({
        apiTest: result,
        timestamp: new Date().toISOString()
      });
    } catch (error) {
      setDebugInfo({
        apiError: error instanceof Error ? error.message : 'Unknown error',
        timestamp: new Date().toISOString()
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card className="mt-4">
      <CardHeader>
        <CardTitle>Debug Information</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-x-2 mb-4">
          <Button onClick={checkAuth} disabled={loading} size="sm">
            Check Auth
          </Button>
          <Button onClick={testAPI} disabled={loading} size="sm">
            Test API
          </Button>
        </div>
        
        {debugInfo && (
          <pre className="bg-gray-100 p-4 rounded text-xs overflow-auto max-h-96">
            {JSON.stringify(debugInfo, null, 2)}
          </pre>
        )}
      </CardContent>
    </Card>
  );
}
