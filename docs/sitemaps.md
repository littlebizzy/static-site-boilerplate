# XML Sitemaps

When the production HTTPS `url` is set in `site.json`, every `python3 build.py` run generates `public/sitemap.xml` automatically. Leave the URL empty for the unconfigured starter; a sitemap cannot contain valid absolute URLs without a domain.

The sitemap includes the clean URLs of published HTML pages, including standalone HTML. It excludes drafts, the 404 page, redirect sources, pages marked `noindex`, and pages whose canonical URL points elsewhere.

## Modification dates

A fragment page can specify an explicit modification date in its front matter:

```yaml
---
title: About Us
lang: en
lastmod: 2026-10-25
---
```

The `lastmod` field must be a real date in `YYYY-MM-DD` format. It takes priority over Git history and is used only for the sitemap, not as an HTML meta tag.

Without that field, the builder uses the most recent Git commit date for the source HTML file. It never uses the build or deployment date. If Git history is missing or shallow, the URL remains in the sitemap without `<lastmod>`. Standalone HTML pages use Git dates because they have no front matter. Changes made only to shared templates or site settings do not update individual source dates.

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
