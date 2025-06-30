"use client";

import React from 'react';
import { MarkdownRenderer } from './MarkdownRenderer';
import { Button } from '@/components/ui/button';
import { Copy, Download, ArrowLeft, ExternalLink } from 'lucide-react';
import { toast } from 'sonner';
import { useRouter } from 'next/navigation';

interface ReadmePreviewProps {
  content: string;
  metadata: {
    repoName: string;
    repoUrl: string;
    repoOwner: string;
    userId: string;
    repoId: string;
    createdAt: string;
    updatedAt: string;
    lastAccessedAt: string;
    projectType: string;
    primaryLanguage: string;
    techStack: string[];
    accuracyLevel: string;
    confidenceScore: number;
    qualityScore: string;
    processingTime: number;
    filesAnalyzedCount: number;
    readmeLength: number;
    readmeUrl: string;
    status: string;
    version: string;
    analysisMethod: string;
    generationMethod: string;
    analysisComplete: boolean;
    hallucinationPrevented: boolean;
    realContentAnalyzed: boolean;
    performanceMetrics: any;
    sourceFilesAnalyzed: string[];
    requestId: string;
    ttl: number;
  };
}

const ReadmePreview: React.FC<ReadmePreviewProps> = ({ content, metadata }) => {
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
                    <p className="text-sm text-slate-900">{metadata.repoOwner}</p>
                  </div>
                  
                  <div>
                    <label className="text-sm font-medium text-slate-600">Language</label>
                    <p className="text-sm text-slate-900">
                      {metadata.primaryLanguage && metadata.primaryLanguage !== "Unknown" 
                        ? metadata.primaryLanguage 
                        : metadata.techStack && metadata.techStack.length > 0 
                          ? metadata.techStack.join(", ")
                          : "Mixed"}
                    </p>
                  </div>
                  
                  {metadata.techStack && metadata.techStack.length > 0 && (
                    <div>
                      <label className="text-sm font-medium text-slate-600">Tech Stack</label>
                      <div className="flex flex-wrap gap-1 mt-1">
                        {metadata.techStack.map((tech, index) => (
                          <span
                            key={index}
                            className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full"
                          >
                            {tech}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                  
                  <div>
                    <label className="text-sm font-medium text-slate-600">Quality Score</label>
                    <div className="flex items-center space-x-2">
                      <span className="text-sm font-semibold text-slate-900 capitalize">{metadata.qualityScore}</span>
                      <span className="text-xs text-slate-600">({metadata.confidenceScore}%)</span>
                    </div>
                  </div>
                  
                  <div>
                    <label className="text-sm font-medium text-slate-600">Analysis</label>
                    <div className="space-y-1">
                      <div className="flex justify-between text-xs">
                        <span className="text-slate-600">{metadata.filesAnalyzedCount} files analyzed</span>
                      </div>
                      <div className="flex justify-between text-xs">
                        <span className="text-slate-600">{metadata.processingTime}s processing</span>
                      </div>
                    </div>
                  </div>
                  
                  <div>
                    <label className="text-sm font-medium text-slate-600">Generated</label>
                    <p className="text-sm text-slate-900">
                      {new Date(metadata.createdAt).toLocaleDateString()}
                    </p>
                  </div>
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

export default ReadmePreview;
