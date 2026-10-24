# Robots.txt

The root `robots.txt` is copied to `public/robots.txt` by `build.py`. Its default rules allow crawlers to access the site:

```text
User-agent: *
Allow: /
```

## Customize crawler access

To discourage compliant crawlers from fetching a section, add a path-specific rule:

```text
User-agent: *
Allow: /
Disallow: /private-section/
```

`User-agent: *` applies to all crawlers that respect robots rules. `Disallow` controls crawling, **not indexing or access**: blocked URLs may still appear in search results, and visitors can still open them. Do not use `robots.txt` to protect confidential files.

For a page you want excluded from search, serve it with a `noindex` robots meta tag (or `X-Robots-Tag` header), and **allow search engines to crawl it** so they can see that directive. Remove genuinely private content from public hosting or require authentication.

## Verify

Open `https://example.com/robots.txt` after deployment to confirm the published rules. Use Google Search Console's URL Inspection tool to investigate crawling or indexing problems; note that a blocked URL cannot be inspected through a live fetch in the usual way.

A `Sitemap:` directive is optional and is intentionally omitted from this boilerplate. See [XML Sitemaps](sitemaps.md).
