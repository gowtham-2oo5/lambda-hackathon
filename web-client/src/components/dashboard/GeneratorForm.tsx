"use client";

import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { FileText, Loader2, Zap, Brain, Globe } from "lucide-react";
import { toast } from "sonner";
import { useReadmeGeneratorSimple } from "@/hooks/useReadmeGeneratorSimple";

interface GeneratorFormProps {
  onGenerationComplete?: () => void;
}

const GeneratorForm: React.FC<GeneratorFormProps> = ({ onGenerationComplete }) => {
  const [githubUrl, setGithubUrl] = useState('');
  const { generateREADME, loading, result, error, progress, reset } = useReadmeGeneratorSimple();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!githubUrl.trim()) return;
    
    // Validate GitHub URL
    const githubRegex = /^https:\/\/github\.com\/[\w\-\.]+\/[\w\-\.]+\/?$/;
    if (!githubRegex.test(githubUrl.trim())) {
      toast.error('Invalid GitHub URL', {
        description: 'Please enter a valid GitHub repository URL',
      });
      return;
    }
    
    try {
      await generateREADME(githubUrl.trim());
      if (onGenerationComplete) {
        onGenerationComplete();
      }
    } catch (err) {
      console.error('Generation failed:', err);
    }
  };

  const handleReset = () => {
    reset();
    setGithubUrl('');
  };

  return (
    <Card className="border-2 border-dashed border-blue-300 bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <CardHeader className="text-center">
        <div className="flex items-center justify-center space-x-3 mb-2">
          <div className="p-3 bg-gradient-to-br from-blue-600 to-purple-600 rounded-full">
            <FileText className="w-8 h-8 text-white" />
          </div>
          <div>
            <CardTitle className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              Smart ReadmeGen Enterprise
            </CardTitle>
            <CardDescription className="text-lg">
              AI-Powered Professional README Generation
            </CardDescription>
          </div>
        </div>
        
        <div className="flex items-center justify-center space-x-4 mt-4">
          <Badge className="bg-green-100 text-green-800 border-green-200">
            <Zap className="w-3 h-3 mr-1" />
            95% Accuracy
          </Badge>
          <Badge className="bg-blue-100 text-blue-800 border-blue-200">
            <Brain className="w-3 h-3 mr-1" />
            Claude Sonnet 4
          </Badge>
          <Badge className="bg-purple-100 text-purple-800 border-purple-200">
            <Globe className="w-3 h-3 mr-1" />
            Enterprise Grade
          </Badge>
        </div>
      </CardHeader>
      
      <CardContent className="space-y-6">
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="github-url" className="text-sm font-medium">
              GitHub Repository URL
            </Label>
            <Input
              id="github-url"
              type="url"
              placeholder="https://github.com/username/repository"
              value={githubUrl}
              onChange={(e) => setGithubUrl(e.target.value)}
              disabled={loading}
              className="text-lg py-3"
            />
            <p className="text-xs text-gray-500">
              Enter the full GitHub repository URL to generate a professional README
            </p>
          </div>
          
          <div className="flex space-x-3">
            <Button
              type="submit"
              disabled={loading || !githubUrl.trim()}
              className="flex-1 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white py-3 text-lg font-semibold"
            >
              {loading ? (
                <>
                  <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                  Generating...
                </>
              ) : (
                <>
                  <FileText className="w-5 h-5 mr-2" />
                  Generate README
                </>
              )}
            </Button>
            
            {(result || error) && (
              <Button
                type="button"
                variant="outline"
                onClick={handleReset}
                className="px-6"
              >
                Reset
              </Button>
            )}
          </div>
        </form>
        
        {/* Progress Display */}
        {loading && progress && (
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <div className="flex items-center space-x-3">
              <Loader2 className="w-5 h-5 animate-spin text-blue-600" />
              <div>
                <div className="font-medium text-blue-900">Processing Repository</div>
                <div className="text-sm text-blue-700">{progress}</div>
              </div>
            </div>
          </div>
        )}
        
        {/* Success Display */}
        {result && !loading && (
          <div className="bg-green-50 border border-green-200 rounded-lg p-4">
            <div className="flex items-center space-x-3">
              <div className="w-5 h-5 bg-green-500 rounded-full flex items-center justify-center">
                <span className="text-white text-xs">✓</span>
              </div>
              <div>
                <div className="font-medium text-green-900">README Generated Successfully!</div>
                <div className="text-sm text-green-700">
                  Check your history below to view and download the generated README.
                </div>
              </div>
            </div>
          </div>
        )}
        
        {/* Error Display */}
        {error && !loading && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4">
            <div className="flex items-center space-x-3">
              <div className="w-5 h-5 bg-red-500 rounded-full flex items-center justify-center">
                <span className="text-white text-xs">✕</span>
              </div>
              <div>
                <div className="font-medium text-red-900">Generation Failed</div>
                <div className="text-sm text-red-700">{error}</div>
              </div>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default GeneratorForm;
