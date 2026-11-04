# Changelog

## [0.1.1](https://github.com/littlebizzy/static-site-boilerplate/releases/tag/0.1.1) — 2026-11-04

- Changed sitemap `<lastmod>` generation to use only explicit `lastmod: YYYY-MM-DD` front matter. Pages without an explicit date remain in the sitemap without `<lastmod>`.
- Removed the automatic Git commit-date fallback and updated the build, metadata, and sitemap documentation accordingly.
- Added comments to `_headers` explaining that a path-specific CSP exception may be needed for XML sitemap styling. No exception is enabled by default.

## [0.1.0](https://github.com/littlebizzy/static-site-boilerplate/releases/tag/0.1.0) — 2026-11-04

- Initial HTML-first static site boilerplate for Cloudflare Workers, supporting both metadata-based fragments and standalone HTML pages.
- Added reusable page templates, clean URLs, per-page SEO metadata, automatic XML sitemaps, redirects, and security headers.
- Included build-time asset and internal-link checks, deployment configuration, and usage documentation.
- Added the MIT license. The project was still marked as under development and not yet production-tested.
