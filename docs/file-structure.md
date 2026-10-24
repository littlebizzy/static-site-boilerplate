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
| `public/` | Generated deployment directory; do not edit files here directly. |
| `docs/` | Project documentation; not copied into the deployed site. |

## Page layouts

Both folder-based and file-based HTML pages work, including nested pages:

| Source file | Clean URL |
| --- | --- |
| `about/index.html` | `/about/` |
| `about.html` | `/about/` |
| `guides/install/index.html` | `/guides/install/` |
| `guides/install.html` | `/guides/install/` |

Choose **one** representation for each URL; do not publish both `about.html` and `about/index.html`. The configured Cloudflare Workers `auto-trailing-slash` setting handles clean URLs.

Run `python3 build.py` to copy root and nested HTML pages, static configuration files, and optional `assets/` into `public/`. The script excludes `docs/`, `public/`, `assets/`, and hidden root directories when scanning for nested HTML; assets are copied separately. Extend the script if your site needs other generated content.
