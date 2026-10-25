# File Structure

| File or directory | Purpose |
| --- | --- |
| `index.html` | Example homepage. |
| `404.html` | Page shown when a URL is not found. |
| `robots.txt` | Default instructions for search crawlers. |
| `_headers` | Security headers for deployed pages and assets. |
| `_redirects` | Commented examples for optional URL redirects. |
| `wrangler.jsonc` | Worker name and static asset deployment settings. |
| `build.py` | Assembles fragment pages and copies standalone pages and assets into `public/`. |
| `assets/` | Optional images, stylesheets, scripts, and other static files. |
| `drafts/` | Unpublished content; HTML in folders named `drafts` is excluded at any depth. |
| `templates/` | Shared base, head, header, and footer for fragment pages; not published directly. |
| `public/` | Generated deployment directory; do not edit files here directly. |
| `docs/` | Project documentation; not copied into the deployed site. |

## Page layouts

Both folder-based and file-based HTML pages work, including nested pages:

| Source file | Clean URL |
| --- | --- |
| `about/index.html` | `/about/` |
| `about.html` | `/about` |
| `guides/install/index.html` | `/guides/install/` |
| `guides/install.html` | `/guides/install` |

With Cloudflare Workers `auto-trailing-slash`, standalone `.html` pages have no trailing slash, while folder `index.html` pages do. Requests to the other slash form redirect to the canonical URL. Choose **one** source representation per page; `build.py` rejects pairs such as `about.html` and `about/index.html` because they share the same page slug.

## Shared layout

The example `index.html` and `404.html` begin with `---` metadata and contain only their page-specific HTML, including `<main>`. The builder combines each fragment with `templates/base.html`, `templates/head.html`, `templates/header.html`, and `templates/footer.html` to produce complete HTML.

A standalone file with its own doctype, `html`, `head`, and `body` (and no starting `---` metadata block) is copied unchanged. The builder never extracts pieces from a complete HTML document. Both page formats use the same clean-URL mapping.

Keep unpublished HTML in `drafts/` or `templates/` folders at any depth, or prefix a file or directory name with `_` or `.`. For example, `pages/drafts/about.html`, `pages/_drafts/about.html`, and `_notes.html` are not published. Move finished pages to normal filenames and locations when ready. The same prefix rule skips files and directories under `assets/`, so an `assets/_originals/` folder stays unpublished. Root `_headers` and `_redirects` are special Cloudflare files copied explicitly.

For copying, exclusions, and clean output behavior, see [Build Process](build.md).
