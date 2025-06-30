"use client";

import React from "react";
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
  AlertCircle,
} from "lucide-react";
import { toast } from "sonner";
import { MarkdownRenderer } from "./MarkdownRenderer";

interface ReadmePreviewModalProps {
  isOpen: boolean;
  onClose: () => void;
  content: string | null;
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
    if (content !== null) {
      onCopy(content);
      toast.success("README copied to clipboard!");
    }
  };

  const handleDownload = (format: "md" | "html" | "txt" = "md") => {
    if (content !== null) {
      onDownload(content, repoName);
      toast.success(`README downloaded as ${format.toUpperCase()}!`);
    }
  };

  const handleOpenRepo = () => {
    window.open(repoUrl, "_blank");
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
                onClick={() => handleDownload("md")}
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
                    <span className="text-lg text-gray-600">
                      Loading README content...
                    </span>
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
                    <p className="text-gray-600 max-w-md">{error}</p>
                  </div>
                </div>
              )}

              {!isLoading && !error && content && (
                <MarkdownRenderer content={content} />
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
                onClick={() => handleDownload("html")}
                disabled={isLoading || !!error}
              >
                HTML
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={() => handleDownload("txt")}
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
