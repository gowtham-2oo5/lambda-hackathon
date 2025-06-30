"use client";

import React from 'react';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { 
  Copy, 
  Download, 
  ExternalLink, 
  FileText, 
  Globe, 
  Loader2,
  AlertCircle 
} from "lucide-react";
import { toast } from "sonner";
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import remarkBreaks from 'remark-breaks';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { oneDark } from 'react-syntax-highlighter/dist/esm/styles/prism';

interface ReadmePreviewModalProps {
  isOpen: boolean;
  onClose: () => void;
  content: string;
  repoName: string;
  repoUrl: string;
  isLoading: boolean;
  error: string | null;
  onCopy: (content: string) => void;
  onDownload: (content: string, repoName: string) => void;
}

const ReadmePreviewModal: React.FC<ReadmePreviewModalProps> = ({
  isOpen,
  onClose,
  content,
  repoName,
  repoUrl,
  isLoading,
  error,
  onCopy,
  onDownload,
}) => {
  const handleCopy = () => {
    onCopy(content);
    toast.success("README copied to clipboard!");
  };

  const handleDownload = (format: 'md' | 'html' | 'txt' = 'md') => {
    onDownload(content, repoName);
    toast.success(`README downloaded as ${format.toUpperCase()}!`);
  };

  const handleOpenRepo = () => {
    window.open(repoUrl, '_blank');
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-4xl max-h-[90vh] flex flex-col">
        <DialogHeader className="flex-shrink-0">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <FileText className="h-6 w-6 text-blue-600" />
              <div>
                <DialogTitle className="text-xl font-bold">
                  README Preview
                </DialogTitle>
                <DialogDescription className="flex items-center space-x-2 mt-1">
                  <span>{repoName}</span>
                  <Badge variant="outline" className="text-xs">
                    Professional README
                  </Badge>
                </DialogDescription>
              </div>
            </div>
            
            {/* Action Buttons */}
            <div className="flex items-center space-x-2">
              <Button
                variant="outline"
                size="sm"
                onClick={handleOpenRepo}
                className="flex items-center space-x-1"
              >
                <ExternalLink className="h-4 w-4" />
                <span>Repo</span>
              </Button>
              
              <Button
                variant="outline"
                size="sm"
                onClick={handleCopy}
                disabled={isLoading || !!error}
                className="flex items-center space-x-1"
              >
                <Copy className="h-4 w-4" />
                <span>Copy</span>
              </Button>
              
              <Button
                variant="outline"
                size="sm"
                onClick={() => handleDownload('md')}
                disabled={isLoading || !!error}
                className="flex items-center space-x-1"
              >
                <Download className="h-4 w-4" />
                <span>Download</span>
              </Button>
            </div>
          </div>
        </DialogHeader>
        
        <Separator className="my-4" />
        
        {/* Content Area with ScrollArea */}
        <div className="flex-1 min-h-0">
          <ScrollArea className="h-full w-full rounded-md border">
            <div className="p-6">
              {isLoading && (
                <div className="flex items-center justify-center py-12">
                  <div className="flex items-center space-x-3">
                    <Loader2 className="h-6 w-6 animate-spin text-blue-600" />
                    <span className="text-lg text-gray-600">Loading README content...</span>
                  </div>
                </div>
              )}
              
              {error && (
                <div className="flex items-center justify-center py-12">
                  <div className="text-center">
                    <AlertCircle className="h-12 w-12 text-red-500 mx-auto mb-4" />
                    <h3 className="text-lg font-semibold text-red-700 mb-2">
                      Failed to Load README
                    </h3>
                    <p className="text-gray-600 max-w-md">
                      {error}
                    </p>
                  </div>
                </div>
              )}
              
              {!isLoading && !error && content && (
                <div className="prose prose-lg max-w-none">
                  <ReactMarkdown
                    remarkPlugins={[remarkGfm, remarkBreaks]}
                    components={{
                      // Custom code block rendering with syntax highlighting
                      code({ node, inline, className, children, ...props }) {
                        const match = /language-(\w+)/.exec(className || '');
                        return !inline && match ? (
                          <SyntaxHighlighter
                            style={oneDark}
                            language={match[1]}
                            PreTag="div"
                            className="rounded-lg"
                            {...props}
                          >
                            {String(children).replace(/\n$/, '')}
                          </SyntaxHighlighter>
                        ) : (
                          <code 
                            className="bg-gray-100 text-gray-800 px-1 py-0.5 rounded text-sm font-mono" 
                            {...props}
                          >
                            {children}
                          </code>
                        );
                      },
                      // Custom heading styling
                      h1: ({ children }) => (
                        <h1 className="text-3xl font-bold text-gray-900 mb-4 pb-2 border-b border-gray-200">
                          {children}
                        </h1>
                      ),
                      h2: ({ children }) => (
                        <h2 className="text-2xl font-semibold text-gray-800 mb-3 mt-8 pb-1 border-b border-gray-100">
                          {children}
                        </h2>
                      ),
                      h3: ({ children }) => (
                        <h3 className="text-xl font-semibold text-gray-800 mb-2 mt-6">
                          {children}
                        </h3>
                      ),
                      // Custom link styling
                      a: ({ href, children }) => (
                        <a 
                          href={href} 
                          target="_blank" 
                          rel="noopener noreferrer"
                          className="text-blue-600 hover:text-blue-800 underline decoration-blue-300 hover:decoration-blue-500"
                        >
                          {children}
                        </a>
                      ),
                      // Custom blockquote styling
                      blockquote: ({ children }) => (
                        <blockquote className="border-l-4 border-blue-500 pl-4 py-2 bg-blue-50 text-gray-700 italic">
                          {children}
                        </blockquote>
                      ),
                      // Custom table styling
                      table: ({ children }) => (
                        <div className="overflow-x-auto">
                          <table className="min-w-full divide-y divide-gray-200 border border-gray-300 rounded-lg">
                            {children}
                          </table>
                        </div>
                      ),
                      th: ({ children }) => (
                        <th className="px-4 py-2 bg-gray-50 text-left text-sm font-semibold text-gray-900 border-b border-gray-200">
                          {children}
                        </th>
                      ),
                      td: ({ children }) => (
                        <td className="px-4 py-2 text-sm text-gray-700 border-b border-gray-100">
                          {children}
                        </td>
                      ),
                      // Custom list styling
                      ul: ({ children }) => (
                        <ul className="list-disc list-inside space-y-1 text-gray-700">
                          {children}
                        </ul>
                      ),
                      ol: ({ children }) => (
                        <ol className="list-decimal list-inside space-y-1 text-gray-700">
                          {children}
                        </ol>
                      ),
                    }}
                  >
                    {content}
                  </ReactMarkdown>
                </div>
              )}
              
              {!isLoading && !error && !content && (
                <div className="flex items-center justify-center py-12">
                  <div className="text-center">
                    <FileText className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                    <h3 className="text-lg font-semibold text-gray-700 mb-2">
                      No Content Available
                    </h3>
                    <p className="text-gray-500">
                      README content is not available for preview.
                    </p>
                  </div>
                </div>
              )}
            </div>
          </ScrollArea>
        </div>
        
        {/* Footer with additional actions */}
        <div className="flex-shrink-0 pt-4 border-t">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2 text-sm text-gray-500">
              <Globe className="h-4 w-4" />
              <span>Generated by Smart ReadmeGen Enterprise</span>
            </div>
            
            <div className="flex items-center space-x-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => handleDownload('html')}
                disabled={isLoading || !!error}
              >
                HTML
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={() => handleDownload('txt')}
                disabled={isLoading || !!error}
              >
                TXT
              </Button>
            </div>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
};

export default ReadmePreviewModal;
