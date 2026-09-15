> ✅ QA-gated by PO batch 2026-09-09 · spot-check: official first-party Mermaid MCP server at mermaid.ai/docs/ai/mcp-server (validation/rendering + Mermaid Chart account tools, VS Code/Cursor/Antigravity support) confirmed via direct fetch ✓

## TL;DR
- Mermaid ecosystem now has an official hosted "Mermaid AI" product plus a dedicated Mermaid MCP server (9 tools, validation + rendering + Mermaid Chart account integration) supporting Copilot/VS Code/Cursor/Antigravity.
- Mermaid Studio 2026.3.1 adds Mermaid.js 11.16.0 support and three new beta diagram types: Cynefin, Railroad, Swimlane (on top of Treemap and Fishbone added earlier in 2026).
- draw.io/diagrams.net now ships official AI diagram generation/validation docs (multi-model: Gemini/Claude/OpenAI configurable by admins) plus a "Generate" tool, and a large third-party OSS project ("Next AI Draw.io", 33k+ GitHub stars) layers natural-language-to-diagram on top with its own MCP server.
- C4-PlantUML is actively maintained into 2026 (v2.13.0, last updated 2026-08-26; tracks PlantUML core release 1.2026.0) — no major format change, just steady upkeep.
- A 2026 "architecture diagram drift" argument is gaining traction: teams treat diagrams as outside code review, so ~68%-of-teams-cited stale docs actively degrade AI coding agents (agents calibrate suggestions to a system that no longer exists) — proposed fix is NL-driven regeneration wired into PR checklists.
- Diagram accessibility content in 2026 is mostly about screen-reader read-order and ARIA-labeled chart elements, not diagram-specific tooling; sketchy/hand-drawn SVG filter techniques are flagged as fine for editorial content but explicitly NOT recommended for technical documentation.

## Findings

**What**: Mermaid now has an official "Mermaid AI" web product (mermaid.ai) and a first-party MCP server (docs at mermaid.ai/docs/ai/mcp-server) exposing ~9 tools: unauthenticated diagram validation/PNG rendering/title-summary generation, plus authenticated Mermaid Chart account tools (list/create/get/update projects and diagrams). Supports GitHub Copilot, VS Code, Cursor, Antigravity, and any MCP client over HTTP/SSE.
**Why it matters**: This is a materially different offering than the previously-reported general "Mermaid MCP" community servers (kayaozkur, hustcc, peng-shawn, narasimhaponnada) — it's the vendor's own server tying MCP directly to a hosted Mermaid Chart account, which changes the trust/versioning story for teams standardizing on Mermaid.
**Confidence**: high (primary source: mermaid.ai/docs/ai/mcp-server; independently re-verified by PO via direct fetch).

**What**: Mermaid Studio 2026.3.1 release adds Mermaid.js 11.16.0 support and introduces three new beta diagram types — Cynefin, Railroad, and Swimlane — building on Treemap (beta) and Fishbone (v11.13.0) added earlier in 2026.
**Why it matters**: Fishbone and Swimlane are directly relevant to this workspace's diagram-design skill (which already supports fishbone/swimlane); confirms Mermaid is converging on parity with the skill's diagram-type coverage, so Mermaid could become a lighter-weight source format for some of those types.
**Confidence**: med (secondary aggregator search snippet referencing mermaidstudio.dev/whatsnew, not independently fetched).

**What**: draw.io's official docs (drawio.com/docs/reference/diagram-generation) now formally spec how AI systems should generate `.drawio` XML: prefer uncompressed XML over Base64/compressed, use the simplified `<mxGraphModel>`-only format, never emit XML comments (wastes tokens / risks parse errors), use relative coordinates for grouped children, and pass generated diagrams into the editor via a `#create` URL parameter. Admins can configure which LLM backend (Gemini/Claude/OpenAI) powers the built-in "Generate" tool.
**Why it matters**: This is a concrete, checkable spec for any pipeline that has an LLM emit draw.io XML directly (as opposed to Mermaid/D2 intermediate formats) — useful as a hard constraint list if this workspace ever generates `.drawio` output directly rather than SVG/HTML.
**Confidence**: high (primary source, official docs).

**What**: A large third-party OSS tool, "Next AI Draw.io" (DayuanJiang/next-ai-draw-io), reports 33,000+ GitHub stars and adds natural-language editing of draw.io diagrams via GPT-4/Claude/Gemini, ships its own MCP server for coding agents, and offers one-click deploy to Vercel/Cloudflare.
**Why it matters**: Signals that "chat with your draw.io diagram" has become a mainstream pattern outside the vendor's own tooling; also a counter-signal exists (an "diagrams.net is better without the AI hype" critique piece) showing pushback against over-indexing on AI generation for correctness-critical diagrams.
**Confidence**: med (GitHub star count and feature claims from secondary/aggregator search results, not independently verified against the repo).

