# Architecture Overview

Seeded: 2026-09-07 · QA gate: symlink resolution + `git status --short` scope check — exit 0

## What this repo is

`/Users/grit` — a home-directory agent workspace formalized as the public repo
`GRITui/grit-lifelong-ai-skills`. It is **not** a conventional code project:
no root `package.json`, no compile step, no test runner. Its product is
accumulated, QA-verified agent knowledge.

## Stack & tooling detected

- **Platform:** macOS (darwin) / zsh
- **Agents:** Claude Code (`CLAUDE.md`), Cline (`.clinerules`), opencode (`.opencode/instructions.md`) — all symlinks to `.agent-harness/INSTRUCTIONS.md`
- **opencode tooling:** `.opencode/package.json` pins `@opencode-ai/plugin` 1.18.23; `node_modules` is local-only (gitignored)
- **Git:** branch `main`; remote `origin` → `https://github.com/GRITui/grit-lifelong-ai-skills.git`; `gh` CLI authed as `GRITui` (HTTPS, `repo` scope)
- **`.gitignore`:** allowlist style — everything denied by default, only scaffolding trackable (secrets structurally excluded)

## Build commands

None at root — no build system.

## Test entry points (QA gate)

No test runner. Gate primitives (see `.agent-harness/INSTRUCTIONS.md` Step 2):

```sh
bash -n <script>                                     # shell scripts
test -f CLAUDE.md && test -f .clinerules && test -f .opencode/instructions.md
git status --short                                   # commit-scope check
```

## Conventions

- Memory: `.agent-memory/topics/<topic>/*.md` — write only after the QA gate passes (exit 0)
- Topics are dynamic; create new subdirectories freely
- Private files (`MEMORY.md`, `memory/`, `TOOLS.md`, `AGENTS.md`) are allowlisted but deliberately uncommitted — remote is public
