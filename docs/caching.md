# Caching

Caching saves copies of files so repeat requests can be served faster.

- **Browser cache:** A visitor's browser may reuse downloaded HTML, CSS, JavaScript, or images.
- **Cloudflare edge cache:** Cloudflare can serve static assets from its network rather than fetching them from the deployment's backing storage. Workers Static Assets handles this delivery automatically.
- **`Cache-Control`:** Response headers tell browsers and shared caches how to treat a response. Cloudflare's internal static-asset caching does not necessarily follow the same lifetime as a visitor's browser.

## Practical defaults

Cloudflare Workers Static Assets already sends `Cache-Control: public, max-age=0, must-revalidate` and an `ETag` for ordinary static-asset requests. This allows browsers to revalidate cached HTML and other files after deployment without always downloading them again.

| File type | Optional browser caching | Reason |
| --- | --- | --- |
| HTML | Keep Cloudflare's revalidation default | Check for updated pages on repeat visits. |
| Unversioned CSS/JS | `public, max-age=3600` | Limit how long an updated file can remain stale. |
| Unversioned images | `public, max-age=86400` | Reuse images while allowing eventual updates. |
| Versioned assets | `public, max-age=31536000, immutable` | Cache for a year when each content change produces a new URL. |

These are optional starting points, not required settings. A new deployment does not instantly invalidate files already cached in visitors' browsers.

## Configure headers

Add rules for assets you want to cache longer to the root `_headers` file, which `build.py` copies into `public/`:

```text
/assets/*.css
  Cache-Control: public, max-age=3600

/assets/*.js
  Cache-Control: public, max-age=3600
```

No extra HTML rule is needed for the default revalidation behavior, including clean URLs such as `/about/`. A rule matching `/*.html` should not be assumed to cover clean URLs. Check the response headers of deployed URLs before adding overrides.

**Cache busting:** Change an asset's URL when its contents change, and update the HTML reference. Only use year-long `immutable` caching when the URL changes with the content.

See [Security Headers](security-headers.md) for other `_headers` rules and [Performance](performance.md) for related static-site guidance.

[Cloudflare Workers static asset headers](https://developers.cloudflare.com/workers/static-assets/headers/)
