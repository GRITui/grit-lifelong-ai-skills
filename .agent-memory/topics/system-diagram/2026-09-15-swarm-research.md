> ✅ QA-gated by PO 2026-09-15 · spot-check: AgentRaft arXiv 2603.07557 describes a Cross-Tool Function Call Graph for data over-exposure detection ✓

## TL;DR
- New this cycle: concrete, checklist-level conventions specifically for **MCP topology diagrams** (host/client/server separation, transport labeling, tool namespacing, auth boundaries) are now published as a named pattern — not just "MCP is a distinct edge type" as noted previously.
- Multi-agent diagram convention is shifting toward showing **structured-output data contracts** (JSON schemas) as the handoff artifact between agents, not just an arrow labeled "delegates to."
- A cluster of 2026 academic work — **Graph of Trace** (ACL 2026 demo), **AgentRaft's Cross-Tool Function Call Graph**, and the survey **"Graphs Meet AI Agents"** — treats agent execution traces and tool-call dependencies explicitly as *graph-structured data* to be automatically extracted and visualized, going beyond the trace-visualization tools (Langfuse, LangSmith) already logged in prior research.
- Still no single formal notation standard for multi-agent/A2A/MCP diagrams as of Sep 2026 — this confirms rather than overturns the prior digest's core conclusion.
- AgentRaft's Cross-Tool Function Call Graph is notable for a new use case: security/data-flow auditing (detecting data over-exposure across tool calls), not just architecture documentation.

## Findings

