import React, { useState, useEffect, useMemo } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { oneDark, oneLight } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { toast } from 'sonner';
import { downloadReadme, downloadMultipleFormats, copyToClipboard } from '../utils/fileDownload';
import { 
  Download, 
  Copy, 
  Eye, 
  Code, 
  BarChart3, 
  Maximize2, 
  Minimize2, 
  FileText,
  Globe,
  Palette,
  List
} from 'lucide-react';

const PreviewPanelAdvanced = ({ result, githubUrl = '', repoName = '' }) => {
  const [activeTab, setActiveTab] = useState('preview');
  const [readmeContent, setReadmeContent] = useState('');
  const [loading, setLoading] = useState(false);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [theme, setTheme] = useState('light');
  const [showToc, setShowToc] = useState(false);

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

  // Generate Table of Contents
  const tableOfContents = useMemo(() => {
    if (!readmeContent) return [];
    
    const headings = [];
    const lines = readmeContent.split('\n');
    
    lines.forEach((line, index) => {
      const match = line.match(/^(#{1,6})\s+(.+)$/);
      if (match) {
        const level = match[1].length;
        const text = match[2].trim();
        const id = text.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
        
        headings.push({
          level,
          text,
          id,
          line: index + 1
        });
      }
    });
    
    return headings;
  }, [readmeContent]);

  // Enhanced download handlers
  const handleDownload = async (format = 'md') => {
    if (!readmeContent) {
      toast.error('No content to download');
      return;
    }

    await downloadReadme(readmeContent, {
      format,
      githubUrl,
      repoName,
    });
  };

  const handleBatchDownload = async () => {
    if (!readmeContent) {
      toast.error('No content to download');
      return;
    }

    await downloadMultipleFormats(readmeContent, ['md', 'html', 'txt'], {
      githubUrl,
      repoName,
    });
  };

  const handleCopy = async (format = 'markdown') => {
    if (!readmeContent) {
      toast.error('No content to copy');
      return;
    }

    await copyToClipboard(readmeContent, format);
  };

  const toggleFullscreen = () => {
    setIsFullscreen(!isFullscreen);
  };

  const scrollToHeading = (id) => {
    const element = document.getElementById(id);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  // Custom markdown components
  const markdownComponents = {
    code({ node, inline, className, children, ...props }) {
      const match = /language-(\w+)/.exec(className || '');
      return !inline && match ? (
        <SyntaxHighlighter
          style={theme === 'dark' ? oneDark : oneLight}
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
    h1: ({ children, ...props }) => (
      <h1 id={String(children).toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '')} {...props}>
        {children}
      </h1>
    ),
    h2: ({ children, ...props }) => (
      <h2 id={String(children).toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '')} {...props}>
        {children}
      </h2>
    ),
    h3: ({ children, ...props }) => (
      <h3 id={String(children).toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '')} {...props}>
        {children}
      </h3>
    ),
  };

  if (!result || !result.readme_generation) {
    return null;
  }

  const tabs = [
    { id: 'preview', label: 'Preview', icon: Eye },
    { id: 'raw', label: 'Raw Markdown', icon: Code },
    { id: 'stats', label: 'Analysis', icon: BarChart3 }
  ];

  const downloadOptions = [
    { format: 'md', label: 'Markdown', icon: FileText, color: 'bg-blue-600' },
    { format: 'html', label: 'HTML', icon: Globe, color: 'bg-green-600' },
    { format: 'txt', label: 'Plain Text', icon: FileText, color: 'bg-gray-600' }
  ];

  return (
    <>
      <Card className={`bg-gradient-to-br from-green-50 via-white to-blue-50 border-green-200 transition-all duration-300 ${
        isFullscreen ? 'fixed inset-4 z-50 overflow-auto shadow-2xl' : ''
      }`}>
        <CardHeader className="bg-gradient-to-r from-green-600 to-blue-600 text-white rounded-t-lg">
          <div className="flex items-center justify-between">
            <CardTitle className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-white/20 rounded-lg flex items-center justify-center">
                <Eye className="h-4 w-4" />
              </div>
              <span>Smart ReadmeGen Preview</span>
              <Badge variant="secondary" className="bg-white/20 text-white border-white/30">
                {readmeContent.length.toLocaleString()} chars
              </Badge>
            </CardTitle>
            
            <div className="flex items-center space-x-2">
              {/* Theme Toggle */}
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}
                className="text-white hover:bg-white/20"
              >
                <Palette className="h-4 w-4" />
              </Button>
              
              {/* TOC Toggle */}
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setShowToc(!showToc)}
                className="text-white hover:bg-white/20"
              >
                <List className="h-4 w-4" />
              </Button>
              
              {/* Fullscreen Toggle */}
              <Button
                variant="ghost"
                size="sm"
                onClick={toggleFullscreen}
                className="text-white hover:bg-white/20"
              >
                {isFullscreen ? <Minimize2 className="h-4 w-4" /> : <Maximize2 className="h-4 w-4" />}
              </Button>
            </div>
          </div>
        </CardHeader>

        <CardContent className="p-0">
          {/* Enhanced Tab Navigation */}
          <div className="flex items-center justify-between border-b bg-gray-50 px-6 py-3">
            <div className="flex space-x-1">
              {tabs.map((tab) => {
                const IconComponent = tab.icon;
                return (
                  <Button
                    key={tab.id}
                    variant={activeTab === tab.id ? "default" : "ghost"}
                    size="sm"
                    onClick={() => setActiveTab(tab.id)}
                    className={`flex items-center space-x-2 ${
                      activeTab === tab.id 
                        ? 'bg-gradient-to-r from-green-600 to-blue-600 text-white' 
                        : 'text-gray-600 hover:text-gray-900'
                    }`}
                  >
                    <IconComponent className="h-4 w-4" />
                    <span>{tab.label}</span>
                  </Button>
                );
              })}
            </div>

            {/* Enhanced Action Buttons */}
            <div className="flex items-center space-x-2">
              {/* Copy Dropdown */}
              <div className="flex space-x-1">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => handleCopy('markdown')}
                  className="flex items-center space-x-1"
                >
                  <Copy className="h-3 w-3" />
                  <span>Copy</span>
                </Button>
              </div>

              {/* Download Options */}
              <div className="flex space-x-1">
                {downloadOptions.map((option) => {
                  const IconComponent = option.icon;
                  return (
                    <Button
                      key={option.format}
                      size="sm"
                      onClick={() => handleDownload(option.format)}
                      className={`${option.color} hover:opacity-90 text-white flex items-center space-x-1`}
                    >
                      <IconComponent className="h-3 w-3" />
                      <span>{option.label}</span>
                    </Button>
                  );
                })}
              </div>

              {/* Batch Download */}
              <Button
                variant="outline"
                size="sm"
                onClick={handleBatchDownload}
                className="flex items-center space-x-1 border-purple-200 text-purple-700 hover:bg-purple-50"
              >
                <Download className="h-3 w-3" />
                <span>All Formats</span>
              </Button>
            </div>
          </div>

          {/* Content Area with TOC */}
          <div className="flex">
            {/* Table of Contents Sidebar */}
            {showToc && tableOfContents.length > 0 && (
              <div className="w-64 border-r bg-gray-50 p-4 max-h-96 overflow-y-auto">
                <h4 className="font-semibold text-gray-900 mb-3 flex items-center">
                  <List className="h-4 w-4 mr-2" />
                  Table of Contents
                </h4>
                <nav className="space-y-1">
                  {tableOfContents.map((heading, index) => (
                    <button
                      key={index}
                      onClick={() => scrollToHeading(heading.id)}
                      className={`block w-full text-left text-sm hover:text-blue-600 transition-colors ${
                        heading.level === 1 ? 'font-medium' : 
                        heading.level === 2 ? 'ml-2' : 
                        heading.level === 3 ? 'ml-4' : 'ml-6'
                      }`}
                      style={{ paddingLeft: `${(heading.level - 1) * 12}px` }}
                    >
                      {heading.text}
                    </button>
                  ))}
                </nav>
              </div>
            )}

            {/* Main Content */}
            <div className="flex-1">
              {loading ? (
                <div className="flex items-center justify-center h-64">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                  <span className="ml-3 text-gray-600">Loading README preview...</span>
                </div>
              ) : (
                <>
                  {/* Preview Tab */}
                  {activeTab === 'preview' && (
                    <div className={`prose max-w-none p-6 ${theme === 'dark' ? 'prose-invert bg-gray-900 text-white' : ''}`}>
                      <ReactMarkdown
                        remarkPlugins={[remarkGfm]}
                        components={markdownComponents}
                      >
                        {readmeContent}
                      </ReactMarkdown>
                    </div>
                  )}

                  {/* Raw Markdown Tab */}
                  {activeTab === 'raw' && (
                    <div className="p-6">
                      <pre className={`whitespace-pre-wrap text-sm rounded-lg p-4 overflow-auto max-h-96 ${
                        theme === 'dark' ? 'bg-gray-900 text-green-400' : 'bg-gray-100 text-gray-800'
                      }`}>
                        {readmeContent}
                      </pre>
                    </div>
                  )}

                  {/* Analysis Stats Tab */}
                  {activeTab === 'stats' && (
                    <div className="p-6 space-y-4">
                      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                        <div className="bg-blue-50 p-4 rounded-lg">
                          <div className="text-2xl font-bold text-blue-600">
                            {readmeContent.length.toLocaleString()}
                          </div>
                          <div className="text-sm text-gray-600">Characters</div>
                        </div>
                        <div className="bg-green-50 p-4 rounded-lg">
                          <div className="text-2xl font-bold text-green-600">
                            {readmeContent.split('\n').length.toLocaleString()}
                          </div>
                          <div className="text-sm text-gray-600">Lines</div>
                        </div>
                        <div className="bg-purple-50 p-4 rounded-lg">
                          <div className="text-2xl font-bold text-purple-600">
                            {readmeContent.split(/\s+/).length.toLocaleString()}
                          </div>
                          <div className="text-sm text-gray-600">Words</div>
                        </div>
                        <div className="bg-orange-50 p-4 rounded-lg">
                          <div className="text-2xl font-bold text-orange-600">
                            {tableOfContents.length}
                          </div>
                          <div className="text-sm text-gray-600">Headings</div>
                        </div>
                      </div>

                      {/* Analysis Summary */}
                      {result?.phase3_analysis && (
                        <div className="bg-gradient-to-r from-blue-50 to-green-50 p-4 rounded-lg">
                          <h4 className="font-semibold text-gray-900 mb-2">Smart Analysis Results</h4>
                          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                            <div>
                              <span className="font-medium">Project Type:</span>
                              <span className="ml-2">{result.phase3_analysis.project_type}</span>
                            </div>
                            <div>
                              <span className="font-medium">Confidence:</span>
                              <span className="ml-2">{(result.phase3_analysis.confidence * 100).toFixed(1)}%</span>
                            </div>
                            <div>
                              <span className="font-medium">Language:</span>
                              <span className="ml-2">{result.phase3_analysis.primary_language}</span>
                            </div>
                            <div>
                              <span className="font-medium">Processing Time:</span>
                              <span className="ml-2">{result.phase3_analysis.processing_time?.toFixed(1)}s</span>
                            </div>
                          </div>
                        </div>
                      )}
                    </div>
                  )}
                </>
              )}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Print Styles */}
      <style jsx>{`
        @media print {
          .prose {
            max-width: none !important;
          }
          .prose h1, .prose h2, .prose h3 {
            break-after: avoid;
          }
          .prose pre {
            break-inside: avoid;
          }
        }
      `}</style>
    </>
  );
};

export default PreviewPanelAdvanced;
