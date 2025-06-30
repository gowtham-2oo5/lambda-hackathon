import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useReadmeGeneratorAdvanced } from '../hooks/useReadmeGeneratorAdvanced';
import { Button } from './ui/button';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from './ui/card';
import { Github, Download, Zap, Brain, FileText, Clock, Mail, Database, Globe, Copy, Eye } from '@/lib/icons';
import { toast } from 'sonner';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { generateS3PreviewUrl } from '../utils/previewUrl';

const ReadmeGeneratorAdvanced = () => {
  const router = useRouter();
  const [githubUrl, setGithubUrl] = useState('');
  const [previewContent, setPreviewContent] = useState('');
  const [showPreview, setShowPreview] = useState(false);
  const { generateREADME, getREADMEUrl, loading, result, error, progress, reset } = useReadmeGeneratorAdvanced();

  const handleOpenPreview = () => {
    if (!result?.readme_generation?.s3_location?.key) return;
    
    const match = githubUrl.match(/github\.com\/([^\/]+)\/([^\/]+)/);
    if (!match) return;
    
    const [, owner, repo] = match;
    
    const previewUrl = generateS3PreviewUrl({
      s3Key: result.readme_generation.s3_location.key,
      repoUrl: githubUrl,
      repoName: repo,
      owner: owner,
      projectType: result.ai_analysis?.project_type,
      primaryLanguage: result.ai_analysis?.primary_language,
      frameworks: result.ai_analysis?.frameworks,
      confidence: result.ai_analysis?.confidence,
      processingTime: result.ai_analysis?.processing_time
    });
    
    router.push(previewUrl);
  };

  const handleOpenPreviewNewTab = () => {
    if (!result?.readme_generation?.s3_location?.key) return;
    
    const match = githubUrl.match(/github\.com\/([^\/]+)\/([^\/]+)/);
    if (!match) return;
    
    const [, owner, repo] = match;
    
    const previewUrl = generateS3PreviewUrl({
      s3Key: result.readme_generation.s3_location.key,
      repoUrl: githubUrl,
      repoName: repo,
      owner: owner,
      projectType: result.ai_analysis?.project_type,
      primaryLanguage: result.ai_analysis?.primary_language,
      frameworks: result.ai_analysis?.frameworks,
      confidence: result.ai_analysis?.confidence,
      processingTime: result.ai_analysis?.processing_time
    });
    
    window.open(previewUrl, '_blank');
  };

  const handleSubmit = async (e) => {
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
    
    await generateREADME(githubUrl.trim());
  };

  const handleReset = () => {
    reset();
    setGithubUrl('');
  };

  const handleDownload = async (format = 'md') => {
    console.log('🔧 DEBUGGING - Download function called with format:', format);
    console.log('🔧 DEBUGGING - Current result:', result);
    console.log('🔧 DEBUGGING - GitHub URL:', githubUrl);
    
    if (!githubUrl) {
      toast.error('No GitHub URL available');
      return;
    }
    
    try {
      // FIXED: Extract owner and repo from GitHub URL
      const match = githubUrl.match(/github\.com\/([^\/]+)\/([^\/]+)/);
      if (!match) {
        throw new Error('Invalid GitHub URL format');
      }
      
      const [, owner, repo] = match;
      console.log('🔧 DEBUGGING - Extracted owner:', owner, 'repo:', repo);
      
      // FIXED: Use the correct S3 key format from your bucket scan
      const correctS3Key = `generated-readmes/${owner}/${repo}.md`;
      console.log('🔧 DEBUGGING - Using S3 key:', correctS3Key);
      
      // Try CloudFront URL with correct key
      const cloudFrontUrl = `https://d3in1w40kamst9.cloudfront.net/${correctS3Key}`;
      console.log('🔧 DEBUGGING - CloudFront URL:', cloudFrontUrl);
      
      let readmeContent;
      
      // Try to fetch the content first
      try {
        const response = await fetch(cloudFrontUrl, {
          method: 'GET',
          headers: {
            'Accept': 'text/markdown,text/plain,*/*',
          },
        });
        
        if (response.ok) {
          readmeContent = await response.text();
          console.log('🔧 DEBUGGING - Successfully fetched content from CloudFront');
        } else {
          throw new Error(`CloudFront fetch failed: ${response.status}`);
        }
      } catch (fetchError) {
        console.log('🔧 DEBUGGING - CloudFront fetch failed, trying direct download:', fetchError.message);
        
        // Fallback: Direct download link (bypasses CORS)
        const a = document.createElement('a');
        a.href = cloudFrontUrl;
        a.download = `${owner}-${repo}-README.${format}`;
        a.target = '_blank';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        
        toast.success(`README download started!`, {
          description: `File: ${owner}-${repo}-README.${format}`
        });
        
        console.log('🔧 DEBUGGING - Direct download link created and clicked');
        return;
      }
      
      if (!readmeContent) {
        throw new Error('No content received');
      }
      
      // Extract repo name for better file naming
      const repoName = `${owner}-${repo}`;
      
      let fileContent = readmeContent;
      let mimeType = 'text/markdown';
      let extension = 'md';
      
      // Handle different formats
      switch (format.toLowerCase()) {
        case 'html':
          fileContent = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${repoName} - README</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
        }
        h1, h2, h3 { color: #2563eb; }
        code { 
            background: #f1f5f9; 
            padding: 2px 4px; 
            border-radius: 3px; 
            font-family: 'Monaco', 'Consolas', monospace;
        }
        pre { 
            background: #1e293b; 
            color: #e2e8f0; 
            padding: 16px; 
            border-radius: 8px; 
            overflow-x: auto;
        }
        .footer {
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #e2e8f0;
            color: #64748b;
            font-size: 14px;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="content">
        ${readmeContent.replace(/\n/g, '<br>')}
    </div>
    </div>
</body>
</html>`;
          mimeType = 'text/html';
          extension = 'html';
          break;
          
        case 'txt':
          // Strip markdown formatting for plain text
          fileContent = readmeContent
            .replace(/#{1,6}\s/g, '')
            .replace(/\*\*(.*?)\*\*/g, '$1')
            .replace(/\*(.*?)\*/g, '$1')
            .replace(/`(.*?)`/g, '$1')
            .replace(/```[\s\S]*?```/g, '[Code Block]')
            .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1');
          mimeType = 'text/plain';
          extension = 'txt';
          break;
      }
      
      // Create and download file
      const blob = new Blob([fileContent], { type: mimeType });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      
      a.href = url;
      a.download = `${repoName}-README.${extension}`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
      
      toast.success(`README downloaded as ${extension.toUpperCase()}!`, {
        description: `File: ${repoName}-README.${extension}`
      });
      
      console.log('🔧 DEBUGGING - File download completed successfully');
      
    } catch (err) {
      console.error('🚨 Download error:', err);
      toast.error('Download failed', {
        description: err.message,
      });
    }
  };
        <p>Generated by <strong>Smart ReadmeGen Enterprise</strong> - AI-Powered README Generation</p>
    </div>
</body>
</html>`;
          mimeType = 'text/html';
          extension = 'html';
          break;
          
        case 'txt':
          // Strip markdown formatting for plain text
          fileContent = readmeContent
            .replace(/#{1,6}\s/g, '')
            .replace(/\*\*(.*?)\*\*/g, '$1')
            .replace(/\*(.*?)\*/g, '$1')
            .replace(/`(.*?)`/g, '$1')
            .replace(/```[\s\S]*?```/g, '[Code Block]')
            .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1');
          mimeType = 'text/plain';
          extension = 'txt';
          break;
      }
      
      // Create and download file
      const blob = new Blob([fileContent], { type: mimeType });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      
      a.href = url;
      a.download = `${repoName}-README.${extension}`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
      
      toast.success(`README downloaded as ${extension.toUpperCase()}!`, {
        description: `File: ${repoName}-README.${extension}`
      });
      
    } catch (err) {
      console.error('Download error:', err);
      toast.error('Download failed', {
        description: err.message,
      });
    }
  };

  // Preview function
  const handlePreview = async () => {
    if (!result?.readme_generation?.s3_location) {
      toast.error('No README available for preview');
      return;
    }
    
    try {
      const cloudFrontUrl = `https://d3in1w40kamst9.cloudfront.net/${result.readme_generation.s3_location.key}`;
      const response = await fetch(cloudFrontUrl);
      
      if (!response.ok) {
        throw new Error(`Failed to fetch README: ${response.status}`);
      }
      
      const content = await response.text();
      setPreviewContent(content);
      setShowPreview(true);
      toast.success('README preview loaded!');
    } catch (err) {
      console.error('Preview error:', err);
      toast.error('Preview failed', {
        description: err.message,
      });
    }
  };

  // Copy to clipboard
  const handleCopy = async () => {
    if (!previewContent) {
      await handlePreview();
    }
    
    if (previewContent) {
      navigator.clipboard.writeText(previewContent);
      toast.success('README copied to clipboard!');
    }
  };

  return (
    <div className="max-w-6xl mx-auto p-6 space-y-6">
      {/* Header */}
      <Card className="bg-gradient-to-r from-blue-50 to-purple-50 border-blue-200">
        <CardHeader className="text-center">
          <CardTitle className="text-3xl font-bold text-gray-900 flex items-center justify-center gap-2">
            <Brain className="h-8 w-8 text-blue-600" />
            🚀 SmartReadmeGen AI Platform
          </CardTitle>
          <CardDescription className="text-lg text-gray-600">
            Enterprise-grade README generation with intelligent analysis & professional formatting
          </CardDescription>
        </CardHeader>
      </Card>

      {/* Input Section */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Github className="h-5 w-5" />
            Repository Analysis
          </CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="flex gap-3">
              <input
                type="url"
                value={githubUrl}
                onChange={(e) => setGithubUrl(e.target.value)}
                placeholder="https://github.com/username/repository"
                className="flex-1 px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                disabled={loading}
                required
              />
              <Button 
                type="submit" 
                disabled={loading || !githubUrl}
                className="px-6 py-2 bg-blue-600 hover:bg-blue-700"
              >
                {loading ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                    Generating...
                  </>
                ) : (
                  <>
                    <Zap className="h-4 w-4 mr-2" />
                    Generate README
                  </>
                )}
              </Button>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="flex items-center gap-2 text-sm text-gray-600 bg-blue-50 p-3 rounded-md">
                <Mail className="h-4 w-4 text-blue-600" />
                <span>📧 Email notifications automatically enabled</span>
              </div>
              <div className="flex items-center gap-2 text-sm text-gray-600 bg-green-50 p-3 rounded-md">
                <Database className="h-4 w-4 text-green-600" />
                <span>💾 Complete pipeline tracking enabled</span>
              </div>
            </div>
          </form>
        </CardContent>
      </Card>

      {/* Progress Section */}
      {progress && (
        <Card className="bg-blue-50 border-blue-200">
          <CardContent className="pt-6">
            <div className="flex items-center">
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-600 mr-3"></div>
              <span className="text-blue-800 font-medium">{progress}</span>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Error Section */}
      {error && (
        <Card className="bg-red-50 border-red-200">
          <CardContent className="pt-6">
            <div className="flex items-center text-red-600">
              <span className="font-medium">❌ {error}</span>
              <Button 
                onClick={handleReset}
                variant="outline"
                size="sm"
                className="ml-auto"
              >
                Try Again
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Results Section */}
      {result && (
        <div className="space-y-6">
          {/* DynamoDB Tracking Info */}
          {result.dynamodb_record_id && (
            <Card className="bg-purple-50 border-purple-200">
              <CardHeader>
                <CardTitle className="text-purple-800 flex items-center gap-2">
                  <Database className="h-5 w-5" />
                  💾 Pipeline Tracking
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <span className="font-medium text-gray-700">Record ID:</span>
                    <span className="ml-2 text-purple-700 font-mono text-sm">
                      {result.dynamodb_record_id}
                    </span>
                  </div>
                  <div>
                    <span className="font-medium text-gray-700">Status:</span>
                    <span className="ml-2 text-green-700 font-semibold">
                      {result.database_tracking?.status || 'Completed'}
                    </span>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}

          {/* AI Analysis Results */}
          <Card className="bg-green-50 border-green-200">
            <CardHeader>
              <CardTitle className="text-green-800 flex items-center gap-2">
                <Brain className="h-5 w-5" />
                🎯 AI Analysis Results
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <div>
                    <span className="font-medium text-gray-700">Project Type:</span>
                    <span className="ml-2 text-green-700 font-semibold">
                      {result.ai_analysis?.project_type || 'Unknown'}
                    </span>
                  </div>
                  <div>
                    <span className="font-medium text-gray-700">Confidence:</span>
                    <span className="ml-2 text-green-700 font-semibold">
                      {result.ai_analysis?.confidence 
                        ? `${(result.ai_analysis.confidence * 100).toFixed(1)}%`
                        : 'N/A'
                      }
                    </span>
                  </div>
                </div>
                <div className="space-y-2">
                  <div>
                    <span className="font-medium text-gray-700">Language:</span>
                    <span className="ml-2 text-green-700 font-semibold">
                      {result.ai_analysis?.primary_language || 'Unknown'}
                    </span>
                  </div>
                  <div>
                    <span className="font-medium text-gray-700">Frameworks:</span>
                    <span className="ml-2 text-green-700 font-semibold">
                      {result.ai_analysis?.frameworks?.join(', ') || 'None detected'}
                    </span>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* README Generation Results */}
          <Card className="bg-blue-50 border-blue-200">
            <CardHeader>
              <CardTitle className="text-blue-800 flex items-center gap-2">
                <FileText className="h-5 w-5" />
                🎨 Professional README Generation Results
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                <div>
                  <span className="font-medium text-gray-700">README Length:</span>
                  <span className="ml-2 text-blue-700 font-semibold">
                    {result.readme_generation?.readme_length?.toLocaleString() || 'Unknown'} characters
                  </span>
                </div>
                <div>
                  <span className="font-medium text-gray-700">Quality Level:</span>
                  <span className="ml-2 text-blue-700 font-semibold">
                    {result.readme_generation?.quality_level || 'Professional Grade'}
                  </span>
                </div>
                <div>
                  <span className="font-medium text-gray-700">Generated:</span>
                  <span className="ml-2 text-blue-700 font-semibold">
                    {result.readme_generation?.generation_timestamp 
                      ? new Date(result.readme_generation.generation_timestamp).toLocaleString()
                      : 'Unknown'
                    }
                  </span>
                </div>
                <div>
                  <span className="font-medium text-gray-700">Format:</span>
                  <span className="ml-2 text-blue-700 font-semibold">
                    Enhanced Markdown
                  </span>
                </div>
              </div>
              
              {/* Enhancement Features */}
              <div className="mb-4 p-3 bg-blue-100 rounded-md">
                <h4 className="font-semibold text-blue-800 mb-2">🎨 Professional Features:</h4>
                <div className="grid grid-cols-2 md:grid-cols-3 gap-2 text-sm text-blue-700">
                  <div>✅ Professional Structure</div>
                  <div>✅ Dynamic Badges</div>
                  <div>✅ Installation Guides</div>
                  <div>✅ Usage Examples</div>
                  <div>✅ API Documentation</div>
                  <div>✅ Contributing Guidelines</div>
                </div>
              </div>
              
              <div className="flex flex-wrap gap-3">
                {/* Preview Button */}
                <Button
                  onClick={handlePreview}
                  className="bg-purple-600 hover:bg-purple-700 flex items-center"
                >
                  <Eye className="h-4 w-4 mr-2" />
                  Preview README
                </Button>
                
                {/* Copy Button */}
                <Button
                  onClick={handleCopy}
                  variant="outline"
                  className="flex items-center"
                >
                  <Copy className="h-4 w-4 mr-2" />
                  Copy to Clipboard
                </Button>
                
                {/* Primary Download Button */}
                <Button
                  onClick={() => handleDownload('md')}
                  className="bg-blue-600 hover:bg-blue-700 flex items-center"
                >
                  <Download className="h-4 w-4 mr-2" />
                  Download Markdown
                </Button>
                
                {/* Additional Format Buttons */}
                <Button
                  onClick={() => handleDownload('html')}
                  className="bg-green-600 hover:bg-green-700 flex items-center"
                >
                  <FileText className="h-4 w-4 mr-2" />
                  Download HTML
                </Button>
                
                <Button
                  onClick={() => handleDownload('txt')}
                  className="bg-gray-600 hover:bg-gray-700 flex items-center"
                >
                  <FileText className="h-4 w-4 mr-2" />
                  Download Text
                </Button>
                
                {/* Batch Download */}
                <Button
                  onClick={async () => {
                    const { downloadMultipleFormats } = await import('../utils/fileDownload');
                    const cloudFrontUrl = `https://d3in1w40kamst9.cloudfront.net/${result.readme_generation.s3_location.key}`;
                    const response = await fetch(cloudFrontUrl);
                    const content = await response.text();
                    await downloadMultipleFormats(content, ['md', 'html', 'txt'], {
                      githubUrl: repoUrl,
                      repoName: getRepoName(repoUrl)
                    });
                  }}
                  variant="outline"
                  className="border-purple-200 text-purple-700 hover:bg-purple-50 flex items-center"
                >
                  <Download className="h-4 w-4 mr-2" />
                  All Formats
                </Button>
                
                <Button
                  onClick={handleOpenPreview}
                  className="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white flex items-center"
                >
                  <Eye className="h-4 w-4 mr-2" />
                  Full Preview
                </Button>
                
                <Button
                  onClick={() => {
                    // Use CloudFront CDN URL instead of direct S3
                    const cloudFrontUrl = `https://d3in1w40kamst9.cloudfront.net/${result.readme_generation?.s3_location?.key}`;
                    window.open(cloudFrontUrl, '_blank');
                  }}
                  variant="outline"
                >
                  <FileText className="h-4 w-4 mr-2" />
                  View Raw
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Email Notification Status */}
          {result.email_notification && (
            <Card className="bg-green-50 border-green-200">
              <CardHeader>
                <CardTitle className="text-green-800 flex items-center gap-2">
                  <Mail className="h-5 w-5" />
                  📧 Email Notification Status
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex items-center gap-2">
                  {result.email_notification.sent ? (
                    <>
                      <span className="text-green-600">✅ Email sent successfully!</span>
                      <span className="text-gray-600">to {result.user_email}</span>
                    </>
                  ) : (
                    <>
                      <span className="text-orange-600">⚠️ Email sending failed</span>
                      <span className="text-gray-600">(README still generated successfully)</span>
                    </>
                  )}
                </div>
              </CardContent>
            </Card>
          )}

          {/* Professional Features */}
          <Card className="bg-purple-50 border-purple-200">
            <CardHeader>
              <CardTitle className="text-purple-800 flex items-center gap-2">
                <Zap className="h-5 w-5" />
                🚀 Professional Features Used
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                {(result.pipeline_features || [
                  'Advanced AI-powered analysis',
                  'Intelligent code understanding',
                  'Multi-model consensus validation',
                  'Professional README generation',
                  'Enhanced markdown formatting',
                  'Email notifications',
                  'Complete pipeline tracking',
                  'Enterprise-grade reliability'
                ]).map((feature, index) => (
                  <div key={index} className="flex items-center text-purple-700">
                    <span className="mr-2">✅</span>
                    {feature}
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Processing Time */}
          <Card className="bg-gray-50 border-gray-200">
            <CardContent className="pt-6">
              <div className="flex items-center justify-center text-gray-600">
                <Clock className="h-4 w-4 mr-2" />
                <span>
                  Processing completed in {result.ai_analysis?.processing_time 
                    ? `${result.ai_analysis.processing_time.toFixed(1)} seconds`
                    : 'under 60 seconds'
                  }
                </span>
              </div>
            </CardContent>
          </Card>

          {/* Working Enhanced README Preview */}
          <READMEPreviewWorking 
            result={result} 
            githubUrl={githubUrl}
            repoName={extractRepoName(githubUrl)}
          />

          {/* Simple README Preview */}
          {showPreview && previewContent && (
            <Card className="bg-gradient-to-br from-green-50 via-white to-blue-50 border-green-200">
              <CardHeader className="bg-gradient-to-r from-green-600 to-blue-600 text-white rounded-t-lg">
                <CardTitle className="flex items-center space-x-3">
                  <Eye className="h-5 w-5" />
                  <span>README Preview</span>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => setShowPreview(false)}
                    className="text-white hover:bg-white/20 ml-auto"
                  >
                    ✕ Close
                  </Button>
                </CardTitle>
              </CardHeader>
              <CardContent className="p-6">
                <div className="prose max-w-none">
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>
                    {previewContent}
                  </ReactMarkdown>
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      )}
    </div>
  );
};

export default ReadmeGeneratorAdvanced;
