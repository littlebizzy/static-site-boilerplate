# HTML Metadata

Give each published page a descriptive, unique title and meta description. Use its preferred public URL as the canonical; generated pages should not reuse the homepage's metadata.

## Fragment page metadata

The default fragment format puts metadata before the HTML content:

```html
---
title: Page Title | Site Name
description: A concise description of this specific page.
lang: en
canonical: https://example.com/page/
image: https://example.com/assets/share.png
---
<main>
  <h1>Page Title</h1>
  <p>Page content.</p>
</main>
```

`title` and `lang` are required. `description`, `canonical`, `image`, and `robots` (such as `noindex`) are optional. The builder uses `templates/head.html` to create the HTML head and escapes metadata values. These are plain single-line `key: value` fields, not full YAML.

Open Graph tags are generated automatically: `og:title` uses `title`, `og:description` uses `description` when present, `og:url` uses `canonical` when present, and `og:type` defaults to `website`. The optional `image` field produces `og:image` only when supplied; use an absolute, publicly accessible image URL.

The shared head adds `<meta name="twitter:card" content="summary">` for a simple link preview. It reuses the existing Open Graph title and description, without duplicate Twitter-specific fields or a required image. The final preview appearance depends on the platform.

## Shared head template

A shared metadata template is recommended for multi-page sites: common markup stays consistent, while each page supplies its own values. This boilerplate uses `templates/head.html` for the charset, viewport, title, favicon, stylesheet, Twitter summary card, and `{{ metadata }}` placeholder. `build.py` fills the page-specific title, description, robots, canonical, and Open Graph tags from front matter.

Edit the shared template for site-wide head markup; edit each fragment's metadata for page-specific values. Do not repeat an entire `<head>` in fragments or hardcode one page's canonical URL across the site. Other platform-specific fields or a different `og:type` require site-specific template/builder changes. Standalone HTML files manage their own `<head>` and are copied unchanged.

## Multilingual pages (optional)

Set each page's `lang` field to its content language (for example, `en`, `th`, or `en-US`), and translate its title, description, and other page-specific metadata. Language versions should generally have their own canonical URLs rather than all pointing to the English page.

When equivalent translated pages exist, identify them with reciprocal `hreflang` links in each version's `<head>`, including a link to itself. For example, the English and Thai homepages would both include:

```html
<link rel="alternate" hreflang="en" href="https://example.com/">
<link rel="alternate" hreflang="th" href="https://example.com/th/">
```

Use real absolute URLs, and add `x-default` only if a language-neutral fallback is appropriate. The starter does not generate `hreflang`; multilingual sites can extend the shared head template and builder with page-specific alternate URLs. Do not add these tags when there are no translated equivalents. See [Google's localized-pages guidance](https://developers.google.com/search/docs/specialty/international/localized-versions).

## JSON-LD and schema.org

JSON-LD expresses structured data using schema.org types, typically in a `<script type="application/ld+json">` element in the `<head>` or `<body>`. Unlike ordinary meta tags, it describes entities and their relationships. The default builder **does not generate JSON-LD automatically**.

For example, a real site's homepage might include:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "Example Site",
  "url": "https://example.com/"
}
</script>
```

Replace example values with the site's real name and production URL before publishing. For a single page, place relevant JSON-LD in its fragment HTML or standalone document. For repeated schema, a shared template or build-time generator is often easier to maintain; generate valid JSON from actual page data, and emit each schema type only on relevant pages.

Common choices:

- **`WebSite`:** A real site's homepage, particularly to communicate its preferred site name.
- **`Organization`:** The homepage of an actual organization with verifiable details.
- **`BreadcrumbList`:** Nested pages with a meaningful breadcrumb hierarchy.
- **`Article`, `Product`, etc.:** Only pages that genuinely contain that type of content.

The starter's placeholder site name and domain are not real entities. Its homepage and 404 page deliberately ship without JSON-LD; do not add generic schema solely to fill every page. Structured data must agree with the visible page and does not guarantee a rich result.

## Checks

- **Indexing:** Search-indexable pages normally need no robots meta tag. Use `<meta name="robots" content="noindex">` where appropriate, and keep the URL crawlable.
- **Sharing:** Use an absolute, publicly accessible image URL for `og:image` when provided; add platform-specific tags only when needed.
- **Validation:** Inspect built HTML, test JSON-LD with [Google's Rich Results Test](https://search.google.com/test/rich-results) or [Schema Markup Validator](https://validator.schema.org/), and check social previews.

See [Google's structured data introduction](https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data) and [general guidelines](https://developers.google.com/search/docs/appearance/structured-data/sd-policies).
