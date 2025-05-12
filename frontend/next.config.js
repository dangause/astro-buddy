const path = require('path'); // 👈 Required

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: false,
  trailingSlash: true,
  pageExtensions: ['js', 'jsx'],
  experimental: {
    esmExternals: false
  },
  webpack: (config) => {
    config.resolve.alias = {
      ...config.resolve.alias,
      apexcharts: path.resolve(__dirname, './node_modules/apexcharts-clevision')
    };
    return config;
  }
};

module.exports = nextConfig;
