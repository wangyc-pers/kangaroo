const withMDX = require('@next/mdx')(
    {
        extension: /\.(md|mdx)$/,
    }
)
 
/** @type {import('next').NextConfig} */
const nextConfig = {
  // Configure `pageExtensions` to include MDX files
  pageExtensions: ['js', 'jsx', 'mdx', 'ts', 'tsx', 'md'],
  // Optionally, add any other Next.js config below
}
 
module.exports = withMDX(nextConfig)
