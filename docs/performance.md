# Performance

This boilerplate serves prebuilt HTML and assets through Cloudflare Workers. There is no application server or client-side framework to optimize.

- Keep HTML and CSS lean; add JavaScript only for features that need it, and use `defer` for external scripts that do not need to block parsing.
- Set image dimensions to prevent layout shifts. Use appropriately sized images and `loading="lazy"` for below-the-fold images, not the main hero image. See [Images](images.md).
- Prefer system fonts when suitable. If using web fonts, limit weights and preload only a font needed immediately.
- Cloudflare handles edge delivery and HTTPS, but cannot fix oversized images, render-blocking resources, or excessive JavaScript.
- Check a deployed page with Lighthouse or PageSpeed Insights when performance appears poor; address measured bottlenecks rather than adding tooling by default.

Keep performance improvements specific to actual static pages and their assets.
