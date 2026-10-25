# XML Sitemaps

Generate `sitemap.xml` from the **published, canonical URLs** during each site build so it stays in sync with the deployed pages. The boilerplate's `build.py` assembles HTML fragments and copies standalone pages and assets, but does not generate a sitemap; add that step when the site has real pages and a known production domain.

## What to include

- Use absolute HTTPS URLs for indexable published pages.
- Exclude drafts, 404 pages, redirects, duplicate URLs, and `noindex` pages.
- Use `<lastmod>` only when a page's content actually changed; do not stamp every URL with the build time.
- Write the resulting XML into `public/sitemap.xml` after generating the pages.

A minimal sitemap looks like this:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://example.com/</loc></url>
  <url><loc>https://example.com/about/</loc></url>
</urlset>
```

For larger sites, split files at **50,000 URLs or 50 MB uncompressed**, whichever comes first, and list them in a sitemap index (`sitemap_index.xml`).

Submit the sitemap URL in Google Search Console and Bing Webmaster Tools. A `Sitemap:` line in `robots.txt` is optional; this boilerplate deliberately leaves it out.
