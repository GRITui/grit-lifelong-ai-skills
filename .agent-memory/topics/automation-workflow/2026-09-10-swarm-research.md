> ✅ QA-gated by PO batch 2026-09-10 · spot-check: n8n blog.n8n.io/idempotency-api/ recommends execution.id + Idempotency-Key header for outbound retries ✓ (curl exit 0, HTTP 200, page contains both terms)

## TL;DR

- n8n gives three complementary error-handling layers — node-level "Continue on Fail"/"Retry on Fail", a workflow-level "Error Workflow" setting that points every workflow at one shared Error Trigger workflow, and an explicit "Stop and Error" node — use all three rather than duplicating try/catch logic per workflow.
- Built-in HTTP Request node retry ("Max Tries" / "Wait Between Tries") covers most transient network failures; custom Set/If/Wait retry loops are only needed for APIs with unusual backoff or rate-limit semantics.
- A shared Error Trigger workflow only fires on failed *automatic* executions and only on hard execution failures — it does NOT catch manual test runs, pre-request credential/signing failures, or nodes configured with "continue on fail" that swallow an error into `runData` while the execution still shows green.
- For idempotency, n8n's own guidance is to pass `execution.id` (or a delivery/event ID) as an idempotency key on outbound HTTP calls, and to dedup inbound webhooks by checking a delivery ID against a data store before running side effects.
- Monitoring failed executions self-hosted typically means either wiring a shared Error Trigger workflow to Slack/email, or polling the n8n REST API hourly for failed executions and posting a digest; Prometheus/Grafana (`N8N_METRICS=true`) is the heavier-weight option for queue-depth/production-scale monitoring.

## Findings

