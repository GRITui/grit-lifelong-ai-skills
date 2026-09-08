# system-diagram — Swarm Research (2026-09-07)

> ✅ QA-gated by PO 2026-09-07 · sources verified present · load-bearing claims spot-checked (Spec Kit 1.0 confirmed; n8n 2.x claims validated by live debugging) · merged from swarm inbox

# system-diagram — Swarm Research Draft (2026-09-07)

## TL;DR
- Mermaid (v11.17.x) is still the default diagrams-as-code tool for Markdown-first repos: native rendering on GitHub/GitLab/Obsidian/VS Code; D2 wins on layout quality but needs a build step.
- Structurizr (C4 reference implementation, build 2026.07.03) pivoted hard into AI-agent territory: MCP server for DSL validation, "models as code — manual layout — AI friendly".
- AI diagram-from-code is the fast-growing 2026 pattern: agent loops emit `.mmd`/`.puml`/`.dsl`, validated by `mmdc` / plantuml `-checkonly` hooks; guidance says regeneration belongs off the PR critical path.
- Excalidraw's plain-JSON `.excalidraw` format + new CLI/MCP ecosystem (2026) makes hand-drawn-style diagrams agent-authorable, diffable artifacts.
- For a file:// dashboard with no CDN: vendor `mermaid.min.js` (standalone, offline, no core telemetry) or pre-render SVGs with `mmdc`/`d2` in the n8n build step.

## Findings

1. **What** Mermaid renders natively in GitHub, GitLab, Notion, Obsidian, and VS Code — VS Code 1.121 (2026) merged native Mermaid support, deprecating the bierner extension; Confluence/Slack/Google Docs do not render it. Current line: v11.17.x. Native embedders often bundle older Mermaid versions, so newest syntax/C4 features may not render everywhere.
   **Why it matters:** zero-pipeline diagrams inside the repo's markdown; but "renders in GitHub" ≠ "renders with latest features" in every host.
   **Confidence: high**

2. **What** Mermaid's C4 support (C4Context/Container/Component/Dynamic/Deployment, C4-PlantUML-compatible syntax) is still officially *experimental*, has no auto-layout (position via statement order), and flipped text-wrap defaults in v11.17.1. Note: it is experimental-but-alive, not removed.
   **Why:** Mermaid-C4 is OK for lightweight context/container views; serious C4 work still points at Structurizr or C4-PlantUML.
   **Confidence: high**

3. **What** D2 (Terrastruct, single Go binary) is the layout-quality pick: dagre + ELK bundled (open source), TALA layout engine proprietary/licensed; themes, composition/imports across files, watch mode, fmt/validate. No major doc platform renders D2 natively — CI or a CLI step must emit SVG.
   **Why:** best auto-layout for architecture/infra maps and large graphs; cost is a rendering contract that must be documented in the repo.
   **Confidence: high**

4. **What** PlantUML keeps the deepest UML vocabulary plus C4-PlantUML stdlib and cloud icon packs (AWS/Azure/GCP/K8s); needs a JVM (local JAR or server), CI validation via `-checkonly`. Multiple 2026 comparisons converge on a *narrow* mixed policy: Mermaid for markdown docs, PlantUML for formal UML, D2 for architecture maps.
   **Why:** three unrestricted syntaxes raise review burden; pick the smallest set that covers the actual diagram types.
   **Confidence: high**

5. **What** Structurizr 2026 state: DSL "models as code", one model → multiple C4 views with consistency rules, interactive HTML output, prebuilt AWS/Azure/GCP/K8s themes; explicitly marketed as AI-friendly with a Structurizr MCP server (DSL validation/parsing/inspection) for agents; CLI commands free except `server`. Tradeoff: layout is manual, not auto.
   **Why:** strongest agent-compatible C4 path (model-level QA beats per-diagram QA), if manual layout is acceptable.
   **Confidence: high** (vendor docs; breadth of adoption unverified)

6. **What** Agent-driven diagram generation matured into a repeatable pattern: AI CLIs (e.g. Codex CLI `codex exec`) analyze repos/Terraform/OpenAPI and emit Mermaid/PlantUML/Structurizr DSL; PostToolUse-style hooks validate every `.mmd` write via `mmdc -i file -o /dev/null` before commit; CI regenerates diagrams as *derived artifacts* (nightly/on-demand, not on the PR path) and commits only on diff.
   **Why:** exactly matches an agent-authored, git-versioned, QA-gated artifact workflow. Static analysis misses runtime context — AI generation lets you add it, but needs review.
   **Confidence: high** (pattern across independent sources; tool-specific specifics: med)

