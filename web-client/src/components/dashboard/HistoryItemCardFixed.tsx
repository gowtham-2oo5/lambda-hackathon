"use client";

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { 
  Download, 
  Copy, 
  Trash2, 
  ExternalLink, 
  Loader2, 
  FileText, 
  Clock, 
  CheckCircle, 
  AlertCircle,
  Eye,
  Monitor
} from "lucide-react";
import { toast } from "sonner";
import ReadmePreviewModal from '@/components/ReadmePreviewModal';
import { ReadmeHistoryItem } from "@/types/dashboard";
import { generateHistoryPreviewUrl } from '@/utils/previewUrl';
import { fetchReadmeContentWithRetry } from '@/utils/contentFetcher';
import { downloadReadme } from '@/utils/fileDownload';

interface HistoryItemCardProps {
  item: ReadmeHistoryItem;
  onCopy: (content: string) => void;
  onDownload: (content: string, repoName: string) => void;
  onDelete: (requestId: string) => void;
  progress: string | null;
}

const HistoryItemCardFixed: React.FC<HistoryItemCardProps> = ({ 
  item, 
  onCopy, 
  onDownload, 
  onDelete, 
  progress 
}) => {
  const router = useRouter();
  const [showPreview, setShowPreview] = useState(false);
  const [readmeContent, setReadmeContent] = useState<string>('');
  const [loadingContent, setLoadingContent] = useState(false);
  const [contentError, setContentError] = useState<string | null>(null);
  const [contentFetched, setContentFetched] = useState(false);

  // Enhanced content fetching with proper error handling
  const fetchReadmeContent = async () => {
    if (contentFetched && readmeContent) {
      console.log('🔧 PREVIEW DEBUG - Using cached content');
      return;
    }

    console.log('🔧 PREVIEW DEBUG - Fetching content for item:', item);
    
    setLoadingContent(true);
    setContentError(null);
    
    try {
      const result = await fetchReadmeContentWithRetry(item, 3, 1000);
      
      if (result.success) {
        setReadmeContent(result.content);
        setContentFetched(true);
        console.log('✅ PREVIEW DEBUG - Content fetched successfully from:', result.source);
        
        if (result.source === 'fallback') {
          toast.warning('Using fallback content', {
            description: 'Original README content not available'
          });
        }
      } else {
        setContentError(result.error || 'Failed to load README content');
        setReadmeContent(result.content); // Use fallback content
        console.error('❌ PREVIEW DEBUG - Content fetch failed:', result.error);
        
        toast.error('Content not available', {
          description: 'Using fallback README content'
        });
      }
    } catch (error) {
      console.error('❌ PREVIEW DEBUG - Unexpected error:', error);
      setContentError('Unexpected error occurred while loading content');
      setReadmeContent(`# ${item.repoName || 'README'}\n\nContent temporarily unavailable. Please try again later.`);
      
      toast.error('Failed to load content', {
        description: 'Please try again later'
      });
    } finally {
      setLoadingContent(false);
    }
  };

  const handlePreviewToggle = async () => {
    if (!showPreview && item.status === 'completed') {
      await fetchReadmeContent();
    }
    setShowPreview(!showPreview);
  };

  const handleModalClose = () => {
    setShowPreview(false);
  };

  const handleCopy = async () => {
    if (!readmeContent && item.status === 'completed') {
      await fetchReadmeContent();
    }
    
    const content = readmeContent || `# ${item.repoName}\n\nContent not available`;
    onCopy(content);
  };

  const handleDownload = async () => {
    if (!readmeContent && item.status === 'completed') {
      setLoadingContent(true);
      await fetchReadmeContent();
      setLoadingContent(false);
    }
    
    const content = readmeContent || `# ${item.repoName}\n\nContent not available`;
    
    // Use the enhanced download utility
    const success = await downloadReadme(content, {
      format: 'md',
      repoName: item.repoName,
      githubUrl: item.repoUrl
    });
    
    if (success) {
      toast.success('README downloaded successfully!');
    }
  };

  const handleDownloadMultipleFormats = async () => {
    if (!readmeContent && item.status === 'completed') {
      setLoadingContent(true);
      await fetchReadmeContent();
      setLoadingContent(false);
    }
    
    const content = readmeContent || `# ${item.repoName}\n\nContent not available`;
    
    // Download in multiple formats
    const formats = ['md', 'html', 'txt'];
    let successCount = 0;
    
    for (const format of formats) {
      const success = await downloadReadme(content, {
        format,
        repoName: item.repoName,
        githubUrl: item.repoUrl
      });
      if (success) successCount++;
      
      // Small delay between downloads
      await new Promise(resolve => setTimeout(resolve, 500));
    }
    
    toast.success(`Downloaded ${successCount}/${formats.length} formats`);
  };

  const handleDelete = () => {
    if (confirm('Are you sure you want to delete this README generation record?')) {
      onDelete(item.requestId);
    }
  };

  const handleOpenRepo = () => {
    window.open(item.repoUrl, '_blank');
  };

  const handleOpenPreview = () => {
    const previewUrl = generateHistoryPreviewUrl(item.requestId);
    router.push(previewUrl);
  };

  const getStatusBadge = () => {
    switch (item.status) {
      case 'completed':
        return (
          <Badge className="bg-green-100 text-green-800 border-green-200">
            <CheckCircle className="w-3 h-3 mr-1" />
            Completed
          </Badge>
        );
      case 'processing':
        return (
          <Badge className="bg-blue-100 text-blue-800 border-blue-200">
            <Loader2 className="w-3 h-3 mr-1 animate-spin" />
            Processing
          </Badge>
        );
      case 'failed':
        return (
          <Badge className="bg-red-100 text-red-800 border-red-200">
            <AlertCircle className="w-3 h-3 mr-1" />
            Failed
          </Badge>
        );
      default:
        return (
          <Badge variant="outline">
            <Clock className="w-3 h-3 mr-1" />
            Unknown
          </Badge>
        );
    }
  };

  const formatDate = (dateString: string) => {
    try {
      return new Date(dateString).toLocaleString();
    } catch {
      return dateString;
    }
  };

  const formatProcessingTime = (seconds?: number) => {
    if (!seconds) return 'N/A';
    if (seconds < 60) return `${seconds.toFixed(1)}s`;
    return `${Math.floor(seconds / 60)}m ${(seconds % 60).toFixed(0)}s`;
  };

  return (
    <>
      <Card className="hover:shadow-lg transition-shadow duration-200 border-l-4 border-l-blue-500">
        <CardContent className="p-6">
          {/* Header */}
          <div className="flex items-start justify-between mb-4">
            <div className="flex-1">
              <div className="flex items-center space-x-3 mb-2">
                <FileText className="w-5 h-5 text-blue-600" />
                <h3 className="font-semibold text-lg text-gray-900">
                  {item.repoName || 'Unknown Repository'}
                </h3>
                {getStatusBadge()}
              </div>
              
              <div className="text-sm text-gray-600 space-y-1">
                <div className="flex items-center space-x-2">
                  <ExternalLink className="w-4 h-4" />
                  <a 
                    href={item.repoUrl} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="text-blue-600 hover:text-blue-800 underline"
                  >
                    {item.repoUrl}
                  </a>
                </div>
                
                <div className="flex items-center space-x-4">
                  <div className="flex items-center space-x-1">
                    <Clock className="w-4 h-4" />
                    <span>Created: {formatDate(item.createdAt)}</span>
                  </div>
                  
                  {item.processingTime && (
                    <div className="flex items-center space-x-1">
                      <span>⚡</span>
                      <span>Processing: {formatProcessingTime(item.processingTime)}</span>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>

          {/* Progress indicator for processing items */}
          {item.status === 'processing' && progress && (
            <div className="mb-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
              <div className="flex items-center space-x-2">
                <Loader2 className="w-4 h-4 animate-spin text-blue-600" />
                <span className="text-blue-800 text-sm font-medium">{progress}</span>
              </div>
            </div>
          )}

          {/* Error display */}
          {item.status === 'failed' && (
            <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg">
              <div className="text-red-700 text-sm">
                <span className="font-medium">❌ Generation Failed:</span>
                <span className="ml-2">{item.error || "Failed to generate README. Please try again."}</span>
              </div>
            </div>
          )}

          {/* Loading indicator when fetching content */}
          {loadingContent && (
            <div className="mb-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
              <div className="flex items-center space-x-2">
                <Loader2 className="w-4 h-4 animate-spin text-blue-600" />
                <span className="text-blue-800 text-sm font-medium">Loading README content...</span>
              </div>
            </div>
          )}

          {/* Action Buttons */}
          <div className="flex items-center justify-between pt-4 border-t border-gray-100">
            <div className="flex items-center space-x-2 flex-wrap gap-2">
              {item.status === 'completed' && (
                <>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={handleOpenPreview}
                    className="flex items-center space-x-1 bg-gradient-to-r from-blue-50 to-indigo-50 hover:from-blue-100 hover:to-indigo-100 border-blue-200"
                  >
                    <Monitor className="w-4 h-4" />
                    <span>Full Preview</span>
                  </Button>
                  
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={handlePreviewToggle}
                    disabled={loadingContent}
                    className="flex items-center space-x-1"
                  >
                    {loadingContent ? (
                      <Loader2 className="w-4 h-4 animate-spin" />
                    ) : (
                      <Eye className="w-4 h-4" />
                    )}
                    <span>Quick View</span>
                  </Button>
                  
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={handleCopy}
                    disabled={loadingContent}
                    className="flex items-center space-x-1"
                  >
                    <Copy className="w-4 h-4" />
                    <span>Copy</span>
                  </Button>
                  
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={handleDownload}
                    disabled={loadingContent}
                    className="flex items-center space-x-1"
                  >
                    {loadingContent ? (
                      <Loader2 className="w-4 h-4 animate-spin" />
                    ) : (
                      <Download className="w-4 h-4" />
                    )}
                    <span>Download</span>
                  </Button>
                  
                  {/* Multi-format download button */}
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={handleDownloadMultipleFormats}
                    disabled={loadingContent}
                    className="flex items-center space-x-1 text-purple-600 hover:text-purple-700"
                  >
                    <Download className="w-4 h-4" />
                    <span>All Formats</span>
                  </Button>
                </>
              )}
              
              <Button
                variant="outline"
                size="sm"
                onClick={handleOpenRepo}
                className="flex items-center space-x-1"
              >
                <ExternalLink className="w-4 h-4" />
                <span>Repo</span>
              </Button>
            </div>
            
            <Button
              variant="outline"
              size="sm"
              onClick={handleDelete}
              className="flex items-center space-x-1 text-red-600 hover:text-red-700 hover:bg-red-50"
            >
              <Trash2 className="w-4 h-4" />
              <span>Delete</span>
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* README Preview Modal */}
      <ReadmePreviewModal
        isOpen={showPreview}
        onClose={handleModalClose}
        content={readmeContent}
        repoName={item.repoName || 'Unknown Repository'}
        repoUrl={item.repoUrl || '#'}
        isLoading={loadingContent}
        error={contentError}
        onCopy={onCopy}
        onDownload={onDownload}
      />
    </>
  );
};

export default HistoryItemCardFixed;
