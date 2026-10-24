# Caching

Caching saves copies of files so repeat requests can be served faster.

- **Browser cache:** A visitor's browser may reuse downloaded HTML, CSS, JavaScript, or images.
- **Cloudflare edge cache:** Cloudflare can serve static assets from its network rather than fetching them from the deployment's backing storage. Workers Static Assets handles this delivery automatically.
- **`Cache-Control`:** Response headers tell browsers and shared caches how to treat a response. Cloudflare's internal static-asset caching does not necessarily follow the same lifetime as a visitor's browser.

## Practical defaults

| File type | Suggested browser caching | Reason |
| --- | --- | --- |
| HTML | `public, max-age=0, must-revalidate` | Check for updated pages on repeat visits. |
| Unversioned CSS/JS | `public, max-age=3600` | Limit how long an updated file can remain stale. |
| Unversioned images | `public, max-age=86400` | Reuse images while allowing eventual updates. |
| Versioned assets | `public, max-age=31536000, immutable` | Cache for a year when each content change produces a new URL. |

These are starting points, not required settings. A new deployment does not instantly invalidate files already cached in visitors' browsers.

## Configure headers

Add rules to the root `_headers` file, which `build.py` copies into `public/`:

```text
/*.html
  Cache-Control: public, max-age=0, must-revalidate

/assets/*.css
  Cache-Control: public, max-age=3600

/assets/*.js
  Cache-Control: public, max-age=3600
```

These examples apply to matching asset paths; clean HTML routes such as `/about/` may not match `/*.html`. Check actual response headers on deployed URLs before relying on an HTML rule. Do not apply a long-lived `immutable` rule to assets whose URLs stay the same when their contents change.

**Cache busting:** Rename an asset or add a versioned URL when its contents change, and update the HTML reference. Only use year-long immutable caching when the URL changes with the content.

See [Security Headers](security-headers.md) for other `_headers` rules and [Performance](performance.md) for related static-site guidance.
