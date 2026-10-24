# Redirects

Edit `_redirects` in the repository root. The build script copies it into `public/`, where Cloudflare Workers reads the rules. Each active rule goes on its own line:

```text
/source/ /destination/ 301
```

Common examples:

```text
# Permanent move
/old-page/ /new-page/ 301

# Temporary move
/temporary-page/ /new-page/ 302

# Keep the remaining path when moving a section
/old-section/* /new-section/:splat 301

# Send all URLs in a retired section to the homepage
/retired-section/* / 301
```

Remove the leading `#` from a commented example to activate it. Use **301** for a permanent move or **302** for a temporary one. Put specific paths before wildcard rules; the first matching rule wins. Review wildcard rules carefully so they do not catch URLs you want to keep.

[Cloudflare Workers redirect reference](https://developers.cloudflare.com/workers/static-assets/redirects/)
