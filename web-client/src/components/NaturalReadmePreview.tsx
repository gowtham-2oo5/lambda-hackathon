"use client";

import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { github } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { Button } from '@/components/ui/button';
import { Copy, Download, ArrowLeft, ExternalLink } from 'lucide-react';
import { toast } from 'sonner';
import { useRouter } from 'next/navigation';

interface NaturalReadmePreviewProps {
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

const NaturalReadmePreview: React.FC<NaturalReadmePreviewProps> = ({ content, metadata }) => {
  const router = useRouter();

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(content);
      toast.success('Copied to clipboard');
    } catch (err) {
      toast.error('Failed to copy');
    }
  };

  const handleDownload = () => {
    const blob = new Blob([content], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `README.md`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    toast.success('Downloaded README.md');
  };

  const markdownComponents = {
    code({ node, inline, className, children, ...props }: any) {
      const match = /language-(\w+)/.exec(className || '');
      return !inline && match ? (
        <SyntaxHighlighter
          style={github}
          language={match[1]}
          PreTag="div"
          customStyle={{
            background: '#f6f8fa',
            border: '1px solid #d1d9e0',
            borderRadius: '6px',
            fontSize: '14px',
            margin: '16px 0'
          }}
          {...props}
        >
          {String(children).replace(/\n$/, '')}
        </SyntaxHighlighter>
      ) : (
        <code 
          className="bg-gray-100 px-1 py-0.5 rounded text-sm font-mono"
          style={{
            backgroundColor: 'rgba(175,184,193,0.2)',
            padding: '0.2em 0.4em',
            fontSize: '85%',
            borderRadius: '3px'
          }}
          {...props}
        >
          {children}
        </code>
      );
    },
    
    h1: ({ children }) => (
      <h1 className="text-3xl font-semibold mb-4 pb-2 border-b border-gray-200">
        {children}
      </h1>
    ),
    h2: ({ children }) => (
      <h2 className="text-2xl font-semibold mb-3 mt-6 pb-1 border-b border-gray-200">
        {children}
      </h2>
    ),
    h3: ({ children }) => (
      <h3 className="text-xl font-semibold mb-2 mt-5">
        {children}
      </h3>
    ),

    a: ({ href, children }) => (
      <a 
        href={href} 
        target="_blank" 
        rel="noopener noreferrer"
        className="text-blue-600 hover:underline"
      >
        {children}
      </a>
    ),

    blockquote: ({ children }) => (
      <blockquote className="border-l-4 border-gray-300 pl-4 py-2 text-gray-600 bg-gray-50 my-4">
        {children}
      </blockquote>
    ),

    table: ({ children }) => (
      <div className="overflow-x-auto my-4">
        <table className="min-w-full border-collapse border border-gray-300">
          {children}
        </table>
      </div>
    ),
    th: ({ children }) => (
      <th className="px-3 py-2 text-left font-semibold border border-gray-300 bg-gray-50">
        {children}
      </th>
    ),
    td: ({ children }) => (
      <td className="px-3 py-2 border border-gray-300">
        {children}
      </td>
    ),

    ul: ({ children }) => (
      <ul className="list-disc ml-6 my-4 space-y-1">
        {children}
      </ul>
    ),
    ol: ({ children }) => (
      <ol className="list-decimal ml-6 my-4 space-y-1">
        {children}
      </ol>
    ),

    p: ({ children }) => (
      <p className="mb-4 leading-relaxed">
        {children}
      </p>
    ),

    hr: () => (
      <hr className="my-6 border-gray-300" />
    ),

    img: ({ src, alt }) => (
      <img 
        src={src} 
        alt={alt} 
        className="max-w-full h-auto rounded-lg my-4"
      />
    )
  };

  return (
    <div className="min-h-screen bg-white">
      {/* Simple header */}
      <div className="border-b border-gray-200 bg-white sticky top-0 z-10">
        <div className="max-w-4xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <Button
                variant="ghost"
                size="sm"
                onClick={() => router.back()}
                className="text-gray-600 hover:text-gray-900"
              >
                <ArrowLeft className="h-4 w-4 mr-2" />
                Back
              </Button>
              <div>
                <h1 className="text-lg font-medium text-gray-900">
                  {metadata.repoName}
                </h1>
                <p className="text-sm text-gray-500">
                  README.md
                </p>
              </div>
            </div>
            
            <div className="flex items-center space-x-2">
              <Button
                variant="outline"
                size="sm"
                onClick={handleCopy}
              >
                <Copy className="h-4 w-4 mr-1" />
                Copy
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={handleDownload}
              >
                <Download className="h-4 w-4 mr-1" />
                Download
              </Button>
              {metadata.repoUrl && (
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => window.open(metadata.repoUrl, '_blank')}
                >
                  <ExternalLink className="h-4 w-4 mr-1" />
                  GitHub
                </Button>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Clean content area */}
      <div className="max-w-4xl mx-auto px-6 py-8">
        <div 
          className="prose prose-lg max-w-none"
          style={{
            fontFamily: '-apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans",Helvetica,Arial,sans-serif',
            fontSize: '16px',
            lineHeight: '1.6',
            color: '#24292f'
          }}
        >
          <ReactMarkdown
            remarkPlugins={[remarkGfm]}
            components={markdownComponents}
          >
            {content}
          </ReactMarkdown>
        </div>
      </div>

      {/* Simple footer */}
      <div className="border-t border-gray-200 bg-gray-50 mt-12">
        <div className="max-w-4xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between text-sm text-gray-500">
            <div>
              Generated by Smart ReadmeGen AI
            </div>
            <div>
              {metadata.primaryLanguage} • {(metadata.confidence * 100).toFixed(0)}% confidence
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default NaturalReadmePreview;
