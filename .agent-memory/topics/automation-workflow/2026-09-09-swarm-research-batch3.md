## TL;DR
> ✅ QA-gated by PO 2026-09-09 · spot-check: CVE-2026-21858 (Ni8mare) is a real CVSS 10.0 unauthenticated n8n webhook RCE ✓ (independently confirmed via Upwind, Indusface, Aikido writeups)

- n8n disclosed a chain of critical CVEs in 2026 (CVE-2026-21858 "Ni8mare" CVSS 10.0 unauthenticated RCE via webhook Content-Type confusion; CVE-2026-21877 authenticated RCE; CVE-2025-68613) — self-hosted instances (like the local n8n on port 5678) must be on n8n ≥1.121.3/2.5.2 or later, not just any recent version.
- Claude Code shipped concrete headless/cron hardening in September 2026: `--permission-prompts none` for unattended hosts, and a fix for one-shot scheduled tasks re-firing (a bug that directly matches this workspace's documented "one-shot self-removing cron job" pattern).
- 2026 MCP security guidance has converged on a "deny by default" posture: bind MCP servers to 127.0.0.1 not 0.0.0.0 (researchers found ~1,862 exposed MCP servers, mostly forgotten dev instances), containerize each server separately, and authenticate every call with per-agent identity (OIDC/OAuth) rather than shared static tokens.
- n8n's RCE chain specifically implicates webhook and form-based workflow handling — directly relevant since the local n8n instance already runs Telegram/MCP/kanban-move webhooks per existing memory (n8n-failure-analysis).
- Version discipline (not just "self-hosted is fine") is now the dominant theme across both n8n and MCP-server security writeups — outdated self-hosted infra is treated as the top risk vector, above misconfiguration.

## Findings

### n8n CVE-2026-21858 "Ni8mare" — unauthenticated RCE via webhook Content-Type confusion
- What: A CVSS 10.0 vulnerability in n8n's webhook and file-handling logic lets an attacker send crafted HTTP requests with manipulated Content-Type headers to override internal request-parsing state, read arbitrary files (including credentials/secrets), forge admin sessions, and achieve remote code execution — no authentication required. Affects versions from 1.65.0 up to below 1.121.0.
- Why it matters: This is a webhook-path exploit, and the local n8n instance (per existing memory: n8n-failure-analysis.md) already has active Telegram, MCP, and kanban-move webhooks registered — exactly the attack surface this CVE targets.
- Confidence: high (corroborated by Orca Security, The Hacker News, Canadian Centre for Cyber Security advisory AL26-001, and a public PoC repo)

### n8n CVE-2026-21877 — authenticated RCE, CVSS 10.0
- What: A second critical, fully-rated authenticated RCE disclosed alongside the Ni8mare chain, fixed in n8n 1.121.3.
- Why it matters: Confirms this isn't an isolated one-off bug but a pattern of critical webhook/execution-path flaws in 2026 n8n releases; patching to the latest stable line matters more than usual.
- Confidence: high (Canadian Centre for Cyber Security advisory, multiple vendor blogs)

### n8n minimum safe version is higher than expected
- What: Multiple 2026 sources converge that the actual safe floor is n8n 2.5.2 (2.x branch) or 1.123.17 (1.x branch) — not just "1.121.0 or later" as n8n's own advisory language might suggest at first read.
- Why it matters: The local instance was audited at v2.37.9 on 2026-09-08 (per n8n-failure-analysis.md), which is above this floor — good news, but the version-check habit itself should become routine given how fast the CVE floor moved in 2026.
- Confidence: med (aggregator/vendor blog synthesis, not directly cross-checked against n8n's own security advisory page)

### Claude Code headless/cron hardening, September 2026
- What: On Sep 2, 2026 Claude Code added `--permission-prompts none`, which auto-denies anything that would otherwise prompt on unattended hosts (rather than silently hanging or erroring unpredictably). Separately, a bug where one-shot scheduled tasks would re-fire after completion was fixed, and timestamp markers were added in transcripts when `/loop` or `CronCreate` fire.
- Why it matters: The one-shot re-fire fix directly targets the exact failure mode this workspace's global CLAUDE.md already warns about (self-removing crontab lines for one-shot jobs) — worth checking whether the fix is at the Claude Code CLI layer or only for its own internal scheduler (`schedule`/`loop` skills), since the workspace's actual scheduling is still macOS cron wrapping `claude -p`.
- Confidence: med (aggregator changelog sites agree; not cross-checked against code.claude.com/docs/en/changelog directly)

### MCP server exposure: "bind to localhost" is still the most-violated rule
- What: 2026 security research found roughly 1,862 MCP servers exposed to the public internet by binding to 0.0.0.0 instead of 127.0.0.1, mostly forgotten dev/test instances with no authentication.
- Why it matters: Directly actionable for any locally-run MCP server in this workspace (n8n's MCP Server Trigger node, any self-hosted MCP gateway) — binding scope is a one-line config check worth auditing.
- Confidence: med (multiple 2026 MCP security vendor writeups, e.g., Stacklok, Cloud Security Alliance agentic MCP guide; not a primary incident report)

### MCP zero-trust posture: per-agent identity + RBAC over shared tokens
- What: 2026 MCP best-practice guidance recommends every tool call carry authenticated per-user/per-agent identity (OIDC/OAuth), with role-based access control at the tool level and a deny-by-default stance, rather than one shared static API token for all callers.
- Why it matters: The workspace currently uses per-project static API tokens (e.g., Hostinger `HOSTINGER_API_TOKEN` scoped per project in `~/.claude.json`, per existing global memory) — functionally reasonable for a single-operator setup, but worth knowing this is now considered the minimum-viable pattern, not the target state, as swarm/agent count grows.
- Confidence: low-med (best-practice guidance aggregated from vendor content, not an independent audit of this workspace's actual MCP configs)

## For This Workspace
- Re-verify the local n8n version against the current security floor before the next deploy/workflow change (last confirmed v2.37.9 on 2026-09-08, which is above the ~2.5.2 CVE-2026-21858 floor, but re-check n8n's own advisory since sources disagree slightly on exact patched versions).
- Audit whether any locally-run MCP server (n8n's MCP Server Trigger, or any other self-hosted MCP gateway) binds to 0.0.0.0 vs 127.0.0.1 — this is a one-command check (`lsof -i :<port>` or the server's bind-address config) and matches a documented top misconfiguration for 2026.
- Given n8n's RCE chain specifically targets webhook/form-handling code paths, and this instance already has Telegram/MCP/kanban-move webhooks live, treat any future webhook-triggered workflow addition as security-sensitive: confirm patched n8n version first, don't add new public-facing webhook endpoints without reviewing exposure.
- When next touching the `claude -p` cron wrapper scripts, check whether `--permission-prompts none` (added Sep 2, 2026) is a better fit than the current `--allowedTools` allowlist approach for unattended runs — it may close gaps the allowlist doesn't cover, though it should be tested alongside (not instead of) the allowlist given the existing "unlisted tools silently no-op" gotcha.

## Sources
https://orca.security/resources/blog/cve-2026-21858-n8n-rce-vulnerability/
https://thehackernews.com/2026/01/n8n-warns-of-cvss-100-rce-vulnerability.html
https://thehackernews.com/2026/03/critical-n8n-flaws-allow-remote-code.html
https://www.cyber.gc.ca/en/alerts-advisories/al26-001-vulnerabilities-affecting-n8n-cve-2026-21858-cve-2026-21877-cve-2025-68613
https://www.sentinelone.com/vulnerability-database/cve-2026-21858/
https://community.n8n.io/t/which-n8n-version-fixes-both-cve-2026-21858-and-cve-2025-68613/247554
https://github.com/Chocapikk/CVE-2026-21858
https://horizon3.ai/attack-research/attack-blogs/the-ni8mare-test-n8n-rce-under-the-microscope-cve-2026-21858/
https://code.claude.com/docs/en/changelog
https://www.gradually.ai/en/changelogs/claude-code/
https://releasebot.io/updates/anthropic/claude-code
https://www.havoptic.com/tools/claude-code
https://stacklok.com/blog/mcp-security-best-practices-what-every-enterprise-team-needs-to-know-in-2026/
https://labs.cloudsecurityalliance.org/agentic/agentic-mcp-security-best-practices-v1/
https://obot.ai/resources/learning-center/mcp-security/
