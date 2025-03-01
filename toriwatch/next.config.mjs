/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  assetPrefix: process.env.NODE_ENV === 'production' ? '.' : '',
  output: 'export',
  distDir: "out",
  trailingSlash: true,
  experimental: {
    serverActions: true,
  },
  exportPathMap: async function () {
    return {
      "/popup": { page: "/popup" },
    };
  },
  env: {
    TWITTER_CLIENT_ID: process.env.TWITTER_CLIENT_ID,
    TWITTER_CLIENT_SECRET: process.env.TWITTER_CLIENT_SECRET,
  },
};
