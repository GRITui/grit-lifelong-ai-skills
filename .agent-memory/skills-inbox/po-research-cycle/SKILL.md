---
name: po-research-cycle
description: Use when acting as Product Owner of the agent-harness memory repo — running one batch research cycle (recall board/topics, pick area, delegate ONE research swarm), QA-gating the draft, merging gated output into .agent-memory/topics/, reindexing the dashboard, or moving kanban cards via the dashboard API. Enforces hard rails.
sources:
  - /Users/grit/.agent-harness/INSTRUCTIONS.md
  - /Users/grit/.agent-harness/skills-pipeline.md
  - /Users/grit/ops/batch-prompt.md
---
# audited: PASS 2026-09-10

## Cycle — exactly one topic per batch, then stop

1. Recall: read `.agent-dashboard/board.json`; list `.agent-memory/topics/` and `.agent-memory/inbox/`; grep topics for existing context.
2. Pick ONE area: rotate among ai-vibe-coding, software-development, automation-workflow, system-diagram, studies — the one with the oldest newest-file wins, unless a backlog card names the focus.
3. Delegate ONE research swarm (`researcher` persona — hard-gated per DELEGATION-CONTRACT; fallback: `general` + researcher brief block) with the briefing template below.
4. QA-gate the draft yourself (checklist below). PASS → merge + remove inbox draft. FAIL → leave draft in inbox, prepend `> ❌ REJECTED <reason>`.
5. Reindex the dashboard (see Board / API).
6. Board: move a card ONLY if it exactly matches this cycle's outcome.

## Briefing template (research swarm)

| Block | Content |
|---|---|
| Role | general research subagent for the chosen area — **tools per DELEGATION-CONTRACT `researcher` profile** (WebSearch/WebFetch/Read/Write; write scope = inbox; ≤12 calls) |
| Focus | ONE area; web-search current-year sources; build on topics/ recall; note gaps |
| Method | web search first, then workspace recall; one draft, no topic writes |
| File format | ONE draft to `.agent-memory/inbox/YYYY-MM-DD-<area>-research.md` with `## TL;DR` (≤5 bullets), `## Findings` (5–8, each What / Why it matters / Confidence high\|med\|low), `## For This Workspace` (2–4 concrete items), `## Sources` (URLs, one per line) |
| Quality bar | draft only — never write to topics/; exit-check required before reporting success; every claim traceable to a listed source |

## QA-gate checklist (PASS requires ALL)

- Structure: draft matches the file-format template above, section for section.
- Sources: every claim traceable to a listed source; all listed sources present.
- Spot-check: independently verify ONE load-bearing claim — via `fact-check`, a web search, OR an on-machine hypothesis test (throwaway `/tmp/hypo-<slug>/` script per DELEGATION-CONTRACT; cite `hypo-test: <claim> → exit X, <fact>`). Load-bearing = the merge rationale rests on it.

## Merge format (PASS)

- Copy draft to `.agent-memory/topics/<area>/YYYY-MM-DD-swarm-research.md`.
- Header line directly after the title: `> ✅ QA-gated by PO <date> · spot-check: <claim> ✓`
- Remove the inbox draft — `rm` is allowed ONLY inside `.agent-memory/inbox/`.

## Board / API

- Reindex: `.agent-harness/tools/board refresh` (never edit data.js directly — it is generated).
- Move card: `.agent-harness/tools/board move <cardId> <column>` (board list shows ids/columns)
- `board.json` is the kanban source of truth; `data.js` regenerates from topics/ on refresh.

## Hard rails

- NO git commit or push.
- NO `rm` outside `.agent-memory/inbox/`.
- NO edits to `.agent-harness/`, `.gitignore`, `~/.claude/`, or any launchd/plist file.
- Budget ≤12 research-related tool calls total per batch.
- Finish with ≤10-line report: area picked, merged/rejected, spot-check result, board/library state.

Validate: `test -f .agent-harness/INSTRUCTIONS.md` — exit 0 = harness present; nonzero = not at repo root, do not run the cycle.
