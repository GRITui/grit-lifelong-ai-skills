# Local n8n subscription-readiness analysis

- Audited local n8n read-only on 2026-09-08. `GET http://127.0.0.1:5678/healthz` returned HTTP 200 and `{"status":"ok"}`; n8n version was 2.37.9.
- No subscription or middleware workflow/webhook is currently registered. The active webhook inventory contains Telegram, MCP, and `kanban-move` paths only.
- Nine historical `dashboard-updater` webhook executions failed with `Module 'fs' is disallowed` in the old `Update dashboard` node. Later scheduled executions succeeded after the workflow shape changed; avoid filesystem-dependent Code nodes unless the JS task-runner policy is deliberately validated.
- The internal Python task runner reports a missing virtual environment. Treat Python-based export generation as unready until separately provisioned and tested.
- Unrelated noise: 111 historical `Slowlife Pipeline Watchdog` failures and repeated inactive `Grit Vibecode Bridge` activation retries. Do not use these as subscription readiness signals.

Commands that worked:

```sh
curl --max-time 10 -sS -i http://127.0.0.1:5678/healthz
sqlite3 -readonly /Users/grit/.n8n/database.sqlite '.tables'
sqlite3 -readonly -header -column /Users/grit/.n8n/database.sqlite "SELECT workflowId,webhookPath,method,node FROM webhook_entity;"
```

Gotcha: n8n event-log timestamps use a different displayed timezone than the local SQLite execution timestamps; compare the date and execution IDs rather than assuming the printed offsets are identical.
