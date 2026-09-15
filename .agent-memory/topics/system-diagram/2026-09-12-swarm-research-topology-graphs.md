> ✅ QA-gated by PO 2026-09-12 · spot-check: Langfuse "Agent Graphs" feature ships Aggregated/Expanded modes (per docs + blog, shipped since July 2026) ✓

## TL;DR
- A third diagram category has emerged, distinct from both static architecture diagrams (MCP/A2A, C4) and OTel trace-tree waterfalls: **live-derived agent topology/dependency graphs**, generated directly from a running or executed swarm rather than from source code or spans alone.
- Langfuse shipped a dedicated "Agent Graphs" feature (blog-dated July 13, 2026) with two rendering modes — **Aggregated** (repeated steps collapsed into one node with a run counter, loops drawn as cycles) and **Expanded** ("as it ran," every call its own node, loops unrolled into a DAG) — auto-inferred from trace observation timing/nesting, no manual modeling required.
- A new open-source CLI, **swarm-test** (PyPI `swarm-test`, works across CrewAI/LangGraph/AutoGen/custom orchestrators), renders an actual multi-agent system's dependency graph as an interactive force-directed D3 diagram, visually flags single points of failure (pulsing red), and exports the topology to Mermaid/DOT/PNG — explicitly framed as "diagram from your real topology, not a hand-drawn one, so it stays accurate."
- LaunchDarkly's "agent graphs" overlay live performance metrics (latency, invocation count, tool-call count) directly onto the workflow-graph nodes, merging the "static topology" and "runtime trace" layers into one view rather than keeping them as separate artifact types (a departure from the earlier finding that architecture and execution diagrams use different vocabularies).
- These tools converge on a shared pattern: derive the graph from actual execution data (traces or live agent state), not from a designer's or an LLM's model of the system — closing the "unverified generated diagram" gap the C4-agentic-skill and Excalidraw findings flagged in prior digests, since the diagram's nodes/edges are load-bearing facts rather than a rendering to be separately validated.

## Findings

