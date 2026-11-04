# XML Sitemaps

When the production HTTPS `url` is set in `site.json`, every `python3 build.py` run generates `public/sitemap.xml` automatically by default. Leave the URL empty for the unconfigured starter; a sitemap cannot contain valid absolute URLs without a domain.

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

## Optional opaque filename

The standard `sitemap.xml` name is the default and works well for most sites. If you want to reduce casual discovery of the URL list, you may instead use a **fixed, randomly chosen 12-character filename** consisting of lowercase letters and digits, followed by `.xml`. Twelve characters is a project convention, not a sitemap protocol requirement. Choose the name once; do not rotate it with every build.

1. In `build.py`, find `write_sitemap()` and change the filename used by `(OUTPUT / "sitemap.xml").write_text(...)` to your chosen name. Update its printed generation message to use the same name.
2. Run `python3 build.py` and check that `public/` contains the renamed sitemap, with no leftover `sitemap.xml`. Do not publish a second copy or a redirect from the default name.
3. Submit the exact new URL directly in Google Search Console or Bing Webmaster Tools. Do not announce the opaque URL through `robots.txt`, public HTML, redirects, manifests, `_headers`, or other deployed files.
4. If the site's CSP interferes with a browser's built-in XML viewer, a generic `/*.xml` rule with `! Content-Security-Policy` in `_headers` can address that without naming the sitemap. It removes CSP for **all** matching XML files, so review that scope; see [Security Headers](security-headers.md).

An opaque name only reduces discoverability: the sitemap remains publicly accessible to anyone who knows its URL, and the filename is visible in `build.py` if the source repository is public. It is **not** authentication or protection for sensitive URLs or content.

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

Submit the sitemap's actual URL in Google Search Console or Bing Webmaster Tools (the default is `https://your-domain/sitemap.xml`). There is no need to link to it from normal pages or navigation. A `Sitemap:` entry in `robots.txt` is optional and is not added by the starter; omit it when using an opaque filename.
