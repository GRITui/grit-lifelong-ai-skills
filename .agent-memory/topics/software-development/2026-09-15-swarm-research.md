# Software Development Research — 2026-09-15 (multi-agent orchestration tooling: deterministic routing)

> ✅ QA-gated by PO batch 2026-09-15 · spot-check: microsoft/conductor GitHub repo exists (public, MIT, created 2026-02-02, 433 stars) → verified via `gh api repos/microsoft/conductor` ✓


## TL;DR
- Microsoft released **Conductor** (`microsoft/conductor`), an open-source CLI for defining multi-agent coding workflows in YAML with **deterministic, non-LLM routing** — a direct, shipping instance of the "code controls orchestration, LLMs are payload generators" pattern this repo already commits to.
- VS Code 1.109 was explicitly positioned by Microsoft as "the home for multi-agent development," and Microsoft's `WorkflowBuilder` (compile-time type-safe directed-graph engine) ships sequential/parallel/conditional/handoff patterns as first-class primitives — the named orchestration patterns from prior digests are now landing as product features, not just taxonomy.
- Conductor's routing uses Jinja2 template/expression evaluation with first-match-wins semantics and explicitly avoids putting an LLM in the orchestration loop "to reduce token spending" — validates deterministic-gate-over-LLM-judgment as an emerging industry default, not just this workspace's idiosyncratic choice.
- Conductor ships built-in safety primitives (max-iteration limits, timeout enforcement, human-in-the-loop gates with Markdown-rendered prompts) as first-class YAML config, not bolted-on — this is the "maker-checker iteration cap + fallback" pattern from the 2026-09-14 digest, now a reusable tool rather than something each team reinvents.
- Multi-provider support (GitHub Copilot SDK, Claude/Anthropic Agents SDK, OpenAI, experimental Hermes/NousResearch) in a single orchestration layer signals orchestration frameworks are decoupling from any single vendor's agent runtime, consistent with the broader 2026 MCP/AGENTS.md standardization trend already tracked in this topic.

## Findings

**What:** Microsoft's `conductor` CLI (github.com/microsoft/conductor) lets teams define multi-agent workflows — code review pipelines, research-then-synthesize flows, plan-then-implement loops — in a single version-controlled YAML file, with agents/prompts/routing all declared as data rather than orchestration logic embedded in an LLM's own reasoning.
**Why it matters:** This is a concrete, shipping counter-example to "let the orchestrator LLM decide the next step" designs criticized in prior research (magentic/handoff failure modes: infinite routing loops, context loss via re-summarization). Routing decisions are evaluated by Jinja2 expressions against structured state, not re-derived by an LLM each hop — closer to this repo's board.json + BullMQ-style deterministic state model than to a "manager agent" pattern.
**Confidence:** high (read directly from the GitHub repo README via WebFetch)

**What:** Conductor bundles safety controls as first-class workflow config: max-iteration caps, timeout enforcement, explicit terminal steps with structured success/failure status, and human-in-the-loop gates that render prompts as Markdown for a human decision point mid-workflow.
**Why it matters:** The 2026-09-14 digest flagged "maker-checker needs an explicit iteration cap and fallback rule, currently implicit in most swarm designs" as a gap. Conductor operationalizes exactly that gap as reusable tooling rather than a documentation convention — evidence the industry is moving iteration-cap/fallback logic out of prose instructions and into enforced config.
**Confidence:** high (repo README, corroborated by independent secondary summaries)

**What:** VS Code 1.109 (per Visual Studio Magazine, Feb 2026) was described by Microsoft as "the home for multi-agent development," shipping `WorkflowBuilder`, a compile-time type-safe directed-graph engine supporting sequential, parallel (fan-out), conditional, and handoff patterns natively in the editor.
**Why it matters:** The five orchestration patterns catalogued from Microsoft's Azure Architecture Center taxonomy (already in this topic's digest) are no longer just a naming exercise — they are now IDE-level, typed primitives developers wire up directly, lowering the bar for teams to adopt named patterns instead of ad-hoc agent-calling-agent code.
**Confidence:** med (secondary source; article not fully fetchable, summary via search snippet only — recommend independent verification before citing the exact VS Code version number externally)

**What:** Conductor explicitly supports multiple agent-runtime providers in one workflow definition — GitHub Copilot SDK and OpenAI (stable), Claude/Anthropic Agents SDK (stable), with experimental Claude Agent SDK, Hermes (NousResearch), and Azure Container Apps sandboxed execution as backends.
**Why it matters:** Orchestration-layer/agent-runtime decoupling mirrors the MCP-goes-foundation-neutral and AGENTS.md-goes-cross-vendor trends already tracked in this topic — suggests 2026's consolidation isn't just at the protocol layer (MCP/A2A) but now also at the workflow-orchestration layer, with YAML-as-lingua-franca replacing framework-specific Python DSLs (LangGraph, AutoGen-style).
**Confidence:** med (repo README + one independent secondary source corroborating provider list)

**What:** Industry commentary (Augment Code's "9 Open-Source Agent Orchestrators," Sept 2026) frames the broader 2026 shift as developers moving away from earlier frameworks like AutoGen toward event-driven or explicit-graph orchestration (LlamaIndex Workflows, LangChain's Agent Framework + LangGraph, Microsoft WorkflowBuilder/Conductor) — the common thread being a move toward explicit, inspectable state machines over implicit LLM-driven control flow.
**Why it matters:** Reinforces a consolidating consensus (not just one vendor's opinion) that "LLM decides what happens next" orchestration is being deliberately retired in favor of typed/declarative graphs with LLMs confined to node-level generation — directly validating this workspace's "host infrastructure controls state... LLMs operate strictly as payload generators" framing as directionally correct relative to where the wider industry is converging in September 2026, not just an idiosyncratic local preference.
**Confidence:** low-med (aggregator/roundup source, not independently cross-checked against each named framework's own docs)

## For This Workspace
- Conductor's YAML-workflow model is close enough to this repo's DELEGATION-CONTRACT.md + BullMQ/board.json state design that it's worth a follow-up spike: evaluate whether `microsoft/conductor` (or its routing-expression pattern) could replace or formalize the currently-prose DELEGATION-CONTRACT.md role grants as inspectable, versioned config — same philosophy, less hand-maintained English.
- Adopt Conductor's explicit pattern of **iteration cap + timeout + structured terminal success/failure status as workflow config, not documentation** — this repo's per-run tool budgets and QA-gate exit codes are close, but the cap/timeout/fallback triad isn't yet expressed as a single enforced artifact; worth mirroring that shape in `.agent-harness/DELEGATION-CONTRACT.md` or a small script.
- The human-in-the-loop-gate-with-rendered-Markdown-prompt pattern is a good template for how the PO QA gate could present sub-agent output for review (structured Markdown decision point) rather than free-form chat — low-cost to borrow even without adopting Conductor itself.
- Track VS Code's `WorkflowBuilder` typed-graph primitives as a signal that "board.json + n8n" is one valid implementation of a now-broader industry pattern (declarative multi-agent graphs) — useful context if this repo ever needs to justify its architecture externally, but treat the VS Code 1.109 specifics as unverified pending a primary-source re-check (the article fetch was blocked; only a search-snippet summary was used).

## Sources
https://github.com/microsoft/conductor
https://www.augmentcode.com/tools/open-source-agent-orchestrators
https://visualstudiomagazine.com/articles/2026/02/09/hands-on-with-new-multi-agent-orchestration-in-vs-code.aspx
