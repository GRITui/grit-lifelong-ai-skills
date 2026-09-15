> ✅ QA-gated by PO 2026-09-14 · spot-check: Structurizr MCP server (docs.structurizr.com/ai) offers DSL validation/parsing/inspection, latest binary v2026.06.28 ✓

## TL;DR
- Distinct from the prior topic's focus on *live-derived* topology graphs (trace/runtime-based), 2026 has a parallel and maturing track of *code-derived, models-as-code* architecture diagramming — Structurizr, D2, and Mermaid are converging on AI-agent-assisted DSL generation rather than freehand drawing.
- Structurizr ships a dedicated **MCP server** (binary v2026.06.28) offering DSL validation, parsing, and inspection tools so an AI agent can generate/critique a C4 model without violating C4's hierarchical rules (e.g., adding a Component at the Container level).
- D2 (Terrastruct) has three interchangeable layout engines — dagre, ELK, and **TALA** (purpose-built for software architecture) — and is spreading into new surfaces in 2026 (an Inkscape extension, VPasCode editor support as of August 2026), positioning it as "code the diagram, not the drag."
- Mermaid's 2026 releases (Mermaid.js 11.16.0 / Mermaid Studio 2026.3.1) add three new beta diagram types (Cynefin, Railroad, Swimlane) and lean into AI less for "write from scratch" and more for **format conversion** (PlantUML → Mermaid → Structurizr) and **diagram-from-existing-code** generation.
- A caution repeated across Structurizr's own materials: AI-generated architecture diagrams have "common problems" (a named topic at a May 2026 BCS event), reinforcing the prior topic's finding that generated diagrams need independent validation before being treated as fact.

## Findings

**What:** Structurizr's MCP server (binary v2026.06.28, per Structurizr's own AI/MCP docs page) exposes DSL validation, parsing, and inspection tools that flag missing descriptions/technology tags and prevent an AI agent from producing a C4 model that breaks the model's hierarchy (e.g., a Component appearing where a Container should be).
Why it matters: This is a concrete guardrail pattern — instead of trusting an LLM's raw diagram output, the validation step happens against a formal grammar (C4/Structurizr DSL) before rendering, which is a stronger check than the "read it back yourself" validation this repo currently relies on for generated diagrams.
Confidence: high (directly fetched and quoted from docs.structurizr.com/ai)

