# Content Management

This boilerplate keeps content in the repository, without a CMS.

- Edit published HTML files directly. Root-level pages and HTML inside regular content directories are copied to `public/` by `build.py`.
- Keep unpublished HTML in `drafts/` or `templates/` folders at any depth, or prefix individual HTML filenames with `_` or `.`. These pages are excluded from builds.
- Move a finished draft into its intended published location when ready. Keep internal links consistent with the final URL.
- For larger sites, JSON or Markdown can serve as source content, but converting them into HTML requires site-specific additions to `build.py`; this boilerplate does not perform that conversion automatically.
- Keep draft-only assets under `drafts/` rather than in `assets/`. The build copies ordinary files from `assets/`, but skips filenames beginning with `_` or `.`.

See [Build Process](build.md) for the default copying rules and [File Structure](file-structure.md) for page layouts.
