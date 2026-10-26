# Static Site Boilerplate

A minimal HTML-first starter for building and deploying static sites with Cloudflare Workers. Pages and assets stay in the repository, a small Python script prepares the deployment files, and no framework or CMS is required.

## Quick Start

1. Set the site name and description in `site.json`; add the production HTTPS `url` when the domain is ready.
2. Customize `index.html`, add pages as files such as `about.html` or folders such as `about/index.html`, and place images, stylesheets, and scripts in `assets/`. Edit `templates/` for shared layout changes.
3. Run `python3 build.py`, review any warnings, and check the generated pages and assets in `public/`. Make corrections in the source files rather than editing `public/` directly.
4. Set a unique Worker `name` in `wrangler.jsonc`, then follow [Cloudflare Workers](docs/cloudflare-workers.md) to connect the GitHub repository and deploy.

Pages with `---` metadata at the top are assembled with `templates/base.html`, `templates/head.html`, and the shared header and footer. Complete HTML files without front matter are copied unchanged. See [Build Process](docs/build.md) for both formats.

## Documentation

Use these guides to organize content and templates, build and deploy with Cloudflare Workers, configure domains, redirects, metadata, security, caching, and SEO, and check performance, accessibility, and launch readiness.

| Document | Description |
| --- | --- |
| [File Structure](docs/file-structure.md) | Learn how source pages, templates, assets, drafts, and generated files are organized and published. |
| [Content Management](docs/content-management.md) | Edit HTML content and page metadata, manage drafts, and reuse templates without installing a CMS. |
| [Build Process](docs/build.md) | See how the Python builder assembles HTML, checks routes and assets, and prepares the deployment directory. |
| [Cloudflare Workers](docs/cloudflare-workers.md) | Connect a GitHub repository to Cloudflare Workers, configure build settings, and deploy generated static assets. |
| [Custom Domains](docs/domains.md) | Connect custom domains, enable HTTPS, and redirect alternate hostnames to your preferred canonical address. |
| [Deploy Hooks](docs/deploy-hooks.md) | Create secure deploy hooks, trigger builds manually, and understand how hooks differ from watch-path filters. |
| [Redirects](docs/redirects.md) | Set up permanent, temporary, and wildcard redirects in the root configuration file and verify URL changes. |
| [404 Errors](docs/404-errors.md) | Customize missing-page responses while preserving correct HTTP statuses and avoiding misleading homepage redirects. |
| [HTML Metadata](docs/metadata.md) | Manage page titles, descriptions, canonical URLs, social previews, and structured data across shared templates. |
| [SEO](docs/seo.md) | Use clean internal links, unique metadata, indexing controls, and Search Console to keep pages discoverable. |
| [Robots.txt](docs/robots-txt.md) | Configure crawler permissions, understand their limitations, and distinguish crawl rules from indexing controls. |
| [XML Sitemaps](docs/sitemaps.md) | Generate canonical sitemap URLs, control modification dates, and submit the sitemap to search engines. |
| [Security Headers](docs/security-headers.md) | Understand the default security headers, adjust policies for site features, and verify deployed responses. |
| [Caching](docs/caching.md) | Compare browser and Cloudflare edge caching, choose suitable file lifetimes, and avoid stale assets. |
| [Images](docs/images.md) | Choose suitable image formats, size responsive images, and improve loading behavior without sacrificing accessibility. |
| [Performance](docs/performance.md) | Keep HTML, CSS, and JavaScript lean, then check image loading and real-world performance measurements. |
| [Accessibility](docs/accessibility.md) | Build accessible pages with semantic HTML, readable content, keyboard support, and useful image alternatives. |
| [Analytics](docs/analytics.md) | Add optional Cloudflare Web Analytics and understand how browser measurements differ from Worker request metrics. |
| [Launch Checklist](docs/launch-checklist.md) | Review build output, domains, redirects, metadata, indexing controls, and security settings before going live. |
| [Agent Guidelines](agents.md) | Follow the repository's editing, validation, and one-file-per-commit conventions when making automated changes. |
