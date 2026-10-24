# Analytics

Analytics are optional. This boilerplate includes no tracking script, cookies, or analytics dependency by default.

## Cloudflare Web Analytics

Cloudflare Web Analytics measures visits and page views using a lightweight browser beacon. To use it:

1. Open **Web Analytics** in the Cloudflare dashboard and add your site.
2. Copy the JavaScript beacon snippet Cloudflare provides for that site.
3. Add the snippet to the HTML pages you want measured, typically before `</body>`. For generated sites, add it to the shared HTML template rather than editing every output file.
4. Deploy and confirm that page views appear in the Web Analytics dashboard. Check your site's Content Security Policy if the beacon is blocked.

Cloudflare's built-in Worker request metrics are different: they report requests handled by the Worker, including non-page requests and bots, and do not require adding a browser script. Web Analytics measures activity from browsers that execute its beacon, so the two sets of numbers will not match exactly.

Only enable tracking if it serves a clear purpose. Review any applicable privacy and disclosure requirements before adding analytics.
