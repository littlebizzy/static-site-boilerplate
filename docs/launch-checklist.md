# Launch Checklist

Before publishing a static HTML site through Cloudflare Workers:

- [ ] Run `python3 build.py` successfully and confirm `public/` contains the intended pages and assets.
- [ ] Confirm the custom domain loads over HTTPS and the alternate `www` or non-`www` hostname redirects to the preferred hostname.
- [ ] Visit a nonexistent URL and confirm the custom `404.html` is shown with an HTTP **404** status.
- [ ] Check that required `_redirects` rules work and `_headers` applies the expected security headers.
- [ ] Confirm each published page has an appropriate title, description, and canonical HTTPS URL.
- [ ] Review `robots.txt` and, if the site uses a sitemap, confirm the generated sitemap contains only intended public URLs.
- [ ] Check that drafts, development files, and internal documentation are not published in `public/`.

See [Cloudflare Workers Deployment](cloudflare-workers.md), [Custom Domains](domains.md), and [Build Process](build.md) for setup details.
