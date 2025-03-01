/** @type {import('next').NextConfig} */
const nextConfig = {
    reactStrictMode: true,
    assetPrefix: process.env.NODE_ENV === 'production' ? '/.' : '',
    output: 'export',
    trailingSlash: true,
    experimental: {
      serverActions: true,
    },
    env: {
      TWITTER_CLIENT_ID: "your-client-id",
      TWITTER_CLIENT_SECRET: "your-client-secret",
    },
  };