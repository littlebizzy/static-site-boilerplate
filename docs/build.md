# Build Process

Run `python3 build.py` from the repository root. Cloudflare Workers uses the same command before deploying the contents of `public/`.

## What the script does

1. Collects root-level and nested HTML files and checks for conflicting public routes **before** touching `public/`. For example, `about.html` and `about/index.html` cannot coexist because both represent `/about/`.
2. Checks links in HTML `<a href="...">` elements for missing internal pages. If a destination is missing, the build stops and reports the source file, line, and URL before clearing `public/`.
3. Deletes the previous `public/` directory and recreates it, so removed pages and assets do not linger. It refuses to clean a symlinked `public/` directory.
4. Copies root-level `*.html` files, including `index.html` and `404.html`, and nested HTML files while preserving their paths.
5. Copies `_headers`, `_redirects`, and `robots.txt` when present.
6. Copies the optional `assets/` directory, including its subfolders.

## Internal link checks

Both absolute links such as `/about/` and relative links such as `../about/` are checked against published HTML files. Relative links resolve from each page's public clean URL under the configured `auto-trailing-slash` behavior, not its source file path. For example, `guides/install.html` is served at `/guides/install/`, so `../about/` resolves to `/guides/about/`. Both `about.html` and `about/index.html` can satisfy the clean `/about/` route (but cannot coexist). Active local 301/302/303/307/308 rules in `_redirects` also count as valid destinations, including simple `/section/*` wildcard sources. Commented rules are ignored; more complex redirect patterns are not interpreted.

The check ignores external URLs, fragment-only links, query strings on otherwise valid URLs, and non-HTML asset paths. It does not fetch remote URLs, validate fragment IDs, or inspect JavaScript-generated links. The check recognizes redirect source paths but does not verify that a redirect's destination exists or that the redirect will work after deployment. Prefer linking directly to the final page when practical.

Only HTML is copied from other top-level directories. The nested HTML scan skips the **root-level** `docs/`, `drafts/`, `assets/`, `public/`, and hidden top-level directories. Everything inside the root `drafts/` directory stays unpublished, including nested HTML files. A different path such as `pages/drafts/` is **not** automatically excluded. Python source files, deployment configuration, and documentation in the root `docs/` directory are not copied into the output.

## Extending the build

Add site-specific generation steps to `build.py` **after cleaning `public/`** and before deployment. For example, generate published pages or a `public/sitemap.xml` file. Do not write source files into `public/` by hand: the next build deletes them. If your build generates HTML pages, run link validation after those pages exist.

See [File Structure](file-structure.md) for example page layouts and [Cloudflare Workers Deployment](cloudflare-workers.md) for deployment settings.
