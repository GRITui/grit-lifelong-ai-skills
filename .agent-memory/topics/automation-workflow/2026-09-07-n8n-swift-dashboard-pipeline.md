# n8n ⇄ Swift Dashboard Pipeline — Verified Setup (2026-09-07)

QA gate: exit-code verified end-to-end (webhook exec `success`, board round-trip, Chrome-loadable). All commands below were run successfully on this machine.

## Architecture

```
Chrome ──http://127.0.0.1:8787──▶ Swift dashboard-server (NWListener, arm64)
                                    ├─ GET  /*            static (.agent-dashboard/)
                                    ├─ POST /api/refresh   regenerates data.js (scans topics/)
                                    ├─ POST /api/kanban-move  board.json move + regen
                                    └─ GET  /api/health
n8n (control plane, :5678)
  ├─ Schedule 15min ──▶ HTTP → Swift /api/refresh   (autonomous library sync)
  └─ Webhook POST /webhook/kanban-move ──▶ HTTP → Swift /api/kanban-move
Dashboard JS POSTs card moves to /api/kanban-move (same origin — no CORS).
```

- Swift source/binary: `.agent-dashboard/src/` (zero deps, Network.framework)
- n8n workflow `dashboard-updater` id `dShb0ardUpd8r1` (4 nodes, no Code node)
- board.json = kanban source of truth; data.js = generated (`window.DASHBOARD_DATA`)

## Hard-won lessons (all reproduced here)

1. **n8n 2.x task-runner sandbox**: Code node `require('fs')` fails even with `NODE_FUNCTION_ALLOW_BUILTIN` set on the main process env — spawned runner may not see it. Never fight it: do file I/O outside n8n (Swift engine) and drive it via HTTP Request nodes.
2. **ExecuteCommand missing in n8n 2.37.9 is by design** (disabled-by-default in 2.x; `NODES_EXCLUDE` re-enables). Not a broken install.
3. **CLI import gotchas**: `n8n import:workflow` fails with `NOT NULL workflow_entity.id` unless the JSON carries an explicit `id`. Importing `active:true` still leaves the webhook unregistered in the running instance.
4. **webhook_entity rows are written at ACTIVATION time, not at boot** — after DB-level activation + restart the production webhook 404s. Fix: insert the row manually (`workflowId, webhookPath, method, node, webhookId, pathLength`) then restart.
5. **CLI/DB-activated workflow can still error on exec**: the *published* version (workflow_history / activeVersionId) can be stale vs `workflow_entity.nodes` — plus an orphaned duplicate n8n process holding :5678 cached the old version. Fix: publish new version + point versionId at it; kill orphan PID.
6. **Swift/Network gotchas**: `print(x, flush:)` invalid (use `fflush(stdout)`); `String.substring(from: Int)` invalid; never slice request bodies via `dropFirst(head.count+4)` — split on `range(of: "\r\n\r\n")`; a single `receive()` can miss the body segment (loop until Content-Length satisfied).
7. **data.js key spacing**: JSONSerialization emits `"key" : value` (spaces) — regexes/JSON-path tools must tolerate it.

## Ops commands

```sh
launchctl kickstart -k gui/$(id -u)/com.n8n.local          # restart n8n
nohup .agent-dashboard/src/dashboard-server > .agent-dashboard/src/server.log 2>&1 &
swiftc -O .agent-dashboard/src/dashboard-server.swift -o .agent-dashboard/src/dashboard-server
sqlite3 ~/.n8n/database.sqlite "SELECT id,status FROM execution_entity ORDER BY id DESC LIMIT 3;"
open -a "Google Chrome" http://127.0.0.1:8787/
```

Known-open: Swift server runs via nohup (not launchd) — dies on reboot; candidate: `com.grit.dashboard-server` KeepAlive plist.
