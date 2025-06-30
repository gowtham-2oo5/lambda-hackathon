import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Configure for Amplify hosting
  output: 'export',
  trailingSlash: true,
  skipTrailingSlashRedirect: true,
  
  // Enable experimental features for better optimization
  experimental: {
    optimizePackageImports: ['lucide-react'],
  },
  
  // Enable compression
  compress: true,
  
  // Optimize images for static export
  images: {
    unoptimized: true,
    formats: ['image/webp', 'image/avif'],
  },
  
  // Disable server-side features for static export
  distDir: '.next',
};

export default nextConfig;
