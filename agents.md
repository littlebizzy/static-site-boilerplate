# Agent Guidelines

- This is a lightweight, HTML-first static site boilerplate for Cloudflare Workers. Keep it simple and framework-free.
- Read `README.md` and relevant files in `docs/` before changing behavior.
- Edit source HTML, `site.json`, `templates/`, or `build.py` as needed. Do not edit generated `public/` files.
- Preserve both metadata-based HTML fragments and standalone HTML pages.
- Run `python3 build.py` to check changes and review warnings before committing.
- Make only requested changes; avoid unrelated cleanup or new dependencies.
- Commit directly to `master`, one changed file per commit. Do not use branches, pull requests, or workflows to edit repository files.
- Do not trigger deployments unless requested.
