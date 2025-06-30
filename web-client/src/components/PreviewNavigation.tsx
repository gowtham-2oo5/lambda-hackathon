"use client";

import React from 'react';
import { Button } from '@/components/ui/button';
import { useRouter } from 'next/navigation';
import { Eye, History, Zap } from 'lucide-react';

const PreviewNavigation = () => {
  const router = useRouter();

  return (
    <div className="fixed bottom-4 right-4 z-50">
      <div className="bg-white rounded-lg shadow-lg border p-4 space-y-2">
        <h4 className="text-sm font-semibold text-gray-900 mb-2">Preview Demo</h4>
        
        <Button
          size="sm"
          variant="outline"
          onClick={() => router.push('/preview-demo')}
          className="w-full justify-start"
        >
          <Zap className="h-4 w-4 mr-2" />
          Demo Page
        </Button>
        
        <Button
          size="sm"
          variant="outline"
          onClick={() => router.push('/preview/demo-example?source=direct&s3Key=mock&name=Demo%20Project&owner=demo-user')}
          className="w-full justify-start"
        >
          <Eye className="h-4 w-4 mr-2" />
          Quick Preview
        </Button>
        
        <Button
          size="sm"
          variant="outline"
          onClick={() => router.push('/dashboard')}
          className="w-full justify-start"
        >
          <History className="h-4 w-4 mr-2" />
          Dashboard
        </Button>
      </div>
    </div>
  );
};

export default PreviewNavigation;
