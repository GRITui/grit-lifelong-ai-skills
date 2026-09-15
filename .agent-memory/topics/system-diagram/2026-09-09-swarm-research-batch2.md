> ✅ QA-gated by PO batch 2026-09-09 · spot-check: AWS Bedrock AgentCore case study (interdealer broker, code-to-diagram-to-CI, 20 repos / 140+ diagrams weekly) confirmed via direct fetch of the AWS ML blog post ✓

## TL;DR
- Excalidraw's Public API + MCP is now in public beta (mid-2026), enabling AI tools (e.g. GPT-5.5-class models) to generate/edit Excalidraw scenes programmatically — a step up from earlier community-only MCP wrappers.
- A dedicated "excalidraw-diagram" Claude Code agent **skill** (coleam00, via explainx.ai) already exists publicly: it generates Excalidraw JSON using a visual pattern library (fan-out, convergence, timelines, trees, cycles) and a "research mandate" step (look up real specs/APIs/event names before drawing) instead of guessing layout.
- D2 remains actively maintained and is gaining third-party editor integrations (e.g. VPasCode added full D2 support, Aug 2026); its three pluggable layout engines (dagre, ELK, TALA — TALA specifically built for software-architecture diagrams) are a differentiator vs. Mermaid's single layout engine.
- Amazon Bedrock AgentCore has a documented production pipeline (running since Q1 2026 at a real interdealer broker) that reads a live .NET codebase, generates architecture diagrams, and keeps them searchable/current via CodePipeline — a concrete, named production example of "code-to-diagram-to-CI" beyond the single blog post found in prior research.
- Across sources, the field still treats generated diagrams as a draft/starting point, not ground truth — every 2026 review of AI diagram tools (this batch and prior batches) converges on "verify against the real system," reinforcing this repo's QA-gate-before-topics model.

## Findings

