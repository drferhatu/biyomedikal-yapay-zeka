// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import mdx from '@astrojs/mdx';
import tailwindcss from '@tailwindcss/vite';
import remarkCallouts from './src/lib/remark-callouts.mjs';
import rehypeBaseLinks from './src/lib/rehype-base-links.mjs';

// GitHub Pages: https://<kullanıcı>.github.io/<depo>/
// Özel alan adına geçilirse SITE_URL ve BASE_PATH ortam değişkenleriyle değiştirilebilir.
const site = process.env.SITE_URL ?? 'https://drferhatu.github.io';
const base = process.env.BASE_PATH ?? '/biyomedikal-yapay-zeka';

export default defineConfig({
  site,
  base,
  trailingSlash: 'ignore',
  integrations: [mdx(), sitemap()],
  markdown: {
    remarkPlugins: [remarkCallouts],
    rehypePlugins: [[rehypeBaseLinks, { base }]],
    // Açık tema varsayılan; koyu tema renkleri --shiki-dark değişkenleriyle gelir (global.css)
    shikiConfig: { themes: { light: 'github-light', dark: 'github-dark' }, wrap: true },
  },
  vite: { plugins: [tailwindcss()] },
});
