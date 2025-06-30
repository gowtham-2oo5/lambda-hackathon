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
import { generateHistoryPreviewUrl, generateS3PreviewUrl } from '@/utils/previewUrl';

interface HistoryItemCardProps {
  item: ReadmeHistoryItem;
  index: number;
  onCopy: (content: string) => void;
  onDownload: (content: string, repoName: string) => void;
  onDelete: (requestId: string) => void;
  progress: string | null;
}

const HistoryItemCard: React.FC<HistoryItemCardProps> = ({ 
  item, 
  index, 
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

  // Fetch README content from the ACTUAL history item data
  const fetchReadmeContent = async () => {
    console.log('🔧 PREVIEW DEBUG - History item:', item);
    
    // First check if we have readmeContent directly in the item
    if ((item as any).readmeContent) {
      console.log('🔧 PREVIEW DEBUG - Using readmeContent from history item');
      setReadmeContent((item as any).readmeContent);
      setLoadingContent(false);
      return;
    }
    
    // If no direct content, try to fetch from S3 URL
    if (item.readmeS3Url && item.status === 'completed') {
      console.log('🔧 PREVIEW DEBUG - Fetching from S3 URL:', item.readmeS3Url);
      
      setLoadingContent(true);
      setContentError(null);
      
      try {
        // Fetch the README content from the S3 URL
        const response = await fetch(item.readmeS3Url, {
          method: 'GET',
          headers: {
            'Accept': 'text/markdown,text/plain,*/*',
          },
        });
        
        if (!response.ok) {
          throw new Error(`Failed to fetch README: ${response.status} - File may not exist yet`);
        }
        
        const content = await response.text();
        setReadmeContent(content);
        console.log('🔧 DASHBOARD DEBUG - Successfully loaded content');
      } catch (error) {
        console.error('Error fetching README from CloudFront:', error);
        setContentError('Failed to load README content - file may not be generated yet');
        setReadmeContent('# README Not Available\n\nThe README file hasn\'t been generated yet or is still processing. Please try again later.');
      } finally {
        setLoadingContent(false);
      }
    } else if (item.content) {
      setReadmeContent(item.content);
    }
  };

  const handlePreviewToggle = () => {
    if (!showPreview && item.status === 'completed') {
      // Check if we already have readmeContent in the item
      if ((item as any).readmeContent) {
        console.log('🔧 PREVIEW DEBUG - Using existing readmeContent from history item');
        setReadmeContent((item as any).readmeContent);
        setLoadingContent(false);
      } else {
        // Fetch from S3 URL if no direct content
        fetchReadmeContent();
      }
    }
    setShowPreview(!showPreview);
  };

  const handleModalClose = () => {
    setShowPreview(false);
  };

  const handleCopy = () => {
    const content = readmeContent || item.content || '';
    onCopy(content);
  };

  const handleDownload = () => {
    const content = readmeContent || item.content || '';
    onDownload(content, item.repoName);
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
    // Navigate to the new preview route
    const previewUrl = generateHistoryPreviewUrl(item.requestId);
    router.push(previewUrl);
  };

  const handleOpenPreviewNewTab = () => {
    // Open preview in new tab
    const previewUrl = generateHistoryPreviewUrl(item.requestId);
    window.open(previewUrl, '_blank');
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

          {/* Action Buttons */}
          <div className="flex items-center justify-between pt-4 border-t border-gray-100">
            <div className="flex items-center space-x-2">
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
                    className="flex items-center space-x-1"
                  >
                    <Eye className="w-4 h-4" />
                    <span>Quick View</span>
                  </Button>
                  
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={handleCopy}
                    className="flex items-center space-x-1"
                  >
                    <Copy className="w-4 h-4" />
                    <span>Copy</span>
                  </Button>
                  
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={handleDownload}
                    className="flex items-center space-x-1"
                  >
                    <Download className="w-4 h-4" />
                    <span>Download</span>
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

export default HistoryItemCard;
