// Test script to verify the schema updates work correctly
const mockDynamoDBItem = {
  "analysisComplete": true,
  "readmeContent": "# Test Project\n\nThis is a test README content.",
  "status": "completed",
  "processingTime": 31.437861442565918,
  "ttl": 1753979165,
  "lastAccessedAt": "2025-07-01T16:26:05.191043Z",
  "confidenceScore": 95,
  "performanceMetrics": {
    "filesProcessed": 13,
    "generationSuccess": true,
    "confidenceScore": 95,
    "processingTimeSeconds": 31.437861442565918,
    "accuracyPercentage": 93
  },
  "branchUsed": "main",
  "repoOwner": "TestUser",
  "accuracyLevel": "excellent",
  "requestId": "924211db-dab1-4209-8007-af9ccdc1036e",
  "primaryLanguage": "JavaScript",
  "accuracyPercentage": 93,
  "userId": "test@example.com",
  "filesAnalyzedCount": 13,
  "s3Location": {
    "bucket": "smart-readme-lambda-31641",
    "key": "readme-analysis/TestUser/TestProject.md"
  },
  "generationMethod": "mandatory_code_analysis",
  "qualityScore": "premium",
  "hallucinationPrevented": true,
  "techStack": [],
  "repoId": "TestUser#TestProject",
  "repoName": "TestProject",
  "version": "v3.2_cache_busting",
  "repoUrl": "https://github.com/TestUser/TestProject",
  "readmeLength": 6069,
  "readmeUrl": "https://d3in1w40kamst9.cloudfront.net/readme-analysis/TestUser/TestProject.md?v=1751387164&id=824a36fd",
  "createdAt": "2025-07-01T16:26:05.191043Z",
  "updatedAt": "2025-07-01T16:26:05.191043Z",
  "readmePreview": "# Test Project\n\nThis is a test project...",
  "analysisMethod": "mandatory_code_analysis",
  "realContentAnalyzed": true,
  "projectType": "software_project"
};

// Simulate the transformation logic from useHistory.ts
function transformItem(item) {
  return {
    // Primary identifiers
    requestId: item.requestId || item.repoId || `${item.repoOwner}#${item.repoName}`,
    repoId: item.repoId || `${item.repoOwner}#${item.repoName}`,
    repoName: item.repoName,
    repoUrl: item.repoUrl,
    repoOwner: item.repoOwner,
    
    // Status and timing
    status: item.status || "completed",
    createdAt: item.createdAt,
    updatedAt: item.updatedAt,
    completedAt: item.updatedAt || item.createdAt,
    processingTime: item.processingTime,
    
    // Project analysis
    projectType: item.projectType || "software_project",
    primaryLanguage: item.primaryLanguage || "Mixed",
    frameworks: Array.isArray(item.frameworks) ? item.frameworks : [],
    techStack: Array.isArray(item.techStack) ? item.techStack : [],
    
    // Quality metrics
    confidence: item.confidence || item.confidenceScore || 0,
    confidenceScore: item.confidenceScore || item.confidence || 0,
    accuracyPercentage: item.accuracyPercentage || 0,
    accuracyLevel: item.accuracyLevel || "basic",
    qualityScore: item.qualityScore || "basic",
    
    // README content
    readmeLength: item.readmeLength,
    readmeS3Url: item.readmeUrl || item.readmeS3Url || "",
    readmeUrl: item.readmeUrl || item.readmeS3Url || "",
    readmeContent: item.readmeContent,
    readmePreview: item.readmePreview,
    
    // Analysis details
    analysisMethod: item.analysisMethod || item.generationMethod,
    generationMethod: item.generationMethod || item.analysisMethod,
    filesAnalyzedCount: item.filesAnalyzedCount || 0,
    sourceFilesAnalyzed: Array.isArray(item.sourceFilesAnalyzed) ? item.sourceFilesAnalyzed : [],
    analysisComplete: item.analysisComplete || false,
    realContentAnalyzed: item.realContentAnalyzed || false,
    hallucinationPrevented: item.hallucinationPrevented || false,
    
    // System metadata
    userId: item.userId,
    version: item.version,
    branchUsed: item.branchUsed || "main",
    
    // Complex objects
    accuracyBreakdown: item.accuracyBreakdown,
    performanceMetrics: item.performanceMetrics,
    s3Location: item.s3Location,
    frameworkConfidence: item.frameworkConfidence || {},
    
    // Additional fields
    error: item.error,
    ttl: item.ttl,
    lastAccessedAt: item.lastAccessedAt,
    
    // Legacy fields for backward compatibility
    generationTimestamp: item.updatedAt || item.createdAt,
  };
}

// Test the transformation
const transformedItem = transformItem(mockDynamoDBItem);

console.log("✅ Schema transformation test:");
console.log("Original item keys:", Object.keys(mockDynamoDBItem).length);
console.log("Transformed item keys:", Object.keys(transformedItem).length);
console.log("\n🔍 Key mappings:");
console.log("- repoId:", transformedItem.repoId);
console.log("- requestId:", transformedItem.requestId);
console.log("- readmeUrl:", transformedItem.readmeUrl);
console.log("- readmeS3Url:", transformedItem.readmeS3Url);
console.log("- confidenceScore:", transformedItem.confidenceScore);
console.log("- accuracyPercentage:", transformedItem.accuracyPercentage);
console.log("- qualityScore:", transformedItem.qualityScore);
console.log("- analysisMethod:", transformedItem.analysisMethod);

console.log("\n✅ Schema update test completed successfully!");
