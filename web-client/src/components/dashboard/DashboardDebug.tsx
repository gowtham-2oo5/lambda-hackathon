"use client";

import React, { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { useHistoryDashboard } from '@/hooks/useHistoryDashboard';

interface DashboardDebugProps {
  userEmail: string;
}

const DashboardDebug: React.FC<DashboardDebugProps> = ({ userEmail }) => {
  const [testResult, setTestResult] = useState<any>(null);
  const [testing, setTesting] = useState(false);
  
  const {
    historyItems,
    loading,
    error,
    refetch
  } = useHistoryDashboard(userEmail);

  const testDirectAPI = async () => {
    setTesting(true);
    try {
      console.log('🧪 Testing direct API call...');
      const response = await fetch(`/api/test-history`);
      const result = await response.json();
      setTestResult(result);
      console.log('🧪 Test result:', result);
    } catch (err) {
      console.error('🧪 Test failed:', err);
      setTestResult({ error: err instanceof Error ? err.message : 'Test failed' });
    } finally {
      setTesting(false);
    }
  };

  const testProxyAPI = async () => {
    setTesting(true);
    try {
      console.log('🧪 Testing proxy API call...');
      const response = await fetch(`/api/history?userId=${encodeURIComponent(userEmail)}`);
      const result = await response.json();
      setTestResult(result);
      console.log('🧪 Proxy test result:', result);
    } catch (err) {
      console.error('🧪 Proxy test failed:', err);
      setTestResult({ error: err instanceof Error ? err.message : 'Proxy test failed' });
    } finally {
      setTesting(false);
    }
  };

  return (
    <Card className="mb-4 border-yellow-200 bg-yellow-50">
      <CardHeader>
        <CardTitle className="text-sm text-yellow-800">🔍 Dashboard Debug Info</CardTitle>
      </CardHeader>
      <CardContent className="text-xs space-y-4">
        <div className="space-y-2">
          <div><strong>User Email:</strong> {userEmail || 'Not provided'}</div>
          <div><strong>Loading:</strong> {loading ? 'Yes' : 'No'}</div>
          <div><strong>Error:</strong> {error || 'None'}</div>
          <div><strong>History Items:</strong> {historyItems ? historyItems.length : 'undefined'}</div>
          {historyItems && historyItems.length > 0 && (
            <div>
              <strong>First Item:</strong>
              <pre className="mt-1 p-2 bg-white rounded text-xs overflow-auto max-h-32">
                {JSON.stringify(historyItems[0], null, 2)}
              </pre>
            </div>
          )}
        </div>
        
        <div className="flex space-x-2">
          <Button 
            size="sm" 
            onClick={testDirectAPI} 
            disabled={testing}
            className="text-xs"
          >
            {testing ? 'Testing...' : 'Test Direct API'}
          </Button>
          <Button 
            size="sm" 
            onClick={testProxyAPI} 
            disabled={testing}
            className="text-xs"
          >
            {testing ? 'Testing...' : 'Test Proxy API'}
          </Button>
          <Button 
            size="sm" 
            onClick={refetch} 
            disabled={loading}
            className="text-xs"
          >
            {loading ? 'Refreshing...' : 'Refresh History'}
          </Button>
        </div>
        
        {testResult && (
          <div>
            <strong>Test Result:</strong>
            <pre className="mt-1 p-2 bg-white rounded text-xs overflow-auto max-h-40">
              {JSON.stringify(testResult, null, 2)}
            </pre>
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default DashboardDebug;
