# Content Management

This boilerplate keeps content in the repository, without a CMS.

- Set the shared site name, description, and optional production HTTPS URL in `site.json`. Fragment pages can use `{{ site_name }}` and `{{ site_description }}`; per-page metadata overrides remain available.
- Edit published HTML source files directly. Pages with a starting `---` metadata block are assembled into complete HTML; other HTML files are copied to `public/` unchanged.
- For the shared layout, put `title` and `lang` (plus optional `description`, `robots`, `canonical`, `image`, and `lastmod` for sitemap dates) in the page's metadata block, then write its page-specific HTML, normally inside `<main>`. Edit `templates/base.html`, `templates/head.html`, `templates/header.html`, or `templates/footer.html` for site-wide changes.
- Keep unpublished HTML in `drafts/` or `templates/` folders at any depth, or prefix a file or directory name with `_` or `.`. Those pages and directory contents are excluded from builds.
- Move a finished draft into its intended published location when ready. Keep internal links consistent with the final URL.
- For larger sites, JSON or Markdown can serve as source content, but converting them into HTML requires site-specific additions to `build.py`; this boilerplate only assembles HTML fragments and copies standalone HTML.
- Keep draft-only assets under `drafts/`, or prefix file or directory names within `assets/` with `_` or `.`. The build skips all such files and folders.

See [Build Process](build.md) for the default copying rules and [File Structure](file-structure.md) for page layouts.
