# ai-vibe-coding — Swarm Research (2026-09-07)

> ✅ QA-gated by PO 2026-09-07 · sources verified present · load-bearing claims spot-checked (Spec Kit 1.0 confirmed; n8n 2.x claims validated by live debugging) · merged from swarm inbox

# ai-vibe-coding — Swarm Research Draft (2026-09-07)

## TL;DR
- AGENTS.md is the de facto cross-tool harness standard (60k+ repos, 30+ tools read it natively, stewarded by the Agentic AI Foundation/Linux Foundation) — but empirical data says keep it lean: an arXiv study found context files buy only ~4% task-success at ~20% higher inference cost.
- GitHub Spec Kit hit 1.0.0 (Aug 2026): spec → plan → tasks → implement, agent-agnostic across 30+ agents — the practical "structured vibe coding" workflow of 2026.
- Supervisor pattern is the production default for multi-agent work; swarms/"agent teams" remain experimental. The #1 cited failure mode is trusting agent output without built-in verification.
- Agent Skills (SKILL.md) is now an open standard (~40 platforms, ~100 tokens/skill via progressive disclosure) — but 99% of published skills carry authoring flaws and public registries have had supply-chain incidents.
- "Agentic engineering" (Karpathy, Feb 2026) is displacing raw vibe coding: persistent context files, task decomposition, and automated verification gates are now the baseline discipline.

## Findings

**1. AGENTS.md won the harness-file war, but file bloat measurably hurts.**
- **What:** AGENTS.md crossed 60,000+ repos and is read natively by Claude Code, Codex CLI, Cursor, Copilot, Gemini CLI, Devin, Aider, Windsurf, Amazon Q; governed by AAIF under the Linux Foundation. However, the first empirical study (arXiv 2602.11988) found developer-written context files raised task success only ~4% while raising inference cost ~19–23%, and LLM-generated ones *decreased* success 2–3%.
- **Why it matters:** For a multi-agent workspace sharing one harness file, less is more — HumanLayer keeps CLAUDE.md under ~60 lines, and OpenAI's "Harness Engineering" post recommends AGENTS.md as a table of contents, enforcing rules with linters/hooks instead of prose.
- **Confidence:** high (multiple independent 2026 sources + peer-reviewable arXiv data)

**2. Spec Kit 1.0 makes spec-driven development practical and agent-agnostic.**
- **What:** GitHub Spec Kit reached 1.0.0 (Aug 21, 2026, one-year anniversary). Core loop: `/speckit.constitution` → `.specify` → `.plan` → `.tasks` → `.implement`, with extensions, presets, and a skills-install mode as of 0.11.0 (June 2026). Integrates with 30+ agents. An arXiv paper (2602.00180) taxonomizes SDD rigor as spec-first / spec-anchored / spec-as-source.
- **Why it matters:** It standardizes inputs/checkpoints around whatever agent you already use — useful for repo work where "did we build the right thing?" beats raw prompt speed, and it composes with (not replaces) AGENTS.md.
- **Confidence:** high (official repo + multiple 2026 reviews)

**3. Subagent orchestration: supervisor is the default; verification is the failure point.**
- **What:** 2026 production patterns converge on supervisor/fan-out/aggregator topologies; parallel only for genuinely independent tasks, sequential when output of A feeds B. Claude Code "agent teams" (formerly swarms) stayed experimental. Most-cited failure: an agent reporting COMPLETE with broken tests — build verification steps in explicitly, never as an afterthought.
- **Why it matters:** For QA-gated swarm work, the aggregator pattern (N parallel workers → 1 aggregator that synthesizes) keeps orchestrator context clean and maps directly onto inbox/handshake-file style coordination.
- **Confidence:** high (corroborated across 4+ independent practitioner sources)

**4. Agent memory: split what-you-write from what-the-agent-writes.**
- **What:** Claude Code's emerging convention: CLAUDE.md = deliberate rules you write; auto-memory MEMORY.md = emergent knowledge the agent writes itself (first ~200 lines auto-loaded; needs periodic pruning or it bloats). Subagents can carry scoped memory (`memory: user|project|local`). Compaction triggers ~83% context fill; community consensus is to compact proactively around 60%.
- **Why it matters:** A QA-gated knowledge system like `.agent-memory/` should mirror this split — curated distillation (MEMORY.md-style) vs raw daily logs — and needs explicit pruning instructions or agents create file sprawl.
- **Confidence:** high (Anthropic-documented behavior + practitioner write-ups)

**5. Agent Skills is an open standard — with a quality and security caveat.**
- **What:** SKILL.md format (agentskills.io, AAIF-stewarded, Dec 2025) adopted by ~40 platforms including Claude, OpenAI Codex, Gemini CLI, OpenCode, Cursor; progressive disclosure costs ~100 tokens per skill until triggered. But arXiv 2607.01456 found 99%+ of 238 real-world skills contain at least one "skill smell," 36% carry security flaws, and Snyk documented malicious skills in public registries (ClawHub) in early 2026. SkillsBench: curated skills raise pass rates +16.2pp over none.
- **Why it matters:** Skills (not more harness prose) are the right container for recurring procedures — but vet any third-party skill before it runs with workspace access.
- **Confidence:** high (spec + peer-reviewed studies + vendor security posts)

