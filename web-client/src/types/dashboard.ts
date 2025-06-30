// Dashboard types to match your DynamoDB structure

export interface ReadmeHistoryItem {
  userId: string;
  requestId: string;
  repoUrl: string;
  repoName: string;
  status: 'processing' | 'completed' | 'failed' | 'unknown';
  createdAt: string;
  completedAt?: string;
  processingTime?: number;
  content?: string;
  error?: string;
  executionArn?: string;
  readmeS3Url?: string;
  readmeContent?: string; // Added this field from DynamoDB
  stage?: string;
  updatedAt?: string;
  lastProgress?: string;
  // Additional fields from DynamoDB
  projectType?: string;
  primaryLanguage?: string;
  frameworks?: string[];
  readmeLength?: number;
  generationTimestamp?: string;
  analysisMethod?: string;
  confidence?: {
    projectType?: number;
    language?: number;
  };
  frameworkConfidence?: Record<string, number>;
}

export interface DashboardStats {
  total: number;
  completed: number;
  processing: number;
  failed: number;
}

export interface HistoryHookReturn {
  history: ReadmeHistoryItem[];
  loading: boolean;
  error: string | null;
  stats: DashboardStats;
  createRecord: (repoUrl: string, executionArn?: string) => Promise<string>;
  updateRecord: (requestId: string, updates: Partial<ReadmeHistoryItem>) => Promise<ReadmeHistoryItem>;
  fetchHistory: () => Promise<ReadmeHistoryItem[]>;
  deleteRecord: (requestId: string) => Promise<boolean>;
  getStats: () => DashboardStats;
  isAuthenticated: () => boolean;
  getCurrentUserId: () => Promise<string>;
}
