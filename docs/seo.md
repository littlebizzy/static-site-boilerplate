# SEO

Static HTML pages are directly readable by search engines without JavaScript rendering. Keep the site structure and published content straightforward:

- Use consistent, descriptive URLs and link to important pages with ordinary HTML `<a href>` links.
- Give each indexable page a distinct, useful title, meta description, and canonical URL. See [HTML Metadata](metadata.md).
- Publish meaningful page content in the HTML itself. Avoid creating near-duplicate or empty pages solely to target search queries.
- Choose one preferred hostname and URL format; redirect outdated or alternate URLs when appropriate. See [Custom Domains](domains.md) and [Redirects](redirects.md).
- Keep drafts and internal pages out of the published build. Use `noindex` for publicly accessible pages that should not appear in search results; blocking crawling in `robots.txt` does not reliably remove URLs from search results. See [Robots.txt](robots-txt.md).
- If generating a sitemap, include only intended canonical, indexable URLs. See [XML Sitemaps](sitemaps.md).

After launch, verify the site in Google Search Console to inspect indexing, submitted sitemaps, and reported crawling problems. Indexing is not guaranteed even when a page is technically accessible.
