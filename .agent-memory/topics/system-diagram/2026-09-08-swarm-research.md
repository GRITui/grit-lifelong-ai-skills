> ✅ QA-gated by PO batch 2026-09-08 · spot-check: AWS deprecated its Diagram MCP Server in favor of an Agent Skills-based replacement ✓ (corroborated via github.com/awslabs/mcp discussion #2615 and issue #2883, matheuscosta.dev post)

## TL;DR
- D2 diagram language keeps maturing as a Mermaid/PlantUML alternative: native Go renderer swap-outs, sketch-mode upgrade, ELK.js 0.12.0 layout engine, and third-party editor adoption (VPasCode) in 2026.
- Excalidraw's MCP-driven AI diagramming got materially better in 2026: smarter auto-layout/spacing, semantic edge coloring, an Autoshape tool (freehand-to-geometry), and an MCP Screenshot Tool for scene/frame capture.
- AWS deprecated its dedicated "Diagram MCP Server" in 2026 in favor of Agent Skills — a signal that the industry is shifting infra-diagram generation from bespoke MCP servers toward packaged agent skills (directly relevant to how this workspace's own diagram-design skill is built).
- Wardley Mapping got a wave of AI tooling in 2026: ArcKit v4.3.0 (multi-command strategic pipeline grounded in reference material) and an MIT-licensed Claude Wardley-mapping skill producing interactive React maps + portable OWM DSL text.
- LLM diagram hallucination research in 2026 confirms two mechanisms relevant to diagram generation specifically: early-token errors compound through the rest of the output, and long/overly complex prompts measurably increase hallucination rate — both argue for short, structured, staged diagram-generation prompts.

## Findings

**What**: D2 (Terrastruct's diagram-as-code language) had concrete engine work in 2026 — the embedded JS runtime for the Dagre layout was replaced with a native Go implementation, the sketch/hand-drawn renderer was upgraded from Rough.js 4.0.4 to 4.6.6, and the ELK layout profile moved to ELK.js 0.12.0. Third-party low-code tools (VPasCode, August 2026) added first-class D2 import/render support.
**Why it matters**: D2's pluggable layout engines (dagre/ELK/TALA) plus native rendering improvements make it a stronger diagram-as-code target than before, and animated connections are now a built-in feature for presentation-style output — worth considering as an alternate intermediate format alongside Mermaid/PlantUML for diagrams that need cleaner large-graph auto-layout.
**Confidence**: med (multiple corroborating blog/aggregator sources, no single canonical changelog checked directly)

**What**: Excalidraw's MCP integration (used from Claude and other AI clients) added an "Autoshape" tool (Shift+X) that converts freehand sketches into perfect geometric shapes/arrows, an API Key Management feature, high-resolution image support up to 8000px, and — specific to AI diagram generation — "smarter AI-driven diagram layouting with improved spacing and semantic edge coloring."
**Why it matters**: Semantic edge coloring and improved auto-spacing directly address two chronic weaknesses of LLM-generated diagrams (overlapping nodes, meaningless line colors); this is a concrete external validation that the same problems this workspace's diagram-design skill tries to solve are being tackled elsewhere too.
**Confidence**: med (sourced from a changelog aggregator + a Medium walkthrough, not the primary Excalidraw+ changelog page content itself)

**What**: AWS deprecated its dedicated "AWS Diagram MCP Server" in 2026 and published a replacement approach based on Agent Skills rather than an MCP server, per an AWS Builder Center post ("The AWS Diagram MCP Server Was Deprecated — Here's the Updated Approach Using Agent Skills").
**Why it matters**: This is a direct precedent for packaging diagram generation as a Claude Skill (as this workspace already does with diagram-design) instead of standing up a dedicated MCP server — AWS's own move suggests skills are becoming the preferred distribution mechanism for diagram-generation capability over narrow single-purpose MCP servers.
<br>**Confidence**: med (single source, but source is an AWS-affiliated builder post directly describing the migration)

**What**: LLM hallucination research applicable to diagram generation identifies error-compounding (a wrong early token conditions everything downstream, cascading errors through the full output) and prompt-complexity effects (long/overly complex instructions increase hallucination rate) as two mechanisms; a companion paper specifically on educational diagram generation found that a single hallucinated in-context example can "spoil the bunch" for later generations.
**Why it matters**: For diagram-as-code generation this argues concretely for (1) generating diagrams in small, validated stages rather than one long prompt, and (2) being careful with few-shot examples fed to a diagram-generation prompt, since one bad example can corrupt subsequent outputs in-session.
**Confidence**: med (general LLM-hallucination literature, one paper specific to diagram generation; not diagram-tooling-vendor-specific)

**What**: ArcKit v4.3.0 (Wardley Mapping) adds four AI-assisted commands — value chain decomposition, doctrine maturity assessment, climatic pattern analysis, and gameplay selection — each grounded in reference material distilled from three Wardley Mapping books (over a million words condensed into reference files the AI reads before generating output).
**Why it matters**: This is a strong pattern for "grounded AI diagram generation": instead of asking an LLM to freehand a strategic diagram, feed it condensed domain reference material first, then generate. Directly transferable to any diagram type where domain correctness matters (e.g., C4, data-flow, security-matrix diagrams).
**Confidence**: high (specific, named tool version with described mechanism, from a Medium post by the tool's apparent maintainer)

**What**: A separate MIT-licensed Wardley Mapping Claude Skill produces three coordinated outputs from one generation pass: an interactive React map (hover tooltips, dependency highlighting, legend) via Opus, a portable OnlineWardleyMaps (OWM) DSL text export, and a structured strategic commentary (evolution rationale, doctrine checks, build-vs-buy recommendation).
**Why it matters**: The "generate multiple synchronized artifacts from one pass" pattern (interactive HTML + portable DSL text + written rationale) is a reusable template for a diagram-design skill: pairing a rendered visual with a portable source-of-truth text format and a short rationale write-up increases both reusability and auditability of AI-generated diagrams.
**Confidence**: med (single skill listing source, not independently verified against the skill's actual repo)

**What**: OnlineWardleyMaps (the reference open web tool for Wardley DSL) shipped WYSIWYG editing for major map elements (Feb 2026) and axis-visibility/evolution controls letting users hide either axis from the DSL (May 2026).
**Why it matters**: Confirms the diagram-as-code + WYSIWYG-editor combination (text source of truth, GUI for tweaks) is an active, still-evolving pattern outside Mermaid/D2/PlantUML too — useful if this workspace ever needs Wardley-style strategic maps as an output type.
**Confidence**: low (single aggregator search summary, no primary changelog fetched)

**What**: Multiple specialized MCP diagram servers exist as of 2026 beyond the AWS one, e.g. UML-MCP (natural-language or direct PlantUML/Mermaid/Kroki input for UML diagrams) and diagram-mcp-server (multi-cloud infra diagrams for AWS/Azure/GCP/Kubernetes), plus general "diagramming MCP servers" round-ups (Eraser.io guide) comparing platforms that support create/search/update/export of diagrams directly from an AI client with permissions and reuse (vs. one-off chat generation).
**Why it matters**: These MCP servers persist diagrams into a stateful platform with permissions/folders — a different value proposition than a stateless skill that emits a standalone HTML/SVG/PNG file each time. Worth knowing as the contrast case: this workspace's diagram-design skill intentionally optimizes for portable standalone artifacts rather than a managed diagramming platform.
**Confidence**: med (GitHub repos + an aggregator guide, not deeply vetted for activity/maintenance status)

## For This Workspace
- Consider D2 (with its native Go/Dagre and ELK.js 0.12.0 layout engine) as an optional intermediate diagram-as-code representation for auto-layout-heavy diagrams (dependency graphs, large architecture diagrams) where Mermaid/PlantUML layout is weak — worth a spike to compare output quality before adopting.
- Apply the ArcKit pattern to the diagram-design skill: for domain-specific diagram types (C4, security-matrix, DP-integration), have the skill read a condensed reference file on correct conventions before generating, rather than generating cold from the prompt alone — reduces hallucinated domain semantics.
- Adopt the "multiple synchronized artifacts per generation" pattern from the Wardley Claude Skill: when producing a branded HTML/SVG diagram, also emit a portable text/DSL source (Mermaid/D2/OWM as applicable) alongside it, so the diagram has a diffable, re-editable source of truth beyond the rendered file.
- Given the error-compounding and prompt-complexity hallucination findings, keep diagram-generation prompts short and staged (e.g., generate structure first, then style/branding pass, then validate) rather than one long combined instruction — and treat any few-shot examples used in the skill's prompts as high-risk if wrong, since one bad example can corrupt the rest of a session's outputs.

## Sources
https://architecturediagram.ai/blog/d2-diagram-language
https://updates.visual-paradigm.com/releases/vpascode-d2-diagram-support-announcement/
https://www.blog.brightcoding.dev/2026/03/09/d2-diagram-language-code-your-visuals-skip-the-drag-and-drop
https://plus.excalidraw.com/changelog
https://medium.com/@siddharthkharche/claude-ai-excalidraw-how-to-generate-instant-system-architecture-diagrams-with-mcp-11d42f610948
https://builder.aws.com/content/3Dd4PzYvNS7knkGhX5qNvtkcbkf/the-aws-diagram-mcp-server-was-deprecated-heres-the-updated-approach-using-agent-skills
https://medium.com/@charan.panthangi/why-llms-hallucinate-its-not-a-bug-it-s-the-architecture-9f4cf2a14b93
https://arxiv.org/pdf/2601.20476
https://medium.com/arckit/arckit-v4-3-0-a-complete-wardley-mapping-suite-for-ai-assisted-strategic-architecture-5848b36c0567
https://skillsmp.com/skills/dreamlab-ai-agentbox-skills-wardley-maps-skill-md
https://onlinewardleymaps.com/en
https://github.com/antoinebou12/uml-mcp
https://github.com/andrewmoshu/diagram-mcp-server
https://www.eraser.io/guides/best-diagramming-mcp-servers-in-2026
