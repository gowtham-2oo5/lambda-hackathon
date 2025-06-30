"use client"

import React from "react"
import Image from "next/image"

import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm"
import remarkEmoji from "remark-emoji"
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter"
import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism"
import { Copy, Check } from "lucide-react"
import { useState } from "react"
import { Button } from "@/components/ui/button"
import rehypeRaw from "rehype-raw"

interface MarkdownRendererProps {
  content: string
}

export function MarkdownRenderer({ content }: MarkdownRendererProps) {
  const [copiedCode, setCopiedCode] = useState<string | null>(null)

  const copyCode = async (code: string) => {
    await navigator.clipboard.writeText(code)
    setCopiedCode(code)
    setTimeout(() => setCopiedCode(null), 2000)
  }

  return (
    <div className="prose prose-slate max-w-none prose-lg">
      <ReactMarkdown
        remarkPlugins={[remarkGfm, remarkEmoji]}
        rehypePlugins={[rehypeRaw]}
        components={{
          // Headings with beautiful styling
          h1: ({ children }) => (
            <h1 className="text-4xl font-bold bg-gradient-to-r from-slate-900 to-slate-700 bg-clip-text text-transparent mb-6 pb-2 border-b-2 border-gradient-to-r from-purple-500 to-blue-500">
              {children}
            </h1>
          ),
          h2: ({ children }) => (
            <h2 className="text-3xl font-semibold text-slate-800 mt-8 mb-4 flex items-center gap-2">
              <span className="w-1 h-8 bg-gradient-to-b from-purple-500 to-blue-500 rounded-full"></span>
              {children}
            </h2>
          ),
          h3: ({ children }) => <h3 className="text-2xl font-semibold text-slate-700 mt-6 mb-3">{children}</h3>,

          // Enhanced paragraphs - handle block elements and badges properly
          p: ({ children }) => {
            // Check if children contains block elements like images
            const hasBlockElements = React.Children.toArray(children).some(
              (child) =>
                React.isValidElement(child) &&
                (child.type === "img" ||
                  (child.props && child.props.className && child.props.className.includes("block"))),
            )

            // Check if paragraph contains only badges
            const childrenArray = React.Children.toArray(children);
            const onlyBadges = childrenArray.every((child) => {
              if (React.isValidElement(child) && child.type === 'img') {
                const src = child.props.src;
                return src && (
                  src.includes('shields.io') ||
                  src.includes('badge') ||
                  src.includes('img.shields.io') ||
                  (src.includes('github.com') && src.includes('badge'))
                );
              }
              return typeof child === 'string' && child.trim() === '';
            });

            if (onlyBadges && childrenArray.some(child => React.isValidElement(child) && child.type === 'img')) {
              return (
                <div className="flex flex-wrap items-center gap-2 my-4">
                  {children}
                </div>
              );
            }

            if (hasBlockElements) {
              return <div className="text-slate-700 leading-relaxed mb-4 text-base">{children}</div>
            }

            return <p className="text-slate-700 leading-relaxed mb-4 text-base">{children}</p>
          },

          // Beautiful and consistent code blocks
          code: ({ inline, className, children, ...props }) => {
            const match = /language-(\w+)/.exec(className || "")
            const codeString = String(children).replace(/\n$/, "")

            if (!inline && match) {
              return (
                <div className="relative group my-6 rounded-lg overflow-hidden border border-slate-200 shadow-sm">
                  <div className="flex items-center justify-between bg-slate-800 text-slate-200 px-4 py-3 text-sm font-medium">
                    <span className="flex items-center gap-3">
                      <div className="flex gap-1.5">
                        <div className="w-3 h-3 rounded-full bg-red-500"></div>
                        <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
                        <div className="w-3 h-3 rounded-full bg-green-500"></div>
                      </div>
                      <span className="text-slate-300">{match[1]}</span>
                    </span>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => copyCode(codeString)}
                      className="opacity-0 group-hover:opacity-100 transition-all duration-200 h-7 px-2 text-slate-300 hover:text-white hover:bg-slate-700 rounded"
                    >
                      {copiedCode === codeString ? (
                        <Check className="w-3.5 h-3.5" />
                      ) : (
                        <Copy className="w-3.5 h-3.5" />
                      )}
                    </Button>
                  </div>
                  <div className="relative">
                    <SyntaxHighlighter
                      style={oneDark}
                      language={match[1]}
                      PreTag="div"
                      className="!mt-0 !mb-0 !rounded-none !border-none"
                      customStyle={{
                        margin: 0,
                        padding: '1rem',
                        fontSize: '0.875rem',
                        lineHeight: '1.5',
                        background: '#0d1117',
                      }}
                      {...props}
                    >
                      {codeString}
                    </SyntaxHighlighter>
                  </div>
                </div>
              )
            }

            // Inline code with consistent styling
            return (
              <code 
                className="bg-slate-100 text-purple-700 px-2 py-0.5 rounded text-sm font-mono border border-slate-200 font-medium" 
                {...props}
              >
                {children}
              </code>
            )
          },

          // Enhanced blockquotes
          blockquote: ({ children }) => (
            <blockquote className="border-l-4 border-blue-500 bg-blue-50 pl-6 pr-4 py-4 my-6 rounded-r-lg">
              <div className="text-slate-700 italic">{children}</div>
            </blockquote>
          ),

          // Beautiful lists
          ul: ({ children }) => <ul className="space-y-2 my-4">{children}</ul>,
          ol: ({ children }) => <ol className="space-y-2 my-4 list-decimal list-inside">{children}</ol>,
          li: ({ children, ...props }) => {
            // Check if it's a task list item
            const isTaskList = typeof children === "object" && Array.isArray(children) && children[0]?.type === "input"

            if (isTaskList) {
              const checkbox = children[0]
              const content = children.slice(1)
              return (
                <li className="flex items-start gap-3 py-1" {...props}>
                  <input
                    type="checkbox"
                    checked={checkbox.props.checked}
                    disabled
                    className="mt-1 w-4 h-4 text-blue-600 rounded focus:ring-blue-500"
                  />
                  <span className={checkbox.props.checked ? "line-through text-slate-500" : "text-slate-700"}>
                    {content}
                  </span>
                </li>
              )
            }

            return (
              <li className="flex items-start gap-2 text-slate-700" {...props}>
                <span className="text-blue-500 font-bold mt-1">•</span>
                <span>{children}</span>
              </li>
            )
          },

          // Enhanced tables
          table: ({ children }) => (
            <div className="overflow-x-auto my-6">
              <table className="w-full border-collapse bg-white rounded-lg shadow-sm border border-slate-200">
                {children}
              </table>
            </div>
          ),
          thead: ({ children }) => <thead className="bg-slate-50">{children}</thead>,
          th: ({ children }) => (
            <th className="border border-slate-200 px-4 py-3 text-left font-semibold text-slate-700">{children}</th>
          ),
          td: ({ children }) => <td className="border border-slate-200 px-4 py-3 text-slate-600">{children}</td>,

          // Enhanced links
          a: ({ href, children }) => (
            <a
              href={href}
              className="text-blue-600 hover:text-blue-800 underline decoration-2 underline-offset-2 hover:decoration-blue-800 transition-colors font-medium"
              target="_blank"
              rel="noopener noreferrer"
            >
              {children}
            </a>
          ),

          // Enhanced images - handle badges vs regular images
          img: ({ src, alt }) => {
            // Check if it's a badge (common badge domains)
            const isBadge = src && (
              src.includes('shields.io') ||
              src.includes('badge') ||
              src.includes('img.shields.io') ||
              src.includes('github.com') && src.includes('badge') ||
              alt?.toLowerCase().includes('badge') ||
              alt?.toLowerCase().includes('shield')
            );

            if (isBadge) {
              return (
                <Image
                  src={src || "/placeholder.svg"}
                  alt={alt || ""}
                  width={100}
                  height={20}
                  className="inline-block h-5 max-w-none rounded border border-slate-200 hover:shadow-sm transition-shadow mr-1 mb-1"
                />
              );
            }

            // Regular images
            return (
              <span className="block my-8">
                <Image
                  src={src || "/placeholder.svg"}
                  alt={alt || ""}
                  width={800}
                  height={400}
                  className="w-full rounded-lg shadow-lg border border-slate-200 hover:shadow-xl transition-shadow"
                />
                {alt && <span className="block text-center text-slate-500 text-sm mt-2 italic">{alt}</span>}
              </span>
            );
          },

          // Horizontal rule
          hr: () => (
            <hr className="my-8 border-0 h-px bg-gradient-to-r from-transparent via-slate-300 to-transparent" />
          ),

          // Strong and emphasis
          strong: ({ children }) => <strong className="font-bold text-slate-900">{children}</strong>,
          em: ({ children }) => <em className="italic text-slate-700">{children}</em>,
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  )
}
