---
name: handoff-brief
description: Use when ending a session so another agent can continue, swapping a swarm lane under a DELEGATION-CONTRACT, or after a hard-gate rejection that demands a fresh context. Compacts the conversation into a handoff brief that references artifacts by path instead of duplicating them. Use script-handoff-brief to spawn the next agent directly instead of saving a file.
sources:
  - /Users/grit/ops/vendor/mattpocock/skills/skills/productivity/handoff/SKILL.md
  - /Users/grit/ops/vendor/mattpocock/skills/skills/in-progress/claude-handoff/SKILL.md
pairs-with:
  - script-handoff-brief (same folder, tool)
  - qa-gate
---
# audited: PASS 2026-09-10 (S3 PO audit)
# status: S2-draft 2026-09-10

## Prime rule

- A handoff brief is a POINTER document, not a dump. Reference artifacts by path/URL; never restate their content.

## When a brief is required

| Trigger | Action |
|---|---|
| Context nearing exhaustion mid-task | Write brief, stop |
| Swarm lane swap under DELEGATION-CONTRACT | Write brief BEFORE releasing the lane |
| Hard-gate rejection needing fresh context | Write brief, cite the gate verdict verbatim |
| Next agent must start immediately in this cwd | Spawn instead: run script-handoff-brief |

## Mode decision

- **Save a brief** (default): next session is unknown, deferred, or human-scheduled.
- **Spawn an agent** (tool): next agent starts NOW in this directory. Run `script-handoff-brief --name "<name>" --file <summary.md>`.
- Both modes consume the SAME summary content. Write the summary once.

## Save location

- Default: OS temp dir (`/var/folders/.../T/opencode/` on this Mac), never inside a git repo (avoids commit-scope noise against qa-gate's allowlist gate).
- Exception: a swarm lane path given by the DELEGATION-CONTRACT overrides temp.
- Filename: `handoff-YYYY-MM-DD-<slug>.md`.

## Summary structure (in this order)

1. **Goal**: one line, what the next session exists to do.
2. **State**: done / in-progress / untouched, as a checklist.
3. **Decisions**: each with its why, one line.
4. **Blockers**: gate verdicts, failed checks, quoted exit codes.
5. **Next actions**: numbered, first one is the entry point.
6. **Suggested skills**: name the Skill-tool calls the next agent should make (e.g. `qa-gate`, `diagnosing-bugs`).
7. **Artifacts referenced**: paths/URLs only.

## Hard rules

- If arguments describe the next session's focus, tailor sections 1, 5, 6 to it; drop sections irrelevant to that focus.
- Redact before writing: tokens, keys, passwords, personal identifiers become `<REDACTED>`. Secrets live in env files the next agent sources, never in the brief.
- Nothing that already lives in a spec, plan, ADR, contract file, commit, or diff gets copied: point to it.
- One screen is the target; if it exceeds ~80 lines, sections 2 and 7 are the usual culprits: collapse them.
