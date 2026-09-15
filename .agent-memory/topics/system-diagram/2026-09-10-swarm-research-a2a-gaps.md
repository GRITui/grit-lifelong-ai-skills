# System-diagram research: A2A protocol, graph engineering, and delegation-diagram gaps (Sep 2026)

> ✅ QA-gated by PO 2026-09-10 · spot-check: Galileo ships an "Agent Graph visualization" feature mapping agent-to-agent communication flows, and A2A protocol transferred to Linux Foundation governance ✓

## TL;DR

- The "OTel trace → Mermaid" auto-converter gap flagged in prior research is still unfilled as a mature standalone tool as of Sep 2026 — it remains a recognized-but-unmet want in the tracing community (Jaeger/Tempo threads), not a shipped product.
- Google's A2A (Agent2Agent) protocol — contributed to the Linux Foundation in 2026, v1.0.1 (May 2026) — gives a machine-readable JSON standard (the "Agent Card", served at `/.well-known/agent.json`) for describing an agent's capabilities/endpoints, which is a plausible input format for auto-generating delegation diagrams, though no diagram-generation tool built on Agent Cards was found.
- "Graph engineering" emerged in 2026 as a named discipline (TrueFoundry, explainx.ai) for representing multi-agent systems as explicit graphs of heterogeneous nodes (agents, functions, routers, joins, tools, human checkpoints) with delegation as edges — but it's described as a contested/emerging framing, not a settled diagramming standard.
- Galileo's platform ships an "Agent Graph visualization" feature that maps agent-to-agent communication flows across a mixed-framework ecosystem for bottleneck/failure-pattern detection — a new (beyond Langfuse/LangSmith/Arize) commercial entrant in trace-visualization space.
- No new standard was found specifically for representing agent-to-agent delegation/handoff graphs as a diagram-as-code format (Mermaid/PlantUML/etc.) — closest analogs are the A2A Agent Card (data spec, not a diagram spec) and LangGraph's existing node/edge graph (already covered in prior research).

## Findings

1. **What:** The desire for an "export trace to Mermaid" feature is explicitly discussed in tracing communities (e.g., a Jaeger GitHub issue on documenting microservice architecture from traces, and Lobsters discussion of Mermaid Gantt charts for distributed traces), but no widely-adopted converter tool has shipped.
   **Why it matters:** Confirms the gap identified in prior research is still open in September 2026 — still a build-it-yourself opportunity, not something to adopt off the shelf.
   **Confidence:** medium (multiple independent community signals, but no negative-result search can fully prove absence).

2. **What:** Google's Agent2Agent (A2A) protocol was contributed to the Linux Foundation in 2026 and reached v1.0.1 in May 2026, adding an extension mechanism for new data/RPC methods/state machines. Its core artifact is the "Agent Card" — a JSON document at `/.well-known/agent.json` declaring service endpoints, auth schemes, skill descriptions (input/output modes), and task capabilities.
   **Why it matters:** Agent Cards are structured, machine-readable, and cross-framework by design — a more standardized input than ad hoc trace logs for auto-generating delegation-graph diagrams (e.g., a script could crawl a fleet of Agent Cards and emit a Mermaid graph of who-can-call-whom). No such generator tool was found yet, so this is a build opportunity rather than an existing solution.
   **Confidence:** high for protocol/status facts (multiple corroborating sources), low for the diagram-generation opportunity (that part is inference, not observed).

3. **What:** "Graph engineering" is a named 2026 practitioner framing (TrueFoundry blog series, explainx.ai) that treats a multi-agent system explicitly as a graph — nodes = agents/functions/routers/joins/tools/human checkpoints, edges = communication and delegation — and calls for "graph observability" (which nodes ran, in what order, with what latency).
   **Why it matters:** This is conceptually close to what a PO+swarm board (this repo's model) already does implicitly; the framing gives vocabulary but TrueFoundry itself notes the synthesis is contested/not-yet-standardized, so treat as terminology, not a tool to adopt.
   **Confidence:** medium (single vendor's editorial framing, corroborated by a second independent blog, but explicitly flagged in sources as unsettled).

4. **What:** Galileo ships an "Agent Graph visualization" product feature that maps agent-to-agent communication flows across mixed-framework ecosystems, aimed at spotting bottlenecks/failure patterns.
   **Why it matters:** A new entrant beyond Langfuse/LangSmith/Arize already covered in prior research; relevant if this workspace ever needs commercial/hosted trace-graph visualization instead of self-hosted.
   **Confidence:** high (directly confirmed via WebFetch of Galileo's own page).

5. **What:** There is an IETF draft, "Multi-Agent Delegation in Sovereign Object Systems" (draft-sato-soos-mad-03), targeting standards track, expiring December 2026.
   **Why it matters:** Signals that formal standardization of agent delegation semantics is being attempted at the IETF level, which could eventually produce a canonical delegation-graph data model — worth a re-check after its expiry/renewal date passes.
   **Confidence:** low (draft-stage IETF document; not yet a standard, unclear adoption path, only surfaced via search snippet not directly fetched).

6. **What:** No dedicated "diagram-as-code" tool specifically scoped to multi-agent/swarm architecture documentation (as distinct from generic software architecture tools like Eraser/Kroki already covered) was found in this search pass.
   **Why it matters:** Confirms this remains a gap in the tooling landscape — existing agent frameworks (LangGraph) bake in their own graph visualization rather than exporting to a portable diagram format.
   **Confidence:** medium (absence-of-evidence finding from a bounded search budget, not exhaustive).

## For This Workspace

- Given the confirmed gap (finding 1), the highest-leverage build here remains a small internal tool (`.agent-harness/tools/`) that reads `.agent-dashboard/board.json` delegation records (PO → swarm task assignments) and emits a Mermaid sequence/flow diagram of who-delegated-what-to-whom — this is exactly the "delegation graph as diagram-as-code" gap, and the data already exists locally, so no external trace format is needed.
- If Agent Card-style JSON (A2A) is ever adopted for any subagent in this repo, treat it as a candidate structured input for such a converter — it's more standardized than ad hoc board.json fields.
- Adopt "graph engineering" vocabulary (nodes = agents/tools/routers/human checkpoints, edges = delegation) loosely for documenting the PO+swarm model in `.agent-memory/topics/system-diagram/`, but do not treat it as requiring a specific tool adoption — it's terminology, not tech.
- Re-check draft-sato-soos-mad delegation-standard status after December 2026 (its stated expiry) to see if it advanced or lapsed — low priority, park as a future research trigger rather than acting now.

## Sources

- https://github.com/jaegertracing/jaeger/issues/1646
- https://lobste.rs/s/nzt6xh/mermaid_gantt_diagrams_are_great_for
- https://galileo.ai/blog/google-agent2agent-a2a-protocol-guide
- https://blog.dailydoseofds.com/p/a-visual-guide-to-agent2agent-a2a
- https://www.truefoundry.com/blog/graph-engineering-enterprise-guide
- https://explainx.ai/blog/graph-engineering-ai-agents-multi-agent-organizations-2026
- https://datatracker.ietf.org/doc/draft-sato-soos-mad/03/
- https://www.truefoundry.com/blog/agent-harness-graph-engineering-system-intelligence
