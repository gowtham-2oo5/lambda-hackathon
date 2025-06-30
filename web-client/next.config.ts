import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Configure for Amplify SSR hosting
  trailingSlash: true,
  
  // Enable experimental features for better optimization
  experimental: {
    optimizePackageImports: ['lucide-react'],
  },
  
  // Enable compression
  compress: true,
  
  // Optimize images
  images: {
    formats: ['image/webp', 'image/avif'],
  },
};

export default nextConfig;
