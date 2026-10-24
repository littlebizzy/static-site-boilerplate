# Build Process

Run `python3 build.py` from the repository root. Cloudflare Workers uses the same command before deploying the contents of `public/`.

## What the script does

1. Collects root-level and nested HTML files and checks for conflicting public routes **before** touching `public/`. For example, `about.html` and `about/index.html` cannot coexist because both represent `/about/`. If there is a conflict, the build stops and identifies the source files.
2. Deletes the previous `public/` directory and recreates it, so removed pages and assets do not linger. It refuses to clean a symlinked `public/` directory.
3. Copies root-level `*.html` files, including `index.html` and `404.html`, and nested HTML files while preserving their paths.
4. Copies `_headers`, `_redirects`, and `robots.txt` when present.
5. Copies the optional `assets/` directory, including its subfolders.

Only HTML is copied from other top-level directories. The nested HTML scan skips the **root-level** `docs/`, `drafts/`, `assets/`, `public/`, and hidden top-level directories. Everything inside the root `drafts/` directory stays unpublished, including nested HTML files. A different path such as `pages/drafts/` is **not** automatically excluded. Python source files, deployment configuration, and documentation in the root `docs/` directory are not copied into the output.

## Extending the build

Add site-specific generation steps to `build.py` **after cleaning `public/`** and before deployment. For example, generate published pages or a `public/sitemap.xml` file. Do not write source files into `public/` by hand: the next build deletes them.

See [File Structure](file-structure.md) for example page layouts and [Cloudflare Workers Deployment](cloudflare-workers.md) for deployment settings.
