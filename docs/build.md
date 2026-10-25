# Build Process

Run `python3 build.py` from the repository root. Cloudflare Workers uses the same command before deploying the contents of `public/`.

## What the script does

1. Collects root-level and nested HTML files and checks for conflicting public routes **before** touching `public/`. For example, `about.html` and `about/index.html` cannot coexist because they share the same page slug, even though their canonical slash forms differ.
2. Checks links in HTML `<a href="...">` elements for missing internal pages. Possible missing destinations are reported with the source file, line, and URL, but do not stop the build.
3. Checks local image, script, stylesheet, CSS `url()`, and other supported asset references under `assets/` and supported root-level static files, warning about missing files before cleaning the output.
4. Deletes the previous `public/` directory and recreates it, so removed pages and assets do not linger. It refuses to clean a symlinked `public/` directory.
5. Assembles pages beginning with front-matter metadata using the shared templates and copies other publishable HTML unchanged, preserving their paths.
6. Copies `_headers`, `_redirects`, and `robots.txt` when present.
7. Copies the optional `assets/` directory and supported root-level static files (`.ico`, `.svg`, `.png`, `.jpg`, `.jpeg`, `.gif`, `.webmanifest`, `.xml`, `.txt`, `.pdf`, `.css`, `.js`), excluding asset filenames beginning with `_` or `.`.

## Internal link checks

Both absolute links such as `/about/` and relative links such as `../about/` are checked against published HTML files. Relative links resolve from each page's actual clean URL under `auto-trailing-slash`: `guides/install.html` is served at `/guides/install`, while `guides/install/index.html` is served at `/guides/install/`. Thus `../about/` resolves to `/about/` from the standalone file and `/guides/about/` from the folder index. The checker accepts either slash form for an existing page, but the source layout determines the canonical URL. Explicit `/index.html` links are recognized as the homepage, and exact redirect sources preserve trailing-slash matching for links ending in `/`. Active local 301/302/303/307/308 rules in `_redirects` also count as valid destinations, including simple `/section/*` wildcard sources. Commented rules are ignored; more complex redirect patterns are not interpreted.

The check ignores external URLs, fragment-only links, query strings on otherwise valid URLs, and non-HTML paths outside `/assets/` or the supported root-level static file types. It does not fetch remote URLs, validate fragment IDs, or inspect JavaScript-generated links. The check recognizes redirect source paths but does not verify that a redirect's destination exists or that the redirect will work after deployment. Warnings are advisory because custom routing or future content can produce false positives; conflicting HTML routes and invalid or missing template requirements still stop the build. Prefer linking directly to the final page when practical.

## Asset checks

The build checks `<a href>` links into `/assets/` as well, including downloads such as PDFs, ZIP archives, and images. It also checks local `src` references in `img`, `script`, `source`, `video`, and `audio` elements, responsive image candidates in `srcset` on `img` and `source` (including inside `picture`), plus `href` in stylesheet, icon, preload, modulepreload, and manifest `link` elements. It resolves relative URLs against the public clean page URL, then verifies references under `/assets/` exist in the root `assets/` directory. Missing files produce warnings identifying the referring HTML file and line; copying and deployment can continue.

Stylesheets under `assets/` are also scanned for simple local CSS `url()` references, with relative URLs resolved from the stylesheet directory. CSS comments, external URLs, data URLs, and `@import` rules are ignored. This is not a complete CSS parser; complex escaped URLs are not supported.

External URLs, dynamic resources, and local paths outside `/assets/` or the supported root-level static file types are not checked. `srcset` candidates are parsed as URL tokens followed by optional descriptors, preserving commas inside URL tokens, including data URLs. This is a lightweight check of deployed static assets, not a complete resource crawler.

Only HTML pages are published from other top-level directories. The HTML scan skips `drafts/` and `templates/` folders at any depth, plus HTML filenames beginning with `_` or `.`. It also skips the root-level `docs/`, `assets/`, `public/`, and hidden top-level directories. For example, `pages/drafts/preview.html` and `_notes.html` stay unpublished. The filename rule also applies to ordinary root static files and files inside `assets/`. The required root `_headers` and `_redirects` are still copied explicitly. Python source files and documentation in the root `docs/` directory are not copied into the output.

## Page formats

### Fragments with metadata (recommended)

Start a page with a simple `---` metadata block, followed by its HTML content:

```html
---
title: About | Site Name
description: Learn about this site and the people behind it.
lang: en
canonical: https://example.com/about/
---
<main>
  <h1>About</h1>
  <p>Page-specific content goes here.</p>
</main>
```

The `title` and `lang` fields are required. `description`, `robots` (for example, `noindex`), `canonical`, and `image` are optional. Use an absolute, publicly accessible URL for `image`. Each field is a single `key: value` line; this is a small built-in parser, not full YAML. Unsupported or duplicate fields, missing required values, empty page content, and missing closing `---` stop the build.

The builder reuses `title` for `og:title`, `description` for `og:description`, and `canonical` for `og:url`. It sets `og:type` to `website`, and includes `og:image` only when `image` is provided. It does not require an image or invent a canonical URL.

The builder inserts page metadata into `templates/head.html` and page HTML into `templates/base.html`, alongside `templates/header.html` and `templates/footer.html`. The template supplies the doctype, `html`, `head`, and `body` elements; a fragment normally supplies its own `<main>`. Do not add a complete HTML document or the old `<!-- template: base -->` marker to a fragment.

### Standalone HTML (optional)

An HTML file without a starting `---` block is copied to `public/` unchanged. Use this for self-contained pages that already include `<!doctype html>`, `<html>`, `<head>`, and `<body>`. No template parsing, reordering, or shared header/footer injection occurs. If the page needs shared navigation or metadata, include those elements in the source yourself.

Both formats use the same file paths and clean URLs. The starter `index.html` and `404.html` demonstrate fragments; standalone files can coexist in any publishable directory.

Fragment content is inserted **before** the shared footer. Place scripts that must run after the footer in the base template after `{{ footer }}`, or load appropriate external scripts with `defer`. Template errors stop the build before `public/` is cleaned. Link checks examine assembled HTML for fragments, so their warning line numbers refer to generated output.

## Extending the build

Add site-specific generation steps to `build.py` **after cleaning `public/`** and before deployment. For example, generate published pages or a `public/sitemap.xml` file. Do not write source files into `public/` by hand: the next build deletes them. If your build generates HTML pages, run link validation after those pages exist.

See [File Structure](file-structure.md) for example page layouts and [Cloudflare Workers Deployment](cloudflare-workers.md) for deployment settings.
