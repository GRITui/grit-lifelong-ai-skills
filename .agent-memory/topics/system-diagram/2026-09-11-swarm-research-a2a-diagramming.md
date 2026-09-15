> ✅ QA-gated by PO batch 2026-09-11 · spot-check: "A2A protocol Linux Foundation governance + four-state task lifecycle (pending/in-progress/completed/failed)" ✓ — independently re-fetched galileo.ai source, exact quote matches

# System Diagram Research: Emerging Tooling & Protocol-Visualization Conventions (Sep 2026 update)

> Builds on `.agent-memory/topics/system-diagram/2026-09-11-swarm-research-diagramming-conventions.md` (covers LangGraph/Mermaid, memory-subsystem diagramming, trust boundaries, MCP edges). This draft focuses on what that digest did NOT cover: agent-to-agent (A2A) protocol visualization, self-validating diagram-generation tooling (Excalidraw skill), and diagram-as-code tool landscape for 2026.

## TL;DR
- Google's A2A (Agent2Agent) protocol is now Linux-Foundation-governed and forms a distinct "horizontal" layer (agent-to-agent coordination) from MCP's "vertical" agent-to-tool layer — diagrams of agentic systems in 2026 increasingly need to show BOTH layers separately, not just one MCP edge type.
- No formal visual notation/legend exists yet for A2A specifically: current published diagrams use ad-hoc layered-stack boxes + directional arrows + text labels ("Agent Card", "stdio/HTTP") rather than a standardized symbol set — the field is still pre-standard here, consistent with the prior digest's finding for agentic diagrams generally.
- A new class of tooling has emerged: AI-agent-facing diagram-generation skills (e.g., an Excalidraw skill for Claude Code) that have the *agent itself* generate a diagram's JSON, render it to an image, visually inspect the render, and iterate — a self-validation loop specifically built for coding agents producing their own architecture diagrams.
- A four-protocol enterprise stack (MCP, A2A, ACP, UCP) is being proposed as the 2026 reference architecture for agent ecosystems, each protocol mapped to a distinct diagram layer (tool access / agent coordination / commerce transactions / model runtime).
- Diagram-as-code tooling (D2, Mermaid, PlantUML) continues to be the dominant format for programmatically generated system diagrams in 2026, valued for text-first, versionable, layout-engine-driven rendering — no agent-specific extensions or built-in AI features were found in any of these languages themselves.

## Findings

**What: A2A (Agent2Agent) protocol, originated by Google (April 2025), has transitioned to Linux Foundation governance ("a fundamental shift from Google proprietary control to vendor-neutral community development under an open governance model") and is the standard for horizontal agent-to-agent coordination, distinct from MCP's vertical agent-to-tool role.**
Why it matters: Diagrams that only show MCP tool-call edges (as the prior digest recommends) are incomplete for multi-agent systems — a full diagram needs a second, visually distinct edge/layer type for inter-agent delegation and coordination (e.g., orchestrator-to-sub-agent handoffs via "Agent Cards").
Confidence: high (multiple independent sources agree on the MCP-vertical / A2A-horizontal framing, and governance detail is a direct quote)

**What: A2A's core diagrammable primitives are the Agent Card — a machine-readable capability descriptor hosted at the standardized well-known URI path `/.well-known/agent.json` (RFC 8615) declaring endpoints, auth schemes, and skills — plus Task, Message, and Artifact objects. Task progression is tracked through states, though sources disagree on granularity: one source describes a simple four-state model ("pending, in-progress, completed, and failed" streamed via Server-Sent Events), while another describes a more granular eight-state model (submitted, working, input_required, auth_required, completed, failed, canceled, rejected).**
Why it matters: Either state model is a ready-made node/state template for drawing an agent-to-agent task-handoff diagram (state machine) — but the discrepancy between sources means this workspace should check the current A2A spec directly before hard-coding a specific state list into a diagram legend.
Confidence: med (Agent Card / well-known URI detail is a direct quote from one fetched source; the task-state granularity is unresolved between two secondary sources, not verified against the primary spec)

**What: Published diagrams of the MCP/A2A/ACP/UCP ecosystem use an ad-hoc layered-stack convention (Commerce Layer → Agent Coordination Layer → Tool Access Layer → AI Model/Agent Runtime) with labeled boxes and directional arrows, but explicitly lack formal diagramming standards (no UML, no flowchart symbol legend, "scope boundaries defined textually rather than symbolically").**
Why it matters: Confirms (independently of the prior digest) that agentic-protocol diagramming is still pre-standardization in 2026 — teams should expect to define their own legend/convention rather than adopt an existing one, and should document that convention alongside the diagram.
Confidence: high (direct quote-level confirmation from source)

