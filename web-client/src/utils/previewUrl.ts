interface PreviewUrlParams {
  id: string;
  source: 'history' | 'direct' | 'share';
  s3Key?: string;
  repoUrl?: string;
  repoName?: string;
  owner?: string;
  projectType?: string;
  primaryLanguage?: string;
  frameworks?: string[];
  confidence?: number;
  processingTime?: number;
}

export function generatePreviewUrl(params: PreviewUrlParams): string {
  const { id, source, ...otherParams } = params;
  const baseUrl = `/preview/${encodeURIComponent(id)}`;
  const searchParams = new URLSearchParams();
  
  searchParams.set('source', source);
  
  // Add optional parameters
  Object.entries(otherParams).forEach(([key, value]) => {
    if (value !== undefined && value !== null) {
      if (Array.isArray(value)) {
        searchParams.set(key, value.join(','));
      } else {
        searchParams.set(key, String(value));
      }
    }
  });
  
  return `${baseUrl}?${searchParams.toString()}`;
}

// Helper function to generate preview URL from history item
export function generateHistoryPreviewUrl(historyId: string): string {
  return generatePreviewUrl({
    id: historyId,
    source: 'history'
  });
}

// Helper function to generate preview URL from S3 key
export function generateS3PreviewUrl(params: {
  s3Key: string;
  repoUrl?: string;
  repoName?: string;
  owner?: string;
  projectType?: string;
  primaryLanguage?: string;
  frameworks?: string[];
  confidence?: number;
  processingTime?: number;
}): string {
  const id = extractIdFromS3Key(params.s3Key);
  
  return generatePreviewUrl({
    id,
    source: 'direct',
    s3Key: params.s3Key,
    repoUrl: params.repoUrl,
    repoName: params.repoName,
    owner: params.owner,
    projectType: params.projectType,
    primaryLanguage: params.primaryLanguage,
    frameworks: params.frameworks,
    confidence: params.confidence,
    processingTime: params.processingTime
  });
}

// Helper function to generate shareable preview URL
export function generateShareablePreviewUrl(params: {
  id: string;
  repoName: string;
  owner: string;
  s3Key?: string;
}): string {
  return generatePreviewUrl({
    id: params.id,
    source: 'share',
    s3Key: params.s3Key,
    repoName: params.repoName,
    owner: params.owner
  });
}

// Extract ID from S3 key (e.g., "readme-analysis/owner/repo.json" -> "owner-repo")
function extractIdFromS3Key(s3Key: string): string {
  const parts = s3Key.split('/');
  if (parts.length >= 3) {
    const owner = parts[1];
    const repoWithExt = parts[2];
    const repo = repoWithExt.replace(/\.(json|md)$/, '');
    return `${owner}-${repo}`;
  }
  
  // Fallback: use the full key as ID
  return s3Key.replace(/[^a-zA-Z0-9-_]/g, '-');
}

// Parse preview URL parameters
export function parsePreviewUrl(searchParams: URLSearchParams) {
  const source = searchParams.get('source') as 'history' | 'direct' | 'share' || 'history';
  const s3Key = searchParams.get('s3Key');
  const repoUrl = searchParams.get('repoUrl') || searchParams.get('repo');
  const repoName = searchParams.get('repoName') || searchParams.get('name');
  const owner = searchParams.get('owner');
  const projectType = searchParams.get('projectType') || searchParams.get('type');
  const primaryLanguage = searchParams.get('primaryLanguage') || searchParams.get('lang');
  const frameworks = searchParams.get('frameworks')?.split(',').filter(Boolean) || [];
  const confidence = searchParams.get('confidence') ? parseFloat(searchParams.get('confidence')!) : undefined;
  const processingTime = searchParams.get('processingTime') || searchParams.get('time') 
    ? parseFloat(searchParams.get('processingTime') || searchParams.get('time')!) 
    : undefined;
  
  return {
    source,
    s3Key,
    repoUrl,
    repoName,
    owner,
    projectType,
    primaryLanguage,
    frameworks,
    confidence,
    processingTime
  };
}