**What:** Langfuse's "Agent Graphs" feature (docs page live as of this research, blog post dated July 13, 2026) auto-generates a graph visualization for any trace containing non-generation/non-span/non-event observations, with two modes: Aggregated (steps sharing a name merge into one node with a counter like `retrieve_docs (3/3)`, loops as cycles) and Expanded (every call its own node, loops unrolled into a DAG).
Why it matters: This is a concrete, productized instance of turning OTel-GenAI-style trace data (the runtime-trace category from the prior digest) into a topology diagram automatically — closing the gap between "spans exist" and "a human can read the shape of what happened" without hand-building a renderer.
Confidence: high (directly quoted from Langfuse's own docs page and corroborated by a search-result synthesis citing the same July 13, 2026 date; PO spot-check independently re-fetched both the docs page and blog post and confirmed the Aggregated/Expanded mechanism and "since July 2026" ship date)

**What:** Langfuse graphs are generated via two mechanisms — automatic inference from trace observation timing/nesting for any framework, and a native LangGraph integration that displays the framework's own graph structure directly.
Why it matters: Shows two different strategies for the same problem (infer topology from timestamps vs. read topology from the orchestrator's own state) — relevant if this workspace ever wants to visualize PO+swarm delegation, since the harness's dashboard could take either approach depending on whether swarm launches emit structured events or just start/stop timestamps.
Confidence: high (direct quote from Langfuse docs)

**What:** `swarm-test` (open-source, `pip install swarm-test`, GitHub `surajkumar811/swarm-test`) analyzes a real multi-agent system's topology (CrewAI/LangGraph/AutoGen/custom) and renders it as an interactive force-directed D3 graph, marking single points of failure in red, with sortable health/redundancy tables and severity-grouped findings; it exports the topology to Mermaid/DOT/PNG and ships a GitHub Action to gate PRs in CI.
Why it matters: This is the clearest 2026 example in the "auto-generate diagrams from a live agent/swarm system" direction the brief asked about — it's not a static-code-reading tool (like the agentic-C4 skill) nor a pure trace-waterfall (like OTel/Langfuse); it specifically targets swarm topology health and turns diagram output into a CI gate, which maps directly onto this repo's own "gate on exit code, not intent" philosophy.
Confidence: med (based on search-result synthesis of a dev.to post and GitHub repo description, not independently fetched/verified against the repo's README)

**What:** LaunchDarkly's "agent graphs" feature overlays live performance metrics — latency, invocation counts, tool-call counts — directly onto workflow-graph nodes, in the context of the full agent workflow shape.
Why it matters: This merges what the prior digest treated as two separate diagram vocabularies (static architecture vs. OTel-GenAI runtime trace) into a single artifact type; if adopted as a norm, this repo's planned "diagram legend" distinguishing architecture vs. execution diagrams may need a third category — "annotated topology" — rather than a strict two-way split.
Confidence: low (based only on a search-result snippet, not independently fetched from LaunchDarkly's own page)

**What:** Industry surveys as of mid-2026 describe three dominant multi-agent topology patterns in production — supervisor/hierarchical, orchestrator-worker (cited as ~70% of production deployments), and swarm (peer agents, no central control) — as the standard vocabulary diagram tools now organize around.
Why it matters: Gives a naming convention for classifying this repo's own PO+swarm model (which is explicitly hierarchical/orchestrator-worker: PO delegates to swarm subagents, no peer-to-peer swarm behavior) when producing any topology diagram, so the diagram's shape matches an externally recognized pattern name rather than an ad hoc label.
Confidence: low (percentage and pattern-naming come only from an unverified search-result synthesis of a single article; not fetched/cross-checked against a primary source)

**What:** "AgenticSwimlanes.com" positions itself as a vendor-neutral reference for AI agent workflow diagrams using five canonical BPMN 2.0-compliant swimlane shapes, with per-process cited examples, last verified April 2026.
Why it matters: A candidate off-the-shelf notation for depicting human-agent handoffs (e.g., PO approval gates in this repo's delegation model) using an established standard (BPMN) rather than an invented convention — worth checking against this repo's QA-gate/escalation points if a swimlane-style diagram is ever needed.
Confidence: low (identified only via search snippet; page itself not fetched, so shape/claim details are unverified)

## For This Workspace
- If `.agent-dashboard/` ever needs to show *which* subagent called which tool and when (not just a static PO→swarm box diagram), the Langfuse Aggregated/Expanded pattern is a directly copyable UX model: default to a collapsed view with per-step run counters, and offer a drill-down "as it ran" expanded view — this avoids the "40 identical cards" anti-pattern this repo's own CLAUDE.md component rules already warn against.
- `swarm-test`'s pattern of exporting real topology to Mermaid/DOT and gating CI on it is a close match for this repo's own philosophy ("the gate passes only on exit code 0, never on intent") — if the harness ever wants a live-verified swarm topology diagram (vs. the agentic-C4 skill's static-code-derived one), evaluate `swarm-test` rather than building a bespoke exporter, since it already targets CrewAI/LangGraph/AutoGen-style orchestrators.
- Classify this repo's own PO+swarm model explicitly as "orchestrator-worker" (not "swarm" in the peer-agent sense) in any future architecture diagram or legend — the current directory name `.agent-dashboard` and rule vocabulary ("swarm subagents") risks miscommunicating the topology as peer-to-peer to a reader familiar with 2026's three-way taxonomy.
- Before merging any future execution/topology diagram into `.agent-memory/topics/system-diagram/`, note in the QA spot-check whether the diagram was derived from real trace/topology data (Langfuse- or swarm-test-style, verifiable) or from a model/skill's inference (agentic-C4-style, needs human validation per the prior digest) — this distinction is now a first-class fact about the diagram's trustworthiness, not just its notation.

## Sources
- https://langfuse.com/blog/2024-07-ai-agent-observability-with-langfuse
- https://langfuse.com/docs/observability/features/agent-graphs
- https://launchdarkly.com/blog/agent-graphs-multi-agent-ai-workflows/
- https://dev.to/suraj_kumar_96bb8767435e2/swarm-test-v033-i-visualized-my-14-agent-system-and-the-bottleneck-was-obvious-73b
- https://github.com/surajkumar811/swarm-test
- https://zylos.ai/research/2026-04-14-graph-based-agent-workflow-orchestration-production/
- https://agenticswimlanes.com/
