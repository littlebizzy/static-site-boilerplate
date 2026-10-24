# Deploy Hooks

A deploy hook is a private URL that triggers a Cloudflare build without requiring a new Git commit. For a Worker connected to GitHub, open its **Settings → Builds** area and look for deploy hook controls; create a hook if available for your setup. Send a POST request to the generated URL to request a build:

```sh
curl -X POST 'YOUR_DEPLOY_HOOK_URL'
```

Treat the URL like a secret: anyone who has it may be able to trigger builds. Keep it out of the repository and public logs.

## Deploy hooks vs. watch paths

- **Deploy hook:** You explicitly trigger a build, useful when you want manual control or an external system to request deployment.
- **Watch paths:** Cloudflare checks which files changed in a Git push and skips builds when the changes do not match configured paths. Git remains the trigger.

For example, watch paths can exclude documentation-only changes while still automatically deploying changes to HTML, assets, or `build.py`. A deploy hook instead lets you decide when to build. If using manual-only deployment, disable or otherwise restrict automatic Git-triggered builds so routine commits do not also deploy.

See [Cloudflare Workers Deployment](cloudflare-workers.md) for the initial Git connection.
