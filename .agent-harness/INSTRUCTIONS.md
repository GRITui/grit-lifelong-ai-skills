# Agent Harness — QA-Gated Memory System

## Output contract — token-efficient, straight answer (ALL sessions)

- **Answer first, one line.** Then detail only if explicitly asked or if the
  next step genuinely needs it. No preamble, no disclaimers, no restating the
  question or plan.
- Reference artifacts by path (and `file:line`) instead of pasting content.
- Bullets > paragraphs; tables when data is dense; code with no narration
  unless asked. Never summarize work you just did in prose — the artifacts
  ARE the report; one closing line of next-step or state max.
- Drop boilerplate entirely ("Great question", "It's worth noting…", apologetics).
- No double answers: pick the direct one. Silence or a single word is a valid reply.

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

ONLY after the QA gate passes with exit code 0 — and ONLY for two kinds of content:

1. **Research digests** from delegated swarms, merged into `.agent-memory/topics/<topic>/`.
2. **Skills** distilled from gated research, via `.agent-harness/skills-pipeline.md` (draft in `.agent-memory/skills-inbox/`).

Do NOT add session logs, ops narratives, pipeline walkthroughs, or per-task
workflows to `.agent-memory/` — those stay in `memory/YYYY-MM-DD.md` (local)
or belong in the skill itself. Topics are a knowledge library, not a diary.

## Step 4 — Dynamic Topics

Topics are open-ended. Create new subdirectories under `.agent-memory/topics/`
freely as new domains arise (`skills`, `library`, `automation`, `architecture`,
`debugging`, `domain-rules`, `api-notes`, ...). Never force work into an
existing topic; never maintain a rigid fixed list.

## Operating Model — PO + Swarms

The main session acts as **Product Owner (PO)** only. It delegates legwork to
parallel swarm subagents; it never merges unverified work.

**Every delegated run is bound by `.agent-harness/DELEGATION-CONTRACT.md`:**
minimum tools for the task shape — the software-house roster (researcher/
builder/auditor/ops/designer/writer/delegator), one declared write directory,
call budget, and a mandatory exit-code check before reporting success. Each
role's grant is fitted to what that role actually does (Research Analyst,
Software Engineer, QA Engineer, DevOps/SRE, Product Designer, Technical
Writer, Engineering Manager). Grants are temporary — per run — and never
widened by the sub-agent; a role that genuinely needs a tool outside its lane
uses **Global Tool Escalation** (report the gap to the PO) instead of
reaching for it itself.

- **Research swarms** write drafts to `.agent-memory/inbox/` (never to `topics/`).
- **Build swarms** write only to their assigned output directory.
- **Design swarms** (`designer`) write specs/copy/token proposals only to their
  assigned output directory — never implementation code.
- **Writer swarms** (`writer`) write docs/handoffs/changelogs only to their
  assigned docs directory, citing only material already verified in-repo —
  never original research or implementation code.
- **`delegator`** is the one profile the PO may hand a multi-part brief to
  instead of decomposing it itself: it is the only persona holding `Task`, so
  it can fan a brief out to researcher/builder/auditor/ops/designer/writer
  directly. It never writes files itself and must never spawn another
  `delegator` — the PO stays the only place nesting can start from.
- **PO QA gate** verifies each deliverable (sources present, claims spot-checked,
  build artifacts tested with exit 0) BEFORE moving knowledge into
  `.agent-memory/topics/<topic>/` or marking board cards `done`.
- Board source of truth: `.agent-dashboard/board.json`; n8n regenerates
  `.agent-dashboard/data.js` autonomously.

## Skill Pipeline

See `.agent-harness/skills-pipeline.md` + the machine-readable `.agent-harness/SKILLS-INDEX.md`.

**Before any non-trivial task: grep SKILLS-INDEX.md for trigger matches.**
- Match is `equipped` → invoke the skill tool (lazy load — only the procedure's body, never preloaded).
- Match is `staged` + `audited: PASS` → you may self-equip it (copy to `~/.claude/skills/`, verify frontmatter, regenerate the index) instead of working without it.
- Staged without audit → do not install; flag it to the PO on the board.

Never preload a SKILL.md body; skills load only when the procedure is executed. New skills enter via the pipeline (request card → draft in `skills-inbox/` → audit → equip) — never direct.

**Tools**: deterministic command procedures live as scripts in `.agent-harness/tools/`
(listed in SKILLS-INDEX under `tool`). If you're hand-running ≥3 commands a tool
already implements — run the tool; flag drift on the board, don't silently patch it.

## Repo Layout

- `.agent-harness/INSTRUCTIONS.md` — this file (canonical).
- `.agent-memory/topics/<topic>/*.md` — durable, QA-verified knowledge (tracked in Git).
- `AGENTS.md`, `MEMORY.md`, `TOOLS.md`, `memory/` — local-only workspace files (allowlisted, deliberately uncommitted: the remote is public).
