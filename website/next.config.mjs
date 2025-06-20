/** @type {import('next').NextConfig} */
const nextConfig = {
  // Configures the Next.js build output
  output: 'standalone',
  
  // This is the crucial part.
  // It ensures that the content.json file is included in the deployment.
  experimental: {
    serverComponentsExternalPackages: ['fs'],
    outputFileTracingIncludes: {
      '/*': ['./src/data/content.json'],
    },
  },
};

export default nextConfig; 