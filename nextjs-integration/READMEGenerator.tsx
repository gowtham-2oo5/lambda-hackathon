'use client';

import React, { useState, useCallback } from 'react';
import { readmeGeneratorService, CompleteResult } from './README-Generator-Service';

interface READMEGeneratorProps {
  onSuccess?: (result: CompleteResult) => void;
  onError?: (error: string) => void;
}

export const READMEGenerator: React.FC<READMEGeneratorProps> = ({
  onSuccess,
  onError,
}) => {
  const [githubUrl, setGithubUrl] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [progress, setProgress] = useState<string>('');
  const [result, setResult] = useState<CompleteResult | null>(null);
  const [error, setError] = useState<string>('');

  const validateGitHubUrl = (url: string): boolean => {
    const githubRegex = /^https:\/\/github\.com\/[\w\-\.]+\/[\w\-\.]+\/?$/;
    return githubRegex.test(url);
  };

  const handleGenerate = useCallback(async () => {
    if (!validateGitHubUrl(githubUrl)) {
      setError('Please enter a valid GitHub repository URL');
      return;
    }

    setIsGenerating(true);
    setError('');
    setResult(null);
    setProgress('🚀 Starting Phase 3 Ultimate AI Platform...');

    try {
      // Start the pipeline
      const startResult = await readmeGeneratorService.generateREADME({
        github_url: githubUrl,
      });

      if (!startResult.success) {
        throw new Error(startResult.message);
      }

      setProgress('📊 Phase 3 Analysis in progress...');

      // Poll for completion
      const executionArn = startResult.execution_arn;
      let attempts = 0;
      const maxAttempts = 24; // 2 minutes with 5-second intervals

      const pollStatus = async (): Promise<void> => {
        if (attempts >= maxAttempts) {
          throw new Error('Generation timeout - please try again');
        }

        attempts++;
        const status = await readmeGeneratorService.checkStatus(executionArn);

        if (status.status === 'SUCCEEDED' && status.output) {
          setProgress('✅ README generation completed!');
          setResult(status.output);
          onSuccess?.(status.output);
          return;
        }

        if (status.status === 'FAILED') {
          throw new Error(status.error || 'Pipeline execution failed');
        }

        if (status.status === 'RUNNING') {
          if (attempts < 3) {
            setProgress('🧠 Phase 3 AI analyzing repository...');
          } else if (attempts < 6) {
            setProgress('🔍 Detecting frameworks and patterns...');
          } else if (attempts < 9) {
            setProgress('📝 Generating professional README...');
          } else {
            setProgress('🎨 Finalizing documentation...');
          }

          // Continue polling
          setTimeout(pollStatus, 5000);
          return;
        }

        // Still running, continue polling
        setTimeout(pollStatus, 5000);
      };

      await pollStatus();
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Unknown error occurred';
      setError(errorMessage);
      onError?.(errorMessage);
    } finally {
      setIsGenerating(false);
      setProgress('');
    }
  }, [githubUrl, onSuccess, onError]);

  return (
    <div className="max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-lg">
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          🏆 Smart README Generator
        </h1>
        <p className="text-gray-600">
          Phase 3 Ultimate AI Platform - Enterprise-grade README generation
        </p>
      </div>

      {/* Input Section */}
      <div className="mb-6">
        <label htmlFor="github-url" className="block text-sm font-medium text-gray-700 mb-2">
          GitHub Repository URL
        </label>
        <div className="flex gap-3">
          <input
            id="github-url"
            type="url"
            value={githubUrl}
            onChange={(e) => setGithubUrl(e.target.value)}
            placeholder="https://github.com/username/repository"
            className="flex-1 px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            disabled={isGenerating}
          />
          <button
            onClick={handleGenerate}
            disabled={isGenerating || !githubUrl}
            className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed font-medium"
          >
            {isGenerating ? '🔄 Generating...' : '🚀 Generate README'}
          </button>
        </div>
      </div>

      {/* Progress Section */}
      {progress && (
        <div className="mb-6 p-4 bg-blue-50 border border-blue-200 rounded-md">
          <div className="flex items-center">
            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600 mr-3"></div>
            <span className="text-blue-800 font-medium">{progress}</span>
          </div>
        </div>
      )}

      {/* Error Section */}
      {error && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-md">
          <div className="flex items-center">
            <span className="text-red-600 font-medium">❌ {error}</span>
          </div>
        </div>
      )}

      {/* Results Section */}
      {result && (
        <div className="space-y-6">
          {/* Analysis Results */}
          <div className="bg-green-50 border border-green-200 rounded-md p-6">
            <h3 className="text-lg font-semibold text-green-800 mb-4">
              🎯 Phase 3 Analysis Results
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <span className="font-medium text-gray-700">Project Type:</span>
                <span className="ml-2 text-green-700">{result.phase3_analysis.project_type}</span>
              </div>
              <div>
                <span className="font-medium text-gray-700">Confidence:</span>
                <span className="ml-2 text-green-700">
                  {(result.phase3_analysis.confidence * 100).toFixed(1)}%
                </span>
              </div>
              <div>
                <span className="font-medium text-gray-700">Language:</span>
                <span className="ml-2 text-green-700">{result.phase3_analysis.primary_language}</span>
              </div>
              <div>
                <span className="font-medium text-gray-700">Frameworks:</span>
                <span className="ml-2 text-green-700">
                  {result.phase3_analysis.frameworks.join(', ') || 'None detected'}
                </span>
              </div>
            </div>
          </div>

          {/* README Generation Results */}
          <div className="bg-blue-50 border border-blue-200 rounded-md p-6">
            <h3 className="text-lg font-semibold text-blue-800 mb-4">
              📝 README Generation Results
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <span className="font-medium text-gray-700">README Length:</span>
                <span className="ml-2 text-blue-700">
                  {result.readme_generation.readme_length.toLocaleString()} characters
                </span>
              </div>
              <div>
                <span className="font-medium text-gray-700">Generated:</span>
                <span className="ml-2 text-blue-700">
                  {new Date(result.readme_generation.generation_timestamp).toLocaleString()}
                </span>
              </div>
            </div>
            
            {/* Download Button */}
            <div className="mt-4">
              <button
                onClick={() => {
                  const [owner, repo] = githubUrl.split('/').slice(-2);
                  window.open(`https://smart-readme-lambda-31641.s3.amazonaws.com/${result.readme_generation.s3_location.key}`, '_blank');
                }}
                className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 font-medium"
              >
                📥 Download README.md
              </button>
            </div>
          </div>

          {/* Enterprise Features */}
          <div className="bg-purple-50 border border-purple-200 rounded-md p-6">
            <h3 className="text-lg font-semibold text-purple-800 mb-4">
              🏆 Enterprise Features Used
            </h3>
            <ul className="space-y-2">
              {result.pipeline_features.map((feature, index) => (
                <li key={index} className="flex items-center text-purple-700">
                  <span className="mr-2">✅</span>
                  {feature}
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
};

export default READMEGenerator;
