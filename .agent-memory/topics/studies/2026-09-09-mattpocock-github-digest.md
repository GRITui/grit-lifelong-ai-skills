# mattpocock (GitHub) — Work Digest (2026-09-09)

> ✅ QA-gated by PO 2026-09-09 · 8 repos cloned to ops/vendor/mattpocock/ · spot-check: skills=257,748★ via GitHub API (surprisingly real — repo exploded), sandcastle/ts-reset counts match ✓

# mattpocock (GitHub) — Work Digest (2026-09-09)

## TL;DR
- TypeScript educator (Total TypeScript, ex-Vercel/Stately, 44.4k followers) who pivoted hard (2025-2026) into AI-coding engineering: skills, agent orchestration, evals.
- Flagship is **skills** (257.7k stars: disciplined SKILL.md engineering for "real engineering, not vibe coding"); **sandcastle** (7.9k) is a TypeScript library for orchestrating sandboxed coding agents.
- Recurring design obsessions: composable small pieces over monolithic frameworks (he explicitly rejects GSD/BMAD/Spec-Kit), ubiquitous language docs (CONTEXT.md), ADRs, red-green TDD with agents, pre-agreed test seams.
- Everything is dogfooded against his own production repos (course-video-manager is a real Turborepo app whose CLAUDE.md/ADRs show mature agent-workflow discipline).
- Course-promo noise (AI Hero, newsletters) is everywhere; the technique lives in the repos, not the marketing.

