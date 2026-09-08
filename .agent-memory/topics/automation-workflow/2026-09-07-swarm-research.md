# automation-workflow — Swarm Research (2026-09-07)

> ✅ QA-gated by PO 2026-09-07 · sources verified present · load-bearing claims spot-checked (Spec Kit 1.0 confirmed; n8n 2.x claims validated by live debugging) · merged from swarm inbox

# automation-workflow — Swarm Research Draft (2026-09-07)

## TL;DR
- n8n 2.x enables the task-runner sandbox by default: `NODE_FUNCTION_ALLOW_BUILTIN` must reach the runner process, not just the main n8n process (internal mode inherits main-process env; external mode requires `n8n-task-runners.json` env-overrides).
- `ExecuteCommand`/`LocalFileTrigger` are disabled by default in n8n 2.x — the workspace's "no executeCommand node" is expected 2.x behavior, reversible via `NODES_EXCLUDE`.
- Webhook CORS: set the node's "Allowed Origins (CORS)" option; CORS headers only apply to production URLs on active workflows; Wait-node preflight is still broken (GH #18143).
- launchd beats cron on a Mac that sleeps: missed calendar jobs fire on wake; cron silently drops them. `WatchPaths`/`QueueDirectories` cover event-driven file watching with no extra tooling.
- Agent↔automation: n8n shipped an instance-level MCP server (built in since ~2.18.4, blogged May 2026) plus an MCP Client Tool node that consumes external MCP endpoints — a natural fit for mcpo :8000.

## Findings

