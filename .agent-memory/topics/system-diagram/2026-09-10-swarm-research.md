# System-diagram research: trace-driven visualization for multi-agent/swarm orchestration

> ✅ QA-gated by PO batch 2026-09-10 · spot-check: Langfuse ships a native graph view for LangGraph traces ✓


## TL;DR
- Prior research (2026-09-09) covered static/code-derived diagram generators (Eraser, Kroki, ER tools); the uncovered gap is **runtime-trace-driven** visualization — diagrams generated live from agent execution, not hand-authored or code-scanned.
- Agent observability platforms (Arize AX/Phoenix, LangSmith, Langfuse, Braintrust) have converged on OpenTelemetry/OpenInference as the common trace schema, with visualization (trajectory graphs, DAGs, span hierarchies) built on top as a standard layer, not a bespoke feature per framework.
- LangGraph + LangSmith show a concrete pattern relevant to swarm/multi-agent workspaces like this one: the "conceptual agent graph" (static topology) is rendered alongside live execution spans, so a viewer sees both "what the pipeline could do" and "what actually ran" in one view.
- Conductor's dashboard (interactive DAG + live streaming + in-browser human-in-the-loop gates) is the closest existing analog to what this repo's `.agent-dashboard/` is manually approximating with `board.json`/`data.js`.
- No mature "OpenTelemetry spans → Mermaid sequence diagram" auto-converter was found as an off-the-shelf tool as of Sep 2026 — this remains a build-it-yourself gap even though Mermaid itself is now positioned as an AI-agent-callable skill (via slash-command "mermaid-diagrams" skill packages).

## Findings

### Trace/observability visualization has standardized on OpenTelemetry+OpenInference as the data layer
- What: Arize AX/Phoenix and similar 2026 observability platforms build agent tracing on OpenTelemetry + OpenInference so the trace schema isn't tied to one orchestration library (LangGraph, AutoGen, CrewAI, etc.); native framework adapters normalize spans/attributes/events into this common schema, with raw OTel instrumentation as fallback.
- Why it matters: If this workspace ever wants to auto-diagram its own swarm runs (PO → subagents → deliverables), OpenTelemetry is the de facto schema to emit from — it decouples "how a diagram is drawn" from "which agent framework produced the trace," matching this topic's established preference for durable, tool-agnostic text formats over per-framework lock-in.
- Confidence: high (consistent across multiple 2026 comparison articles: Arize, Confident AI, Braintrust).

