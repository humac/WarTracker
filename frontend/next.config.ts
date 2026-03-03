import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Proxy API requests to backend
  // In Docker: uses 'backend' service name
  // In browser: Next.js dev server proxies the request
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://backend:8000/api/:path*',
      },
    ]
  },
  // Disable strict mode for development
  reactStrictMode: false,
  // Force all pages to be dynamically rendered (no static generation)
  // This is needed because we use browser APIs like window.location
  output: 'standalone',
};

export default nextConfig;
