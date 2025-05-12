const path = require('path');

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: false,
  trailingSlash: true,
  pageExtensions: ['js', 'jsx'],
  experimental: {
    esmExternals: false
  },
  // 👇 Tells Next.js to look in `src/pages` instead of the default root/pages
  dir: 'src',
  webpack: (config) => {
    config.resolve.alias = {
      ...config.resolve.alias,
      apexcharts: path.resolve(__dirname, './node_modules/apexcharts-clevision')
    };
    return config;
  }
};

module.exports = nextConfig;
