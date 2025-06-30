"use client";

import React from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { useRouter } from 'next/navigation';
import { generateS3PreviewUrl, generateHistoryPreviewUrl } from '@/utils/previewUrl';
import { Eye, FileText, History, AlertCircle, CheckCircle, Info } from 'lucide-react';

const PreviewDemoPage = () => {
  const router = useRouter();

  const handleWorkingPreview = () => {
    // This will use mock data since real S3 files may not exist
    const previewUrl = `/preview/demo-working?source=direct&s3Key=mock-demo&name=Smart%20ReadmeGen%20Demo&owner=demo-user&type=Web%20Application&lang=TypeScript&frameworks=React,Next.js&confidence=0.95&time=28.5`;
    router.push(previewUrl);
  };

  const handleHistoryPreview = () => {
    // This will fallback to mock data if history doesn't exist
    const previewUrl = generateHistoryPreviewUrl('demo-history-123');
    router.push(previewUrl);
  };

  const handleRealS3Preview = () => {
    // This might fail with 403 if the S3 file doesn't exist
    const previewUrl = generateS3PreviewUrl({
      s3Key: 'generated-readmes/example-user/example-repo.md',
      repoUrl: 'https://github.com/example-user/example-repo',
      repoName: 'example-repo',
      owner: 'example-user',
      projectType: 'Web Application',
      primaryLanguage: 'JavaScript',
      frameworks: ['React', 'Node.js', 'Express'],
      confidence: 0.95,
      processingTime: 28.5
    });
    
    router.push(previewUrl);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            📖 README Preview System Demo
          </h1>
          <p className="text-gray-600 text-lg">
            Test the new dynamic preview routes with different data sources and fallback mechanisms
          </p>
        </div>

        {/* Status Alert */}
        <Card className="mb-8 border-amber-200 bg-amber-50">
          <CardContent className="pt-6">
            <div className="flex items-start space-x-3">
              <Info className="h-5 w-5 text-amber-600 mt-0.5" />
              <div>
                <h3 className="font-semibold text-amber-800 mb-2">Current Status & Fallbacks</h3>
                <div className="text-sm text-amber-700 space-y-1">
                  <p>• <strong>Real S3 files</strong>: May return 403 errors if files don't exist yet</p>
                  <p>• <strong>History API</strong>: Falls back to mock data if DynamoDB records are missing</p>
                  <p>• <strong>Mock data</strong>: Always works and shows the full preview functionality</p>
                  <p>• <strong>Error handling</strong>: Graceful fallbacks ensure preview always loads</p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          {/* Working Demo Preview */}
          <Card className="border-green-200 bg-green-50">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <CheckCircle className="h-5 w-5 text-green-600" />
                <span>Working Demo</span>
              </CardTitle>
              <Badge className="bg-green-100 text-green-800 w-fit">Always Works</Badge>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-600 mb-4">
                Uses mock data to demonstrate the full preview functionality including themes, TOC, and all features.
              </p>
              <Button 
                onClick={handleWorkingPreview}
                className="w-full bg-green-600 hover:bg-green-700"
              >
                <Eye className="h-4 w-4 mr-2" />
                Open Working Preview
              </Button>
            </CardContent>
          </Card>

          {/* History Preview */}
          <Card className="border-blue-200 bg-blue-50">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <History className="h-5 w-5 text-blue-600" />
                <span>History Preview</span>
              </CardTitle>
              <Badge className="bg-blue-100 text-blue-800 w-fit">Fallback Ready</Badge>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-600 mb-4">
                Attempts to fetch from history API, falls back to mock data if no records exist.
              </p>
              <Button 
                onClick={handleHistoryPreview}
                className="w-full bg-blue-600 hover:bg-blue-700"
              >
                <Eye className="h-4 w-4 mr-2" />
                Try History Preview
              </Button>
            </CardContent>
          </Card>

          {/* Real S3 Preview */}
          <Card className="border-amber-200 bg-amber-50">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <AlertCircle className="h-5 w-5 text-amber-600" />
                <span>Real S3 Preview</span>
              </CardTitle>
              <Badge className="bg-amber-100 text-amber-800 w-fit">May Fail</Badge>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-600 mb-4">
                Attempts to fetch real S3 file. Will show 403 error if file doesn't exist, then fallback to mock.
              </p>
              <Button 
                onClick={handleRealS3Preview}
                className="w-full bg-amber-600 hover:bg-amber-700"
              >
                <Eye className="h-4 w-4 mr-2" />
                Test Real S3 Preview
              </Button>
            </CardContent>
          </Card>
        </div>

        {/* Navigation */}
        <div className="flex justify-center space-x-4 mt-8">
          <Button
            variant="outline"
            onClick={() => router.push('/dashboard')}
          >
            <History className="h-4 w-4 mr-2" />
            Go to Dashboard
          </Button>
          <Button
            variant="outline"
            onClick={() => router.push('/')}
          >
            <FileText className="h-4 w-4 mr-2" />
            Back to Home
          </Button>
        </div>
      </div>
    </div>
  );
};

export default PreviewDemoPage;
