"use client";

import React from 'react';
import { useRouter } from 'next/navigation';
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { 
  Download, 
  Copy, 
  Trash2, 
  ExternalLink, 
  FileText, 
  Clock, 
  CheckCircle, 
  AlertCircle,
  Monitor
} from "lucide-react";
import { toast } from "sonner";
import { ReadmeHistoryItem } from "@/types/dashboard";

interface HistoryItemCardProps {
  item: ReadmeHistoryItem;
  onCopy: (content: string) => void;
  onDelete: (requestId: string) => void;
  progress: string | null;
}

const HistoryItemCardSimple: React.FC<HistoryItemCardProps> = ({ 
  item, 
  onCopy, 
  onDelete, 
  progress 
}) => {
  const router = useRouter();

  const handleCopy = async () => {
    // Simply fetch from readmeS3Url using proxy
    if (item.readmeS3Url) {
      try {
        const proxyResponse = await fetch(`/api/proxy-s3?url=${encodeURIComponent(item.readmeS3Url)}`);
        if (proxyResponse.ok) {
          const proxyData = await proxyResponse.json();
          if (proxyData.content) {
            onCopy(proxyData.content);
            return;
          }
        }
      } catch (error) {
        console.error('Copy error:', error);
      }
    }
    
    // Fallback
    onCopy(`# ${item.repoName}\n\nContent not available`);
  };

  const handleDownload = async () => {
    // Simply fetch from readmeS3Url using proxy
    if (item.readmeS3Url) {
      try {
        console.log('🔍 DOWNLOAD DEBUG - Fetching from S3 URL:', item.readmeS3Url);
        
        const proxyResponse = await fetch(`/api/proxy-s3?url=${encodeURIComponent(item.readmeS3Url)}`);
        if (proxyResponse.ok) {
          const proxyData = await proxyResponse.json();
          if (proxyData.content) {
            downloadFile(proxyData.content, item.repoName);
            toast.success('README downloaded successfully!');
            return;
          }
        }
        throw new Error('Failed to fetch content via proxy');
      } catch (error) {
        console.error('Download error:', error);
        toast.error('Failed to download README');
      }
    } else {
      // Fallback
      const content = `# ${item.repoName}\n\nContent not available`;
      downloadFile(content, item.repoName);
    }
  };
  
  const downloadFile = (content: string, repoName: string) => {
    try {
      const blob = new Blob([content], { type: "text/markdown" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");

      a.href = url;
      a.download = `${(repoName || "README").replace("/", "-")}-README.md`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    } catch (error) {
      console.error("Download error:", error);
      toast.error("Failed to download README");
    }
  };

  const handleDelete = () => {
    if (confirm('Are you sure you want to delete this README generation record?')) {
      onDelete(item.requestId);
    }
  };

  const handleOpenRepo = () => {
    window.open(item.repoUrl, "_blank");
  };

  const handleOpenPreview = () => {
    // DEBUG: Log all item fields to see what's available
    console.log("🔍 FULL PREVIEW DEBUG - Complete item object:");
    console.log(JSON.stringify(item, null, 2));
    console.log("🔍 FULL PREVIEW DEBUG - Item keys:", Object.keys(item));
    console.log("🔍 FULL PREVIEW DEBUG - readmeS3Url field:", item.readmeS3Url);
    
    // Pass metadata directly in URL params
    const params = new URLSearchParams({
      repoName: item.repoName || 'Unknown Repository',
      repoUrl: item.repoUrl || '#',
      owner: item.repoUrl ? item.repoUrl.split('/')[3] || 'Unknown' : 'Unknown',
      projectType: item.projectType || 'Unknown',
      primaryLanguage: item.primaryLanguage || 'Unknown',
      frameworks: (item.frameworks || []).join(','),
      confidence: String(item.confidence || 0),
      processingTime: String(item.processingTime || 0),
      createdAt: item.createdAt || new Date().toISOString(),
      readmeS3Url: item.readmeS3Url || '',
      status: item.status || 'completed'
    });
    
    // Navigate to dynamic preview route with all metadata
    const previewUrl = `/preview/${encodeURIComponent(item.requestId)}?${params.toString()}`;
    console.log("🔍 FULL PREVIEW DEBUG - Generated preview URL:", previewUrl);
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
            <Clock className="w-3 h-3 mr-1" />
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
              <Clock className="w-4 h-4 text-blue-600" />
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
                  <span>Preview</span>
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
  );
};

export default HistoryItemCardSimple;
