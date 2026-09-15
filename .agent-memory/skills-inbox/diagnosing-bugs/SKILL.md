---
name: diagnosing-bugs
description: Use when something is broken, failing, throwing, or slow and the cause is not obvious: a Swift dashboard build/runtime failure, an n8n workflow misbehaving, a cron or batch-research job not firing or emitting bad output, or a swarm lane erroring. Enforces a red-first feedback loop BEFORE any hypothesising.
sources:
  - /Users/grit/ops/vendor/mattpocock/skills/skills/engineering/diagnosing-bugs/SKILL.md
pairs-with:
  - n8n-troubleshoot
  - qa-gate
---
# audited: PASS 2026-09-10 (S3 PO audit)
# status: S2-draft 2026-09-10

## Prime rules

- Phase 1 IS the skill: build a tight pass/fail loop that goes red on THIS bug before reading code for theories. If caught theorising first, STOP.
- Skip phases only with explicit justification written down.
- Redact every secret in shown output (`<REDACTED>`); build loops against env vars, not hardcoded creds.
- n8n-specific fixes live in n8n-troubleshoot; this skill is the loop discipline beneath it.

## Phase 1: Feedback loop (spend disproportionate effort here)

Loop seam menu for THIS workspace, in order:

| Bug shape | Loop |
|---|---|
| Swift dashboard build/runtime | `swift build && swift run <target>` with a fixture input; assert on the exact wrong output/crash |
| n8n workflow | replay the captured webhook/payload via `curl` against a local test webhook; diff response |
| cron/batch research not firing | one-shot pinned invocation of the same command with same env (`env -i` + sourced env file), check exit + log |
| digest/research output wrong | run the prompt/pipe on a saved input file, diff against a golden snapshot |
| swarm lane erroring | re-run the single failing step command with its env; assert on its exit code |
| timing/flaky | pinned-seed or N-times loop (`for i in {1..100}; do ...`) to raise reproduction rate |

Tighten any loop until: one command, already run once (show redacted invocation+output), red-capable on the user's exact symptom, deterministic (or pinned high repro rate), fast (seconds), agent-runnable.

## Phase 2: Reproduce + minimise

- [ ] Loop shows the USER's failure mode, not a nearby different one
- [ ] Reproduces across multiple runs (or high pinned rate)
- [ ] Exact symptom captured verbatim for later verify
- Then minimise: cut inputs/config/steps ONE at a time, re-run after each cut, keep only load-bearing parts. Done when removing anything else turns it green.

## Phase 3: Hypothesise

- Generate 3-5 ranked hypotheses BEFORE testing any (single-idea anchoring is the failure mode).
- Each must be falsifiable: "If X is the cause, then changing Y makes it disappear / Z makes it worse". No prediction = vibe = discard.
- Show the ranked list to the human as a cheap checkpoint; do not block if they are AFK.

## Phase 4: Instrument

- One variable at a time; each probe maps to one Phase-3 prediction.
- Preference: debugger/REPL inspection > targeted boundary logs > never log-everything-and-grep.
- Tag every debug log `[DEBUG-<4hex>]`; cleanup becomes one grep.
- Perf branch: measure first (baseline timing/profiler/query plan), fix second; logs are usually the wrong tool there.

## Phase 5: Fix + regression test

- Write the regression test BEFORE the fix, but only at a CORRECT seam (one that exercises the real bug pattern as it occurs at the call site).
- No correct seam = that is itself the finding; document it, flag for architecture follow-up.
- Sequence: minimised repro -> failing test -> watch red -> fix -> watch green -> re-run Phase 1 loop on the ORIGINAL scenario.
- Hand the regression test to qa-gate as the permanent check.

## Phase 6: Cleanup checklist

- [ ] Phase-1 loop no longer reproduces (re-run it)
- [ ] Regression test green at correct seam (or seam absence documented)
- [ ] `grep -r "\[DEBUG-"` returns nothing
- [ ] Throwaway harnesses deleted
- [ ] Correct hypothesis recorded in the commit/report so the next debugger learns

## Cannot build a loop

Stop and say so. List attempts. Ask for: (a) access to the reproducing environment, (b) a redacted captured artifact (HAR, log dump, core, screen recording), (c) permission for temporary instrumentation. Never hypothesise without a loop.
