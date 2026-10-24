# Content Management

This boilerplate keeps content in the repository, without a CMS.

- Edit published HTML files directly. Root-level pages and HTML inside regular content directories are copied to `public/` by `build.py`.
- Keep unpublished HTML under the root `drafts/` directory. The build excludes that directory, including its subfolders, so draft pages are not deployed.
- Move a finished draft into its intended published location when ready. Keep internal links consistent with the final URL.
- For larger sites, JSON or Markdown can serve as source content, but converting them into HTML requires site-specific additions to `build.py`; this boilerplate does not perform that conversion automatically.
- Keep unpublished assets out of `assets/`, which is copied in full. Store draft-only files under `drafts/` instead.

See [Build Process](build.md) for the default copying rules and [File Structure](file-structure.md) for page layouts.
