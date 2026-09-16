# c21 one-shot unblock brief (2026-09-16 08:30 +0700)

Status probe (`.agent-harness/tools/deploy-blockers-check`, exit 1 = blocked):
secret ABSENT · protection main enforce_admins=true checks=0 pr=none restrictions=0 ·
cloudflared dead · dashboard :8787 200.

All three remaining blockers are USER-side. Do them in one sitting:

## 1. Set the repo secret (unblocks the CI path)

Run from the repo root (sets a repo-level secret on `GRITui/grit-lifelong-ai-skills`):

```sh
gh secret set CLAUDE_CODE_OAUTH_TOKEN
# paste the Claude Code OAuth token when prompted
gh secret list   # verify CLAUDE_CODE_OAUTH_TOKEN appears
```

## 2. Approve resume → Hostinger deploy

User-side infra action (PO cannot execute from the repo). Once the secret exists,
resume the paused deploy flow and let it complete to Hostinger.

## 3. Domain decision — stable tunnel URL

| Option | Cost | Stability | Notes |
|---|---|---|---|
| A. Use a domain you already own | $0 | stable | point its DNS at Cloudflare, then named tunnel on a subdomain |
| B. Buy a cheap domain (~$10/yr) | ~$10/yr | stable | most robust standalone; registrar → Cloudflare nameservers |
| C. Random `trycloudflare.com` URL | $0 | unstable | rejected — URL changes on every cloudflared restart |

After the domain is decided (A or B):

```sh
cloudflared tunnel create <tunnel-name>
cloudflared tunnel route dns <tunnel-name> <sub>.<domain>
# ingress: <sub>.<domain> -> http://localhost:8787 (or the deploy target)
cloudflared tunnel run <tunnel-name>
```

## Verify

Re-run `sh .agent-harness/tools/deploy-blockers-check` — exit 0 with
`DEPLOY BLOCKERS: CLEARED` means the card can move to `done` (PO re-audit).
