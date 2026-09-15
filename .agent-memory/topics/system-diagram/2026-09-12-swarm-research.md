> ✅ QA-gated by PO 2026-09-12 · spot-check: OTel GenAI semantic conventions define `invoke_agent`/`execute_tool`/`chat` span types ✓

## TL;DR
- A second, distinct diagram category exists beyond static architecture diagrams: **runtime trace visualization** via OpenTelemetry's GenAI semantic conventions — a standardized waterfall/span-tree view of what an agent actually did (model calls, tool calls, MCP round-trips), not what it was designed to do.
- OTel GenAI conventions define concrete span types (`invoke_agent`, `execute_tool`, `chat`) and attributes (`gen_ai.*`, `mcp.*`) that map directly onto a trace-tree diagram — this is closer to a "standard notation" than anything found in the prior A2A/MCP static-diagram research, though the spec itself remains pre-1.0/experimental.
- MCP-specific trace attributes (`mcp.method.name`, `mcp.session.id`) let a single trace nest a client-side tool call span under a server-side execution span across the protocol boundary via W3C Trace Context propagation — giving a concrete way to diagram an MCP round-trip as a waterfall rather than a single arrow.
- A new "agentic C4" pattern has emerged: a Claude-Code-style skill that auto-generates C4-model diagrams (context/container/component/deployment/sequence, via C4-PlantUML) from a repo's actual code, output as a local interactive HTML explorer rather than static images — explicitly scoped as human-review tooling, not a decision-maker.
- Neither new pattern is agent-orchestration-specific by design (OTel GenAI conventions are provider/vendor-neutral observability; C4 is generic software architecture) — both are being adapted to agent systems rather than purpose-built for them, consistent with the prior finding that agentic-system diagramming remains largely improvised on top of general-purpose tools.

## Findings

**What: OpenTelemetry's GenAI semantic conventions (v1.41+, moved to a dedicated repo as of v1.42.0, June 2026) define standardized span types for agent execution: `invoke_agent` (agent reasoning, kind INTERNAL for local / CLIENT for remote), `execute_tool` (tool calls, with `gen_ai.tool.name` required in the span name), and `chat` (LLM calls, with token-usage attributes).**
Why it matters: This is a genuinely standardized (if still experimental/pre-1.0) vocabulary for diagramming an agent's *execution*, distinct from the architecture-layer conventions (MCP/A2A boxes-and-arrows) covered in the prior digest — it gives node/span names a workspace could reuse verbatim when building a runtime trace diagram or dashboard, rather than inventing labels.
Confidence: high (attribute/span names are direct quotes from a fetched source, and the v1.42.0 repo-move detail is corroborated by search-result summaries)

**What: For MCP tool calls specifically, OTel GenAI conventions add `mcp.method.name` (e.g. `tools/call`), `mcp.session.id`, and `jsonrpc.request.id`, so that when both the calling agent and the MCP server propagate W3C Trace Context, the server-side execution span nests under the client-side call span in one unified trace.**
Why it matters: This resolves a gap the prior digest left open — it shows a concrete way to diagram an MCP tool-call not as a single opaque arrow but as a two-part waterfall (client call → server execution) sharing one trace ID, useful if this workspace ever visualizes actual MCP traffic (e.g. dashboard swarm activity) rather than just static architecture.
Confidence: med (single fetched source; mechanism is concrete and quoted, but not cross-verified against a second source)

**What: OTel GenAI conventions distinguish `invoke_agent` (autonomous/adaptive reasoning) from `invoke_workflow` (predetermined path execution) as separate span/operation types.**
Why it matters: Gives a ready-made way to visually or structurally distinguish "the agent decided this" nodes from "this was a scripted step" nodes in a runtime diagram — directly useful for a PO+swarm harness like this repo's, where some steps are deterministic (QA gate commands) and others are agent judgment calls (delegation decisions).
Confidence: med (single source, direct quote)

