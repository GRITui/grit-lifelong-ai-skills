# OpenCode NDJSON event schema — verified digest (T1, retry)

**Pinned version:** @opencode-ai/sdk 1.18.23 + @opencode-ai/plugin 1.18.23
[verified: /Users/grit/.opencode/package.json, /Users/grit/.opencode/node_modules/@opencode-ai/sdk/package.json]
**Primary source (local, authoritative):** OpenAPI-generated SDK types
`/Users/grit/.opencode/node_modules/@opencode-ai/sdk/dist/v2/gen/types.gen.d.ts` (11,653 lines; below: "types", line refs `:N`)
**CLI behavior source:** https://raw.githubusercontent.com/sst/opencode/dev/packages/opencode/src/cli/cmd/run.ts (fetched this run; dev branch may drift from 1.18.23)

## TL;DR

- `opencode run --format json` = "raw event streaming" to stdout; non-interactive mode "streams events to stdout, and exits when the session goes idle." [verified: run.ts file header comment, https://raw.githubusercontent.com/sst/opencode/dev/packages/opencode/src/cli/cmd/run.ts]
- **No** `step_start` / `tool_use` / `step_finish` events exist. Steps and tools are **parts**: the wire event is `message.part.updated`, and `properties.part.type` is `step-start` | `tool` | `step-finish`. [verified: types:4 (Event union), :618, :389-426]
- A second experimental family `session.next.*` exists in the same Event union (per-event, typed properties — no part upserting). [verified: types:4, :634-915]
- Event envelope: `{id, type, properties}`; the SDK SSE stream wraps it as `GlobalEvent {directory, project?, workspace?, payload:{id,type,properties}}`. [verified: types:553-563]
- All timestamps are **epoch milliseconds** (`number`), not ISO strings. [verified: types:622, :383-386, :720, :851]

## Verified fields

### Event type names (exact strings)

| Purpose | Classic (stable baseline) | `session.next.*` (experimental) |
|---|---|---|
| Step start | `message.part.updated` + `part.type:"step-start"` | `session.next.step.started` |
| Tool invocation | `message.part.updated` + `part.type:"tool"`; status in `part.state.status` | `session.next.tool.called` → `.tool.progress` → `.tool.success` / `.tool.failed` |
| Step finish (tokens/cost/timing) | `message.part.updated` + `part.type:"step-finish"` | `session.next.step.ended` |
| Message w/ msg-level tokens+cost | `message.updated` | — |
| Shell command | — (bash tool via `part.type:"tool"`) | `session.next.shell.started` / `.shell.ended` |
| Turn end (run exits) | `session.idle` | — |
| Error | `session.error` | `session.next.step.failed` / `.tool.failed` |

[verified: types — Event union :4; `message.updated` :604; `message.part.updated` :618; `session.next.step.started` :718; `.step.ended` :729; `.step.failed` :750; `.tool.called` :849; `.tool.progress` :866; `.tool.success` :879; `.tool.failed` :898; `.shell.started` :699; `.shell.ended` :709; `session.error` :991; `session.idle` :1225]

### Exact JSON field paths

**`message.part.updated`** → `properties: {sessionID, part, time}` where `time` is ms epoch. [verified: types:618-623]

- **Step-start part:** `part.{id, sessionID, messageID, type:"step-start", snapshot?}` [verified: types:401-407]
- **Tool part:** `part.{id, sessionID, messageID, type:"tool", callID, tool, state, metadata?}` [verified: types:389-400]
  - Tool **name**: `part.tool` (string, e.g. `"bash"`) [verified: types:395]
  - **Status**: `part.state.status` ∈ `pending | running | completed | error` [verified: types:388 (ToolState union)]
  - **Target** (file path / shell command): `part.state.input` — an **untyped record** `{[key: string]: unknown}`; keys are tool-specific (`command` for bash, `filePath` for file tools). [verified: types:339-341 shape; assumed: specific key names `command`/`filePath` are tool-convention, not in generated types]
  - **Timing**: `part.state.time.start` (ms); `part.state.time.end` (ms) present on completed/error states. [verified: types:383-386; assumed: `.start`-only on pending/running per ToolState union shape :337-388]
  - **Result/error**: `part.state.output` (completed), `part.state.error` (error). [verified: types:337-388]
- **Step-finish part:** `part.{id, sessionID, messageID, type:"step-finish", reason, snapshot?, cost, tokens}` [verified: types:408-426]
  - **Tokens**: `part.tokens.{total?, input, output, reasoning, cache.read, cache.write}` — `total` is optional; `reasoning` and `cache` are first-class. [verified: types:416-425]
  - **Cost**: `part.cost` (number, USD). [verified: types:415]
- **`message.updated`** → `properties.{sessionID, info}` where `info` is AssistantMessage: `info.cost` [verified: types:232]; `info.tokens.{total?, input, output, reasoning, cache.read, cache.write}` [verified: types:233-242]; `info.finish?` [verified: types:245]; `info.modelID` / `info.providerID` / `info.agent` [verified: types:223-226]
- **`session.idle`** → `properties.sessionID` (this is the run-exit signal). [verified: types:1225-1228]
- **`session.error`** → `properties.{sessionID?, error?}`. [verified: types:991-995]
- **`session.next.step.ended`** → `properties.{timestamp, sessionID, assistantMessageID, finish, cost, tokens:{input, output, reasoning, cache:{read, write}}, snapshot?, files?}` — note: **no `total`** here. [verified: types:729-747]
- **`session.next.tool.called`** → `properties.{timestamp, sessionID, assistantMessageID, callID, tool, input:{[k]:unknown}, provider:{executed, metadata?}}` [verified: types:849-863]; `.tool.success` adds `outputPaths?: string[]`, `result?` [verified: types:879-895]; `.tool.failed` has `error`, `result?` [verified: types:898-910]

### Minimal realistic NDJSON sample (classic family, GlobalEvent wrapper form)

```ndjson
{"directory":"/Users/grit/proj","project":"proj","payload":{"id":"evt_01","type":"message.part.updated","properties":{"sessionID":"ses_abc","time":1757900000123,"part":{"id":"prt_01","sessionID":"ses_abc","messageID":"msg_01","type":"step-start"}}}}
{"directory":"/Users/grit/proj","project":"proj","payload":{"id":"evt_02","type":"message.part.updated","properties":{"sessionID":"ses_abc","time":1757900001000,"part":{"id":"prt_02","sessionID":"ses_abc","messageID":"msg_01","type":"tool","callID":"call_01","tool":"bash","state":{"status":"running","input":{"command":"ls -la"},"time":{"start":1757900001000}}}}}}
{"directory":"/Users/grit/proj","project":"proj","payload":{"id":"evt_03","type":"message.part.updated","properties":{"sessionID":"ses_abc","time":1757900002789,"part":{"id":"prt_02","sessionID":"ses_abc","messageID":"msg_01","type":"tool","callID":"call_01","tool":"bash","state":{"status":"completed","input":{"command":"ls -la"},"output":"total 8\n...","time":{"start":1757900001000,"end":1757900002500}}}}}}
{"directory":"/Users/grit/proj","project":"proj","payload":{"id":"evt_04","type":"message.part.updated","properties":{"sessionID":"ses_abc","time":1757900004012,"part":{"id":"prt_03","sessionID":"ses_abc","messageID":"msg_01","type":"step-finish","reason":"stop","cost":0.0021,"tokens":{"total":1523,"input":1200,"output":280,"reasoning":43,"cache":{"read":0,"write":0}}}}}}
{"directory":"/Users/grit/proj","project":"proj","payload":{"id":"evt_05","type":"session.idle","properties":{"sessionID":"ses_abc"}}}}
```

Field names all from generated types; **values are illustrative**. [verified: types:389-426, 553-563, 618-623, 1225-1228; assumed: sample values; assumed: wrapper form — see Open risk]

## What contradicts the assumed schema (`step_start` / `tool_use` / `step_finish` with `part.tokens` + `part.cost`)

| Assumption | Reality | Verdict |
|---|---|---|
| Event names `step_start` / `tool_use` / `step_finish` | No such events. Wire events are `message.part.updated` (classic) / `session.next.*` (experimental); `step-start` / `tool` / `step-finish` are **`part.type` values** inside `properties.part` | ❌ [verified: types:4, :618, :401-426] |
| `part.tokens` on the tool event | Tokens exist only on the **step-finish part** (`part.tokens.*`) and on the assistant message (`info.tokens`); `ToolPart` has **no** tokens field | ❌ [verified: types:389-400, :416-425] |
| `part.cost` on the tool event | Cost exists only on the step-finish part (`part.cost`) and the message (`info.cost`) | ❌ [verified: types:389-400, :415, :232] |
| One event per tool call | Classic stream **re-emits the same `part.id`/`callID`** as `state.status` moves pending→running→completed/error; parser must **upsert by `part.id`**. (The `session.next.*` family does emit distinct per-phase events.) | ⚠️ [verified: types:337-388] |
| tokens = input/output/total | Real shape: `{total?, input, output, reasoning, cache:{read, write}}` — `total` optional, `reasoning` + `cache` first-class; `session.next.step.ended` omits `total` entirely | ⚠️ [verified: types:416-425, :736-744] |
| File path / command as first-class fields | They live in `part.state.input`, an untyped record; keys are tool-specific (`command`, `filePath`, …) | ⚠️ [verified: types:339-341; assumed: key names] |
| ISO timestamp strings | All timestamps are **epoch milliseconds** (`properties.time`, `part.state.time.start/end`, `properties.timestamp`) | ❌ [verified: types:622, :383-386, :720] |

## Open risk (builder: confirm at runtime)

- **Stdout line shape — bare `{id,type,properties}` vs GlobalEvent wrapper:** `run.ts` uses `createOpencodeClient` from `@opencode-ai/sdk/v2` and its `event.subscribe()` SSE endpoint returns `GlobalEvent` per types:553-563, so the wrapper form is the leading candidate — but the exact `JSON.stringify` target inside `execute()` was not verifiable this run (run.ts middle section truncated on fetch; `run/execute.ts` is 404 on dev; local binary is minified). **Capture one real `opencode run --format json` line and branch on presence of `payload`.** [assumed: wrapper per types:553-563 + run.ts header "streams events to stdout"]
- `session.next.*` may only emit with the experimental event system enabled; classic `message.part.updated` is the safe baseline. [assumed: not re-verified this run]
- run.ts was read from the `dev` branch; pin behavior against installed binary 1.18.23 if drift matters. [assumed: version skew]

## Sources

- /Users/grit/.opencode/node_modules/@opencode-ai/sdk/dist/v2/gen/types.gen.d.ts (local v1.18.23, OpenAPI-generated — all `types:N` refs)
- /Users/grit/.opencode/package.json, /Users/grit/.opencode/node_modules/@opencode-ai/sdk/package.json (version pins)
- https://raw.githubusercontent.com/sst/opencode/dev/packages/opencode/src/cli/cmd/run.ts (fetched this run: header comment, sdk/v2 import)
- /Users/grit/.opencode/bin/opencode (installed binary, 144MB, minified — grep for format-json code inconclusive)

## Validate

- file exists: `test -f` → PASS (report below)
- non-empty: `wc -c` → PASS (report below)
- contains `## Verified fields` → PASS (report below)
- ≥1 fenced `ndjson` block → PASS (report below)