7. **What** Excalidraw went agent-first in 2026: official Excalidraw MCP (one-shot prompt→diagram widget); community mcp-excalidraw-server v2.0.0 (Jul 2026; element-level CLI + ~26 MCP tools, `.excalidraw` import/export, mermaid→excalidraw conversion, works with Claude Code/Codex/OpenCode); multiple small excalidraw-cli packages (npm/PyPI, first releases Mar 2026) generate/export `.excalidraw` headlessly.
   **Why:** `.excalidraw` is plain JSON — hand-drawn diagrams become diffable repo artifacts agents can create without a browser.
   **Confidence: med** (young, fast-moving, mostly zero-star packages)

8. **What** Offline/file:// rendering is solved: `mermaid.min.js` is a standalone bundle that works with no network and core Mermaid has no telemetry (maintainer statement, GitHub discussion); `mmdc` renders `.mmd`→SVG/PNG via headless Chromium (npm/npx/Docker; brew install no longer supported); draw.io headless export via drawio-desktop CLI (+ xvfb on Linux); diagram-sync (npm, May 2026) unifies PlantUML/Mermaid/Graphviz/Draw.io/D2/Excalidraw/BPMN→SVG/PNG export.
   **Why:** keeps the local HTML dashboard fully static and CDN-free; pre-rendered SVG also sidesteps JS entirely.
   **Confidence: high**

Source-quality note: several 2026 comparison blogs (InfraSketch, ArchitectureDiagram.ai, CodePic, Beauty Diagram) are SEO/vendor content — feature claims above were cross-checked against vendor docs (mermaid.js.org, structurizr.com, GitHub) where possible. One spammy "benchmark" page (johal.in, fake precision stats) was discarded.

## For This Workspace
- **Dashboard rendering:** vendor `mermaid.min.js` (v11.x) into the dashboard folder beside the HTML and render fenced mermaid blocks client-side on file:// (offline-safe, no CDN). Simpler and more robust: have the n8n → data.js build step pre-render diagrams to SVG via `npx -p @mermaid-js/mermaid-cli mmdc`, keeping the dashboard pure-static.
- **Tool policy (narrow):** Mermaid fenced blocks inside `topics/**.md` as the default; D2 (`brew install d2`) only for architecture maps Mermaid's dagre layout mangles — commit rendered SVG next to the `.d2` source since nothing renders D2 natively.
- **QA gate:** every diagram the agent writes gets validated before commit: `mmdc -i x.mmd -o /dev/null` (Mermaid), `plantuml -checkonly` (`.puml`), `d2 validate`/fmt (`.d2`) — mirrors the 2026 agent-hook pattern.
- **If C4 rigor is ever needed:** reach for Structurizr DSL + its MCP validation server before Mermaid-C4 (experimental, no auto-layout); skip drawio unless a hand-laid one-off artifact is genuinely required.

## Sources
- https://codepic.cc/blog/mermaid-vs-plantuml-vs-d2 — CodePic comparison (Aug 2026)
- https://www.beauty-diagram.com/blog/diagrams-as-code-2026-landscape — Beauty Diagram (Jul 2026)
- https://diagrams.so/learn/diagram-as-code-comparison — Diagrams.so (D2/PlantUML/Graphviz detail)
- https://mermaid.js.org/syntax/c4.html — Mermaid official docs, v11.17.2 (C4 experimental)
- https://github.com/mermaid-js/mermaid-cli — mermaid-cli (mmdc) README
- https://github.com/orgs/mermaid-js/discussions/4412 — Mermaid GitHub discussion (offline/telemetry)
- https://forum.cursor.com/t/built-in-mermaid-renderer-doesnt-support-c4container-diagrams-older-mermaid-version-bundled/162935 — Cursor forum (Jun 2026, VS Code 1.121 native Mermaid)
- https://structurizr.com/ — Structurizr official site (2026.07.03 build)
- https://docs.structurizr.com/ai/mcp — Structurizr docs (AI / MCP server)
- https://c4model.com/ — C4 model official site
- https://codex.danielvaughan.com/2026/05/13/codex-cli-architecture-diagrams-mermaid-c4-plantuml-source-code-visualisation/ — Codex KB (May–Jul 2026, agent diagram workflows + hooks)
- https://datadef.io/guides/en/automate-architecture-diagram-in-ci — datadef.io (Aug 2026, CI cadence guidance)
- https://github.com/yctimlin/mcp_excalidraw — mcp-excalidraw-server v2.0 (Jul 2026)
- https://pypi.org/project/excalidraw-cli/ — PyPI excalidraw-cli (Mar 2026)
- https://github.com/Buffden/diagram-sync — diagram-sync multi-provider export CLI (May 2026)