**What**: C4-PlantUML remains actively maintained (v2.13.0, last commit 2026-08-26), tracking PlantUML core's 1.2026.0 release; no structural/format changes reported, just incremental library upkeep (macros, stereotypes, VS Code snippets).
**Why it matters**: Confirms C4-model-via-PlantUML is a stable, low-drama option rather than a fast-moving target — useful as a "boring and reliable" fallback next to Mermaid/D2 for teams that need strict C4 semantics.
**Confidence**: med (search-snippet level; version/date not independently fetched from GitHub releases page).

**What**: A 2026 "architecture diagram drift" thesis (architecturediagram.ai/blog/architecture-diagram-drift, published 2026-06-26) argues diagrams sit outside code review so they silently go stale (cites 68% of teams with docs >6 months old), and that this specifically degrades AI coding agents, since agent suggestions get calibrated against a system architecture that no longer exists. Proposed remedy: NL-driven diagram regeneration (~30 seconds) wired into PR checklists and quarterly ownership audits, alongside diagrams-as-code tools (IcePanel, Structurizr) and infra-extraction tools (Brainboard, Cloudcraft).
**Why it matters**: Extends (rather than duplicates) the already-covered "architecture as code with CI drift detection" ground — the new angle is the specific causal link to degraded AI-agent output quality, plus a concrete practice (ARCHITECTURE.md + PR checklist + rotating owner) this workspace could adopt for its own diagrams if any become load-bearing for future agent runs.
**Confidence**: med (single vendor blog post, self-interested source promoting its own product — treat the 68% stat and specific tool list as unverified marketing claims).

**What**: Diagram/chart accessibility discourse in 2026 centers on screen-reader read-order (elements are announced in insertion order, not visual order, so templates need predefined navigation order) and on making chart labels real tabbable/ARIA-annotated HTML elements rather than baked-into-image text. Separately, sketchy/hand-drawn SVG turbulence-filter styling is explicitly called out as suited to editorial/essay contexts but NOT recommended for technical documentation.
**Why it matters**: Directly actionable for the diagram-design skill's "sketchy/hand-drawn styling" and "accessible motion" features — if diagrams are meant to be technical/reference material, the sketchy filter should probably stay opt-in/cosmetic rather than default, and any exported SVG/HTML diagrams should preserve DOM element order matching visual/logical flow plus ARIA labels for text.
**Confidence**: med (aggregated from multiple secondary sources: INCOBS accessible-diagram-design draft, html-in-canvas.dev accessible-charts demo, Google/Microsoft accessibility help docs).

## For This Workspace
- If diagram-design skill ever emits `.drawio` XML directly, adopt the official constraints found: uncompressed XML, `<mxGraphModel>`-only simplified format, no XML comments, relative coords for grouped children — these are concrete, testable QA-gate checks (`grep -c '<!--'` should be 0, etc.).
- Consider evaluating the official Mermaid MCP server (mermaid.ai/docs/ai/mcp-server) as an alternative/complement to hand-rolled Mermaid generation, since it adds built-in syntax validation before render — could reduce QA-gate failures on Mermaid-sourced diagrams.
- For any diagram this workspace treats as load-bearing documentation (e.g. architecture references consumed by future agent runs), apply the "diagram drift" mitigation pattern: keep a single source-of-truth file next to the diagram, note last-verified date, and re-verify before trusting it in a new session — consistent with this repo's existing QA-gate-before-memory-write discipline.
- When adding "sketchy/hand-drawn" styling in the diagram-design skill, keep it opt-in for technical/reference diagrams and ensure exported SVG/HTML preserves logical (not just visual) element order plus text alternatives, per the 2026 accessibility guidance above.

## Sources
https://mermaid.ai/docs/ai/mcp-server
https://mermaidstudio.dev/whatsnew/2026-3-1/
https://mermaid.ai/blog/posts/page/1
https://www.drawio.com/docs/reference/diagram-generation/
https://drawio-app.com/blog/the-generate-tool-in-draw-io/
https://github.com/DayuanJiang/next-ai-draw-io
https://next-ai-drawio.jiang.jp/en
https://discover.oreateai.com/discover/diagramsnet-drawio-is-better-without-the-ai-hype
https://github.com/plantuml-stdlib/C4-PlantUML/releases
https://plantuml.com/changes
https://plantuml-stdlib.github.io/C4-PlantUML/
https://architecturediagram.ai/blog/architecture-diagram-drift
https://www.incobs.de/articles/items/diagram-a11y.html
https://html-in-canvas.dev/demos/accessible-charts/
https://support.google.com/accessibility/answer/6058689?hl=en
https://support.microsoft.com/en-us/office/make-your-visio-diagram-accessible-to-people-with-disabilities-e2c847a9-f010-4fef-af65-16e252829d44
