## TL;DR
> ✅ QA-gated by PO 2026-09-12 · spot-check: CVE-2026-21858 (Ni8mare) CVSS 10.0 n8n RCE fixed in ≥1.121.0 ✓
- n8n has shipped multiple critical (CVSS 9.9–10.0) RCE/file-read CVEs through 2026 (Ni8mare/N8scape family) — self-hosted instances must be pinned to patched versions, not left on old tags.
- n8n's September 2026 release cycle adds MCP OAuth support, an MCP TypeScript SDK v2-based instance MCP server, and makes the VM expression engine default — relevant if this workspace's n8n talks to Claude/MCP tooling.
- launchd is the macOS-native, Apple-preferred scheduler over cron in 2026; it handles sleep/wake far better than plain cron and integrates with system logging.
- Claude Code headless (`claude -p`) automation guidance in 2026 converges on `--allowedTools`, `--max-turns`, and `--max-budget-usd` as the three mandatory unattended-run guardrails.
- Recent xml2js/XML-node/HTTP-Request-node prototype-pollution CVEs in n8n (July 2026) show third-party node dependencies are a recurring n8n attack surface, not just core.

## Findings

1. **What**: n8n disclosed CVE-2026-21858 ("Ni8mare", CVSS 10.0, unauthenticated file read/RCE via unvalidated file-upload form fields) and CVE-2026-21877 (CVSS 9.9, authenticated arbitrary code execution), both requiring upgrade to n8n ≥1.121.0/1.121.3.
   **Why it matters**: Any self-hosted n8n instance exposed to the internet (even behind a webhook) is a high-value RCE target; version pinning without a patch cadence is a real risk.
   **Confidence**: high

2. **What**: A further RCE, CVE-2026-25049, was fixed in n8n 1.123.17 and 2.5.2.
   **Why it matters**: Confirms an ongoing pattern of RCE-class bugs across 2026 releases — self-hosted n8n needs continuous patching, not a one-time upgrade.
   **Confidence**: high

3. **What**: Three prototype-pollution CVEs landed in July 2026 in the xml2js library (CVE-2026-42231), the XML node (CVE-2026-42232), and the HTTP Request node (CVE-2026-44789).
   **Why it matters**: These hit commonly-used nodes (HTTP Request, XML) that a typical automation workflow (e.g. calling external APIs) would use directly, widening the practical blast radius beyond exotic file-upload flows.
   **Confidence**: high

4. **What**: n8n's September 2026 release notes describe MCP OAuth deployment support, migration of the instance MCP server to MCP TypeScript SDK v2, Postgres pool teardown/recovery fixes, and the VM expression engine becoming the default expression engine.
   **Why it matters**: If n8n workflows in this environment integrate with MCP servers or Postgres-backed queues, these are the concrete upgrade-relevant changes to check compatibility against before bumping versions.
   **Confidence**: med (aggregated from changelog-summary sites, not the raw n8n GitHub release notes directly)

5. **What**: Apple's guidance and community consensus in 2026 continues to favor launchd LaunchAgents over cron on macOS — launchd is the officially supported path, integrates with unified logging, and (unlike vanilla cron) can run missed jobs shortly after wake depending on power state/config.
   **Why it matters**: Directly contradicts relying on plain crontab for schedules that need to survive sleep; a LaunchAgent with `StartCalendarInterval` plus `RunAtLoad`/power-assertion handling is the more robust primitive for a solo-dev Mac automation box.
   **Confidence**: high

6. **What**: cron remains present on macOS purely for backward compatibility (Sequoia even added explicit legacy-cron toggles in System Settings), but is not the tool macOS's own scheduled features use internally.
   **Why it matters**: Confirms cron isn't being actively hardened/extended by Apple — new sleep/wake or event-triggered automation needs should be built on launchd, with cron treated as legacy-only.
   **Confidence**: med

7. **What**: Current best-practice guidance for `claude -p` (Claude Code headless mode) in CI/pipeline/cron-style unattended contexts centers on three flags: `--allowedTools` (explicit tool allowlist, since unlisted tools silently no-op with no human to approve), `--max-turns` (caps action count), and `--max-budget-usd` (caps spend); output can be text/json/stream-json and stdin/stdout piping lets Claude Code act as one node in a larger multi-agent pipeline.
   **Why it matters**: Matches and reinforces this workspace's existing lesson (tools not in `--allowedTools` silently no-op) and adds two guardrails (turn cap, budget cap) not currently documented for headless runs here.
   **Confidence**: med (drawn from third-party guides/blogs summarizing Anthropic docs, not the primary Anthropic docs page itself)

## For This Workspace
- Add a periodic n8n version/CVE check to the ops routine (e.g. a monthly board card) — pin to a specific n8n release and re-verify against the n8n security-advisories page rather than assuming "already patched."
- If any n8n workflow here uses the HTTP Request or XML nodes, confirm the instance is past the July 2026 patch level (fixes CVE-2026-42231/42232/44789) before trusting untrusted input into those nodes.
- Consider migrating scheduled headless `claude -p` / n8n trigger jobs currently on crontab to launchd LaunchAgents for better sleep/wake behavior, keeping the existing "self-removing one-shot" and "no dedup on crontab append" lessons but expressed as plist `StartCalendarInterval` + `RunAtLoad`.
- When writing/updating headless `claude -p` invocations, add `--max-turns` and `--max-budget-usd` alongside the already-documented `--allowedTools` requirement, to cap runaway unattended runs.

## Sources
- https://thehackernews.com/2026/01/n8n-warns-of-cvss-100-rce-vulnerability.html
- https://www.rapid7.com/blog/post/etr-ni8mare-n8scape-flaws-multiple-critical-vulnerabilities-affecting-n8n/
- https://blog.securelayer7.net/cve-2026-25049/
- https://www.cyber.gc.ca/en/alerts-advisories/al26-001-vulnerabilities-affecting-n8n-cve-2026-21858-cve-2026-21877-cve-2025-68613
- https://aicybr.com/blog/n8n-august-2026-security-advisories-rce-upgrade
- https://releasebot.io/updates/n8n
- https://blog.mean.ceo/n8n-news-september-2026/
- https://x.com/cathrynlavery/status/2024247142571741656
- https://www.jeremycherfas.net/blog/scheduled-jobs-with-launchd-rather-than-cron
- https://devops.sarmento.org/en/posts/scheduling-tasks-on-macos-with-launchd-no-cron-no-workarounds/
- https://picklog.cc/blog/launchd-vs-cron
- https://amux.io/guides/claude-code-headless/
- https://hidekazu-konishi.com/entry/claude_code_cicd_and_headless_automation.html
