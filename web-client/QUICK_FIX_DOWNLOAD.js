// QUICK FIX - Replace your handleDownload function with this:

const handleDownload = async (format = 'md') => {
  console.log('🔧 DEBUGGING - Download function called with format:', format);
  console.log('🔧 DEBUGGING - Current result:', result);
  console.log('🔧 DEBUGGING - GitHub URL:', githubUrl);
  
  if (!githubUrl) {
    toast.error('No GitHub URL available');
    return;
  }
  
  try {
    // FIXED: Extract owner and repo from GitHub URL
    const match = githubUrl.match(/github\.com\/([^\/]+)\/([^\/]+)/);
    if (!match) {
      throw new Error('Invalid GitHub URL format');
    }
    
    const [, owner, repo] = match;
    console.log('🔧 DEBUGGING - Extracted owner:', owner, 'repo:', repo);
    
    const correctS3Key = `generated-readmes/${owner}/${repo}.md`;
    console.log('🔧 DEBUGGING - Using S3 key:', correctS3Key);
    
    const cloudFrontUrl = `https://d3in1w40kamst9.cloudfront.net/${correctS3Key}`;
    console.log('🔧 DEBUGGING - CloudFront URL:', cloudFrontUrl);
    
    const a = document.createElement('a');
    a.href = cloudFrontUrl;
    a.download = `${owner}-${repo}-README.${format}`;
    a.target = '_blank';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    
    toast.success(`README download started!`, {
      description: `File: ${owner}-${repo}-README.${format}`
    });
    
    console.log('🔧 DEBUGGING - Download link created and clicked');
    
  } catch (err) {
    console.error('🚨 Download error:', err);
    toast.error('Download failed', {
      description: err.message,
    });
  }
};

// ALSO - Make sure you're calling this function, not the old one!
// Check your component and replace the old handleDownload with this one.
