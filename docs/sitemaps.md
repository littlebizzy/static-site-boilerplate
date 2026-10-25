# XML Sitemaps

When the production HTTPS `url` is set in `site.json`, every `python3 build.py` run generates `public/sitemap.xml` automatically. Leave the URL empty for the unconfigured starter; a sitemap cannot contain valid absolute URLs without a domain.

The sitemap includes the clean URLs of published HTML pages, including standalone HTML. It excludes drafts, the 404 page, redirect sources, pages marked `noindex`, and pages whose canonical URL points elsewhere.

## Modification dates

Each `<lastmod>` is the date of the most recent Git commit affecting that page's source HTML file, not the current build or deployment date. Dates use the `YYYY-MM-DD` format.

A complete Git history must be available to retrieve these dates. If the build uses a shallow checkout, runs outside a Git repository, or a page has no recorded commit, that page remains in the sitemap without `<lastmod>`. This avoids publishing misleading dates. Changes made only to shared templates or site settings do not update the source page's date.

## Example

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://example.com/</loc>
    <lastmod>2026-10-25</lastmod>
  </url>
</urlset>
```

The sitemap format supports up to **50,000 URLs or 50 MB uncompressed** per file. Sites beyond that size need split sitemaps and a sitemap index.

Submit `https://your-domain/sitemap.xml` in Google Search Console or Bing Webmaster Tools. A `Sitemap:` entry in `robots.txt` is optional and is not added by the starter.
