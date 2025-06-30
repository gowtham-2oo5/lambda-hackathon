import type { NextConfig } from "next";

const nextConfig: NextConfig = {
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
