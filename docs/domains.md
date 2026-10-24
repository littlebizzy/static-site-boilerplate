# Custom Domains

After deploying the Worker, connect your domain in the Cloudflare dashboard:

1. Add the domain to Cloudflare and ensure its DNS is managed by Cloudflare.
2. Open **Workers & Pages**, select the Worker, and add the hostname under **Settings → Domains & Routes → Add → Custom Domain**. Cloudflare configures the required DNS record and certificate for that hostname.
3. Wait for the custom domain and HTTPS certificate to become active, then visit the site over `https://`.

## Preferred hostname

Choose either `example.com` or `www.example.com` as the primary hostname. If you want both, configure the alternate hostname separately and redirect it to the primary one with a Cloudflare Redirect Rule (preserving the path and query string). Do not serve duplicate pages on both hostnames.

Update canonical URLs, Open Graph URLs, and generated sitemap URLs to use the preferred HTTPS hostname. Check that the alternate hostname redirects and that the primary site loads without certificate errors.

See [Cloudflare Workers Deployment](cloudflare-workers.md) for build and deployment settings.