**What:** n8n exposes three separate error-handling mechanisms: node-level settings ("Continue on Error" / "Retry on Fail"), a dedicated "Error Trigger" node used inside a separate error-handling workflow, and a "Stop and Error" node for deliberately throwing a structured error.
**Why it matters:** These are meant to be composed, not chosen from — retry handles transient node failures, Error Trigger handles centralized alerting/logging across many workflows, Stop and Error handles intentional business-rule failures. Centralizing on one shared Error Trigger workflow (rather than copy-pasting a Slack-notify branch into every workflow) avoids logic duplication as the instance grows.
**Confidence: med** (corroborated by multiple 2026 blog writeups; I could not load the official docs.n8n.io error-handling page directly — it 404'd on fetch — so this is not confirmed against first-party docs in this session.)

**What:** Any workflow can be pointed at a single shared "error workflow" via a workflow-level setting, and that shared workflow starts with an Error Trigger node that receives details of the failed execution (which workflow, which node, the error).
**Why it matters:** This is the mechanism that avoids per-workflow duplication — you build the Slack/email notification logic once in the error-handling workflow and every other workflow just references it in its settings.
**Confidence: med** (multiple independent secondary sources agree; not verified against a first-party docs page in this session).

**What:** The Error Trigger / shared error workflow only fires on failures during *automatic* executions of a workflow that failed outright — a manual test run in the editor will not trigger it. Separately, a node configured with "continue on fail" (onError: continueRegularOutput) completes and marks the execution as successful (green) even though the actual error is captured inside that node's `runData` — so execution-status-only monitoring misses these silent failures.
**Why it matters:** Directly relevant to any reliability design: if a node's error is deliberately swallowed to keep a workflow running, you need to explicitly check node-level result data (not just top-level execution status) if you want alerting to catch it. Likewise, testing a fix by manually running a workflow will never exercise the error-alerting path.
**Confidence: med** (sourced from an n8n community forum post describing real production debugging; forum posts are user-reported, not officially documented behavior, so treat exact field name `onError`/`continueRegularOutput` as indicative rather than guaranteed-exact API).

**What:** The HTTP Request node has built-in retry settings (commonly described as "Retry on Fail" / "Max Tries" and a wait-between-tries interval) that can absorb most transient failures (network blips, momentary 5xx) without custom logic; custom retry loops built from Set/If/Wait nodes are reserved for APIs needing non-standard backoff, jitter, or conditional retry (e.g., retry only on specific status codes).
**Why it matters:** Confirms the built-in setting should be the default choice for the workspace's dashboard-refresh and kanban-move workflows, saving custom node wiring for cases the built-in retry can't express.
**Confidence: med** (consistent across several 2026 sources; exact field labels may differ slightly by n8n version — verify in the actual node UI before relying on a specific label).

**What:** For idempotent/retry-safe design, n8n's own blog recommends (a) attaching an idempotency key — commonly the workflow's `execution.id`, or a deterministic hash of the payload — as a header (e.g. `Idempotency-Key`) on outbound HTTP Request calls so a retried execution doesn't create duplicate side effects on the receiving API, and (b) for inbound webhooks, extracting the provider's delivery/event ID early and checking it against a durable store (n8n's Data Table node, or an external DB) before any side-effect node runs, aborting the run if that ID was already processed.
**Why it matters:** This is the recommended pattern for making retries safe by construction rather than relying on "hope the downstream API is idempotent" — directly applicable to any workflow that calls an external API or receives webhooks and might be retried by n8n's own retry-on-fail or by an upstream provider's redelivery.
**Confidence: high** (sourced directly from n8n's own blog, blog.n8n.io/idempotency-api/, fetched this session).

**What:** Self-hosted failed-execution monitoring is commonly implemented one of two ways: (1) route the shared Error Trigger workflow's output to a Slack/email node for real-time per-failure alerts, or (2) run a separate scheduled workflow that polls n8n's own REST API for executions that failed in a recent time window, groups them by workflow, and posts a digest (this catches failures the shared Error Trigger might miss, per the community-forum caveat above, since it inspects execution records directly). Heavier production setups additionally expose Prometheus metrics (referenced via an `N8N_METRICS` environment variable) for dashboards in Grafana.
**Why it matters:** Gives two levels of monitoring effort appropriate to a small self-hosted instance versus a larger production deployment; the REST-API-polling approach is a reasonable middle ground for a low-volume instance since it doesn't require standing up Prometheus/Grafana.
**Confidence: med** (Slack/email-via-Error-Trigger and REST-API-polling patterns corroborated by multiple 2026 sources and an official n8n workflow template listing; the exact `N8N_METRICS` env var name comes from a secondary blog source only and was not verified against first-party n8n docs in this session — treat that specific env var name as unverified/low confidence on its own).

## For This Workspace

- For the dashboard-refresh and kanban-move launchd-managed n8n workflows (port 5678, SQLite), set the workflow-level "error workflow" setting on both to point at one shared error-handling workflow with an Error Trigger node, rather than adding a Slack/email branch inside each — this matches the instance's small scale (two automations) while still avoiding duplicated logic if a third automation is added later.
- Enable the HTTP Request node's built-in retry (Max Tries + wait-between-tries) on any node in these workflows that calls an external service (e.g. the n8n instance's own REST API for regenerating `.agent-dashboard/data.js`, or any webhook the kanban-move workflow posts to) before writing custom retry loops — this covers the common transient-failure case with no extra nodes.
- Because a manually-triggered test run of either workflow will NOT exercise the shared error workflow, don't rely on "I ran it manually and got no alert" as evidence the alerting path works — test failure alerting by forcing an automatic run to fail (or by manually running the error workflow itself with sample input).
- If either workflow is later changed to accept external input (e.g. a webhook triggering the kanban-move automation), apply the idempotency-key pattern from n8n's own blog: use the triggering event's ID (or n8n's `execution.id`) to dedup before writing to the board JSON, since a redelivered/retried trigger should not double-move a card.

## Sources
- https://blog.n8n.io/idempotency-api/
- https://community.n8n.io/t/the-n8n-failures-your-error-workflow-will-never-catch/307316
- https://n8n.io/workflows/7076-automated-hourly-n8n-error-monitoring-with-slack-notifications/
- https://community.n8n.io/t/notification-on-workflow-execution-failure/248754
- https://rajsuyash.com/blog/n8n-error-handling-best-practices.html
- https://n8nlab.io/blog/n8n-error-handling-best-practices
- https://www.emilingemarkarlsson.com/blog/n8n-error-trigger-workflow-error-catching/
- https://nextgrowth.ai/n8n-workflow-error-alerts-guide/
- https://medium.com/@1nick1patel1/n8n-retries-done-right-no-more-duplicate-side-effects-658b94d22c83
- https://medium.com/@Modexa/idempotent-webhook-retries-in-n8n-without-duplicates-8380273a95a2
