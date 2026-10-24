# 404 Errors and Custom Error Pages

Cloudflare Workers uses `not_found_handling: "404-page"` in `wrangler.jsonc` to serve the built `public/404.html` when a page is missing, with an HTTP 404 status. `build.py` copies the root `404.html` into `public/`.

## Customize the template

Edit the root `404.html`: change its title, heading, message, and homepage link, or add your site's CSS and layout. Keep the `noindex` meta tag and a useful way back to the site. No JavaScript is required. Run `python3 build.py` to include changes in the deployment.

## Choose the right response

- **404:** The URL does not exist, and no replacement is known.
- **301:** The content permanently moved; redirect to its relevant new URL using `_redirects`.
- **410:** The content was intentionally removed and is permanently gone; requires explicit response handling rather than the default 404 template.

Missing asset URLs should also return a real error status, not an HTML page with HTTP 200. Avoid redirecting every missing URL to the homepage: that can create misleading *soft 404s* for search engines.

## Verify

Visit a nonexistent URL and inspect the **Network** tab in browser developer tools, or run:

```sh
curl -I https://example.com/nonexistent-page/
```

Confirm the status is `404`, even when your custom page is displayed. Also check a missing image or script URL.