**What: Major observability vendors (Datadog, Honeycomb, New Relic) already support OTel GenAI conventions, and agent frameworks (LangChain, CrewAI, AutoGen, AG2) emit OTel-compliant spans natively or via instrumentation packages as of early 2026.**
Why it matters: Confirms this isn't a theoretical spec — there's an existing tooling ecosystem that would render a compliant trace as a waterfall/flame-graph automatically, meaning a workspace wanting runtime visualization doesn't need to build a renderer, just emit conformant spans.
Confidence: med (search-result synthesis, not independently verified against each vendor's own docs)

**What: A "C4-architecture" agentic skill (for Claude Code and similar tools) auto-generates C4-model diagrams (System Context, Container, Component, Deployment, plus Dynamic/sequence views) from a repository's actual code using C4-PlantUML, outputting a local interactive HTML explorer (not static images) that bundles all views together with project summaries, timestamps, and commit-hash traceability.**
Why it matters: This is a distinct, more mature pattern than the Excalidraw self-validation skill in the prior digest — it targets a well-established, pre-existing notation (C4, invented by Simon Brown, adopted at organizations like Capital One and UK GDS) rather than an ad-hoc convention, and produces a browsable multi-view artifact rather than a single image, which may suit a multi-service repo like this one better than a single diagram file.
Confidence: high (direct quotes from fetched source describing purpose, output format, and scope)

**What: The C4-architecture skill is explicitly scoped as review tooling — "it does not make architectural decisions, it helps humans inspect them" — and every generated diagram carries traceability metadata (generation timestamp, commit hash) plus an explicit warning that the diagrams require human validation before being trusted.**
Why it matters: This is a directly reusable QA-gate pattern for this repo's own diagram outputs (if any get automated): stamp every generated diagram with the commit/timestamp it was generated from, and treat auto-generated diagrams as unverified until a human (or a render-and-inspect step, per the prior digest's Excalidraw finding) confirms them — consistent with this repo's "gate passes only on exit code 0, never on intent" philosophy extended to diagrams.
Confidence: high (direct quote)

## For This Workspace
- If the dashboard (`.agent-dashboard/`) or harness ever needs to visualize actual swarm/PO execution (not just static architecture), adopt OTel GenAI span naming (`invoke_agent`, `execute_tool`, `chat`, plus `mcp.*` attributes for any MCP calls) rather than inventing custom event names — this gives a path to reuse existing OTel-compatible viewers instead of building a bespoke trace renderer.
- Use the `invoke_agent` vs `invoke_workflow` distinction as a labeling convention for any future execution diagram of the PO+swarm model: mark deterministic QA-gate steps (`bash -n`, `test -f`, etc.) as workflow/scripted nodes and PO delegation/escalation decisions as agent/reasoning nodes, so a reader can tell at a glance which steps were judgment calls.
- Consider the agentic C4 skill's pattern (repo → auto-generated multi-view HTML explorer, stamped with commit hash + timestamp, explicitly marked "needs human validation") as a template if this repo ever wants an auto-refreshed architecture diagram of the harness itself (PO, swarms, dashboard, memory topics) — it directly satisfies this repo's existing rule that unverified generated artifacts must be flagged, not treated as ground truth.
- When writing this workspace's own diagram legend (as recommended in the prior digest), add a short note distinguishing "architecture diagrams" (static, C4/MCP/A2A-style, hand- or skill-generated) from "execution/trace diagrams" (runtime, OTel-GenAI-span-shaped) — the two categories use different vocabularies and this draft is the first evidence they need to be kept separate rather than merged into one legend.

## Sources
- https://uptrace.dev/blog/opentelemetry-ai-systems
- https://greptime.com/blogs/2026-05-09-opentelemetry-genai-semantic-conventions
- https://veraexmachina.com/tech/opentelemetry-genai-agent-observability-production/
- https://blog.heuel.org/2026/02/an-agentic-skill-for-interactive-c4-architecture-diagrams/
- https://github.com/softaworks/agent-toolkit/blob/main/skills/c4-architecture/README.md
- https://architecturediagram.ai/blog/c4-model-architecture-diagrams
