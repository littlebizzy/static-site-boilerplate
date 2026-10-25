# Static Site Boilerplate

A minimal HTML-first starter for building and deploying static sites with Cloudflare Workers. Pages and assets stay in the repository, a small Python script prepares the deployment files, and no framework or CMS is required.

## Quick Start

1. Edit `index.html` and add pages or files under `assets/` as needed.
2. Run `python3 build.py` to generate `public/`. Do not edit generated files directly.
3. Set a unique Worker `name` in `wrangler.jsonc`, then follow [Cloudflare Workers](docs/cloudflare-workers.md) to connect your repository and deploy.

## Documentation

These guides explain how to organize pages and assets, deploy with Cloudflare Workers, manage content, and configure redirects, security headers, caching, and SEO. Use the relevant topics as you customize and maintain your site.

| Document | Description |
| --- | --- |
| [Cloudflare Workers](docs/cloudflare-workers.md) | Configure GitHub builds and deploy static assets to Cloudflare Workers. |
| [Custom Domains](docs/domains.md) | Connect a domain, configure HTTPS, and choose a preferred hostname. |
| [Deploy Hooks](docs/deploy-hooks.md) | Trigger builds manually and compare deploy hooks with watch paths. |
| [File Structure](docs/file-structure.md) | Understand the purpose of the boilerplate files and directories. |
| [Build Process](docs/build.md) | Run clean builds and understand copied files and output. |
| [Content Management](docs/content-management.md) | Manage published HTML, drafts, and source content without a CMS. |
| [Redirects](docs/redirects.md) | Add permanent, temporary, and wildcard URL redirects. |
| [Security Headers](docs/security-headers.md) | Configure and verify security headers for static assets. |
| [Caching](docs/caching.md) | Understand browser and Cloudflare caching, cache durations, and versioned assets. |
| [404 Errors](docs/404-errors.md) | Handle missing URLs and customize the error page. |
| [XML Sitemaps](docs/sitemaps.md) | Generate and submit XML sitemaps for published pages. |
| [Robots.txt](docs/robots-txt.md) | Configure crawler permissions and indexing controls. |
| [HTML Metadata](docs/metadata.md) | Set search, social sharing, and structured data metadata. |
| [SEO](docs/seo.md) | Keep static HTML pages discoverable and avoid indexing problems. |
| [Images](docs/images.md) | Choose image formats, optimize loading, and use responsive images. |
| [Performance](docs/performance.md) | Keep static HTML and assets fast without extra tooling. |
| [Accessibility](docs/accessibility.md) | Follow practical accessibility standards for plain HTML pages. |
| [Analytics](docs/analytics.md) | Optionally measure visits with Cloudflare Web Analytics. |
| [Launch Checklist](docs/launch-checklist.md) | Verify deployment, routing, metadata, and published files before launch. |
