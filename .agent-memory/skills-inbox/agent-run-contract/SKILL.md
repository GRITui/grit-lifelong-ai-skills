---
name: agent-run-contract
description: Use when orchestrating headless agent runs (cron, batch, AFK loops) — designing completion signals, structured-output tags, iteration/timeout policy, or prompt files with dynamic context for unattended `claude -p`-style invocations. Turns "run and hope" into a contract a harness can verify.
sources:
  - /Users/grit/ops/vendor/mattpocock/sandcastle/README.md
  - /Users/grit/ops/vendor/mattpocock/sandcastle/src/Orchestrator.ts
  - /Users/grit/ops/vendor/mattpocock/sandcastle/src/extractStructuredOutput.ts
---
# audited: PASS 2026-09-10 (S3 PO audit)

# Agent-run contract

Distilled from sandcastle (agent orchestration library), adapted to this workspace's
headless `claude -p` / cron pattern. An unattended run needs a CONTRACT, not a prompt:
how it ends, what it returns, and when to give up.

## Prime rule

- An unattended run is well-formed only when it has: exactly one prompt source,
  a documented completion signal, explicit iteration and timeout policy, and a
  machine-checkable result. Anything less is a fire-and-forget gamble.

## 1. One prompt source, one shape

- Exactly one of: inline prompt OR prompt file — never both (ambiguity = error).
- Prompt file is the default for cron/batch: it is diffable, reusable, and supports
  substitution. Inline strings are for one-off interactive use.
- Convention: keep run prompts under `<workdir>/<name>/prompt.md` next to the run's
  other artifacts (logs, results) so a run is a self-contained folder.

## 2. Dynamic context in prompt files

Two mechanisms, in this order of execution:

1. `{{KEY}}` placeholders — substituted on the host from a key/value map BEFORE any
   command expansion. A placeholder with no matching arg = hard error; an unused arg
   = warning. Never hand user-authored text through substitution expecting it to run.
2. `` !`command` `` blocks — replaced by the command's stdout, all blocks run in
   parallel; any non-zero exit fails the run immediately. Use for pulling in repo /
   tracker state (`git log --oneline -5`, issue bodies).

- Safety property worth keeping: `` !`…` `` patterns arriving INSIDE an arg value are
  inert text, not executed. Pass untrusted content (issue titles, web excerpts) via
  `{{KEY}}` args, never by string-building them into the prompt body.
- Built-ins worth mimicking: inject source/target context (e.g. `{{BASE_BRANCH}}`,
  run ID, date) automatically; forbid the caller from overriding them.

## 3. Completion signals (the loop)

- The agent emits a literal marker to end the run early — sandcastle default:
  `<promise>COMPLETE</promise>`. The engine never injects it; the PROMPT documents
  the convention and the agent obeys it.
- Accept a list of signals and stop on the first match (e.g. `TASK_COMPLETE` /
  `TASK_ABORTED`) — then branch on WHICH signal fired instead of just "it ended".
- The matched signal must be returned in the result. `undefined` = never fired =
  the run exhausted its iterations without declaring an outcome → treat as failure,
  not success.

## 4. Two timeouts, two different phases

- **Idle timeout** (before any signal seen; default 10 min, resets on every output
  event): genuinely stuck agent → FAIL the run. This is the watchdog.
- **Completion grace** (after the signal is seen but the process lingers — typically
  a spawned `gh`/git child or MCP server keeping stdout open; default 60 s, resets
  on each new line): resolve as SUCCESS with a warning, keeping commits/output
  already produced. Healthy runs exit before it matters.
- Keep them separate: collapsing both into one timeout throws away finished work on
  hanging-process runs, and keeping only the grace window lets stuck agents hang
  forever.
- Workspace note: cron `claude -p` runs have no TTY — wrap with `timeout`-style
  limits at the cron layer AND the in-prompt idle policy at the agent layer.

## 5. Structured output (machine-consumed results)

- For runs whose output feeds another process, have the agent emit its answer inside
  an XML tag (`<result>…</result>`) described in the prompt, then parse + validate
  that tag against a schema. Returns a typed payload instead of prose to regex.
- Constraints that make it reliable: single-iteration runs only; the tag literal must
  appear in the resolved prompt; extraction/validation failure is a distinct,
  catchable error carrying the tag, raw match, and session id.
- Retry discipline: on failure, resume the SAME session and feed back a
  token-efficient description of the validation error so the agent re-emits the tag
  without redoing the work. Manual variant: catch, then re-run with
  `resumeSession: <id>` + "your previous output failed: … re-emit inside <tag>".

## 6. Iterations and session reuse

- Default max iterations: 1. Raise only for agentic loops that commit work per
  iteration; the signal (§3) ends the loop early, so a high cap + signal = "as long
  as needed, bounded".
- Long-running/repeated cron work: prefer resuming a prior session over a fresh run
  — cheaper, keeps context. Structured-output retries REQUIRE resumable agents.
- Reusable-environment pattern: for multi-step runs (implement → verify → review),
  keep one warm workspace; gate step 2 on an actual command's exit code between
  agent invocations (`exitCode !== 0 → throw`), not on the agent's claim of success.

## 7. Result contract (what every run returns)

Check these fields, in this order: `completionSignal` (did it declare an outcome?),
artifacts produced (commits/files), `stdout` (combined output for the log), log
file path (per-run, inspectable after the fact). Log mode: file for cron, stdout
only for interactive debugging.

## 8. Pairing in this workspace

- `qa-gate` validates the DELIVERABLE after the run (exit-code gates, independent
  review). This skill defines the RUN itself. A cron job is complete only when both
  pass: contract satisfied AND gate green.
- Headless runs silently no-op unlisted tools — the prompt must state the signal
  convention, output tag, and stop conditions explicitly; nothing is implied.
