> ✅ QA-gated by PO 2026-09-12 · spot-check: "AGENTS.md used by over 60,000 open-source projects" ✓ (WebFetch of https://agents.md, exit 0, confirms verbatim: "used by over 60k open-source projects")

## TL;DR
- AGENTS.md — the open, tool-agnostic "README for agents" format — has scaled past 60,000 open-source projects and is now natively read by 20+ coding agents/IDEs, and was donated to a new Linux Foundation body (the Agentic AI Foundation) for neutral governance.
- Spec-Driven Development (SDD) — specs-as-source-of-truth, code as a generated/verifiable artifact — is the named 2026 successor to "vibe coding," directly responding to intent-drift failures from underspecified prompts.
- GitHub's own SDD toolkit, Spec Kit, grew from ~90k to ~117k GitHub stars between May and July 2026 and now integrates with 30+ agent tools (Claude Code, Copilot, Cursor, Gemini CLI, Codex CLI, Windsurf, Amp, Roo Code).
- JetBrains' 2026 Developer Ecosystem Survey (May-Jul 2026) puts weekly AI-coding-agent use at 90% of professional developers, with 68% daily; Claude Code leads tool share at 39% global / 47% US, Codex jumped 3%→16% since January 2026, and Copilot fell 29%→21% year-over-year.
- Net signal for this workspace: the industry is converging on exactly the two things `CLAUDE.md`/`.clinerules`/`.opencode/instructions.md` already do (a canonical per-project agent-context file, symlinked across tools) — the new piece worth adopting is the specify→plan→tasks→implement structured workflow underneath, not just the context file itself.

## Findings

**What:** AGENTS.md is an open, markdown-based, tool-agnostic format for giving coding agents project context (build/test commands, code style, testing frameworks, PR guidelines, security notes), distinct from the human-facing README.md. It originated from collaboration among OpenAI Codex, Amp, Google's Jules, Cursor, and Factory, and was donated to the Agentic AI Foundation under the Linux Foundation for neutral stewardship.
**Why it matters:** It's the industry's converged answer to the exact problem this repo's `CLAUDE.md` → `.clinerules` / `.opencode/instructions.md` symlink trio already solves (one canonical agent-context file, read by whichever tool is active) — validates the pattern and gives it a name/spec other tools already understand.
**Confidence:** high (primary spec site, agents.md, fetched directly)

**What:** As of the current 2026 count, AGENTS.md is used by over 60,000 open-source projects (examples cited: Apache Airflow, Temporal SDK, OpenAI's own Codex repo) and is natively supported by 20+ tools including VS Code, GitHub Copilot, Cursor, Zed, Aider, JetBrains Junie, Google Devin, and Jules. It supports nested AGENTS.md files in monorepos, where the closest file to the edited path takes precedence.
**Why it matters:** The nested/closest-file-wins precedence rule is a concrete design detail this workspace doesn't currently use (it has one root-level file symlinked three ways, not per-subdirectory overrides) — worth considering if agent-harness ever needs different instructions for, say, `.agent-memory/` vs a future `apps/` subtree.
**Confidence:** high (primary spec site, agents.md, fetched directly)

**What:** Spec-Driven Development (SDD) is described across multiple 2026 sources as the direct response to three failure modes that emerged once LLM coding agents went mainstream in 2024-2025: intent drift (an underspecified prompt like "add login" lets the model guess and mismatch what the team meant), among others. In SDD, a versioned, structured, executable specification is the source of truth, and code is treated as a generated, re-derivable artifact rather than the primary asset.
**Why it matters:** This directly targets a known weak point in ad-hoc "prompt and hope" delegation — relevant to how this workspace's `.agent-harness/DELEGATION-CONTRACT.md` currently briefs subagents (task description + tool grant), which is closer to prompt-driven than spec-driven.
**Confidence:** med (consistent framing across several 2026 secondary/aggregator sources — dev.to, Devoteam, DevToolLab — not a single primary research paper; no controlled study was located for the underlying claim itself)

**What:** GitHub's own SDD toolkit, Spec Kit (`github/spec-kit`), grew from roughly 90k+ GitHub stars and 8k+ forks in May 2026 to 117k stars by July 3, 2026, and by June 2026 had 30+ tool integrations (Claude Code, GitHub Copilot, Cursor, Gemini CLI, Windsurf, Codex CLI, Amp, Roo Code, and more). It provides a `specify` CLI and slash commands structuring work into specify → plan → tasks → implement phases.
**Why it matters:** Concrete, fast-growing adoption evidence (not just a proposed methodology) for treating specs as the unit of work handed to an agent, rather than a free-text task description — a candidate structural upgrade for how the PO briefs build swarms in this repo.
**Confidence:** med (star-count figures came from secondary aggregator summaries of the GitHub repo, not verified directly against the live repo page at time of writing)

**What:** JetBrains' Developer Ecosystem Survey 2026 (fieldwork May-July 2026) found 90% of professional developers used AI coding agents at work at least weekly, and 68% used them daily. Tool-level shares: Claude Code 39% globally (47% in the US, 31% as primary tool), Codex 16% (up from 3% in January 2026), GitHub Copilot 21% (down from 29% a year prior), Cursor 12%, JetBrains AI 9%, OpenCode 7%, Google Antigravity 6%.
**Why it matters:** Confirms AI-agent-assisted development is now the default mode, not an early-adopter behavior, and shows Copilot's share eroding to Claude Code / Codex — useful market context if this workspace ever needs to justify tool choice or plan for multi-tool AGENTS.md-style compatibility rather than one-tool lock-in.
**Confidence:** med (single named survey, summarized via WebFetch of the JetBrains blog post rather than the raw dataset; numbers are as reported by JetBrains, not independently re-derived)

## For This Workspace
- Formally adopt the AGENTS.md-equivalent "closest-file-wins" nesting rule as a documented option in `.agent-harness/INSTRUCTIONS.md` if agent-harness ever splits into subdirectories needing different agent instructions (e.g. a future `apps/` tree) — currently the repo relies on one root file symlinked three ways, which won't scale to per-subtree overrides.
- Consider naming/aliasing the root `CLAUDE.md` as `AGENTS.md` (or adding a fourth symlink) so any future non-Claude/Cline/opencode tool that natively reads the AGENTS.md open standard picks up the same instructions without a bespoke adapter — low-cost interoperability given 20+ tools already read that filename.
- Evaluate whether `.agent-harness/DELEGATION-CONTRACT.md` briefs should move from free-text task descriptions toward a lightweight spec structure (goal, acceptance criteria, out-of-scope) per the specify→plan→tasks→implement pattern — directly targets the "intent drift" failure mode SDD sources name, and is cheap to test on the next research/build swarm task.
- Track Claude Code's reported 39%/47% market share and Codex's 3%→16% jump as a signal to periodically re-check that skill/tool guidance in `.agent-harness/skills-pipeline.md` isn't silently Claude-Code-only if other agents (Codex, Cursor) are ever invoked against this repo.

## Sources
- https://agents.md
- https://blog.jetbrains.com/research/2026/08/ai-coding-agent-adoption-2026/
- https://dev.to/krlz/spec-driven-development-in-2026-what-it-is-the-tooling-and-how-teams-actually-use-it-2fk2
- https://www.devoteam.com/expert-view/spec-driven-development-2026/
- https://devtoollab.com/blog/spec-driven-development-ai-agents
- https://letsdatascience.com/news/github-open-sources-spec-kit-for-spec-driven-development-1d51a7f7
- https://aitechpartner.blog/2026/07/03/tools-spec-kit-github/
- https://github.com/github/spec-kit
- https://codersera.com/blog/agents-md-complete-guide-2026/
