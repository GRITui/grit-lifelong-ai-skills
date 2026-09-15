# System Diagram Research: Agentic-System Diagramming Conventions (2026)

> ✅ QA-gated by PO 2026-09-11 · spot-check: "LangGraph models workflows as directed graphs with nodes/edges + shared mutable state" ✓ (WebFetch of architecturediagram.ai/blog/langgraph-architecture-diagram, exit 0, quote confirms nodes/edges/shared-state claim; Mermaid auto-render detail not explicitly confirmed by this source but is a minor non-load-bearing addition)

## TL;DR
- No single universal notation standard exists yet for agentic-system diagrams as of Sep 2026; the field is converging on shared *elements* (decision loops, tool registries, memory stores, trust boundaries) rather than a formal grammar like UML/C4.
- MCP (Model Context Protocol) is the de facto standard for tool-integration edges in these diagrams — most 2026 frameworks natively support it, so diagrams increasingly draw a distinct "MCP tool call" edge type separate from plain function calls.
- LangGraph's directed-graph model (nodes = processing steps, edges = transitions, shared mutable state) is becoming a common lingua franca; it renders natively to Mermaid, which lowers the bar for turning code into a diagram.
- Recommended agent-specific diagram elements beyond generic dataflow: decision/feedback loops, conditional routing branches, explicit memory read/write arrows (short-term vs long-term vs working buffer), human-in-the-loop trust boundaries, and failure/error pathways.
- Memory architecture is now commonly drawn as its own subsystem (durable stores + retrieval policy + context-assembly step + write-back path), often fed through MCP rather than direct DB calls.

## Findings

**What: Agentic diagrams need decision-loop and conditional-routing notation that generic dataflow/architecture diagrams don't have.**
Why it matters: A standard box-and-arrow dataflow diagram implies a single pass; agent systems loop (call tool → get result → decide next step) and branch on confidence/escalation thresholds. Diagrams that don't show this loop explicitly misrepresent the system's actual runtime behavior to reviewers.
Confidence: med

**What: Trust boundaries (autonomous vs human-approved actions) are being called out as a required diagram element for agentic systems, not just security diagrams.**
Why it matters: Stakeholder communication and audit/compliance review depend on visually separating what the agent can do unattended from what requires human-in-the-loop gates — this is now treated as a first-class diagram layer, not an annotation.
Confidence: med

**What: Failure-pathway mapping (LLM failures, tool timeouts, guardrail activations) is recommended as an explicit diagram layer because agentic systems have materially more failure modes than deterministic software.
Why it matters: Traditional architecture diagrams mostly show the happy path; for agent systems, the error/guardrail paths are argued to be as architecturally significant as the main flow.
Confidence: med

**What: Recommended core component vocabulary for agent diagrams: orchestrator/planner, tool registry, sub-agents/specialists, human-in-the-loop gates, state/checkpoint store, guardrail/evaluation layer.**
Why it matters: This gives a repeatable checklist of "boxes that must appear" when diagramming any agent system, similar to how C4 fixes "container/component" — useful as a completeness check even without a formal grammar.
Confidence: med

**What: LangGraph models workflows as directed graphs with nodes (processing steps) and edges (transitions), plus a shared state object that persists across the whole graph — and this graph structure can be auto-rendered as a Mermaid diagram.
Why it matters: Because LangGraph is one of the most widely adopted orchestration frameworks in 2026, its graph model is becoming a practical, tool-generated notation for multi-agent orchestration diagrams rather than something hand-drawn.
Confidence: med

**What: Agent memory is increasingly diagrammed as a distinct subsystem with four parts: durable stores, retrieval policy, context-assembly step, and write-back path — commonly accessed via MCP tool calls rather than direct database edges.
Why it matters: Treating memory as an architectural subsystem (rather than an implicit detail inside the "agent" box) clarifies latency/cost tradeoffs (short-term conversation history vs. vector-DB long-term memory vs. working buffers) that matter for system design reviews.
Confidence: med

**What: MCP compatibility is now near-ubiquitous across major AI frameworks/enterprise tools by 2026, making "MCP tool call" a recognizable, distinct edge type worth its own visual treatment in orchestration diagrams (vs. generic API calls).
Why it matters: If MCP edges are visually distinguished from other integration types, diagrams communicate which integrations follow the standardized protocol (portable, tool-discoverable) vs. bespoke/one-off integrations.
Confidence: low (single-source claim, general trend framing rather than a specific spec)

## For This Workspace
- Extend this repo's existing orchestration-diagram patterns with an explicit "decision loop" and "conditional routing" edge/annotation convention (agent → tool → result → decision), since prior diagrams here likely treat orchestration as one-way dataflow.
- Add a "trust boundary" visual convention (e.g., a dashed boundary or shaded zone) to distinguish autonomous-agent actions from human-in-the-loop gates in board/orchestration diagrams — useful given this repo already tracks PO-gated vs. delegated-swarm work.
- Model memory/context flow as its own subsystem block (durable store + retrieval policy + context assembly + write-back), and if any diagrammed system uses MCP for memory access, draw that as a distinct edge type from direct DB/API edges.
- Consider adopting LangGraph's node/edge/shared-state vocabulary (and its Mermaid auto-render path) as a candidate lightweight notation for future orchestration diagrams in this repo, given it's tool-generated and increasingly standard.

## Sources
- https://architecturediagram.ai/blog/ai-agent-architecture-diagrams
- https://architecturediagram.ai/blog/langgraph-architecture-diagram
- https://www.graphlit.com/blog/survey-of-ai-agent-memory-frameworks
- https://medium.com/@charlesmcchan/building-agentic-memory-with-langgraph-graphiti-via-mcp-bfab711c29eb
- https://rasa.com/blog/agent-orchestration-tools
