# Cloudflare Workers Deployment

1. Edit `wrangler.jsonc` and choose a unique `name` for the Worker. This name must match the Worker name in Cloudflare. Keep `assets.directory` set to `./public` unless you change the build output.
2. In the Cloudflare dashboard, open **Workers & Pages** and select **Create application**. Choose **GitHub**, authorize access if prompted, and select the repository.
3. Use these build settings:

   | Setting | Value |
   | --- | --- |
   | Production branch | Repository's default branch |
   | Root directory | `/` |
   | Build command | `python3 build.py` |
   | Deploy command | `npx wrangler deploy` |

4. Select **Save and Deploy**.

The build script copies root HTML files, `_headers`, `_redirects`, `robots.txt`, and an optional `assets/` directory into `public/`. Cloudflare deploys the files in `public/`, and `wrangler.jsonc` enables custom `404.html` responses.

Future commits to the production branch will trigger new builds. If the Worker already exists, connect the repository under **Settings → Builds** instead.

No GitHub Actions workflow is required.