**What:** ArchitectureDiagram.ai's MCP-specific guide lists six concrete elements an MCP topology diagram should show: (1) host/client/server kept visually distinct because they carry different trust levels, (2) every connection labeled with its transport (stdio vs. HTTP+SSE), since transport determines whether a server is local or remote, (3) tool namespacing shown to avoid collisions across servers (e.g. `filesystem__read_file` vs `github__read_file`), (4) auth boundaries annotated per-server (API keys, OAuth tokens, DB connection strings), (5) protocol-version/capability-negotiation annotations for mixed deployments, (6) trust/sandboxing marks distinguishing read-only vs. read-write and flagging destructive capabilities.
Why it matters: This is more prescriptive than the prior digest's finding that "MCP is worth distinguishing as an edge type" — it gives a specific checklist usable directly as a diagram-review rubric for any workspace diagramming its own MCP server fleet.
Confidence: med (single vendor blog, not cross-checked against a second independent source, but content is consistent with MCP's actual host/client/server spec model)

**What:** 2026 commentary on multi-agent architecture (openlayer.com, clickittech.com, and related guides) describes a shift from free-text inter-agent messages toward **structured outputs defined by JSON schemas** functioning as an explicit "data contract" between agents, alongside the already-known need to show decision loops, conditional routing, and memory read/write operations.
Why it matters: A diagram convention built around "data contract" edges (schema-typed) rather than plain arrows would let a diagram double as a validation source — the schema itself is checkable — which is a stronger artifact than a label-only arrow.
Confidence: low (aggregated search-synthesis across multiple non-primary blog sources, no single canonical spec identified)

**What:** "Graph of Trace" (ACL 2026 demo track paper, NeuroAIHub/Graph-of-Trace on GitHub) records intermediate agent steps (tool calls, code executions) and renders them as real-time-updating visual traces exposing workflow structure, aimed at scientific/research agents specifically, to let users see where failures emerge mid-run.
Why it matters: This is a peer-reviewed (ACL demo track) academic instance of the "live topology from real execution" pattern already logged for swarm-test/Langfuse, but applied to a different domain (scientific-agent pipelines) and published with an open GitHub repo — a second independent implementation validating the pattern's generality beyond commercial observability vendors.
Confidence: med (identified via search + GitHub repo existence confirmed; paper content not directly fetched)

**What:** AgentRaft (arXiv 2603.07557) builds a "Cross-Tool Function Call Graph" from an agent system by identifying inter-tool and intra-tool function dependencies, using this graph as a structural blueprint specifically for detecting data over-exposure (a security/privacy audit use case) rather than for documentation or debugging.
Why it matters: This is a new diagram *purpose* not previously logged — tool-call graphs used as an automated security-audit artifact (data-flow analysis for over-exposure) rather than architecture documentation or debugging aid. Suggests tool-call graphs have a security-tooling use case distinct from the observability use case already covered.
Confidence: low (identified via arXiv listing/search snippet only; PDF content not directly fetched, so graph-construction methodology is unconfirmed)

**What:** The survey "Graphs Meet AI Agents: Taxonomy, Progress, and Future Opportunities" (arXiv 2506.18019, with a maintained companion GitHub list "Awesome-Graphs-Meet-Agents") proposes a taxonomy for how graph techniques and AI agents mutually reinforce each other — framing agent planning, memory, and multi-agent coordination as problems where "data structurization" (turning disorganized agent state into graph-structured form) is the enabling step.
Why it matters: This is the closest thing to an academic framework treating agent-system diagramming as a formal subfield (graphs as the underlying data structure for agent state/coordination), rather than an ad-hoc collection of vendor tools — useful as a reference point if this workspace ever wants to justify a graph-based (vs. tree/flowchart-based) internal representation for its own agent topology.
Confidence: low (survey abstract and framing only; full taxonomy details not fetched)

**What:** As of this research pass, no source found describes a single formal, universally adopted notation standard for multi-agent system diagrams (equivalent to UML for OOP) — sources continue to describe only converging conventions (roles, handoffs, shared context, orchestration logic, decision loops, structured-output contracts).
Why it matters: Directly confirms (does not contradict) the prior digest's "notation gap" finding — teams should keep documenting their own diagram legend rather than assume a standard now exists; the gap persists into mid-September 2026.
Confidence: high (consistent conclusion across multiple independent 2026 sources this pass and the prior digest's Sep 7-14 batches)

## For This Workspace
- If `.agent-dashboard/` or any harness component ever diagrams its own MCP server usage, adopt the ArchitectureDiagram.ai six-point MCP checklist as a review rubric (host/client/server separation, transport label per edge, tool namespacing, auth-boundary annotation, capability/version notes, read-only vs. read-write trust marks) rather than inventing an ad-hoc legend from scratch.
- If a future swarm-run visualization needs to show inter-agent handoffs (PO to subagent), consider labeling the handoff edge with the actual data-contract shape (the JSON payload/schema passed in the Task tool call) rather than a plain text arrow — this keeps the diagram literally checkable against real payloads, consistent with this repo's "gate on exit code, not intent" principle already applied elsewhere.
- Treat tool-call graphs as having (at least) two distinct legitimate uses this repo could apply separately: (a) debugging/observability (already covered via Langfuse/swarm-test pattern) and (b) a security/data-flow audit lens (AgentRaft's over-exposure detection framing) — if this workspace ever audits which subagents have access to which credentials/data via which tool calls, the latter framing is the more relevant one, not the observability framing.
- No action needed on notation standardization — continue documenting this repo's own diagram legend (per the existing digest's Part 3 recommendation) since the gap persists industry-wide as of Sep 2026; revisit only if a dedicated standard is announced.

## Sources
- https://architecturediagram.ai/blog/mcp-architecture-diagram
- https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture
- https://www.skyvern.com/blog/mcp-server-architecture-explained/
- https://architecturediagram.ai/blog/ai-agent-architecture-diagrams
- https://www.openlayer.com/blog/post/multi-agent-system-architecture-guide
- https://www.clickittech.com/ai/multi-agent-system-architecture/
- https://aclanthology.org/2026.acl-demo.29/
- https://github.com/NeuroAIHub/Graph-of-Trace
- https://arxiv.org/pdf/2603.07557
- https://arxiv.org/abs/2506.18019
- https://github.com/YuanchenBei/Awesome-Graphs-Meet-Agents
- https://langfuse.com/docs/observability/features/agent-graphs
