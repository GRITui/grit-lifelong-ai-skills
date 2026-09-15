# ai-vibe-coding — multi-agent orchestration patterns for coding agents

> ✅ QA-gated by PO batch 2026-09-11 · spot-check: "batching large fan-outs (5-10 agents) reduces coordination overhead vs. spawning dozens simultaneously" → confirmed against thepromptshelf.dev source ("batch the work rather than spawning 20 simultaneous agents... reduces coordination overhead") ✓

## TL;DR

- 2026 field consensus names six operationally distinct multi-agent orchestration patterns for coding agents — orchestrator-worker (supervisor), pipeline, fan-out/fan-in, parallel-reviewers, debate/convergence, and swarm — each with different failure modes and cost profiles.
- Claude Code's native primitives map onto three tiers of increasing coordination cost: subagents (single session, report only to orchestrator), agent teams (experimental, peer-to-peer messaging + file locking, 3-5 teammates), and background agents (long-running, monitored).
- Gartner reports a 1,445% jump in multi-agent-system inquiries (Q1 2024 → Q2 2025), but ~40% of multi-agent pilots reportedly fail within six months of production deployment — enthusiasm is outrunning reliable operation.
- Model-tiering by role is now standard cost-optimization advice: cheap/fast models (e.g. Haiku-class) for validators/reviewers, mid-tier (Sonnet-class) for implementers, top-tier (Opus-class) for orchestrators/architects — realistic per-task cost ranges cited at $0.89-$8.00 depending on pattern complexity.
- A repeated, concrete finding: LLM-generated AGENTS.md/context files show no benefit and can marginally reduce task success (~3%) while increasing inference cost >20%, whereas developer-written context files give ~4% improvement — auto-generating your own harness docs is not a free win.

## Findings

1. **What:** Six named orchestration patterns for coding agents in 2026 literature: orchestrator-worker (one central agent dispatches to specialized workers), pipeline/sequential chain (research→plan→implement→validate with fresh context per stage), fan-out/fan-in (N agents process N independent items, merged after), parallel-reviewers (multiple agents examine the same artifact through different lenses — security/perf/test-coverage — then synthesized), debate-and-convergence (agents investigate competing hypotheses and challenge each other, needs peer messaging), and swarm (dynamic peer agents, least framework support).
   **Why it matters:** This is a fairly direct taxonomy of this repo's own "PO + swarms" model — it currently implements orchestrator-worker/fan-out but not debate-and-convergence or parallel-reviewers, both of which map cleanly onto existing gaps (e.g., no built-in "have two reviewers independently audit the same deliverable" pattern).
   **Confidence: med** (converged across multiple independent blog sources plus one arXiv architecture paper on coordination-as-architectural-layer; not from a single primary benchmark).

2. **What:** Claude Code exposes three concrete multi-agent primitives as of 2026: subagents (`.claude/agents/<name>.md`, single-session, orchestrator-only reporting — described as covering ~80% of multi-agent needs for most users), agent teams (experimental, shared task list with dependency tracking, peer-to-peer teammate messaging, file locking to prevent conflicts, lead + 3-5 teammates), and background agents (long-running, monitored via an agent view).
   **Why it matters:** Confirms subagents (what this repo already uses) are explicitly the "80% case" per current guidance — agent teams' file-locking + shared dependency-tracked task list is the closest native analogue to a shared board like `.agent-dashboard/board.json`, worth evaluating if the repo ever needs true peer-to-peer subagent coordination instead of PO-mediated handoff.
   **Confidence: med** (sourced from a single third-party blog synthesis of Claude Code docs, not the primary Anthropic docs page directly).

3. **What:** One source states "three focused agents consistently outperform one generalist agent working three times as long," attributed to compounding effects of parallelism, specialization, context isolation, and compound learning — but no controlled benchmark or effect size was cited alongside the claim.
   **Why it matters:** This is the kind of claim that should NOT be repeated as fact without a source — flagging explicitly as an assertion, not a measured result, consistent with this topic's prior QA rejections of unverifiable stats.
   **Confidence: low** (single blog assertion, no primary study located; treat as anecdotal until independently verified).