1. **What**: Excalidraw's Public API and MCP server are now in public beta (as of mid-2026), explicitly positioned for AI-tool integration (scene creation/editing by external models), not just human collaborative drawing.
   **Why it matters**: Confirms the Excalidraw MCP path flagged as "med confidence" in the 2026-09-08 batch is maturing into an officially-supported integration surface, not just community hacks — lowers risk of relying on it for hand-drawn-style diagram output.
   **Confidence**: med (WebSearch synthesis; not independently fetched from Excalidraw's own changelog).

2. **What**: A public Claude Code **skill** named "excalidraw-diagram" (author coleam00, indexed on explainx.ai/toolhunter.cc) generates Excalidraw JSON directly from natural-language prompts, using a named visual-pattern library (fan-out for one-to-many, convergence for aggregation, timelines for sequences, trees, cycles) plus a "research mandate" requiring the agent to look up real specs/APIs/data formats before laying out a technical diagram.
   **Why it matters**: This is functionally a sibling/competitor to this workspace's own `diagram-design` skill, but targets Excalidraw JSON output instead of HTML/SVG/PNG. Worth a closer look (or even adoption of its pattern-library naming) since it's a working, published skill rather than vendor marketing.
   **Confidence**: med (fetched the skill's description page directly, but did not inspect its actual SKILL.md/source).

3. **What**: D2 (Terrastruct) ships three pluggable layout engines — dagre (default, hierarchical), ELK (node-link with ports), and TALA (purpose-built for software-architecture diagrams) — plus a built-in autoformatter and multi-error-tolerant parser. Third-party editors (e.g. VPasCode, Aug 2026) are now adding native D2 rendering support alongside their own formats.
   **Why it matters**: TALA's architecture-specific layout is a concrete technical reason to prefer D2 over Mermaid specifically for *software/system architecture* diagrams (vs. flowcharts/sequence diagrams, where Mermaid is fine) — a more precise selection rule than the prior "D2 for code-first diagrams" generalization.
   **Confidence**: med (WebSearch synthesis of multiple secondary sources; D2's own GitHub releases page was listed in search results but not fetched directly).

4. **What**: Amazon published a named, dated (Q1 2026 production) case study: a global interdealer broker built an "agentic architecture documentation" pipeline on Amazon Bedrock AgentCore that analyzes a live .NET codebase, auto-generates architecture diagrams, and indexes them into Bedrock Knowledge Bases, wired into existing AWS CodePipeline CI/CD for an electronic trading platform.
   **Why it matters**: Upgrades the "code-to-diagram in CI" pattern from the prior batch's single low-confidence blog post (Codex CLI, one author) to a named vendor case study with a real company and a production date — still one story, but a materially stronger source (AWS ML blog vs. personal blog).
   **Confidence**: med (found via WebSearch snippet quoting the AWS blog title/summary; the full post at aws.amazon.com/blogs/machine-learning/from-code-to-diagrams-... was not directly fetched in this pass).

5. **What**: 2026 "state of AI coding agents" commentary explicitly names the pattern "Claude Code skills + MCP servers (Mermaid MCP, Diagram MCP, C4 Architecture plugin) read a repository and generate diagrams automatically, with a CI hook keeping them in sync with the codebase" as an established, if still-emerging, workflow — not hypothetical.
   **Why it matters**: Corroborates (via a second, independent 2026 source) the "architecture as code with CI-based drift detection" pattern already identified in the 2026-09-08 batch; strengthens confidence that this is a real, replicable pattern rather than a one-off.
   **Confidence**: low-med (aggregator/roundup article, not a primary source or hands-on verification).

6. **What**: Frontier-model commentary for 2026 states that current-generation models (referenced as "Claude Opus 4.7 / GPT-5.1"-class) can ingest an entire repository and propose architecture changes grounded in the actual codebase, going beyond just rendering a diagram from a description to reasoning about the system's actual structure first.
   **Why it matters**: Suggests the near-term direction for a diagram-generating agent in this workspace is not "prompt to Mermaid" but "read the repo, then diagram what's actually there" — matches this repo's own PO+swarm model where swarms are expected to ground claims in real files, not just describe intent.
   **Confidence**: low (single roundup article characterizing capability; not independently tested against real repo-reading behavior in this pass).

## For This Workspace
- Evaluate the public "excalidraw-diagram" Claude Code skill (coleam00) as a reference or drop-in alternative when a task specifically wants hand-drawn-style, Excalidraw-native output — compare its pattern-library naming (fan-out/convergence/timeline/tree/cycle) against this repo's own `diagram-design` skill's terminology so PO/swarm prompts use consistent vocabulary either way.
- When picking a tool for this repo's own architecture diagrams (PO+swarms+board.json+n8n), prefer D2 over Mermaid specifically if the diagram is a *software/system architecture* view — D2's TALA layout engine is purpose-built for that, whereas Mermaid is better suited to flowcharts/sequence/state diagrams already used elsewhere in this workspace.
- If/when a swarm is tasked with auto-generating a diagram of this repo's own structure, borrow the "research mandate" idea from the excalidraw-diagram skill: require the agent to actually read `.agent-dashboard/board.json`, the topic directory tree, and `.claude/agents/` before drawing, rather than diagramming from memory of what the harness "should" look like — directly enforces this repo's own recall-before-work rule (Step 1 in CLAUDE.md) applied to diagramming specifically.
- The AWS Bedrock AgentCore case study (code -> diagram -> CI/CD -> searchable knowledge base) is a template worth revisiting if this workspace ever wants its own diagrams to be queryable/searchable rather than just static files under `.agent-memory/topics/system-diagram/` — not urgent, but worth a follow-up research pass once/if diagram volume grows.

## Sources
https://plus.excalidraw.com/changelog
https://diagrammingai.com/docs/guide/excalidraw-editor
https://kurtis-redux.medium.com/let-ai-draw-our-flowcharts-i-tried-a-few-excalidraw-mcp-options-e9445c1a4b73
https://toolhunter.cc/tools/excalidraw-diagram-skill
https://explainx.ai/skills/coleam00/excalidraw-diagram-skill/excalidraw-diagram
https://architecturediagram.ai/blog/d2-diagram-language
https://www.blog.brightcoding.dev/2026/03/09/d2-diagram-language-code-your-visuals-skip-the-drag-and-drop
https://updates.visual-paradigm.com/releases/vpascode-d2-diagram-support-announcement/
https://github.com/d2lang/d2
https://aws.amazon.com/blogs/machine-learning/from-code-to-diagrams-agentic-architecture-documentation-with-amazon-bedrock-agentcore/
https://medium.com/@dave-patten/the-state-of-ai-coding-agents-2026-from-pair-programming-to-autonomous-ai-teams-b11f2b39232a
https://www.metacto.com/blogs/leveraging-ai-for-system-design-and-architecture-decisions
