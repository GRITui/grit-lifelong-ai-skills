> ✅ QA-gated by PO batch 2026-09-08 · spot-check: Mermaid v11.16.0 GitHub release (2026-06-25) confirmed via GitHub API — Cynefin (beta), Railroad, and Swimlane diagram types verified present in release notes ✓

## TL;DR
- Every major "diagram as code" tool (PlantUML, draw.io, Mermaid) shipped its own official MCP server or first-party AI generator in 2026 — the "agent talks directly to the diagram engine" pattern is now standard, not just a community wrapper trend.
- Mermaid core itself (not just third-party MCP wrappers) is on a fast release cadence in 2026, adding several new diagram types (Ishikawa/fishbone, Venn, Wardley Map, TreeView, Event Modeling, Cynefin, Railroad, Swimlane) plus new themes and shapes — several of these map 1:1 onto chart types the diagram-design skill already claims to support.
- Consumer/enterprise whiteboard tools (Lucidchart, Miro, Whimsical) all now do text-to-diagram, but multiple 2026 comparative reviews independently conclude generated diagrams are "plausible rather than correct" — verification against the real system remains manual work, reinforcing the value of a QA gate.
- Diagram-as-code is being positioned in 2026 as "architecture as code": text sources in Git, rendered in CI, PRs fail on invalid diagram syntax, and drift between diagram and system is reviewable like any other code diff.
- SVG diagram accessibility is still an unsolved, manual problem in 2026 — WCAG 2.2 criteria apply (non-text contrast, keyboard access, name/role/value) but tools don't auto-generate accessible SVG; ARIA labeling has to be added by hand, and WCAG 3.0 is still only a draft.

## Findings

1. **What**: PlantUML shipped `@plantuml/mcp-js` (June 2026, npm) — a pure Node.js/TeaVM local MCP server exposing PlantUML rendering to AI assistants — plus `@plantuml/core` (May 2026), a browser-runnable engine with no server/Java dependency, and a PlantUML Editor "AI Assistant" (May 2026) supporting OpenAI/Anthropic/GitHub Models/OpenRouter API keys.
   **Why it matters**: PlantUML is now a viable no-server, no-Java text-to-diagram backend an agent could call locally via MCP, distinct from D2/Mermaid/Structurizr already covered in the prior research file — worth comparing its UML-specific diagram fidelity (sequence, class, state) against this workspace's current HTML/SVG generation approach.
   **Confidence**: med (search-result synthesis of GitHub/npm/changelog listings, not independently fetched).

2. **What**: draw.io/diagrams.net added a "Generate" tool (sparkle button, January 2026) that intelligently routes a prompt to multiple underlying AI generators to produce a diagram directly in the toolbar; version 30.0.4 (May 27, 2026) added AI-driven diagram generation for technical prompts plus 3x rendering performance for diagrams with 1000+ shapes.
   **Why it matters**: draw.io is the format this workspace's diagram-design skill already redraws from (.drawio/.drawio.png/.drawio.svg); knowing draw.io itself now natively generates from text prompts (not just redraws) is relevant if the skill's redraw pipeline ever needs to interoperate with draw.io-native AI output rather than only hand-authored files.
   **Confidence**: low-med (WebFetch on the primary blog post failed — content was truncated in the fetch tool; claim is from WebSearch snippet only, not independently verified against full article).

3. **What**: Mermaid.js core (not a wrapper) has been shipping new diagram types through 2026 point releases: Ishikawa/fishbone and Venn (v11.13.0), Wardley Map and TreeView as beta (v11.14.0), Event Modeling (v11.15.0), and Cynefin, Railroad, and Swimlane as beta (v11.16.0), alongside new "Neo" and "Redux" themes.
   **Why it matters**: Several of these (fishbone, Venn, Wardley map, swimlane) are chart types the diagram-design skill's own capability list already names — first-party Mermaid now natively supports them, so Mermaid could serve as a validated reference layout/spec for those specific diagram types rather than the skill inventing layout rules from scratch.
   **Confidence**: low-med — WebSearch summary is plausible and internally consistent, but a direct WebFetch of github.com/mermaid-js/mermaid/releases returned garbled/contradictory dates (labeled "August 2024" for v11.17.x, which conflicts with the 2026 version-number progression implied by the search results); treat exact version/date pairing as unverified and re-check against the live releases page before relying on it.

4. **What**: Multiple independent 2026 reviews (Dupple, InfraSketch, AI Diagram Maker roundups) comparing Lucidchart, Miro, and Whimsical AI diagram generation converge on the same limitation: each tool converts text prompts to flowcharts reasonably well for simple cases, but "generated diagrams are plausible rather than correct, and verifying them against your actual system is most of the work" — none of them check correctness against a real codebase or infra state.
   **Why it matters**: Independent convergence across competitor products on this exact failure mode (fluent but unverified output) is a strong signal — it validates the CLAUDE.md-mandated QA-gate philosophy at the tool-market level, not just as an internal preference. Reinforces finding #5 from the prior research file (DiagramEval) with real-world product evidence rather than just an academic paper.
   **Confidence**: med (consistent theme across 3+ independent 2026 review sources, though all are secondary/comparison-blog sources rather than hands-on testing by this agent).

