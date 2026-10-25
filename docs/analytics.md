# Analytics

Analytics are optional. This boilerplate includes no tracking script, cookies, or analytics dependency by default.

## Cloudflare Web Analytics

Cloudflare Web Analytics measures visits and page views using a lightweight browser beacon. To use it:

1. Open **Web Analytics** in the Cloudflare dashboard and add your site.
2. For a site proxied through Cloudflare, use automatic setup. Cloudflare injects the beacon without changes to your HTML and sends reports to your own `/cdn-cgi/rum` endpoint.
3. The default `_headers` CSP already allows the beacon script from `https://static.cloudflareinsights.com` and includes `connect-src 'self'` for automatic reporting. This does not enable analytics on its own.
4. If using manual setup instead, add Cloudflare's snippet to your HTML pages, typically before `</body>` (or to the shared template for generated sites). Manual beacons report to `https://cloudflareinsights.com`, so also add that origin to `connect-src` in `_headers`. See [Security Headers](security-headers.md).
5. Deploy and confirm that page views appear in the Web Analytics dashboard.

Cloudflare's built-in Worker request metrics are different: they report requests handled by the Worker, including non-page requests and bots, and do not require adding a browser script. Web Analytics measures activity from browsers that execute its beacon, so the two sets of numbers will not match exactly.

Only enable tracking if it serves a clear purpose. Review any applicable privacy and disclosure requirements before adding analytics.
