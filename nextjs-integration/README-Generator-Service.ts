/**
 * 🏆 Smart README Generator Service for Next.js
 * Phase 3 Ultimate AI Platform Integration
 */

export interface GitHubRepository {
  github_url: string;
}

export interface Phase3Analysis {
  project_type: string;
  confidence: number;
  primary_language: string;
  frameworks: string[];
  processing_time: number;
}

export interface READMEGeneration {
  readme_length: number;
  s3_location: {
    bucket: string;
    key: string;
  };
  generation_timestamp: string;
}

export interface CompleteResult {
  success: boolean;
  message: string;
  phase3_analysis: Phase3Analysis;
  readme_generation: READMEGeneration;
  pipeline_features: string[];
  github_url: string;
  timestamp: string;
}

export interface ExecutionStatus {
  status: 'RUNNING' | 'SUCCEEDED' | 'FAILED' | 'TIMED_OUT';
  output?: CompleteResult;
  error?: string;
}

export class SmartREADMEGeneratorService {
  private readonly API_BASE_URL = process.env.NEXT_PUBLIC_README_API_URL || 'https://api.smart-readme-generator.com/v3';
  private readonly STEP_FUNCTIONS_REGION = 'us-east-1';

  /**
   * 🚀 Start Complete README Generation Pipeline
   */
  async generateREADME(repository: GitHubRepository): Promise<{
    success: boolean;
    execution_arn: string;
    message: string;
  }> {
    try {
      const response = await fetch(`${this.API_BASE_URL}/generate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(repository),
      });

      if (!response.ok) {
        throw new Error(`API request failed: ${response.status}`);
      }

      const result = await response.json();
      return result;
    } catch (error) {
      console.error('README generation failed:', error);
      throw error;
    }
  }

  /**
   * 📊 Check Pipeline Execution Status
   */
  async checkStatus(executionArn: string): Promise<ExecutionStatus> {
    try {
      // Extract execution ID from ARN for API call
      const executionId = executionArn.split(':').pop();
      
      const response = await fetch(`${this.API_BASE_URL}/status/${encodeURIComponent(executionArn)}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`Status check failed: ${response.status}`);
      }

      const result = await response.json();
      return {
        status: result.status,
        output: result.output ? JSON.parse(result.output) : undefined,
        error: result.error,
      };
    } catch (error) {
      console.error('Status check failed:', error);
      throw error;
    }
  }

  /**
   * 📝 Get Generated README Content
   */
  async getREADME(owner: string, repo: string): Promise<{
    readme_content: string;
    s3_url: string;
  }> {
    try {
      const response = await fetch(`${this.API_BASE_URL}/readme/${owner}/${repo}`, {
        method: 'GET',
      });

      if (!response.ok) {
        throw new Error(`README fetch failed: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('README fetch failed:', error);
      throw error;
    }
  }

  /**
   * 🔄 Poll for Completion (with timeout)
   */
  async waitForCompletion(
    executionArn: string,
    timeoutMs: number = 120000, // 2 minutes
    pollIntervalMs: number = 5000 // 5 seconds
  ): Promise<CompleteResult> {
    const startTime = Date.now();

    while (Date.now() - startTime < timeoutMs) {
      const status = await this.checkStatus(executionArn);

      if (status.status === 'SUCCEEDED' && status.output) {
        return status.output;
      }

      if (status.status === 'FAILED') {
        throw new Error(`Pipeline failed: ${status.error || 'Unknown error'}`);
      }

      if (status.status === 'TIMED_OUT') {
        throw new Error('Pipeline execution timed out');
      }

      // Still running, wait and check again
      await new Promise(resolve => setTimeout(resolve, pollIntervalMs));
    }

    throw new Error('Polling timeout reached');
  }

  /**
   * 🎯 One-Shot Generation (Start + Wait for Completion)
   */
  async generateAndWait(repository: GitHubRepository): Promise<CompleteResult> {
    // Start the pipeline
    const startResult = await this.generateREADME(repository);
    
    if (!startResult.success) {
      throw new Error(`Failed to start pipeline: ${startResult.message}`);
    }

    // Wait for completion
    return await this.waitForCompletion(startResult.execution_arn);
  }

  /**
   * 📊 Get Repository Analysis Only (without README generation)
   */
  async analyzeRepository(repository: GitHubRepository): Promise<Phase3Analysis> {
    // This would use the analysis-only workflow
    // For now, we'll use the complete pipeline and extract analysis
    const result = await this.generateAndWait(repository);
    return result.phase3_analysis;
  }
}

// Export singleton instance
export const readmeGeneratorService = new SmartREADMEGeneratorService();