5. **What**: 2026 coverage frames "architecture as code" as the maturing category name for diagram-as-code: DSL/text sources (Mermaid, D2, PlantUML, Structurizr, LikeC4, IcePanel) live in Git, render in CI, and CI can fail a build on invalid diagram syntax; Structurizr specifically is cited for CLI validation/rendering in CI/CD so "architecture drift is detectable because the diagram definition is reviewable in pull requests."
   **Why it matters**: Gives a concrete verification pattern this workspace's QA gate could adopt for diagram source files if the diagram-design skill ever stores redrawable .mmd/.d2/PlantUML sources in-repo: a lint/render step (`bash -n`-equivalent for diagrams) that must exit 0 before the diagram is considered done, matching the existing "Shell script → bash -n" row in this repo's CLAUDE.md verification table.
   **Confidence**: med (multiple 2026 roundup/blog sources agree on the pattern; not verified against a live CI pipeline by this agent).

6. **What**: WCAG 2.2 (published 2023, still current in 2026; WCAG 3.0 remains only a working draft as of Sept 2025) applies several success criteria directly to SVG diagrams — non-text contrast (1.4.11), keyboard operability (2.1.1), and name/role/value (4.1.2) — but SVGs are not accessible by default; accessibility requires manually adding `aria-labelledby`/`aria-describedby`, semantic grouping, and deciding whether each SVG is decorative (hidden from AT) or informative (labeled). No mainstream diagram tool auto-generates this.
   **Why it matters**: This is a genuine gap not covered in the prior research file. If the diagram-design skill's standalone HTML/SVG output is meant to be broadly usable (not just decorative images), it currently has no accessibility layer — a concrete, scoped enhancement would be to add ARIA labels/descriptions and decorative-vs-informative tagging as a post-generation step, independent of branding or layout work.
   **Confidence**: high for the WCAG criteria themselves (W3C/WCAG source material is authoritative); med for "no mainstream tool auto-generates this" (inferred from multiple secondary accessibility-blog sources, not a tool-by-tool audit).

7. **What**: A May 2026 workflow (Codex CLI, per Daniel Vaughan's knowledge base) demonstrates reading source code directly and emitting diagram-as-code artifacts (Mermaid, PlantUML, or Structurizr DSL) automatically, then keeping them current via CI — i.e., AST/codebase-to-diagram generation as an established (if niche) workflow pattern in 2026, not just a "future direction" as characterized in the prior file's roundup-sourced finding #7.
   **Why it matters**: Moves the "generate diagrams from live code/infra" idea (previously flagged as low-confidence/aggregated commentary in the earlier file) from speculative to "at least one documented working example exists" — still a single source, but a concrete implementation rather than a marketing prediction.
   **Confidence**: low (single blog/knowledge-base source, not independently reproduced or fetched in full).

## For This Workspace

1. Treat Mermaid's native (core, non-MCP) diagram-type additions in 2026 — especially fishbone/Ishikawa, Venn, and swimlane, which the diagram-design skill already lists as supported outputs — as a free reference implementation: before hand-rolling layout logic for those types, compare against how Mermaid's own renderer lays them out, even if the skill's final output stays HTML/SVG/PNG rather than Mermaid syntax. Re-verify exact Mermaid version numbers/dates directly against https://github.com/mermaid-js/mermaid/releases first, since this agent's own WebFetch attempt returned inconsistent dates for that page.
2. Add a minimal accessibility pass to the diagram-design skill's output step: tag each generated SVG's root with a chosen `role` and either `aria-labelledby`/`aria-describedby` (informative diagrams) or `aria-hidden="true"` (purely decorative ones), and check non-text/edge contrast against WCAG 2.2's 1.4.11 threshold. This is a small, scoped gap with no current coverage in the skill or the prior research file.
3. If PlantUML's new no-Java `@plantuml/core` (browser-runnable) or local `@plantuml/mcp-js` MCP server hold up under a quick trial, they're a lighter-weight alternative to a JVM-based PlantUML install for any future UML-specific (sequence/class/state) diagram sourcing — cheaper to spin up than Structurizr for one-off UML diagrams.
4. Borrow the "architecture as code in CI" verification pattern (Structurizr/D2/Mermaid sources rendered + lint-checked in CI, build fails on invalid syntax) as a template for this repo's own QA gate wording if diagram source files (not just rendered HTML/SVG/PNG) ever get checked into `.agent-memory/` or a future diagrams directory — mirrors the existing `bash -n <script>` row in CLAUDE.md's verification table.

## Sources
https://plantuml.com/news
https://github.com/plantuml/plantuml/releases
https://plantumleditor.com/changelog/
https://drawio-app.com/blog/the-generate-tool-in-draw-io/
https://github.com/mermaid-js/mermaid/releases
https://mermaidstudio.dev/whatsnew/2026-1-11/
https://dupple.com/learn/best-ai-diagram-tools
https://infrasketch.net/blog/best-diagram-as-code-tools-2026
https://infrasketch.net/blog/best-ai-diagram-tools-2026
https://www.catio.tech/blog/architecture-as-code
https://uxxu.io/blog/diagramming-tools-software-architecture/
https://codex.danielvaughan.com/2026/05/13/codex-cli-architecture-diagrams-mermaid-c4-plantuml-source-code-visualisation/
https://www.disabilityworld.org/articles/accessible-data-viz-tooling-2026/
https://github.com/mgifford/ACCESSIBILITY.md/blob/main/examples/SVG_ACCESSIBILITY_BEST_PRACTICES.md
https://www.w3.org/TR/SVG/access.html
https://en.wikipedia.org/wiki/Web_Content_Accessibility_Guidelines
