"use client";

import React from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { useRouter } from 'next/navigation';
import { Eye, TestTube } from 'lucide-react';

const PreviewTest = () => {
  const router = useRouter();

  const testWorkingPreview = () => {
    const url = `/preview/test-working?source=direct&s3Key=mock&name=Test%20Project&owner=test-user&type=Demo&lang=TypeScript`;
    console.log('🧪 Testing preview with URL:', url);
    router.push(url);
  };

  return (
    <Card className="fixed bottom-20 right-4 w-64 z-40 bg-white shadow-lg border-2 border-blue-200">
      <CardHeader className="pb-2">
        <CardTitle className="text-sm flex items-center">
          <TestTube className="h-4 w-4 mr-2" />
          Preview Test
        </CardTitle>
      </CardHeader>
      <CardContent className="pt-0">
        <Button
          size="sm"
          onClick={testWorkingPreview}
          className="w-full bg-blue-600 hover:bg-blue-700"
        >
          <Eye className="h-4 w-4 mr-2" />
          Test Preview
        </Button>
      </CardContent>
    </Card>
  );
};

export default PreviewTest;
