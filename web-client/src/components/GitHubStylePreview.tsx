"use client";

import React, { useState } from 'react';
import Image from 'next/image';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import remarkBreaks from 'remark-breaks';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { github } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { Button } from '@/components/ui/button';
import { 
  Copy, 
  Download, 
  ExternalLink, 
  Star, 
  GitFork, 
  Eye,
  Code,
  FileText,
  Users,
  Calendar,
  Tag,
  ArrowLeft
} from 'lucide-react';
import { toast } from 'sonner';
import { useRouter } from 'next/navigation';

interface GitHubStylePreviewProps {
  content: string;
  metadata: {
    repoName: string;
    repoUrl: string;
    owner: string;
    generatedAt: string;
    projectType: string;
    primaryLanguage: string;
    frameworks: string[];
    confidence: number;
    processingTime: number;
  };
}

const GitHubStylePreview: React.FC<GitHubStylePreviewProps> = ({ content, metadata }) => {
  const router = useRouter();
  const [activeTab, setActiveTab] = useState<'readme' | 'code'>('readme');
  const [stars] = useState(Math.floor(Math.random() * 1000) + 100);
  const [forks] = useState(Math.floor(Math.random() * 200) + 20);
  const [watchers] = useState(Math.floor(Math.random() * 50) + 10);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(content);
      toast.success('README copied to clipboard!');
    } catch {
      toast.error('Failed to copy to clipboard');
    }
  };

  const handleDownload = () => {
    const blob = new Blob([content], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${metadata.repoName}-README.md`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    toast.success('README downloaded!');
  };

  const markdownComponents = {
    // Code blocks with GitHub styling
    code({ inline, className, children, ...props }: any) {
      const match = /language-(\w+)/.exec(className || '');
      return !inline && match ? (
        <SyntaxHighlighter
          style={github}
          language={match[1]}
          PreTag="div"
          className="github-code-block"
          customStyle={{
            background: '#f6f8fa',
            border: '1px solid #d0d7de',
            borderRadius: '6px',
            fontSize: '14px',
            lineHeight: '1.45',
            overflow: 'auto',
            padding: '16px',
            margin: '16px 0'
          }}
          {...props}
        >
          {String(children).replace(/\n$/, '')}
        </SyntaxHighlighter>
      ) : (
        <code 
          className="bg-gray-100 text-gray-800 px-1 py-0.5 rounded text-sm font-mono border"
          style={{
            backgroundColor: 'rgba(175,184,193,0.2)',
            padding: '0.2em 0.4em',
            fontSize: '85%',
            borderRadius: '6px'
          }}
          {...props}
        >
          {children}
        </code>
      );
    },
    
    // GitHub-style headings
    h1: ({ children }) => (
      <h1 className="text-3xl font-semibold text-gray-900 mb-4 pb-2 border-b border-gray-200" 
          style={{ borderBottom: '1px solid #d0d7de', paddingBottom: '0.3em', marginBottom: '16px' }}>
        {children}
      </h1>
    ),
    h2: ({ children }) => (
      <h2 className="text-2xl font-semibold text-gray-900 mb-3 mt-6 pb-1 border-b border-gray-200"
          style={{ borderBottom: '1px solid #d0d7de', paddingBottom: '0.3em', marginTop: '24px', marginBottom: '16px' }}>
        {children}
      </h2>
    ),
    h3: ({ children }) => (
      <h3 className="text-xl font-semibold text-gray-900 mb-2 mt-5"
          style={{ marginTop: '24px', marginBottom: '16px' }}>
        {children}
      </h3>
    ),
    h4: ({ children }) => (
      <h4 className="text-lg font-semibold text-gray-900 mb-2 mt-4"
          style={{ marginTop: '24px', marginBottom: '16px' }}>
        {children}
      </h4>
    ),
    h5: ({ children }) => (
      <h5 className="text-base font-semibold text-gray-900 mb-2 mt-4"
          style={{ marginTop: '24px', marginBottom: '16px' }}>
        {children}
      </h5>
    ),
    h6: ({ children }) => (
      <h6 className="text-sm font-semibold text-gray-900 mb-2 mt-4"
          style={{ marginTop: '24px', marginBottom: '16px' }}>
        {children}
      </h6>
    ),

    // GitHub-style links
    a: ({ href, children }) => (
      <a 
        href={href} 
        target="_blank" 
        rel="noopener noreferrer"
        className="text-blue-600 hover:underline"
        style={{ color: '#0969da' }}
      >
        {children}
      </a>
    ),

    // GitHub-style blockquotes
    blockquote: ({ children }) => (
      <blockquote 
        className="border-l-4 pl-4 py-2 text-gray-600 bg-gray-50"
        style={{
          borderLeft: '0.25em solid #d0d7de',
          padding: '0 1em',
          color: '#656d76',
          margin: '16px 0'
        }}
      >
        {children}
      </blockquote>
    ),

    // GitHub-style tables
    table: ({ children }) => (
      <div className="overflow-x-auto my-4">
        <table 
          className="min-w-full border-collapse"
          style={{
            borderSpacing: 0,
            borderCollapse: 'collapse',
            marginTop: '16px',
            marginBottom: '16px'
          }}
        >
          {children}
        </table>
      </div>
    ),
    th: ({ children }) => (
      <th 
        className="px-3 py-2 text-left text-sm font-semibold text-gray-900 border border-gray-300 bg-gray-50"
        style={{
          padding: '6px 13px',
          border: '1px solid #d0d7de',
          backgroundColor: '#f6f8fa',
          fontWeight: 600
        }}
      >
        {children}
      </th>
    ),
    td: ({ children }) => (
      <td 
        className="px-3 py-2 text-sm text-gray-700 border border-gray-300"
        style={{
          padding: '6px 13px',
          border: '1px solid #d0d7de'
        }}
      >
        {children}
      </td>
    ),

    // GitHub-style lists
    ul: ({ children }) => (
      <ul 
        className="list-disc ml-6 space-y-1 text-gray-700"
        style={{ paddingLeft: '2em', margin: '16px 0' }}
      >
        {children}
      </ul>
    ),
    ol: ({ children }) => (
      <ol 
        className="list-decimal ml-6 space-y-1 text-gray-700"
        style={{ paddingLeft: '2em', margin: '16px 0' }}
      >
        {children}
      </ol>
    ),
    li: ({ children }) => (
      <li style={{ margin: '0.25em 0' }}>
        {children}
      </li>
    ),

    // GitHub-style paragraphs
    p: ({ children }) => (
      <p 
        className="text-gray-700 leading-relaxed"
        style={{ 
          marginTop: '16px', 
          marginBottom: '16px',
          lineHeight: '1.6'
        }}
      >
        {children}
      </p>
    ),

    // GitHub-style horizontal rules
    hr: () => (
      <hr 
        className="my-6 border-gray-200"
        style={{
          height: '0.25em',
          padding: 0,
          margin: '24px 0',
          backgroundColor: '#d0d7de',
          border: 0
        }}
      />
    ),

    // GitHub-style images
    img: ({ src, alt }) => (
      <Image 
        src={src || ''} 
        alt={alt || ''} 
        width={800}
        height={400}
        className="max-w-full h-auto rounded-lg shadow-sm"
        style={{ maxWidth: '100%', height: 'auto' }}
      />
    )
  };

  return (
    <div className="min-h-screen bg-white">
      {/* GitHub-style header */}
      <div className="bg-gray-50 border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between py-4">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => router.back()}
              className="flex items-center space-x-2 text-gray-600 hover:text-gray-900"
            >
              <ArrowLeft className="h-4 w-4" />
              <span>Back</span>
            </Button>
            
            <div className="flex items-center space-x-4">
              <Button
                variant="outline"
                size="sm"
                onClick={handleCopy}
                className="flex items-center space-x-1"
              >
                <Copy className="h-4 w-4" />
                <span>Copy</span>
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={handleDownload}
                className="flex items-center space-x-1"
              >
                <Download className="h-4 w-4" />
                <span>Download</span>
              </Button>
              {metadata.repoUrl && (
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => window.open(metadata.repoUrl, '_blank')}
                  className="flex items-center space-x-1"
                >
                  <ExternalLink className="h-4 w-4" />
                  <span>View on GitHub</span>
                </Button>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* GitHub-style repository header */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <div className="flex items-center space-x-2 mb-2">
                <FileText className="h-5 w-5 text-gray-600" />
                <h1 className="text-2xl font-semibold text-blue-600 hover:underline cursor-pointer">
                  {metadata.owner} / <span className="font-bold">{metadata.repoName}</span>
                </h1>
                <span className="px-2 py-1 text-xs font-medium text-gray-600 bg-gray-100 rounded-full border">
                  Public
                </span>
              </div>
              
              <p className="text-gray-600 mb-4">
                AI-generated professional README documentation
              </p>
              
              <div className="flex items-center space-x-6 text-sm text-gray-600">
                <div className="flex items-center space-x-1">
                  <Star className="h-4 w-4" />
                  <span className="font-semibold">{stars}</span>
                  <span>stars</span>
                </div>
                <div className="flex items-center space-x-1">
                  <GitFork className="h-4 w-4" />
                  <span className="font-semibold">{forks}</span>
                  <span>forks</span>
                </div>
                <div className="flex items-center space-x-1">
                  <Eye className="h-4 w-4" />
                  <span className="font-semibold">{watchers}</span>
                  <span>watching</span>
                </div>
              </div>
            </div>
            
            <div className="flex items-center space-x-2">
              <Button variant="outline" size="sm" className="flex items-center space-x-1">
                <Eye className="h-4 w-4" />
                <span>Watch</span>
              </Button>
              <Button variant="outline" size="sm" className="flex items-center space-x-1">
                <GitFork className="h-4 w-4" />
                <span>Fork</span>
              </Button>
              <Button variant="outline" size="sm" className="flex items-center space-x-1">
                <Star className="h-4 w-4" />
                <span>Star</span>
              </Button>
            </div>
          </div>
        </div>
      </div>

      {/* GitHub-style navigation tabs */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <nav className="flex space-x-8">
            <button
              onClick={() => setActiveTab('readme')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'readme'
                  ? 'border-orange-500 text-gray-900'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <div className="flex items-center space-x-2">
                <FileText className="h-4 w-4" />
                <span>README</span>
              </div>
            </button>
            <button
              onClick={() => setActiveTab('code')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'code'
                  ? 'border-orange-500 text-gray-900'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <div className="flex items-center space-x-2">
                <Code className="h-4 w-4" />
                <span>Code</span>
              </div>
            </button>
          </nav>
        </div>
      </div>

      {/* Main content area */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'readme' ? (
          <div className="bg-white">
            {/* README header */}
            <div className="flex items-center justify-between mb-6 pb-4 border-b border-gray-200">
              <div className="flex items-center space-x-2">
                <FileText className="h-5 w-5 text-gray-600" />
                <h2 className="text-lg font-semibold text-gray-900">README.md</h2>
              </div>
              <div className="flex items-center space-x-2 text-sm text-gray-500">
                <Calendar className="h-4 w-4" />
                <span>Generated {new Date(metadata.generatedAt).toLocaleDateString()}</span>
              </div>
            </div>

            {/* README content with GitHub styling */}
            <div 
              className="prose max-w-none"
              style={{
                fontFamily: '-apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans",Helvetica,Arial,sans-serif',
                fontSize: '16px',
                lineHeight: '1.6',
                color: '#1f2328'
              }}
            >
              <ReactMarkdown
                remarkPlugins={[remarkGfm, remarkBreaks]}
                components={markdownComponents}
              >
                {content}
              </ReactMarkdown>
            </div>
          </div>
        ) : (
          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <div className="text-center py-12">
              <Code className="h-12 w-12 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Repository Code View
              </h3>
              <p className="text-gray-600 mb-4">
                This would show the repository file structure and code files.
              </p>
              <div className="bg-gray-50 rounded-lg p-4 text-left max-w-md mx-auto">
                <div className="font-mono text-sm text-gray-700">
                  <div className="flex items-center space-x-2 mb-1">
                    <span className="text-blue-600">📁</span>
                    <span>src/</span>
                  </div>
                  <div className="flex items-center space-x-2 mb-1 ml-4">
                    <span className="text-green-600">📄</span>
                    <span>index.{metadata.primaryLanguage.toLowerCase()}</span>
                  </div>
                  <div className="flex items-center space-x-2 mb-1">
                    <span className="text-green-600">📄</span>
                    <span>package.json</span>
                  </div>
                  <div className="flex items-center space-x-2 mb-1">
                    <span className="text-green-600">📄</span>
                    <span>README.md</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <span className="text-green-600">📄</span>
                    <span>LICENSE</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* GitHub-style footer info */}
      <div className="bg-gray-50 border-t border-gray-200 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between text-sm text-gray-600">
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-1">
                <div className="w-3 h-3 bg-blue-500 rounded-full"></div>
                <span>{metadata.primaryLanguage}</span>
              </div>
              <div className="flex items-center space-x-1">
                <Tag className="h-4 w-4" />
                <span>{metadata.projectType}</span>
              </div>
              <div className="flex items-center space-x-1">
                <Users className="h-4 w-4" />
                <span>AI Confidence: {(metadata.confidence * 100).toFixed(1)}%</span>
              </div>
            </div>
            <div className="text-xs text-gray-500">
              Generated by Smart ReadmeGen AI in {metadata.processingTime.toFixed(1)}s
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default GitHubStylePreview;