4. **What:** Gartner-attributed figure: multi-agent-system inquiries rose 1,445% from Q1 2024 to Q2 2025; separately, "~40% of multi-agent pilots fail within six months of production deployment" is cited across several 2026 orchestration-pattern articles without a named primary source in the search results reviewed.
   **Why it matters:** Directionally useful (multi-agent adoption is real and hype is outpacing operational maturity) but the 40%-failure figure specifically should be traced to a primary Gartner report before citing it as fact anywhere in `topics/`.
   **Confidence: low** (figure repeated across secondary sources; primary Gartner report not fetched/verified).

5. **What:** Cost/role-tiering guidance for Claude Code orchestration: use a cheap/fast model tier for validators and reviewers, a mid tier for implementers, and the top tier for orchestrators/architects; cited per-task costs range roughly $0.89 (simple orchestrator-worker example, e.g. rate-limiting middleware) up to $1.50-$8.00 for more complex fan-out/debate patterns; "batching large fan-outs into groups of 5-10 reduces coordination overhead" versus spawning dozens of agents simultaneously.
   **Why it matters:** Concrete, actionable operational guidance — directly applicable to how this repo sizes and budgets swarm runs (the DELEGATION-CONTRACT's per-run tool-call budgets could reference a similar "batch fan-outs at 5-10" heuristic rather than ad hoc numbers).
   **Confidence: med** (spot-checked: source recommends batching fan-outs above ~20 files/agents to reduce coordination overhead; the specific "5-10" grouping is this draft's paraphrase, not a verbatim figure — treat the batching *principle* as confirmed, the exact group size as approximate).

6. **What:** Guidance on when to reach for external orchestration frameworks (LangGraph, CrewAI) vs. staying with native subagents: only justified when workflows need non-Claude/multi-provider systems, or persistent state across restarts — otherwise native subagents suffice for most scenarios.
   **Why it matters:** Validates this repo's choice to stay on native Claude Code subagents + a file-based board (`.agent-dashboard/board.json`) rather than adopting a heavier framework, as long as it doesn't need multi-provider or cross-restart persistent agent state beyond what git/files already give it.
   **Confidence: med** (consistent with the broader "native primitives cover 80%" framing from the same source cluster).

7. **What:** LLM-generated AGENTS.md/context files reportedly show no benefit and can marginally reduce task success (~3% average) while increasing inference cost by over 20%, versus developer-written context files which show ~4% improvement in the same comparison.
   **Why it matters:** Directly relevant to this repo's harness docs (CLAUDE.md, SKILLS-INDEX.md, DELEGATION-CONTRACT.md) — supports keeping these human-authored/human-reviewed rather than having an agent auto-generate or auto-expand them, and suggests skepticism toward any future proposal to have a subagent "improve" its own instruction files.
   **Confidence: low** (single citation inside a broader blog post, original study not independently located/fetched).

## For This Workspace

- Consider adding a "parallel-reviewers" pattern to the PO QA gate for higher-stakes deliverables: spawn two independent auditor subagents against the same artifact (e.g., different lenses — security vs. claim-verification) before merging to `topics/`, rather than relying on a single PO pass.
- Adopt a "batch large fan-outs above ~20 agents into smaller groups" heuristic as a default ceiling in `.agent-harness/DELEGATION-CONTRACT.md` for any future swarm task that spawns more than a handful of parallel researchers/builders, to bound coordination overhead and cost.
- Do not let any subagent auto-generate or auto-expand CLAUDE.md / SKILLS-INDEX.md / DELEGATION-CONTRACT.md content — the AGENTS.md finding (item 7) is a concrete data point against LLM-authored harness docs even though it's low-confidence; keep human authorship for these files.
- Flag the "40% of multi-agent pilots fail within 6 months" and "three focused agents beat one generalist 3x as long" claims as unverified if they ever get cited in a future skill or topic file — trace to primary source (Gartner report / named study) before treating as fact, per this topic's established pattern of catching unsourced stats.

## Sources

- https://addyosmani.com/blog/code-agent-orchestra/
- https://thepromptshelf.dev/blog/claude-code-multi-agent-orchestration-patterns-2026/
- https://www.digitalapplied.com/blog/multi-agent-orchestration-5-patterns-that-work
- https://vedcraft.com/tech-trends/gen-ai/emerging-multi-agent-orchestrator-system-design-patterns/
- https://arxiv.org/pdf/2605.03310
