# Agent Harness — QA-Gated Memory System

Single source of truth for every agent working in this repository.
Claude Code reads `CLAUDE.md`, Cline reads `.clinerules`, opencode reads
`.opencode/instructions.md` — all three are symlinks to this file, so the
harness is identical everywhere by construction.

This repository is an **agent workspace**, not a conventional code project.
Its long-term value is accumulated, verified knowledge.

## Step 1 — Recall

Before starting any non-trivial task:

- Search `.agent-memory/topics/` for existing context:
  - `grep -ri "<keywords>" .agent-memory/topics/`
  - glob `.agent-memory/topics/**/*.md`
- Read and build on what exists; note gaps for Step 3.

## Step 2 — Execute & QA Gate

Do the task, then verify. The gate passes **only on exit code 0** — never on
intent. This repo has no test runner; the gate is built from the primitives
matching what you changed:

| Changed              | Verification                                                                   |
|----------------------|--------------------------------------------------------------------------------|
| Shell script         | `bash -n <script>` (plus `shellcheck <script>` if installed)                    |
| Harness / symlinks   | `test -f CLAUDE.md && test -f .clinerules && test -f .opencode/instructions.md` |
| Memory / markdown    | file exists, non-empty, headers and relative links resolve                      |
| Commit scope         | `git status --short` shows only intended files                                  |

## Step 3 — Write Memory (gated)

ONLY after the QA gate passes with exit code 0:

- Write one focused `.md` file under `.agent-memory/topics/<topic>/`.
- Filenames: kebab-case, dated where useful (e.g. `2026-09-07-deploy-401.md`).
- Record: what was done, what was learned, exact commands that worked, gotchas.
- If the gate failed: fix, re-verify, then write. Never document unverified work.

## Step 4 — Dynamic Topics

Topics are open-ended. Create new subdirectories under `.agent-memory/topics/`
freely as new domains arise (`skills`, `library`, `automation`, `architecture`,
`debugging`, `domain-rules`, `api-notes`, ...). Never force work into an
existing topic; never maintain a rigid fixed list.

## Repo Layout

- `.agent-harness/INSTRUCTIONS.md` — this file (canonical).
- `.agent-memory/topics/<topic>/*.md` — durable, QA-verified knowledge (tracked in Git).
- `AGENTS.md`, `MEMORY.md`, `TOOLS.md`, `memory/` — local-only workspace files (allowlisted, deliberately uncommitted: the remote is public).
