# System Diagram Research — 2026-09-11 (swarm batch)

> ✅ QA-gated by PO 2026-09-11 · spot-check: A2A Linux Foundation governance ✓ (v1.0 version claim disconfirmed & corrected)


## TL;DR
- Excalidraw shipped MCP server v2.0 ("Interchange-Grade Exports & MCP 2026-07-28") — 26 tools over stdio, Node≥20, local-first, plus an Agent Skill/CLI for Claude Code/Codex/Cursor/OpenCode.
- Azure's Architecture Diagram Builder is now agent-callable as an MCP `render_diagram` tool, returning SVG with grouped zones, labeled flows, and cost badges inline in agent conversations.
- 2026 consensus: the interesting new work isn't new diagram languages, it's MCP servers fronting existing tools (Excalidraw, tldraw, Mermaid) so agents read/write live canvases instead of emitting static text blocks.
- Mermaid remains the dominant LLM target language (best-known grammar, native GitHub rendering); D2 has nicer default layout but far less LLM training familiarity — this tradeoff is now a stable, not shifting, fact as of 2026.
- A2A protocol is Linux Foundation governed (confirmed on primary repo); the "v1.0" version claim from aggregator sources is **not corroborated** by the primary spec page, which describes A2A as still evolving with no explicit release number — no agent-topology-diagram standard has emerged around it yet, visualization stays vendor-specific (e.g., Galileo's "Agent Graph").

## Findings

1. **What:** Excalidraw MCP server v2.0 released 2026-07-28, adopting the new MCP "2026-07-28" spec revision (server/discover, per-request `_meta` envelope, tool calls without handshake), while staying backward-compatible with 2025-era `initialize`-based clients. Requires Node ≥20.
   **Why it matters:** This is a concrete, dated example of an MCP protocol-version bump landing in a widely-used diagramming tool — useful precedent for anyone wiring Excalidraw MCP into this repo's agent stack, and a signal that MCP client/server code should tolerate both handshake styles.
   **Confidence:** high (primary GitHub release notes via search snippet).

2. **What:** Excalidraw MCP exposes 26 tools over stdio for any MCP client, plus a separate REST API for LangChain/custom frameworks, and a zero-config Agent Skill+CLI for coding agents that auto-starts the canvas. Mermaid-to-Excalidraw conversion runs locally in-browser, no API keys required.
   **Why it matters:** Local-first, no-API-key diagram authoring is directly compatible with this repo's preference for deterministic, auditable tooling over opaque SaaS calls.
   **Confidence:** high.

3. **What:** Microsoft's Azure Architecture Diagram Builder is now agent-ready as an MCP server: agents call `render_diagram` with structured params (title, format, direction, theme, region) and get back SVG with grouped zones, labeled flows, and cost badges.
   **Why it matters:** First major cloud vendor to expose a "params in, rendered architecture diagram out" MCP tool rather than expecting the agent to hand-write DSL — a pattern worth watching for a possible generic/cloud-agnostic equivalent.
   **Confidence:** med (single vendor blog, no cross-check).

4. **What:** Community/practitioner consensus through late 2025–2026: Mermaid stays the default LLM-generated diagram language because of grammar familiarity and native GitHub Markdown rendering; D2 produces better default layouts but LLMs are less fluent in its syntax.
   **Why it matters:** Confirms no format shift is likely soon — safe to keep standardizing on Mermaid for in-repo docs/diagrams rather than betting on D2 becoming the new default.
   **Confidence:** med (aggregated blog/community sentiment, not a single authoritative source).

5. **What:** The broadly cited 2026 framing is "the agent lives with your diagram" — i.e., MCP servers that let an agent read back and incrementally edit an existing live canvas (Excalidraw/tldraw/Mermaid) rather than regenerating a diagram from scratch each time.
   **Why it matters:** Implies diagram tooling should be treated as stateful shared artifacts an agent maintains over a session/project lifetime, not one-shot generation — relevant to how this repo could maintain a living system diagram instead of regenerating docs each pass.
   **Confidence:** med (recurring theme across multiple aggregator sources, not one primary doc).

6. **What:** A2A (Agent2Agent) protocol is governed by the Linux Foundation (confirmed directly on github.com/a2aproject/A2A: "an open source project under the Linux Foundation, contributed by Google"), with Agent Cards (JSON capability descriptors), Tasks, and Messages as its core primitives. PO spot-check against that primary source found **no "v1.0" release statement** — the repo describes the spec as still evolving under "Protocol Enhancements," contradicting the aggregator-sourced "v1.0" claim in the original draft (corrected here).
   **Why it matters:** Agent Cards are structured JSON and a natural source for auto-generating agent-topology diagrams (who can call whom, what capabilities) — but as of this search, no standard visualization/diagram format has emerged for A2A ecosystems; only closed vendor dashboards (e.g., Galileo Agent Graph) exist.
   **Confidence:** high for governance (primary source verified); the version-number claim from aggregator "Galileo"/"Tyk" style guides is retracted as unconfirmed.

7. **What:** No search turned up a new open standard specifically for "live system topology visualization" of running agent fleets in 2026; existing offerings remain proprietary observability dashboards layered on top of A2A/MCP traces.
   **Why it matters:** Confirms this remains a gap (consistent with the earlier 2026-09-10 "a2a-gaps" batch already in topics/) — still an opportunity space, not yet commoditized.
   **Confidence:** low (absence-of-evidence finding from a small number of searches; not exhaustive).

## For This Workspace
- Consider adding an Excalidraw-MCP-based "living diagram" of the agent-harness topology (PO + swarm subagents + inbox/topics flow) as a maintained artifact under `.agent-dashboard/` rather than a static Mermaid block, since v2.0 supports local, no-API-key operation compatible with this repo's secrets policy.
- If/when the dashboard (`.agent-dashboard/src/dashboard-server.swift`) grows a visual topology view, look at Excalidraw MCP's REST API (for non-MCP-native consumers) as an integration path rather than building custom SVG rendering.
- Keep Mermaid as the default diagram language for in-repo docs (SKILLS-INDEX, board, memory files) — no evidence yet justifies migrating to D2.
- Track `a2aproject` GitHub directly (not aggregator blogs) before citing A2A v1.0 governance/version claims in any committed memory topic file — current sourcing here is secondary and should be upgraded on next research pass.

## Sources
- https://techcommunity.microsoft.com/blog/azurearchitectureblog/beyond-the-canvas-the-azure-architecture-diagram-builder-becomes-agent-ready/4534590
- https://github.com/excalidraw/excalidraw-mcp
- https://github.com/yctimlin/mcp_excalidraw
- https://mcpservers.org/servers/yctimlin/mcp_excalidraw
- https://pypi.org/project/excalidraw-mcp/
- https://www.taskade.com/blog/history-of-mermaid
- https://infrasketch.net/blog/best-diagram-as-code-tools-2026
- https://nimbalyst.com/blog/best-ai-diagram-tools-2026/
- https://galileo.ai/blog/google-agent2agent-a2a-protocol-guide
- https://tyk.io/learning-center/a2a-protocol-architecture-and-technical-specification/
- https://www.digitalapplied.com/blog/ai-agent-protocol-ecosystem-map-2026-mcp-a2a-acp-ucp
