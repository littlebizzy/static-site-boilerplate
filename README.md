# Static Site Boilerplate

A minimal HTML-first starter for building and deploying static sites with Cloudflare Workers. Pages and assets stay in the repository, a small Python script prepares the deployment files, and no framework or CMS is required.

## Quick Start

1. Set the site name and description in `site.json`, add the production HTTPS URL when known, then edit the homepage in `index.html` and add pages or assets as needed.
2. Run `python3 build.py` to assemble content fragments into full HTML pages and generate `public/`. Do not edit generated files directly.
3. Set a unique Worker `name` in `wrangler.jsonc`, then follow [Cloudflare Workers](docs/cloudflare-workers.md) to connect your repository and deploy.

Pages with `---` metadata at the top are assembled with `templates/base.html`, `templates/head.html`, and the shared header and footer. Complete HTML files without front matter are copied unchanged. See [Build Process](docs/build.md) for both formats.

## Documentation

These guides explain how to organize pages and assets, deploy with Cloudflare Workers, manage content, and configure redirects, security headers, caching, and SEO. Use the relevant topics as you customize and maintain your site.

| Document | Description |
| --- | --- |
| [Agent Guidelines](agents.md) | Follow the repository's editing, validation, and one-file-per-commit conventions when making automated changes. |
| [Cloudflare Workers](docs/cloudflare-workers.md) | Connect a GitHub repository to Cloudflare Workers, configure build settings, and deploy generated static assets. |
| [Custom Domains](docs/domains.md) | Connect custom domains, enable HTTPS, and redirect alternate hostnames to your preferred canonical address. |
| [Deploy Hooks](docs/deploy-hooks.md) | Create secure deploy hooks, trigger builds manually, and understand how hooks differ from watch-path filters. |
| [File Structure](docs/file-structure.md) | Learn how source pages, templates, assets, drafts, and generated files are organized and published. |
| [Build Process](docs/build.md) | See how the Python builder assembles HTML, checks routes and assets, and prepares the deployment directory. |
| [Content Management](docs/content-management.md) | Edit HTML content and page metadata, manage drafts, and reuse templates without installing a CMS. |
| [Redirects](docs/redirects.md) | Set up permanent, temporary, and wildcard redirects in the root configuration file and verify URL changes. |
| [Security Headers](docs/security-headers.md) | Understand the default security headers, adjust policies for site features, and verify deployed responses. |
| [Caching](docs/caching.md) | Compare browser and Cloudflare edge caching, choose suitable file lifetimes, and avoid stale assets. |
| [404 Errors](docs/404-errors.md) | Customize missing-page responses while preserving correct HTTP statuses and avoiding misleading homepage redirects. |
| [XML Sitemaps](docs/sitemaps.md) | Generate canonical sitemap URLs, control modification dates, and submit the sitemap to search engines. |
| [Robots.txt](docs/robots-txt.md) | Configure crawler permissions, understand their limitations, and distinguish crawl rules from indexing controls. |
| [HTML Metadata](docs/metadata.md) | Manage page titles, descriptions, canonical URLs, social previews, and structured data across shared templates. |
| [SEO](docs/seo.md) | Use clean internal links, unique metadata, indexing controls, and Search Console to keep pages discoverable. |
| [Images](docs/images.md) | Choose suitable image formats, size responsive images, and improve loading behavior without sacrificing accessibility. |
| [Performance](docs/performance.md) | Keep HTML, CSS, and JavaScript lean, then check image loading and real-world performance measurements. |
| [Accessibility](docs/accessibility.md) | Build accessible pages with semantic HTML, readable content, keyboard support, and useful image alternatives. |
| [Analytics](docs/analytics.md) | Add optional Cloudflare Web Analytics and understand how browser measurements differ from Worker request metrics. |
| [Launch Checklist](docs/launch-checklist.md) | Review build output, domains, redirects, metadata, indexing controls, and security settings before going live. |