1. **n8n 2.x task-runner sandbox + allowlist placement**
   - **What:** n8n 2.0 turns task runners on by default; all Code node JS runs in the runner sandbox. `NODE_FUNCTION_ALLOW_BUILTIN`/`_EXTERNAL` must be visible to the runner: in internal mode the runner is spawned by the main process and inherits its environment (so the launchd plist approach is valid); in external mode the vars belong in `/etc/n8n-task-runners.json` `env-overrides`, and env vars set directly on the runner are ignored (multiple Jan 2026 reports). `N8N_BLOCK_ENV_ACCESS_IN_NODE` now defaults to true and `$evaluateExpression()` no longer works inside Code nodes.
   - **Why it matters:** Upgrades have repeatedly broken allowlist propagation ("Module 'path' is disallowed" threads) and v2.0.x had a Code node "Task request timed out after 60 seconds" regression (GH #23553, closed Feb 2026) — worth knowing when debugging Code nodes on 2.37.9.
   - **Confidence: high**

2. **ExecuteCommand / LocalFileTrigger disabled by default in 2.x**
   - **What:** v2.0 breaking change removes both nodes by default for security; re-enable by setting `NODES_EXCLUDE="[]"` (or removing them from the exclusion list) in the launchd `EnvironmentVariables`.
   - **Why it matters:** Explains the workspace's missing executeCommand node. Since `child_process` is already allowlisted for Code nodes, calling `require('child_process')` there is the lower-blast-radius substitute for shell-outs.
   - **Confidence: high**

3. **Webhook CORS behavior**
   - **What:** Per-webhook "Allowed Origins (CORS)" node option plus env vars (`N8N_CORS_ALLOW_ORIGIN`, `WEBHOOK_CORS_ALLOWED_ORIGINS/METHODS/HEADERS`). Headers only apply to production URLs on active workflows — never test mode. Open bug: Wait-node webhook OPTIONS preflight fails even with correct env (GH #18143; regressed in 1.103, still open Mar 2026); staff guidance is the webhook node does not handle OPTIONS preflight — terminate it at a reverse proxy.
   - **Why it matters:** Any browser page calling local n8n webhooks (open-webui, custom UIs) hits preflight 403s unless origins are configured and the workflow is active.
   - **Confidence: high**

4. **Schedule trigger: per-workflow timezone, cron over interval**
   - **What:** Fire time = workflow Settings > Timezone (IANA name), falling back to `GENERIC_TIMEZONE`; self-hosted default is America/New_York. `GENERIC_TIMEZONE` does not override a timezone already saved in a workflow's JSON. Prefer Custom (Cron) over interval mode: intervals can drift after restarts and have an open firing bug (GH #23943).
   - **Why it matters:** Hardcoded UTC crons drift an hour at each DST boundary and fail silently — the workflow runs, just at the wrong hour.
   - **Confidence: high**

5. **Error workflow pattern**
   - **What:** Dedicated workflow starting with an Error Trigger node; assign per-workflow in Settings > Error Workflow (one handler serves many workflows). Layered practice: node-level Retry on Fail → Continue on Error for non-critical branches → global error workflow for the rest, logging to a sheet/DB plus alerting. The Error Trigger only fires for published/active workflows — it cannot be exercised via editor "Execute".
   - **Why it matters:** Self-hosted n8n has no built-in failure notification; silent failure is the default state.
   - **Confidence: high**

6. **macOS substrate: launchd over cron + event-driven file watching**
   - **What:** cron skips jobs whose time passes while the Mac sleeps; launchd `StartCalendarInterval` coalesces and fires one catch-up run on wake. For long-running services (n8n) `KeepAlive=true` is correct; launchd jobs get a minimal environment so `EnvironmentVariables` in the plist is mandatory (already done); test with `launchctl kickstart gui/$(id -u)/<label>` and `plutil -lint`. File events: `WatchPaths` fires on any modification; `QueueDirectories` re-fires until the directory drains (better for drop-folder processing); `fswatch` (FSEvents, brew-installable) for dev-style watchers (`fswatch -o path | xargs -n1 -I{} cmd`).
   - **Why it matters:** The same launchd config hosting n8n can host watchers, and wake catch-up protects overnight jobs on a Mac that sleeps.
   - **Confidence: high**

7. **CLI/API activation flakiness is real, with a documented workaround**
   - **What:** Longstanding behavior (GH #4701, closed not-planned): CLI imports don't register triggers in the running instance; GH #21770 (2025): importing with `active:false` doesn't stop executions until restart. In 2026, GH #34038 reported the activate API returning 200 while the webhook stayed unregistered in-memory; the reporter's follow-up blamed legacy `{workflowId}/{nodeName}/{path}` `webhook_entity` rows missing `webhookId`, and the reliable fix was deactivate→activate (or restart) to rebuild in-memory state. New official `@n8n/cli` (API-based: `workflow activate/deactivate`, plus `skill install` for Claude Code) now exists alongside the legacy server CLI.
   - **Why it matters:** Confirms the workspace's "CLI activation historically flaky": after any API/CLI activation of webhook workflows, probe the production URL and cycle deactivate→activate on 404 "not registered."
   - **Confidence: high** (workaround), **med** (root-cause detail rests on one reporter's analysis)

8. **Agent↔automation integration via MCP (the 2026 default)**
   - **What:** n8n shipped an instance-level MCP server (blogged May 2026; built in since ~2.18.4 under Settings > MCP, all editions incl. Community): exposed workflows become agent-callable tools, and it can now build/update workflows from chat. Per-workflow alternative: the MCP Server Trigger node (SSE/streamable HTTP, bearer-token auth). Reverse direction: the MCP Client Tool node lets an n8n AI Agent call external MCP servers — e.g., tools exposed by mcpo on :8000. Community `n8n-mcp` (czlonkowski) manages n8n from any MCP client.
   - **Why it matters:** Two clean loops without custom API glue: agent → n8n workflows (as MCP tools), and n8n → agent toolbox (mcpo).
   - **Confidence: high**

## For This Workspace
- **Verify the allowlist reaches the 2.37.9 runner:** run a one-line Code node `require('child_process')`; on "Module disallowed", check `launchctl print gui/$(id -u)/com.n8n.local` for the env var (homebrew native = internal mode, so main-process env should propagate). Set `N8N_RUNNERS_TASK_TIMEOUT` above the 60s default for long Code nodes.
- **Prefer Code node + `child_process` over re-enabling ExecuteCommand**; if a workflow truly needs the node, add `NODES_EXCLUDE="[]"` to the plist and reload (`launchctl bootout` + `load`).
- **Make activation deterministic:** after CLI/API changes, `POST /api/v1/workflows/{id}/deactivate` → `activate`, then probe the production webhook URL; re-import older workflows lacking `webhookId` to shed legacy prefixed paths. Adopt official `@n8n/cli` over raw curl.
- **Observability:** create one Error Trigger workflow (alert via the existing telegram-bot container), point every workflow's Settings at it, and test by activating a throwaway workflow (manual runs never trigger it). For a dashboard, Homepage (gethomepage) is the safer 2026 pick over Glance — Glance's last commit was 2026-05-30 per a maintenance tracker, though recent reviews remain positive (signal contested).

## Sources
- https://docs.n8n.io/2-0-breaking-changes/ — n8n Docs
- https://docs.n8n.io/deploy/host-n8n/configure-n8n/basic-configuration/use-environment-variables/task-runners — n8n Docs
- https://docs.n8n.io/deploy/host-n8n/configure-n8n/basic-configuration/configuration-examples/enable-modules-in-code-node — n8n Docs
- https://github.com/n8n-io/n8n/issues/23553 — GitHub
- https://community.n8n.io/t/external-task-runner-ignores-module-allowlist-in-code-node/190145 — n8n Community
- https://corsproxy.io/blog/fix-n8n-cors-errors/ — corsproxy.io blog
- https://github.com/n8n-io/n8n/issues/18143 — GitHub
- https://community.n8n.io/t/how-to-handle-preflight-options-request-on-a-webhook/65387 — n8n Community
- https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.scheduletrigger — n8n Docs
- https://techpotions.com/lab/n8n-schedule-trigger-timezone-daylight-saving — techpotions
- https://stacksheriff.com/automation/n8n-schedule-trigger-tutorial — StackSheriff
- https://docs.n8n.io/build/flow-logic/handle-errors-gracefully — n8n Docs
- https://community.n8n.io/t/how-to-set-up-an-error-workflow-in-n8n-before-production-fails/293914 — n8n Community
- https://nextgrowth.ai/n8n-workflow-error-alerts-guide — NextGrowth
- https://srmdn.com/blog/launchd-vs-cron-macos — srmdn.com
- https://konadu.dev/launchd-vs-cron-macos-laptop-automation — konadu.dev
- https://gist.github.com/possibilities/14200eb9dcf164f96eec8b628ded542e — GitHub gist
- https://devops.sarmento.org/en/posts/monitoring-files-and-folders-with-launchd-watchpaths-in-practice — /var/log/janio
- https://github.com/emcrisostomo/fswatch — GitHub
- https://github.com/n8n-io/n8n/issues/34038 — GitHub
- https://github.com/n8n-io/n8n/issues/21770 — GitHub
- https://docs.n8n.io/connect/n8n-cli — n8n Docs
- https://blog.n8n.io/n8n-mcp-server — n8n Blog
- https://fast.io/resources/mcp-server-for-n8n — Fastio
- https://abhijeetbuilts.tech/blog/n8n-mcp-server-ai-agent-tools-2026 — AbhijeetBuilts
- https://ideaproof.io/open-source/vs/glance-vs-homepage-by-gethomepage — IdeaProof
- https://sumguy.com/glance-vs-homepage-vs-dashy/ — SumGuy
- https://codeshrew.github.io/ai-lab-notes/posts/2026-02-08_homepage-dashboards-self-hosters-comparison/ — AI Lab Notes
