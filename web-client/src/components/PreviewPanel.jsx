import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { oneDark } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { toast } from 'sonner';

const READMEPreview = ({ result, onDownload }) => {
  const [activeTab, setActiveTab] = useState('preview');
  const [readmeContent, setReadmeContent] = useState('');
  const [loading, setLoading] = useState(false);
  const [isFullscreen, setIsFullscreen] = useState(false);

  // Fetch README content from S3/CloudFront
  useEffect(() => {
    const fetchReadmeContent = async () => {
      if (!result?.readme_generation?.s3_location?.key) return;
      
      setLoading(true);
      try {
        const cloudFrontUrl = `https://d3in1w40kamst9.cloudfront.net/${result.readme_generation.s3_location.key}`;
        const response = await fetch(cloudFrontUrl);
        
        if (!response.ok) {
          throw new Error(`Failed to fetch README: ${response.status}`);
        }
        
        const content = await response.text();
        setReadmeContent(content);
      } catch (error) {
        console.error('Error fetching README:', error);
        toast.error('Failed to load README preview');
        setReadmeContent('# Error Loading README\n\nUnable to load README content for preview.');
      } finally {
        setLoading(false);
      }
    };

    fetchReadmeContent();
  }, [result]);

  const handleCopyContent = () => {
    navigator.clipboard.writeText(readmeContent);
    toast.success('README content copied to clipboard!');
  };

  const handleCopySection = (section) => {
    navigator.clipboard.writeText(section);
    toast.success('Section copied to clipboard!');
  };

  const toggleFullscreen = () => {
    setIsFullscreen(!isFullscreen);
  };

  if (!result || !result.readme_generation) {
    return null;
  }

  const tabs = [
    { id: 'preview', label: '👀 Preview', icon: '👀' },
    { id: 'raw', label: '📝 Raw Markdown', icon: '📝' },
    { id: 'stats', label: '📊 Analysis', icon: '📊' }
  ];

  return (
    <>
      <Card className={`bg-gradient-to-br from-green-50 via-white to-blue-50 border-green-200 ${isFullscreen ? 'fixed inset-4 z-50 overflow-auto' : ''}`}>
        <CardHeader className="bg-gradient-to-r from-green-600 to-blue-600 text-white rounded-t-lg">
          <div className="flex items-center justify-between">
            <CardTitle className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-white/20 rounded-lg flex items-center justify-center">
                👀
              </div>
              <span>README Preview</span>
              <Badge variant="secondary" className="bg-white/20 text-white border-white/30">
                {readmeContent.length.toLocaleString()} characters
              </Badge>
            </CardTitle>
            <div className="flex items-center space-x-2">
              <Button
                variant="ghost"
                size="sm"
                onClick={toggleFullscreen}
                className="text-white hover:bg-white/20"
              >
                {isFullscreen ? '🗗 Exit Fullscreen' : '🗖 Fullscreen'}
              </Button>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setIsFullscreen(false)}
                className="text-white hover:bg-white/20"
              >
                ✕
              </Button>
            </div>
          </div>
        </CardHeader>

        <CardContent className="p-0">
          {/* Tab Navigation */}
          <div className="flex border-b border-gray-200 bg-white">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex-1 px-4 py-3 text-sm font-medium transition-colors ${
                  activeTab === tab.id
                    ? 'border-b-2 border-blue-500 text-blue-600 bg-blue-50'
                    : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'
                }`}
              >
                <span className="mr-2">{tab.icon}</span>
                {tab.label}
              </button>
            ))}
          </div>

          {/* Tab Content */}
          <div className={`${isFullscreen ? 'h-[calc(100vh-200px)]' : 'max-h-96'} overflow-auto`}>
            {loading ? (
              <div className="flex items-center justify-center py-12">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mr-3"></div>
                <span className="text-gray-600">Loading README preview...</span>
              </div>
            ) : (
              <>
                {/* Preview Tab */}
                {activeTab === 'preview' && (
                  <div className="p-6 prose prose-lg max-w-none">
                    <ReactMarkdown
                      remarkPlugins={[remarkGfm]}
                      components={{
                        code({ node, inline, className, children, ...props }) {
                          const match = /language-(\w+)/.exec(className || '');
                          return !inline && match ? (
                            <SyntaxHighlighter
                              style={oneDark}
                              language={match[1]}
                              PreTag="div"
                              {...props}
                            >
                              {String(children).replace(/\n$/, '')}
                            </SyntaxHighlighter>
                          ) : (
                            <code className={className} {...props}>
                              {children}
                            </code>
                          );
                        },
                        h1: ({ children }) => (
                          <div className="group relative">
                            <h1 className="text-3xl font-bold text-gray-900 mb-4 pb-2 border-b-2 border-blue-200">
                              {children}
                            </h1>
                            <button
                              onClick={() => handleCopySection(`# ${children}`)}
                              className="absolute right-0 top-0 opacity-0 group-hover:opacity-100 transition-opacity bg-blue-100 hover:bg-blue-200 text-blue-600 px-2 py-1 rounded text-xs"
                            >
                              📋 Copy
                            </button>
                          </div>
                        ),
                        h2: ({ children }) => (
                          <div className="group relative">
                            <h2 className="text-2xl font-semibold text-gray-800 mt-8 mb-3">
                              {children}
                            </h2>
                            <button
                              onClick={() => handleCopySection(`## ${children}`)}
                              className="absolute right-0 top-0 opacity-0 group-hover:opacity-100 transition-opacity bg-blue-100 hover:bg-blue-200 text-blue-600 px-2 py-1 rounded text-xs"
                            >
                              📋 Copy
                            </button>
                          </div>
                        ),
                        h3: ({ children }) => (
                          <div className="group relative">
                            <h3 className="text-xl font-semibold text-gray-800 mt-6 mb-2">
                              {children}
                            </h3>
                            <button
                              onClick={() => handleCopySection(`### ${children}`)}
                              className="absolute right-0 top-0 opacity-0 group-hover:opacity-100 transition-opacity bg-blue-100 hover:bg-blue-200 text-blue-600 px-2 py-1 rounded text-xs"
                            >
                              📋 Copy
                            </button>
                          </div>
                        ),
                      }}
                    >
                      {readmeContent}
                    </ReactMarkdown>
                  </div>
                )}

                {/* Raw Markdown Tab */}
                {activeTab === 'raw' && (
                  <div className="relative">
                    <div className="absolute top-4 right-4 z-10">
                      <Button
                        onClick={handleCopyContent}
                        size="sm"
                        className="bg-blue-600 hover:bg-blue-700 text-white"
                      >
                        📋 Copy All
                      </Button>
                    </div>
                    <SyntaxHighlighter
                      language="markdown"
                      style={oneDark}
                      customStyle={{
                        margin: 0,
                        borderRadius: 0,
                        fontSize: '14px',
                        lineHeight: '1.5',
                      }}
                      showLineNumbers
                    >
                      {readmeContent}
                    </SyntaxHighlighter>
                  </div>
                )}

                {/* Analysis Tab */}
                {activeTab === 'stats' && (
                  <div className="p-6 space-y-6">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
                        <h4 className="font-semibold text-blue-800 mb-2">📊 Content Analysis</h4>
                        <div className="space-y-2 text-sm">
                          <div className="flex justify-between">
                            <span>Total Characters:</span>
                            <span className="font-semibold">{readmeContent.length.toLocaleString()}</span>
                          </div>
                          <div className="flex justify-between">
                            <span>Word Count:</span>
                            <span className="font-semibold">{readmeContent.split(/\s+/).length.toLocaleString()}</span>
                          </div>
                          <div className="flex justify-between">
                            <span>Lines:</span>
                            <span className="font-semibold">{readmeContent.split('\n').length.toLocaleString()}</span>
                          </div>
                          <div className="flex justify-between">
                            <span>Sections:</span>
                            <span className="font-semibold">{(readmeContent.match(/^#+\s/gm) || []).length}</span>
                          </div>
                        </div>
                      </div>

                      <div className="bg-green-50 p-4 rounded-lg border border-green-200">
                        <h4 className="font-semibold text-green-800 mb-2">🏆 Quality Metrics</h4>
                        <div className="space-y-2 text-sm">
                          <div className="flex justify-between">
                            <span>Project Type:</span>
                            <span className="font-semibold">{result.ai_analysis?.project_type || 'Unknown'}</span>
                          </div>
                          <div className="flex justify-between">
                            <span>Confidence:</span>
                            <span className="font-semibold">
                              {result.ai_analysis?.confidence 
                                ? `${(result.ai_analysis.confidence * 100).toFixed(1)}%`
                                : 'N/A'
                              }
                            </span>
                          </div>
                          <div className="flex justify-between">
                            <span>Language:</span>
                            <span className="font-semibold">{result.ai_analysis?.primary_language || 'Unknown'}</span>
                          </div>
                          <div className="flex justify-between">
                            <span>Generated:</span>
                            <span className="font-semibold">
                              {result.readme_generation?.generation_timestamp 
                                ? new Date(result.readme_generation.generation_timestamp).toLocaleString()
                                : 'Unknown'
                              }
                            </span>
                          </div>
                        </div>
                      </div>
                    </div>

                    {/* Frameworks */}
                    {result.ai_analysis?.frameworks && result.ai_analysis.frameworks.length > 0 && (
                      <div className="bg-purple-50 p-4 rounded-lg border border-purple-200">
                        <h4 className="font-semibold text-purple-800 mb-3">🔧 Detected Frameworks</h4>
                        <div className="flex flex-wrap gap-2">
                          {result.ai_analysis.frameworks.map((framework, index) => (
                            <Badge key={index} variant="secondary" className="bg-purple-100 text-purple-700">
                              {framework}
                            </Badge>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </>
            )}
          </div>

          {/* Action Buttons */}
          <div className="border-t border-gray-200 bg-gray-50 px-6 py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2 text-sm text-gray-600">
                <span>✨ Professional README generated by SmartReadmeGen AI</span>
              </div>
              <div className="flex items-center space-x-3">
                <Button
                  onClick={handleCopyContent}
                  variant="outline"
                  size="sm"
                  className="flex items-center space-x-2"
                >
                  <span>📋</span>
                  <span>Copy Content</span>
                </Button>
                <Button
                  onClick={onDownload}
                  className="bg-gradient-to-r from-green-600 to-blue-600 hover:from-green-700 hover:to-blue-700 text-white flex items-center space-x-2"
                >
                  <span>💾</span>
                  <span>Download README.md</span>
                </Button>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Fullscreen Backdrop */}
      {isFullscreen && (
        <div 
          className="fixed inset-0 bg-black/50 z-40"
          onClick={() => setIsFullscreen(false)}
        />
      )}
    </>
  );
};

export default READMEPreview;
