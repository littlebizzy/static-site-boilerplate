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

Run `python3 build.py` to prepare the site. By default, the script copies HTML files from the repository root, the three static configuration files, and everything under `assets/` if present. Update the script if your site needs additional folders or generated pages.