## Repository Digest
- **skills** — 257.7k★, MIT, MIT-licensed set of 26 agent skills (Shell/MD) in `engineering/` + `productivity/` buckets; shipped as a Claude Code plugin AND via `npx skills@latest add`. Notable: user-invoked vs model-invoked split (frontmatter `disable-model-invocation` / `policy.allow_implicit_invocation`), `ask-matt` skill as router over the others, promoted-bucket promotion rules enforced in README + plugin manifest, `scripts/link-skills.sh` symlinks into `~/.claude/skills`, docs pages per skill, no-em-dashes prose rule. Uses AGENTS.md-orchestrated repo (buckets, ADRs, router-accuracy rule). Maturity: very high, actively maintained (Sep 2026). Cloned: YES.
- **sandcastle** — 7.9k★, MIT, TypeScript lib (@ai-hero/sandcastle) to run coding agents (claudeCode/codex/opencode/etc.) inside Docker/Podman/Vercel sandboxes with branch strategies, worktrees, iterations, completion signals (`<promise>COMPLETE</promise>`), structured output via Standard Schema + session-resume retries, hooks, `await using` cleanup. Excellent ADR culture (docs/adr/). Templates: simple-loop, sequential-reviewer, parallel-planner. Maturity: high, pre-1.0 with changesets. Cloned: YES.
- **ts-reset** — 8.6k★, MIT: "CSS reset for TypeScript" improving built-in lib types (JSON.parse → unknown, filter(Boolean), includes). Small, surgical d.ts entrypoints pattern (`src/entrypoints` + package exports). Maturity: stable/mature. Cloned: YES.
- **dictionary-of-ai-coding** — 4.3k★: plain-English glossary of AI-coding terms (~140-char descriptions, 200+ word entries, generated README from `dictionary/*.md` + curriculum). Terms like harness, statelessness, prefix cache, attention degradation, grilling. Editorial CLAUDE.md worth stealing (symptom-weaving prose, de-hyped register). Maturity: curated content repo. Cloned: YES.
- **evalite** — 1.7k★, MIT: TypeScript-native LLM evals built on Vitest — `.eval.ts` files with `data()`/task/scorers, SQLite results store, Fastify+React UI with WebSocket live updates, AI SDK tracing. pnpm monorepo (packages/*, apps/evalite-ui). Maturity: active, pre-1.0. Cloned: YES.
- **ai-hero-cli** — 113★, MIT, TypeScript: course-exercise runner CLI; notable for AGENTS.md showing **bd (beads)** issue-tracker integration, non-interactive-shell-command rules (cp -f/mv -f/rm -f to avoid agent hangs), mandatory push workflow. Maturity: niche internal tool. Cloned: YES.
- **agent-rules-books** — 458★ (fork he star-forks), MIT: rule sets distilled from 14 classic engineering books into agents-ready rules in mini/nano/full sizes with a release matrix of line/rule/byte counts. Maturity: content repo, curated. Cloned: YES.
- **course-video-manager** — 724★, TypeScript Turborepo: his own video-publishing production tool (React Router app, Remotion overlays, Drizzle, Hono RPC on Vercel, `cvm` agent CLI over HTTP with schema-version gating). Notable: `packages/core` is filesystem-free enforced by `lint:boundaries`; additive-only migrations applied by hand; deep-module package rule. His showpiece of agent-developed engineering discipline. Maturity: high (dogfood). Cloned: YES.

## Patterns & Takeaways
- **Ubiquitous language doc (CONTEXT.md)** — What: shared domain vocabulary file agents read; language sharpens until "materialization cascade" replaces 20 words. Why: he calls it possibly his single most powerful technique; agent tokens spent on thinking drop, naming stays consistent (README + course-video-manager CONTEXT.md). Confidence: high.
- **User-invoked vs model-invoked skill taxonomy** — What: skills reachable only by human (`/grill-me`) orchestrate; model-invoked skills hold reusable discipline (tdd, code-review); user-invoked never chains to user-invoked. Why: prevents ambiguity about control flow and makes skills composable + auditable. Confidence: high (encoded in his SKILL.md frontmatter).
- **Router skill must never lie** — What: `ask-matt` maps the flow; rule: any add/rename/change means update the router same-time as the skill. Why: a stale router silently misroutes agents. Confidence: high (AGENTS.md).
- **Iteration + completion-signal harness loop** — What: agents run in maxIterations loops, emit `<promise>COMPLETE</promise>`, idle timeout before signal vs grace timeout after; structured output extracted from a tagged stdout with schema + resume-based retries. Why: robust AFK orchestration with typed results from sandboxed runs. Confidence: high.
- **Pre-agreed seams for agent TDD** — What: tests only at public interfaces agreed with the human before any test is written; vertical slices, red before green, anti-pattern list (tautological/implementation-coupled tests). Why: keeps agent testing effort on critical paths; survives refactors. Confidence: high.
- **Structural boundary linting** — What: enforce with tooling that the domain package cannot touch filesystem/child_process/git; deep modules expose only entry points. Why: keeps packages deployable and agent-refactor-safe. Confidence: high.

## For This Workspace
- Adopt the `skills` repo layout for the skills pipeline: bucket folders + README references as promotion gate, `link-skills.sh`-style symlinking into `~/.claude/skills`, and a router skill that must be updated whenever any skill changes — a natural fit for QA-gated .agent-memory/ (source: ops/vendor/mattpocock/skills/).
- Steal sandcastle's orchestration contract for any AFK agent work: explicit branch strategy, completion signals, idle/completion timeouts, and structured output via tagged stdout + schema validation; retrospective ADRs in docs/adr/ to capture design decisions.
- Distill dictionary-of-ai-coding + CONTEXT.md practice into a workspace CONTEXT.md so QA gates and the Swift dashboard share vocabulary with agents; pair with agent-rules-books mini/nano rules for context-budget-aware AGENTS.md.
- Borrow course-video-manager's additive-only, hand-applied migration stance and boundary lint for GRITui data-store changes; evaluate evalite as the eval harness for grit-lifelong-ai-skills quality checks.

## Sources
- https://github.com/mattpocock (profile, repositories tab)
- Cloned repos (read README/AGENTS.md/CLAUDE.md/SKILL.md): skills, sandcastle, ts-reset, dictionary-of-ai-coding, evalite, ai-hero-cli, agent-rules-books, course-video-manager → /Users/grit/ops/vendor/mattpocock/
