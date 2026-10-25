# File Structure

| File or directory | Purpose |
| --- | --- |
| `index.html` | Example homepage. |
| `404.html` | Page shown when a URL is not found. |
| `robots.txt` | Default instructions for search crawlers. |
| `_headers` | Security headers for deployed pages and assets. |
| `_redirects` | Commented examples for optional URL redirects. |
| `wrangler.jsonc` | Worker name and static asset deployment settings. |
| `build.py` | Copies site files into `public/` for deployment. |
| `assets/` | Optional images, stylesheets, scripts, and other static files. |
| `drafts/` | Unpublished content; HTML in folders named `drafts` is excluded at any depth. |
| `templates/` | Optional HTML templates; excluded from publishing at any depth. |
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

Keep unpublished HTML in `drafts/` or `templates/` folders at any depth, or prefix an HTML filename with `_` or `.`. For example, `pages/drafts/about.html` and `_notes.html` are not published. Move finished pages to normal filenames and locations when ready. Keep draft-only assets out of `assets/`: its ordinary files are copied, but filenames beginning with `_` or `.` are excluded.

For copying, exclusions, and clean output behavior, see [Build Process](build.md).
