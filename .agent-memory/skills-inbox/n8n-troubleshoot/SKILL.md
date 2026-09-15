---
name: n8n-troubleshoot
description: Use when local n8n 2.37.9 (launchd label com.n8n.local, port 5678) misbehaves — Code node require() failures, missing ExecuteCommand node, workflow import/activation errors, production webhooks 404ing, stale published versions, orphaned processes holding :5678, or diagnosing executions in the SQLite DB. Also the safe restart procedure.
sources:
  - /Users/grit/.agent-memory/topics/automation-workflow/2026-09-08-n8n-failure-analysis.md
---
# audited: PASS 2026-09-10

## Task-runner sandbox / node availability

- Code node `require('fs')` fails even with `NODE_FUNCTION_ALLOW_BUILTIN` set on the main process — the spawned runner doesn't see it. NEVER fight the sandbox: do file I/O outside n8n (local Swift engine on :8787) and drive it via HTTP Request nodes.
- ExecuteCommand missing in 2.37.9 is BY DESIGN (disabled-by-default in 2.x). Re-enable only via `NODES_EXCLUDE`, deliberately validated — absence is not a broken install.
- Python task runner reports missing venv — treat Python-based nodes as unready until separately provisioned and tested.

## Import / activation

- `n8n import:workflow` fails `NOT NULL workflow_entity.id` unless the JSON carries an explicit `id` — always include it.
- Importing with `active:true` does NOT register webhooks: `webhook_entity` rows are written at ACTIVATION time, not at boot.
- DB-level activation + restart still 404s the production webhook → insert the row manually (`workflowId, webhookPath, method, node, webhookId, pathLength`), then restart.

## Stale version / port cache

- A CLI/DB-activated workflow can still run a STALE published version: `workflow_history` / `activeVersionId` drifts from `workflow_entity.nodes`.
- An orphaned duplicate n8n process keeps :5678 and caches the old version → kill the orphan PID.
- Fix = publish a NEW version + point activeVersionId at it + kill the orphan PID.

## Ops commands (verified on this machine)

- Restart: `launchctl kickstart -k gui/$(id -u)/com.n8n.local`
- Health: `curl\ -s\ http://localhost:5678/health` (`/healthz` returns `{"status":"ok"}` on 2.37.9)
- Recent executions: `sqlite3 -readonly ~/.n8n/database.sqlite "SELECT id,status FROM execution_entity ORDER BY id DESC LIMIT 3;"`
- Webhook inventory: `sqlite3 -readonly -header -column ~/.n8n/database.sqlite "SELECT workflowId,webhookPath,method,node FROM webhook_entity;"`

## Diagnosis rules

- `execution_entity` / `execution_data` store flattened JSON — resolve string references recursively to reconstruct payloads.
- Compare runs by date + execution IDs, never printed timezones (event-log vs SQLite offsets differ).
- Read-only DB access via `sqlite3 -readonly`; never write to the DB while n8n is live.
- Historical noise (`Module 'fs' is disallowed`, unrelated watchdog failures) is not a signal for current readiness — judge by recent executions of the workflow in question.

Validate: `curl\ -s\ http://localhost:5678/health` — HTTP 200 + `{"status":"ok"}` = n8n reachable; nonzero/connection refused = not running, use the restart command.
