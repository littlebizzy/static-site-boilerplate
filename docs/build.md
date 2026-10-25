# Build Process

Run `python3 build.py` from the repository root. Cloudflare Workers uses the same command before deploying the contents of `public/`.

## What the script does

1. Collects root-level and nested HTML files and checks for conflicting public routes **before** touching `public/`. For example, `about.html` and `about/index.html` cannot coexist because they share the same page slug, even though their canonical slash forms differ.
2. Checks links in HTML `<a href="...">` elements for missing internal pages. Possible missing destinations are reported with the source file, line, and URL, but do not stop the build.
3. Checks local image, script, stylesheet, CSS `url()`, and other supported asset references under `assets/` and supported root-level static files, warning about missing files before cleaning the output.
4. Deletes the previous `public/` directory and recreates it, so removed pages and assets do not linger. It refuses to clean a symlinked `public/` directory.
5. Copies root-level `*.html` files, including `index.html` and `404.html`, and nested HTML files while preserving their paths.
6. Copies `_headers`, `_redirects`, and `robots.txt` when present.
7. Copies the optional `assets/` directory, including its subfolders, and supported root-level static files (`.ico`, `.svg`, `.png`, `.jpg`, `.jpeg`, `.gif`, `.webmanifest`, `.xml`, `.txt`, `.pdf`, `.css`, `.js`).

## Internal link checks

Both absolute links such as `/about/` and relative links such as `../about/` are checked against published HTML files. Relative links resolve from each page's actual clean URL under `auto-trailing-slash`: `guides/install.html` is served at `/guides/install`, while `guides/install/index.html` is served at `/guides/install/`. Thus `../about/` resolves to `/about/` from the standalone file and `/guides/about/` from the folder index. The checker accepts either slash form for an existing page, but the source layout determines the canonical URL. Explicit `/index.html` links are recognized as the homepage, and exact redirect sources preserve trailing-slash matching for links ending in `/`. Active local 301/302/303/307/308 rules in `_redirects` also count as valid destinations, including simple `/section/*` wildcard sources. Commented rules are ignored; more complex redirect patterns are not interpreted.

The check ignores external URLs, fragment-only links, query strings on otherwise valid URLs, and non-HTML paths outside `/assets/` or the supported root-level static file types. It does not fetch remote URLs, validate fragment IDs, or inspect JavaScript-generated links. The check recognizes redirect source paths but does not verify that a redirect's destination exists or that the redirect will work after deployment. Warnings are advisory because custom routing or future content can produce false positives; only conflicting HTML routes remain a build-stopping validation error. Prefer linking directly to the final page when practical.

## Asset checks

The build checks `<a href>` links into `/assets/` as well, including downloads such as PDFs, ZIP archives, and images. It also checks local `src` references in `img`, `script`, `source`, `video`, and `audio` elements, responsive image candidates in `srcset` on `img` and `source` (including inside `picture`), plus `href` in stylesheet, icon, preload, modulepreload, and manifest `link` elements. It resolves relative URLs against the public clean page URL, then verifies references under `/assets/` exist in the root `assets/` directory. Missing files produce warnings identifying the referring HTML file and line; copying and deployment can continue.

Stylesheets under `assets/` are also scanned for simple local CSS `url()` references, with relative URLs resolved from the stylesheet directory. CSS comments, external URLs, data URLs, and `@import` rules are ignored. This is not a complete CSS parser; complex escaped URLs are not supported.

External URLs, dynamic resources, and local paths outside `/assets/` or the supported root-level static file types are not checked. `srcset` candidates are parsed as URL tokens followed by optional descriptors, preserving commas inside URL tokens, including data URLs. This is a lightweight check of deployed static assets, not a complete resource crawler.

Only HTML is copied from other top-level directories. The nested HTML scan skips the **root-level** `docs/`, `drafts/`, `assets/`, `public/`, and hidden top-level directories. Everything inside the root `drafts/` directory stays unpublished, including nested HTML files. A different path such as `pages/drafts/` is **not** automatically excluded. Python source files, deployment configuration, and documentation in the root `docs/` directory are not copied into the output.

## Extending the build

Add site-specific generation steps to `build.py` **after cleaning `public/`** and before deployment. For example, generate published pages or a `public/sitemap.xml` file. Do not write source files into `public/` by hand: the next build deletes them. If your build generates HTML pages, run link validation after those pages exist.

See [File Structure](file-structure.md) for example page layouts and [Cloudflare Workers Deployment](cloudflare-workers.md) for deployment settings.
