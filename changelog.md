# Changelog

## 0.1.4

- Increased the default HTTPS HSTS `max-age` from six months (`15768000`) to one year (`31536000`).

## 0.1.3

- Added optional `sitemap_filename` configuration in `site.json`, retaining `sitemap.xml` by default and accepting fixed 12-character lowercase alphanumeric `.xml` names.
- Validated custom filenames and root-file collisions before cleaning build output, including a root `sitemap.xml` alongside a custom filename; the build log reports the selected filename.
- Added sitemap filename regression tests and updated build and sitemap documentation. The generic XML CSP exception remains optional, not enabled by default.

## 0.1.2

- Added optional standalone HTML sitemap dates using a `<meta name="last-modified" content="YYYY-MM-DD">` tag in the page's `<head>`.
- Validated standalone dates and rejected duplicate tags before cleaning build output, including on pages excluded from the sitemap; fragment `lastmod:` behavior remains unchanged, and dates are omitted when unspecified.
- Updated sitemap, metadata, and build documentation to explain both date formats and their limitations.

## 0.1.1

- Changed sitemap `<lastmod>` generation to use only explicit `lastmod: YYYY-MM-DD` front matter. Pages without an explicit date remain in the sitemap without `<lastmod>`.
- Removed the automatic Git commit-date fallback and updated the build, metadata, and sitemap documentation accordingly.
- Added comments to `_headers` explaining that a path-specific CSP exception may be needed for XML sitemap styling. No exception is enabled by default.

## 0.1.0

- Initial HTML-first static site boilerplate for Cloudflare Workers, supporting both metadata-based fragments and standalone HTML pages.
- Added reusable page templates, clean URLs, per-page SEO metadata, automatic XML sitemaps, redirects, and security headers.
- Included build-time asset and internal-link checks, deployment configuration, and usage documentation.
- Added the MIT license. The project was still marked as under development and not yet production-tested.
