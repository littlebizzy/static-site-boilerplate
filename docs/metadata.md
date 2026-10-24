# HTML Metadata

Give each published page a descriptive, unique title and meta description. Use its preferred public URL as the canonical; generated pages should not reuse the homepage's metadata.

## Example

```html
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Page Title | Site Name</title>
  <meta name="description" content="A concise description of this specific page.">
  <link rel="canonical" href="https://example.com/page/">
  <meta property="og:type" content="website">
  <meta property="og:title" content="Page Title">
  <meta property="og:description" content="A concise description of this specific page.">
  <meta property="og:url" content="https://example.com/page/">
  <meta property="og:image" content="https://example.com/assets/share.png">
  <meta name="twitter:card" content="summary_large_image">
</head>
```

- **Indexing:** Pages intended for search normally need no robots meta tag. Use `<meta name="robots" content="noindex">` for pages that should not appear in search; keep them crawlable so search engines can see it. `follow` is generally the default.
- **Sharing:** Use an absolute, publicly accessible image URL for `og:image`. Open Graph tags also supply common social previews; add platform-specific tags only when needed.
- **Structured data:** Add JSON-LD only when it accurately describes visible content. `WebPage`, `Article`, and other schema types serve different purposes; do not add them indiscriminately.
- **Validation:** Inspect the deployed HTML, check relevant JSON-LD with Google's Rich Results Test, and test social previews on the platforms that matter.