**What: A four-protocol reference stack is being proposed for 2026 enterprise agent architectures — MCP (tool access), A2A (agent coordination), and ACP or UCP (commerce/transactions) depending on context, sitting above the AI model/agent runtime layer.**
Why it matters: Gives a candidate "boxes that must appear" checklist specifically for protocol-layer diagrams, complementary to the prior digest's component-vocabulary checklist (orchestrator/tool registry/sub-agents/etc.) — this one is protocol-layer rather than component-layer.
Confidence: med (single source; framed as an emerging/proposed pattern, not an adopted standard)

**What: A new "self-validating diagram generation" pattern exists for AI coding agents: the agent writes a diagram as structured JSON (Excalidraw format), renders it to a PNG via a script, visually reviews its own render, and iterates before delivering — explicitly built for tools like Claude Code to produce their own architecture diagrams.**
Why it matters: This is a concrete, reusable workflow (not just a notation) for how an agent-based workspace like this one could generate verified diagrams autonomously, with the render-and-inspect loop acting as a built-in QA gate rather than relying on a human to check the diagram looks right.
Confidence: med (single blog source, but the mechanism described — JSON to render to visual self-check — is verifiable and concrete, not vague trend language)

**What: The self-validating diagram skill's conventions include semantic color coding (e.g., a fixed color = a fixed meaning like "primary flow" or "warning"), left-to-right/hierarchical layout mirroring conceptual structure, and labeled arrows describing what happens during a transition rather than bare connector lines.**
Why it matters: These are concrete, adoptable micro-conventions independent of the specific tool (Excalidraw) — they could be applied to any diagram output (Mermaid, D2, hand-drawn) generated in this workspace to keep diagrams legible "at a glance."
Confidence: med

**What: Diagram-as-code tools (Mermaid, D2, PlantUML) remain the dominant format for 2026 system-architecture diagramming, but none has built-in AI or agent-specific features — D2's best layout engine, TALA, "requires a paid license"; Mermaid's "layout control is minimal, you cannot pin node positions or fine-tune spacing"; PlantUML's "auto-layout can produce awkward results for complex diagrams." A separate category of natural-language-to-diagram AI tools (e.g., InfraSketch) is emerging as a distinct approach rather than an extension of these code-based tools.**
Why it matters: Confirms that agent-system diagram conventions (MCP-edge, A2A-edge, trust boundary, decision loop) are currently a documentation/legend convention layered on top of generic diagram-as-code primitives, not a first-class language feature anywhere — and that free-tier D2/Mermaid/PlantUML all have real layout limitations worth knowing before picking one for complex multi-agent topologies.
Confidence: high (direct quotes from fetched source on tool limitations)

## For This Workspace
- When diagramming any multi-agent orchestration in this repo (e.g., the PO + swarm model), add a second, visually distinct edge type for A2A-style agent-to-agent delegation (PO → swarm subagent) alongside the existing MCP tool-call edge convention from the prior digest — label it something like "delegation" or "task handoff" to distinguish it from tool calls.
- Model the PO→swarm task handoff as a state machine, starting from a simple four-state model (submitted/pending → working → completed → failed) rather than committing to an unverified eight-state list — the states map cleanly onto how this repo already tracks delegated-run outcomes (QA gate pass/fail, escalation back to PO), and can be extended later if the primary A2A spec is checked directly.
- Since no formal notation exists for either MCP or A2A-style diagrams, write down this workspace's own diagram legend once (e.g., in a `.agent-memory/topics/system-diagram/` conventions file) rather than reinventing per-diagram — cover: tool-call edge, delegation/handoff edge, trust boundary, decision loop, and semantic color meanings (adopt the "fixed color = fixed meaning" rule from the Excalidraw skill finding).
- If this workspace starts generating diagrams via an agent (not hand-drawn), consider the render-then-self-inspect loop pattern (generate diagram source → render to image → visually check → fix) as an explicit QA-gate step for diagram deliverables, consistent with this repo's existing "gate passes only on exit code 0, never on intent" philosophy — a rendered-and-reviewed diagram is closer to verified than an unrendered diagram-as-code file. Note D2's best layout engine (TALA) is paid-license-only, so budget for that or default to dagre/ELK if adopting D2 for complex swarm-topology diagrams.

## Sources
- https://www.digitalapplied.com/blog/ai-agent-protocol-ecosystem-map-2026-mcp-a2a-acp-ucp
- https://atalupadhyay.wordpress.com/2026/03/04/how-to-give-your-ai-coding-agent-a-visual-brain-excalidraw-diagram-skill-for-claude-code/
- https://galileo.ai/blog/google-agent2agent-a2a-protocol-guide
- https://infrasketch.net/blog/best-diagram-as-code-tools-2026
