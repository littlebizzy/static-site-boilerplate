# Deploy Hooks

A deploy hook is a private URL that triggers a Cloudflare Workers build for a selected branch without requiring a new Git commit.

1. In **Workers & Pages**, select the Worker connected to your Git repository.
2. Open **Settings → Builds → Deploy Hooks**.
3. Enter a name, select the branch, choose **Create**, and copy the generated URL.
4. Send an HTTP POST request to trigger a build:

```sh
curl -X POST 'YOUR_DEPLOY_HOOK_URL'
```

Treat the URL like a secret: anyone who has it can trigger builds. Keep it out of the repository and public logs.

## Deploy hooks vs. watch paths

- **Deploy hook:** Explicitly triggers a build for its configured branch, independently of Git pushes.
- **Watch paths:** Filters Git-push builds by changed paths, such as excluding documentation-only commits. It does not trigger builds by itself.

Deploy hooks do **not** disable automatic Git-triggered builds. If you want manual-only builds, configure Git build triggers separately so ordinary commits do not also deploy.

See [Cloudflare Workers Deployment](cloudflare-workers.md) for the initial Git connection and [Cloudflare's Deploy Hooks documentation](https://developers.cloudflare.com/workers/ci-cd/builds/deploy-hooks/) for current dashboard instructions.