### LangGraph/LangSmith renders static topology + live execution together
- What: LangSmith's graph view (beta) shows the conceptual agent graph (nodes/edges = possible flow) overlaid with the actual execution's spans/generations, making the hierarchy of each span within the graph explicit as it steps through a run.
- Why it matters: This is a distinct visualization pattern from anything in the prior research file (which only covered static diagram generation from prompts/Terraform/DB schemas) — it's specifically for **multi-agent orchestration debugging**, the closest match to what this workspace's PO+swarm model would need if it wanted to visualize a delegation run rather than just document architecture.
- Confidence: med (feature description confirmed via direct fetch of Langfuse's own trace-graph-view changelog page, which describes the *equivalent* Langfuse feature for LangGraph traces; LangSmith's own docs weren't independently fetched, only search-snippet level).

### Langfuse offers the same pattern open-source/self-hostable
- What: Langfuse (MIT-licensed, OpenTelemetry-based) added a native graph view for LangGraph traces that visualizes the agent graph structure directly from trace data, framework-agnostic and self-hostable, stitching distributed traces across agent boundaries.
- Why it matters: Unlike LangSmith (hosted, LangChain-ecosystem-tied) or Arize (enterprise), Langfuse is the self-hostable option — directly relevant given this workspace already prefers self-hosted/OSS tooling (Kroki self-host was flagged in prior research) over SaaS lock-in.
- Confidence: high (direct WebFetch of langfuse.com changelog page confirmed the feature exists and its stated purpose; the fetch explicitly noted the page does NOT document the OTel-to-graph generation mechanism internally, so the "how" remains unverified).

### Orchestration dashboards increasingly ship live interactive DAG views, not static exports
- What: Conductor's web dashboard renders workflows as an interactive DAG with real-time/live streaming updates and in-browser human-approval gates, plus a terminal-UI ("Fleet Manager TUI") for the same data outside a browser.
- Why it matters: This is a concrete precedent for what a "board.json → live DAG" upgrade of this repo's `.agent-dashboard/` could look like — going from a static regenerated `data.js` snapshot to a live-updating graph view, and it validates that a TUI alternative to the web dashboard is a normal pattern, not a niche one.
- Confidence: med (search-snippet-level detail only; Conductor's own docs not independently fetched).

### No off-the-shelf OTel-trace-to-Mermaid converter exists yet
- What: Despite Mermaid now being distributed as an AI-agent-invocable "skill" (slash-command packages for tools like Cursor) and general "AI generates Mermaid from a description" tooling being common, a targeted search for a tool that converts OpenTelemetry agent-execution spans directly into a Mermaid sequence diagram turned up no dedicated, mature project as of Sep 2026.
- Why it matters: This is a genuine gap, not just an unexplored corner — it means any workspace wanting "auto-diagram my last swarm run as a Mermaid sequence diagram" today has to write the OTel→Mermaid translation layer itself (feeding trace JSON to an LLM prompt, or a custom script), rather than reaching for an existing library.
- Confidence: med (absence-of-evidence from one search round is weaker than a positive finding; a deeper GitHub-specific search could still surface something).

### Mermaid is now packaged as a reusable AI-agent "skill," not just a rendering library
- What: Mermaid diagram generation is distributed as an installable agent skill (e.g., "mermaid-diagrams" skill packages referenced for Cursor and similar tool-using agents as of April/Aug 2026 sources), invoked via slash command rather than the agent hand-writing Mermaid syntax from scratch each time.
- Why it matters: This mirrors this workspace's own skill-pipeline model (equip/stage/audit in `.agent-harness/SKILLS-INDEX.md`) — Mermaid-as-a-skill is a directly applicable pattern if this repo wants a vetted, reusable "draw this as Mermaid" procedure instead of ad hoc prompting each time a diagram is needed.
- Confidence: low (search-snippet level only, specific skill package names/publishers not independently verified by direct fetch).

## For This Workspace
- Emit OpenTelemetry-style spans (or a minimal JSON trace log) from PO→swarm delegation runs; even without adopting LangSmith/Langfuse, this gives a durable, tool-agnostic trace format this workspace could later feed to Kroki/Mermaid for auto-generated "what actually ran" diagrams, consistent with the topic's existing text-source-in-git principle.
- Consider a Langfuse self-hosted instance (OSS, OTel-based, MIT license) rather than a hosted SaaS if this workspace wants agent-run trace visualization — it fits the workspace's established self-host-over-SaaS bias (same rationale as choosing self-hosted Kroki over per-tool CLIs in prior research).
- Treat `.agent-dashboard/board.json` + regenerated `data.js` as this workspace's static-snapshot analog to Conductor's live DAG dashboard; a concrete incremental upgrade path is adding a "live" polling/refresh view rather than only regenerating on n8n triggers, since board.json already models tasks as a graph of cards/state.
- If a future task needs "diagram my last swarm run," package the OTel/JSON-trace-to-Mermaid translation as a proper skill draft in `.agent-memory/skills-inbox/` (per the skills-pipeline) rather than ad hoc prompting each time — no mature open-source tool was found to fill this gap directly, so it would be homegrown.

## Sources
https://www.lowcode.agency/blog/how-to-build-an-ai-agent-orchestration-dashboard-for-complex-workflows
https://arize.com/blog/best-ai-observability-tools-for-autonomous-agents-in-2026/
https://www.kimi.com/resources/agent-orchestration-platforms
https://www.confident-ai.com/knowledge-base/compare/best-ai-agent-observability-tools-2026
https://www.braintrust.dev/articles/agent-observability-complete-guide-2026
https://langfuse.com/changelog/2025-02-14-trace-graph-view
https://zylos.ai/research/2026-04-14-graph-based-agent-workflow-orchestration-production/
https://louie-py.readthedocs.io/en/latest/guides/agents/mermaid/
https://ona.com/docs/ona/agents/mermaid-diagrams
https://explainx.ai/skills/hoodini/ai-agents-skills/mermaid-diagrams
https://explainx.ai/skills/softaworks/agent-toolkit/mermaid-diagrams
