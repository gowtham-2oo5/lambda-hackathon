"use client";

import React from 'react';
import { MarkdownRenderer } from './MarkdownRenderer';
import { Button } from '@/components/ui/button';
import { Copy, Download, ArrowLeft, ExternalLink } from 'lucide-react';
import { toast } from 'sonner';
import { useRouter } from 'next/navigation';

interface NaturalReadmePreviewProps {
  content: string;
  metadata: {
    repoName: string;
    repoUrl: string;
    owner: string;
    generatedAt: string;
    projectType: string;
    primaryLanguage: string;
    frameworks: string[];
    confidence: number;
    processingTime: number;
  };
}

const NaturalReadmePreview: React.FC<NaturalReadmePreviewProps> = ({ content, metadata }) => {
  const router = useRouter();

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(content);
      toast.success('Copied to clipboard');
    } catch {
      toast.error('Failed to copy');
    }
  };

  const handleDownload = () => {
    const blob = new Blob([content], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `README.md`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    toast.success('Downloaded README.md');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-blue-50">
      {/* Header */}
      <div className="sticky top-0 z-10 bg-white/80 backdrop-blur-sm border-b border-slate-200">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <Button
                variant="ghost"
                size="sm"
                onClick={() => router.back()}
                className="flex items-center space-x-2"
              >
                <ArrowLeft className="w-4 h-4" />
                <span>Back</span>
              </Button>
              
              <div className="h-6 w-px bg-slate-300" />
              
              <div>
                <h1 className="text-xl font-bold text-slate-900">
                  {metadata.repoName}
                </h1>
                <p className="text-sm text-slate-600">
                  Generated README Preview
                </p>
              </div>
            </div>

            <div className="flex items-center space-x-3">
              <Button
                variant="outline"
                size="sm"
                onClick={() => window.open(metadata.repoUrl, '_blank')}
                className="flex items-center space-x-2"
              >
                <ExternalLink className="w-4 h-4" />
                <span>View Repository</span>
              </Button>
              
              <Button
                variant="outline"
                size="sm"
                onClick={handleCopy}
                className="flex items-center space-x-2"
              >
                <Copy className="w-4 h-4" />
                <span>Copy</span>
              </Button>
              
              <Button
                size="sm"
                onClick={handleDownload}
                className="flex items-center space-x-2 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700"
              >
                <Download className="w-4 h-4" />
                <span>Download</span>
              </Button>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-6xl mx-auto px-6 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Sidebar with metadata */}
          <div className="lg:col-span-1">
            <div className="sticky top-24">
              <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
                <h3 className="text-lg font-semibold text-slate-900 mb-4">
                  Project Details
                </h3>
                
                <div className="space-y-4">
                  <div>
                    <label className="text-sm font-medium text-slate-600">Repository</label>
                    <p className="text-sm text-slate-900 font-mono break-all">
                      {metadata.repoName}
                    </p>
                  </div>
                  
                  <div>
                    <label className="text-sm font-medium text-slate-600">Owner</label>
                    <p className="text-sm text-slate-900">{metadata.owner}</p>
                  </div>
                  
                  <div>
                    <label className="text-sm font-medium text-slate-600">Project Type</label>
                    <p className="text-sm text-slate-900">{metadata.projectType}</p>
                  </div>
                  
                  <div>
                    <label className="text-sm font-medium text-slate-600">Primary Language</label>
                    <p className="text-sm text-slate-900">{metadata.primaryLanguage}</p>
                  </div>
                  
                  {metadata.frameworks && metadata.frameworks.length > 0 && (
                    <div>
                      <label className="text-sm font-medium text-slate-600">Frameworks</label>
                      <div className="flex flex-wrap gap-1 mt-1">
                        {metadata.frameworks.map((framework, index) => (
                          <span
                            key={index}
                            className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full"
                          >
                            {framework}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                  
                  <div>
                    <label className="text-sm font-medium text-slate-600">Generated</label>
                    <p className="text-sm text-slate-900">
                      {new Date(metadata.generatedAt).toLocaleDateString()}
                    </p>
                  </div>
                  
                  {metadata.processingTime > 0 && (
                    <div>
                      <label className="text-sm font-medium text-slate-600">Processing Time</label>
                      <p className="text-sm text-slate-900">
                        {metadata.processingTime.toFixed(1)}s
                      </p>
                    </div>
                  )}
                  
                  {metadata.confidence > 0 && (
                    <div>
                      <label className="text-sm font-medium text-slate-600">Confidence</label>
                      <div className="flex items-center space-x-2">
                        <div className="flex-1 bg-slate-200 rounded-full h-2">
                          <div
                            className="bg-gradient-to-r from-green-500 to-blue-500 h-2 rounded-full"
                            style={{ width: `${metadata.confidence * 100}%` }}
                          />
                        </div>
                        <span className="text-sm text-slate-900">
                          {Math.round(metadata.confidence * 100)}%
                        </span>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>

          {/* README Content */}
          <div className="lg:col-span-3">
            <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
              <div className="px-8 py-6 border-b border-slate-200 bg-slate-50">
                <div className="flex items-center space-x-3">
                  <div className="flex space-x-1">
                    <div className="w-3 h-3 rounded-full bg-red-500"></div>
                    <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
                    <div className="w-3 h-3 rounded-full bg-green-500"></div>
                  </div>
                  <span className="text-sm font-medium text-slate-600">README.md</span>
                </div>
              </div>
              
              <div className="p-8">
                <MarkdownRenderer content={content} />
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <div className="border-t border-slate-200 bg-slate-50">
        <div className="max-w-6xl mx-auto px-6 py-6">
          <div className="flex items-center justify-between">
            <div className="text-sm text-slate-600">
              Generated by <span className="font-semibold text-slate-900">Smart ReadmeGen</span> - 
              AI-Powered Professional README Generation
            </div>
            
            <div className="flex items-center space-x-4">
              <Button
                variant="ghost"
                size="sm"
                onClick={handleCopy}
                className="text-slate-600 hover:text-slate-900"
              >
                <Copy className="w-4 h-4 mr-2" />
                Copy Markdown
              </Button>
              
              <Button
                variant="ghost"
                size="sm"
                onClick={handleDownload}
                className="text-slate-600 hover:text-slate-900"
              >
                <Download className="w-4 h-4 mr-2" />
                Download File
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default NaturalReadmePreview;