**6. MCP: standardization won, production hardening is the 2026 story.**
- **What:** Anthropic donated MCP to AAIF (Dec 9, 2025) with ~97M monthly SDK downloads and 10k+ public servers. The 2026 roadmap prioritizes stateless/transport scaling (removing stateful session bottlenecks) and enterprise readiness (audit trails, SSO, gateways); 30+ CVEs were filed Jan–Feb 2026. Security model: consent, credential scope, and per-tool allow-lists live in the *host*, not the protocol.
- **Why it matters:** MCP is the safe default bet for tool integration, but treat each server as untrusted-by-default and scope credentials per agent identity.
- **Confidence:** high (official roadmap + ecosystem reports; specific star/download numbers med — single-source)

**7. Vibe coding quality: QA is the most-neglected layer; gates belong in CI.**
- **What:** An ICSE 2026 systematic review (101 sources) found QA the most overlooked dimension of vibe-coding workflows; a cited Stanford study found developers trusting AI output were ~41% more likely to introduce security vulnerabilities. Recommended pattern: a 5-layer PR gate — lint → type-check → security scan (SAST/deps) → generated-test execution → agentic/behavioral E2E testing — because "the gate must assume the author may not understand the diff."
- **Why it matters:** Human review assumes a careful author; agent-authored PRs break that contract, so automated gates (exactly what a QA-gated memory system already does for content) are the compensating control.
- **Confidence:** high (academic sources + converging practitioner guides)

## For This Workspace
1. **Keep `.agent-harness/INSTRUCTIONS.md` under ~100 lines** and treat it as a table of contents; move recurring procedures (research swarm, QA gate, deploy checks) into SKILL.md-format skills so all three agents (Claude Code, Cline, opencode) load them on demand at ~100 tokens each instead of paying for full prose every session.
2. **Add a dated Decision Log section to the harness** (pattern from 60k-repo analysis): recording "we do X because Y on date Z" stops agents from "helpfully" reverting deliberate choices across sessions.
3. **Formalize the memory split in `.agent-memory/`**: curated distilled files (≤200 lines, QA-gated) vs raw daily notes, plus an explicit "prune/merge, don't hoard" instruction — agents left unguided create dozens of tiny files.
4. **Vet before ingest:** any third-party skill or MCP server (including n8n-adjacent integrations on :5678) gets a grep-audit for `curl|nc|exec|eval` and least-privilege credentials; MCP security lives in the host, so scope per-agent allow-lists deliberately.

## Sources
- https://thepromptshelf.dev/blog/agents-md-best-practices-2026/ — The Prompt Shelf (60k-repo AGENTS.md analysis)
- https://blog.buildbetter.ai/agents-md-complete-guide-for-engineering-teams-in-2026/ — BuildBetter (AGENTS.md tool-compatibility survey)
- https://arxiv.org/html/2602.11988v1 — arXiv (Evaluating AGENTS.md: empirical context-file study)
- https://github.com/dianyike/claude-code-insights/blob/main/claude-md-best-practices.md — claude-code-insights (HumanLayer/OpenAI harness-engineering refs)
- https://github.com/github/spec-kit — GitHub Spec Kit (official repo, 1.0.0)
- https://intuitionlabs.ai/articles/spec-driven-development-spec-kit — IntuitionLabs (SDD guide, arXiv 2602.00180 taxonomy)
- https://vibecoding.app/blog/spec-kit-review — vibecoding.app (Spec Kit 0.11 features, agent support list)
- https://thepromptshelf.dev/blog/claude-code-subagents-best-practices-2026/ — The Prompt Shelf (subagent patterns, aggregator)
- https://www.digitalapplied.com/blog/multi-agent-orchestration-5-patterns-that-work — Digital Applied (5-pattern framework, supervisor default)
- https://www.eesel.ai/blog/claude-code-multiple-agent-systems-complete-2026-guide — eesel AI (agent teams experimental status)
- https://orchestrator.dev/blog/2026-04-06--claude-code-agent-memory-2026/ — orchestrator.dev (memory layers, compaction thresholds)
- https://atlan.com/know/ai-agent/ai-agent-skills/what-are-agent-skills/ — Atlan (SKILL.md adoption, skill-smells study, SkillsBench)
- https://agentskills.io/specification — Agent Skills (official spec)
- https://chatforest.com/guides/mcp-ecosystem-2026-state-of-the-standard/ — ChatForest (AAIF donation, MCP CVEs, protocol landscape)
- https://blog.modelcontextprotocol.io/posts/2026-mcp-roadmap/ — MCP Blog (official 2026 roadmap)
- https://getautonoma.com/blog/quality-gate-vibe-coding — Autonoma (5-layer PR quality gate, ICSE 2026 + Stanford findings)
- https://www.kunalganglani.com/blog/vibe-coding-best-practices-2026 — kunalganglani.com (Karpathy "agentic engineering" shift)
- https://arxiv.org/abs/2606.22413 — arXiv (Forge: formal-method verification loop for vibe-coded code)
