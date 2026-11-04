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

Standalone HTML pages can specify the date with a tag inside their `<head>`:

```html
<meta name="last-modified" content="2026-10-25">
```

Both methods require a valid `YYYY-MM-DD` date representing the page's last significant update. The builder rejects invalid or duplicate standalone-page date tags. Pages without an explicit date remain in the sitemap without `<lastmod>`.

The fragment `lastmod` field affects only the sitemap and does not generate an HTML meta tag. The standalone `last-modified` tag is read by this builder, **not** a standard Google SEO meta tag; standalone HTML is copied unchanged. Dates are never inferred from Git commits, file timestamps, or build/deployment times. Update a date when the page's main content, structured data, or relevant links change significantly, not for minor cosmetic edits.

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

Submit `https://your-domain/sitemap.xml` in Google Search Console or Bing Webmaster Tools. There is no need to link to the sitemap from normal pages or navigation. A `Sitemap:` entry in `robots.txt` is optional and is not added by the starter.