**What:** Structurizr is explicitly "models as code" (one DSL model → many generated views) as distinct from "diagrams as code" tools like D2/Mermaid/PlantUML that describe one diagram at a time; Structurizr's docs claim its text format is well-suited to LLMs specifically because it's diff-friendly and version-controllable.
Why it matters: For a repo that already version-controls everything (git), a models-as-code approach means one source-of-truth file could generate multiple diagram views (context, container, component) with PR-diffable changes, rather than maintaining several hand-drawn or independently-generated diagram files that can drift out of sync with each other.
Confidence: med (from Structurizr's own docs, which is a vendor source; not independently cross-checked against a neutral comparison)

**What:** D2 (Terrastruct) offers three swappable layout engines — dagre (default, hierarchical), ELK (for node-link diagrams with ports), and TALA (Terrastruct's own engine built specifically for software-architecture-shaped diagrams) — and expanded distribution in 2026 via an Inkscape extension (March 2026) and VPasCode editor support (August 2026).
Why it matters: Layout-engine choice directly affects whether an auto-generated diagram is legible without manual cleanup; TALA being purpose-built for architecture (vs. generic graph layout) is relevant if this repo ever auto-generates a topology diagram from the harness's own state and needs it to render cleanly without hand-tweaking node positions.
Confidence: med (search-result synthesis across multiple blog/tool sources, not independently fetched from Terrastruct's own site)

**What:** Mermaid Studio 2026.3.1 (tracking Mermaid.js 11.16.0) adds three new beta diagram types — Cynefin, Railroad, and Swimlane — plus improved inline documentation and formatting options for architecture diagrams specifically to keep complex diagrams organized.
Why it matters: Swimlane-type diagrams (also flagged in the prior topic's AgenticSwimlanes.com finding) are now landing in mainstream tooling (Mermaid), not just niche BPMN sites — so a PO/swarm handoff diagram (human approval gates, escalation points) could plausibly be authored directly in Mermaid soon rather than requiring a separate BPMN tool.
Confidence: med (search-result synthesis, not independently fetched from mermaidstudio.dev)

**What:** 2026 commentary on AI+diagramming (including a "PlantUML to Mermaid to Structurizr" conversion pattern) states the real value of LLMs in this space is conversion between diagram formats, error debugging of diagram syntax, and generating diagrams from existing code — explicitly downplaying "write an architecture diagram from a prose description" as the weaker use case.
Why it matters: This suggests the highest-value AI-diagram workflow for this repo is pointing an agent at actual harness/dashboard code to emit a diagram, not asking an agent to imagine an architecture from a description — which aligns with this workspace's existing "verify against real state, not intent" principle already applied to code gates.
Confidence: low (aggregated from a single search-synthesis paragraph, sources not independently fetched)

**What:** A May 2026 BCS (British Computer Society) event titled "The C4 model, Structurizr vNext, and AI" is explicitly scoped to cover "common problems with AI-generated software architecture diagrams and how to get better results from your AI agent" if used as a diagram-generation tool.
Why it matters: Even Structurizr's own ecosystem (the C4 model's reference implementation) is treating AI-generated diagrams as failure-prone by default and worth a dedicated public talk — corroborating, from a second independent source, the prior topic's stance that generated diagrams require validation before being trusted as accurate.
Confidence: low (identified via search snippet/event listing only; talk content itself not fetched, so the specific "common problems" are unknown)

## For This Workspace
- If `.agent-dashboard/` or `.agent-harness/` ever needs a maintained architecture diagram (not just the runtime topology graphs from the prior digest), prefer a **models-as-code** approach (Structurizr DSL) over a single hand-authored Mermaid/D2 file — one DSL source can generate multiple views (system context, container, component) that stay consistent with each other and diff cleanly in git, matching this repo's existing all-in-git workflow.
- Before trusting any AI-agent-generated diagram of this repo's own structure (Structurizr, D2, or Mermaid output), run it through a validation step analogous to Structurizr's MCP inspection tools — e.g., check that every node in the diagram maps to a real file/directory/service that actually exists, rather than accepting the LLM's rendering as ground truth. This is the same "gate on exit code, not intent" principle CLAUDE.md already applies to code, extended to diagrams.
- If the Swift dashboard app (`.agent-dashboard/src/dashboard-server.swift`) ever needs to render a PO→swarm handoff/approval-gate diagram, evaluate Mermaid's new Swimlane beta type (2026.3.1) before reaching for a separate BPMN tool like AgenticSwimlanes.com (flagged in the prior digest) — it may now be renderable in the same Mermaid pipeline already used elsewhere in this ecosystem.
- Treat any future "AI, draw our architecture" request as lower-confidence than "AI, generate a diagram from our actual code/config" — per the 2026 commentary, code-to-diagram and format-conversion are the higher-value, more reliable LLM diagram use cases versus prose-to-diagram.

## Sources
- https://docs.structurizr.com/ai
- https://docs.structurizr.com/as-code
- https://structurizr.com/
- https://www.bcs.org/events-calendar/2026/may/the-c4-model-structurizr-vnext-and-ai/
- https://architecturediagram.ai/blog/d2-diagram-language
- https://youvenz.github.io/blog/2026-03-05-d2-inkscape-extension-code-diagrams-inside-inkscape/
- https://updates.visual-paradigm.com/releases/vpascode-d2-diagram-support-announcement/
- https://infrasketch.net/blog/best-diagram-as-code-tools-2026
- https://mermaidstudio.dev/whatsnew/2026-3-1/
- https://markaicode.com/ai-architecture-diagrams-mermaid/
