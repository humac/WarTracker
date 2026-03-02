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
};

export default nextConfig;
