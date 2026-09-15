# System-Diagram Research Digest (2026-09-07 through 2026-09-14)

> **Consolidated from 17 research batches by swarm (Sep 2026)**
>
> All findings sourced from files already present in `.agent-memory/topics/system-diagram/` and `.agent-memory/inbox/`. No external claims added.

---

## Executive Summary

In 2026, diagram-as-code tooling (Mermaid, D2, PlantUML, Structurizr) has matured from standalone CLI utilities into MCP-fronted services and AI-agent-callable skills. The field is splitting into three distinct diagram categories — **static architecture** (C4/boxes-and-arrows), **runtime trace visualization** (OTel/GenAI spans), and **live-derived topology graphs** (from actual execution data) — each with its own vocabulary and validation requirements. AI-assisted diagram generation is now standard, but every source converges on "generated diagrams need independent validation before being treated as fact." No formal notation standard yet exists for agentic systems specifically, though MCP and A2A protocols are emerging as distinct edge types in orchestration diagrams.

---

## Part 1: Diagram Tools & Formats — 2026 Maturity State

### Mermaid.js

- **Core capability:** Native GitHub/GitLab/VS Code rendering; Mermaid.js reached v11.16.0+ in 2026 with ~22 native diagram types.
- **C4 support:** Still experimental, no auto-layout; position via statement order only. C4-specific work still better handled by Structurizr or C4-PlantUML.
- **2026 new types:** Cynefin, Railroad, Swimlane (beta); Fishbone, Treemap (2026.1.x); Wardley Map, TreeView (2026.2.x, beta).
- **MCP integration:** Official Mermaid MCP server launched (mermaid.ai/docs/ai/mcp-server, ~9 tools: validation, PNG rendering, Mermaid Chart account integration). Supports GitHub Copilot, VS Code, Cursor, Antigravity.
- **AI angle:** Packaged as reusable agent skills (slash-command invocation); Mermaid Studio 2026.3.1+ now offers MCP tools for AI-assisted generation/validation natively.
- **LLM fluency:** Remains the highest-confidence format for LLM generation (best grammar familiarity vs. competing formats; D2 produces better layouts but LLMs are less fluent in its syntax per 2026 consensus).
- **Rendering:** Client-side via `mermaid.min.js` (standalone, offline-safe, no core telemetry per maintainer) or pre-rendered SVG via `mmdc` CLI.

### D2 (Terrastruct)

- **Layout engines:** Three swappable options — dagre (default, hierarchical), ELK (node-link with ports), TALA (purpose-built for software-architecture diagrams, paid license).
- **2026 maturity:** Native Go renderer (replaced embedded JS runtime), sketch-mode upgrade to Rough.js 4.6.6, ELK.js 0.12.0.
- **Ecosystem:** Third-party editor adoption expanding (VPasCode added D2 support Aug 2026; Inkscape extension, Mar 2026).
- **Tradeoff:** Best auto-layout quality for architecture/infra maps; no major doc platform renders D2 natively (CI step required to emit SVG).
- **Limitation:** TALA (best for architecture) is paid-license only; dagre/ELK free tiers have known layout weaknesses for complex multi-agent topologies.

### PlantUML

- **C4 support:** C4-PlantUML (v2.13.0, last updated 2026-08-26) is actively maintained, stable, no format changes. Deepest UML vocabulary (sequence, class, state diagrams) plus cloud icon packs.
- **New in 2026:** `@plantuml/core` (May 2026, browser-runnable, no Java/server), `@plantuml/mcp-js` (June 2026, Node.js MCP server, no JVM), PlantUML Editor "AI Assistant" (May 2026, OpenAI/Anthropic/GitHub Models/OpenRouter keys).
- **Validation:** CI via `-checkonly` flag; multiple 2026 frameworks converge on "narrow mixed policy" — Mermaid for markdown docs, PlantUML for formal UML, D2 for architecture maps.

### Structurizr (C4 Reference Implementation)

- **Positioning:** "Models as code" — one DSL model generates multiple C4 views (context, container, component) with consistency rules and interactive HTML output.
- **2026 evolution:** MCP server (binary v2026.06.28) offers DSL validation, parsing, inspection tools so agents can generate/critique models without violating C4 hierarchy.
- **AI advantage:** Designed as agent-friendly with built-in validation guardrails (prevents Component at Container level, etc.); explicitly marketed as stronger QA-gate than text-only diagram output.
- **Layout:** Manual, not auto (unlike Mermaid/D2) — tradeoff is deliberate consistency over automatic prettiness.

### Excalidraw

- **2026 shift:** Hand-drawn style diagrams → agent-authorable via MCP. Public API + MCP in public beta (mid-2026).
- **MCP v2.0 (2026-07-28):** 26 tools over stdio, Node ≥20, Mermaid-to-Excalidraw conversion runs locally, zero API keys.
- **Agent skill:** Claude Code / Codex-compatible Agent Skill + CLI; Autoshape tool (Shift+X) converts freehand sketches to perfect shapes.
- **2026 improvements:** Smarter auto-layout/spacing, semantic edge coloring, high-res support up to 8000px.
- **Format:** Plain JSON `.excalidraw` files — hand-drawn diagrams become diffable repo artifacts.

### Eraser.io (DiagramGPT)

- **Input flexibility:** Natural-language prompts, existing Eraser DSL, image/PDF attachments (base64, ≤10MB), **Git repos directly** (Terraform/IaC input for architecture diagrams).
- **Output:** Eraser DSL (editable text) + PNG (1–3x quality), across sequence, ERD, cloud-architecture, flowchart, BPMN, freeform types.
- **Integration:** Syncs to GitHub, embeds into Confluence/Notion; MCP server usable from Claude, Cursor, VS Code, ChatGPT.
- **Unique feature:** "Point it at a Git repo of Terraform and get an architecture diagram" path not documented for Mermaid AI, draw.io, or Excalidraw.

### Kroki (Unified Rendering API)

- **Purpose:** Single self-hostable HTTP service wrapping 30+ diagram engines (Mermaid, PlantUML, D2, GraphViz, Excalidraw, DBML, WaveDrom, C4-PlantUML, etc.) behind one consistent API.
- **Request format:** GET with deflate+base64 URL encoding, or POST with JSON/plaintext + Content-Type.
- **Distribution:** Free hosted instance (Exoscale), self-hosting via Docker.
- **Value:** Collapses "maintain N separate CLIs" problem into one container + one request format; enables "diagram as URL" embedding (MediaWiki native support).

### Database/ER Diagramming

- **DrawSQL:** NL-to-schema AI design; MySQL/PostgreSQL/SQL Server support.
- **ChartDB:** Open-source (20k+ GitHub stars), reverse-engineers live DB in ~15s via generated query (no direct connection needed), exports SQL DDL across 9+ dialects, AI-assisted schema generation, embeds into Notion/Miro/Confluence.
- **dbdiagram.io:** Code-first, DBML (plain-text source, analogous to Mermaid/D2 for architecture), remains the "boring and reliable" option.

---

## Part 2: AI-Assisted Diagram Generation Patterns

### Diagram-from-Code (LLM-driven)

1. **Swark** (VS Code extension, AGPL-3.0, ~1.7k GitHub stars): Scans a folder, builds a prompt from files, invokes GitHub Copilot via VS Code Language Model API, renders as Mermaid in markdown preview. No external API dependency.

2. **Agentic C4 Skill** (Heuel, Resilens): Claude Code / Codex-compatible skill that generates C4 views (context, container, component, deployment, sequence) from a repo, bundles into an interactive HTML explorer, stamped with generation timestamp + commit hash. Deliberately keeps a human review gate: "diagrams are auto-generated... must be validated by someone who knows the project."

3. **Amazon Bedrock AgentCore Case Study** (Q1 2026 production): Reads live .NET codebase, generates architecture diagrams, indexes into Knowledge Bases, wired into CodePipeline CI/CD for an electronic trading platform. Named, dated example of "code-to-diagram-to-CI."

### Self-Validating Loop (Agent Produces & Reviews Own Diagram)

- **Excalidraw Skill Pattern:** Agent writes Excalidraw JSON → renders to PNG via script → visually reviews own render → iterates before delivering.
- **Conventions:** Semantic color coding (fixed color = fixed meaning, e.g. "primary flow" / "warning"), left-to-right hierarchical layout, labeled arrows describing transitions.
- **Advantage:** Built-in QA gate (render-and-inspect) acts as verification rather than relying on human to check visually.

### LLM Hallucination Research (2026)

- **Error-compounding:** Wrong early token conditions everything downstream; cascading errors through full output.
- **Prompt-complexity:** Long/overly complex instructions increase hallucination rate; single bad few-shot example can "spoil the bunch" for later generations in a session.
- **Implication for diagram generation:** Keep prompts short and staged (generate structure → style → validate in separate passes); treat few-shot examples as high-risk if wrong.

### Grounded Diagram Generation (Domain Reference Pattern)

- **ArcKit v4.3.0 (Wardley Mapping):** AI-assisted commands grounded in reference material (three Wardley books condensed to reference files the AI reads before generating output). Four AI-assisted commands: value-chain decomposition, doctrine-maturity assessment, climatic-pattern analysis, gameplay selection.
- **Template:** Feed condensed domain reference material to an LLM before generating domain-specific diagrams (C4, security-matrix, DP-integration) rather than generating cold from prompt alone — reduces hallucinated domain semantics.

### "The Agent Lives With Your Diagram" (Live Canvas Pattern)

- **2026 consensus:** Instead of AI regenerating a diagram from scratch each time, MCP servers let agents read back and incrementally edit existing live canvases (Excalidraw/tldraw/Mermaid).
- **Implication:** Diagram tooling should be treated as stateful shared artifacts an agent maintains over a session, not one-shot generation.

---

## Part 3: Standardization & Protocols — Notation Gaps

### MCP (Model Context Protocol) as Diagram Edge Type

- **Status:** Near-ubiquitous across major AI frameworks/enterprise tools by 2026; now a recognizable, distinct edge type in orchestration diagrams vs. generic API calls.
- **Visual treatment:** Worth distinguishing from other integration types to communicate which integrations follow the standardized protocol (portable, tool-discoverable) vs. bespoke/one-off.

### A2A (Agent2Agent) Protocol

- **Governance:** Originated by Google (April 2025), transitioned to Linux Foundation governance in 2026. Open governance model, vendor-neutral community development.
- **Core primitives:** Agent Card (JSON capability descriptor at `/.well-known/agent.json`, RFC 8615), Task, Message, Artifact objects.
- **Task state models:** Sources disagree — one describes four-state (pending/in-progress/completed/failed, streamed via Server-Sent Events); another describes eight-state (submitted, working, input_required, auth_required, completed, failed, canceled, rejected). Neither is independently verified against the primary spec by this research.
- **Distinct layer from MCP:** A2A = horizontal agent-to-agent coordination; MCP = vertical agent-to-tool layer. Diagrams of multi-agent systems need to show BOTH layers separately.
- **Diagram standard:** No formal visual notation exists yet for A2A specifically. Published diagrams use ad-hoc layered-stack boxes + directional arrows + text labels. Scope boundaries defined textually, not symbolically.

### Four-Protocol Stack (2026 Proposed Reference Architecture)

1. **MCP** (tool access, vertical)
2. **A2A** (agent coordination, horizontal)
3. **ACP or UCP** (commerce/transactions)
4. **AI Model/Agent Runtime** (base layer)

Each protocol maps to a distinct diagram layer. Framed as emerging/proposed, not yet adopted standard.

### OTel (OpenTelemetry) GenAI Semantic Conventions

- **Status:** v1.41+, moved to dedicated repo as v1.42.0 (June 2026); still experimental/pre-1.0.
- **Span types:** `invoke_agent` (agent reasoning, kind INTERNAL for local/CLIENT for remote), `execute_tool` (tool calls, `gen_ai.tool.name` required), `chat` (LLM calls, token-usage attributes), `invoke_workflow` (predetermined execution).
- **Distinction:** `invoke_agent` = autonomous/adaptive reasoning; `invoke_workflow` = scripted step.
- **MCP trace attributes:** `mcp.method.name`, `mcp.session.id`, `jsonrpc.request.id` let both calling agent and MCP server propagate W3C Trace Context so server execution nests under client call in one unified trace.
- **Tooling:** Major observability vendors (Datadog, Honeycomb, New Relic) already support; frameworks (LangChain, CrewAI, AutoGen, AG2) emit compliant spans natively or via instrumentation packages.

### Notation Gaps

- **Finding:** No single universal notation standard exists yet for agentic-system diagrams as of Sep 2026. Field is converging on shared *elements* (decision loops, tool registries, memory stores, trust boundaries) rather than formal grammar like UML/C4.
- **Diagram-as-code tools** (Mermaid, D2, PlantUML) remain dominant but none has built-in agentic features. D2's best layout (TALA) requires paid license; Mermaid "cannot pin node positions or fine-tune spacing"; PlantUML's "auto-layout can produce awkward results for complex diagrams."
- **Consequence:** Agentic-protocol diagramming is pre-standardization in 2026; teams should define their own legend/convention and document it alongside diagrams, not assume an existing one exists.

### Recommended Agent-Diagram Elements

- **Core component vocabulary:** Orchestrator/planner, tool registry, sub-agents/specialists, human-in-the-loop gates, state/checkpoint store, guardrail/evaluation layer.
- **Required edge types:** Tool calls, agent-to-agent delegation/handoff, trust boundaries, decision/feedback loops.
- **Memory as subsystem:** Durable stores, retrieval policy, context-assembly step, write-back path (often accessed via MCP rather than direct DB edges).
- **Failure pathways:** Error/guardrail paths as architecturally significant as main flow.

---

## Part 4: Runtime & Trace Visualization

### OpenTelemetry + OpenInference (Common Trace Schema)

- **Convergence:** Agent observability platforms (Arize AX/Phoenix, LangSmith, Langfuse, Braintrust) converged on OTel/OpenInference as common trace schema.
- **Advantage:** Decouples "how a diagram is drawn" from "which agent framework produced the trace." Native framework adapters normalize spans/attributes/events.
- **Three diagram categories distinct:** (1) Static architecture (C4/MCP/A2A); (2) Runtime trace visualization (OTel-GenAI span trees, waterfalls); (3) Live-derived topology graphs (from actual execution).

### LangGraph + LangSmith Pattern

- **Static + live together:** LangSmith's graph view shows conceptual agent graph (nodes/edges = possible flow) overlaid with actual execution's spans/generations, making span hierarchy explicit as run steps through.
- **LangGraph model:** Nodes (processing steps), edges (transitions), shared mutable state persists across graph. Auto-renders to Mermaid.

### Langfuse (Self-Hosted Alternative)

- **MIT-licensed, OpenTelemetry-based:** Self-hostable alternative to LangSmith (hosted, LangChain-ecosystem-tied) or Arize (enterprise).
- **Agent Graphs feature** (shipped July 2026): Two rendering modes — **Aggregated** (repeated steps collapsed into one node with run counter, loops as cycles) and **Expanded** ("as it ran," every call its own node, loops unrolled into DAG).
- **Auto-inference:** From trace observation timing/nesting, no manual modeling required.

### swarm-test (Live Topology from Real System)

- **Tool:** Open-source CLI (PyPI `swarm-test`), renders actual multi-agent system's dependency graph as interactive force-directed D3 diagram.
- **Features:** Visually flags single points of failure (pulsing red), sortable health/redundancy tables, severity-grouped findings, exports topology to Mermaid/DOT/PNG.
- **Scope:** Works across CrewAI/LangGraph/AutoGen/custom orchestrators. GitHub Action included to gate PRs in CI.
- **Value:** "Diagram from your real topology, not a hand-drawn one, so it stays accurate."

### LaunchDarkly Agent Graphs

- **Approach:** Overlays live performance metrics (latency, invocation counts, tool-call counts) directly onto workflow-graph nodes.
- **Merging layers:** Combines what prior research treated as two separate categories (static architecture + runtime trace) into single artifact type with annotated performance data.

### Conductor Dashboard

- **Interactive DAG:** Real-time/live streaming updates, in-browser human-approval gates, plus terminal-UI ("Fleet Manager TUI") for same data outside browser.
- **Analog to this workspace:** Precedent for "board.json → live DAG" upgrade of static snapshot dashboard.

### Gap: OTel → Mermaid Converter

- **Status (Sep 2026):** No mature, off-the-shelf tool converts OpenTelemetry agent-execution spans directly into Mermaid sequence diagram.
- **Implication:** Any workspace wanting "auto-diagram my last swarm run as Mermaid" must write the OTel→Mermaid translation layer itself (feed trace JSON to LLM prompt or custom script).

---

## Part 5: Architecture Diagram Drift & Governance

### Diagram Staleness as Named Problem

- **Metric:** ~68% of teams reportedly run on architecture docs >6 months stale (Thoughtworks, per ArchitectureDiagram.ai blog).
- **Causal link to AI:** Agents calibrate suggestions to a system architecture that no longer exists; stale diagrams actively degrade AI coding agent output quality.

### Architecture Fitness Functions (Drift Prevention)

- **Pattern:** Automated CI tests (ArchUnit for Java, NetArchTest for .NET, dependency-cruiser for JS/TS) assert structural rules (allowed dependency directions, layer boundaries) and fail build on violation.
- **Advantage:** Drift-*prevention* mechanism that doesn't require a diagram-generation tool at all — encodes diagram's rules as executable tests.
- **Ratchet variant:** Only block *new* violations so existing drift can shrink over time but never silently grow.
- **Durable:** Survive after meetings end and diagrams go unmaintained (explicit 2026 positioning).

### Lightweight Process Fix (No New Tooling)

- **Pattern:** Canonical `ARCHITECTURE.md` (diagram-as-code source) in repo root, PR checklist item to update it, rotating quarterly diagram-owner audits.
- **Staleness checklist:** Deprecated services still shown, missing integrations, diagrams >90 days old, AI agents making false assumptions from stale docs.

### AI-Assisted Regeneration Trade-off

- **Speed:** NL-to-diagram regeneration ~30 seconds (e.g., ArchitectureDiagram.ai).
- **Bottleneck:** "The description, not the drawing" — if regenerating is cheap, staleness is a discipline failure, not a tooling gap.
- **Status:** Fully automated "codebase vs. architecture description" drift detection explicitly stated as "not yet mature/automated" as of 2026.

### Three Production Topology Patterns (Named Vocabulary)

1. **Supervisor/hierarchical** — central authority delegates to workers.
2. **Orchestrator-worker** (~70% of production deployments per mid-2026 survey) — PO+swarm model maps to this.
3. **Swarm** (peer agents, no central control).

---

## Part 6: Accessibility & Quality

### SVG Accessibility (WCAG 2.2)

- **Criteria:** Non-text contrast (1.4.11), keyboard operability (2.1.1), name/role/value (4.1.2).
- **Gap:** SVGs not accessible by default; requires manually adding `aria-labelledby`/`aria-describedby`, semantic grouping, deciding informative vs. decorative.
- **Status:** No mainstream diagram tool auto-generates accessible SVG; ARIA labeling and decorative-vs-informative tagging must be added by hand.
- **Sketch styling:** Sketchy/hand-drawn SVG turbulence-filter techniques fine for editorial content, explicitly NOT recommended for technical documentation.

### LLM Diagram Understanding Benchmarks

- **SADU benchmark** (154 diagrams, 2,431 QA pairs): Best VLM (gemini-3-flash-preview) reaches ~70.18% accuracy; gpt-4o-mini scores ~17.77%. Tests ability to *read* and reason about architecture diagrams.
- **SAKE benchmark** (2,154 expert-curated MCQs on architectural knowledge, not diagram images): LLMs score 89–94% on architecture *concepts*.
- **Gap implication:** Models know architecture theory far better than they can visually parse an actual diagram. Do NOT rely on a vision-capable model to "read" and judge a rendered diagram; verify against the text source (Mermaid/D2/DSL) instead.

### Generated Diagram Validation Requirements

- **Pattern across all sources:** Generated diagrams have "common problems" (named topic at May 2026 BCS event on C4/Structurizr/AI); treated as failure-prone by default.
- **Validation approach:** "Unverified, needs human review" stamping; provenance (commit hash, timestamp); explicit review gate before treating as fact.
- **Structurizr guard rails:** MCP server validates that generated C4 models don't break hierarchy (e.g., Component at Container level).

---

## Part 7: Workspace Recommendations

### If Building a Living Agent Topology Diagram

1. **Data source:** Choose between OTel-style event emission (timestamps + nesting) or read state directly from orchestrator (LangGraph model).
2. **Rendering:** Langfuse Aggregated/Expanded pattern (default collapsed with run counters, drill-down expanded view) avoids "40 identical cards" anti-pattern.
3. **Export:** If Mermaid output is needed, use `swarm-test` pattern (real topology → Mermaid/DOT/PNG) rather than LLM-generated Mermaid.

### For Static Architecture Diagrams of the Harness Itself

1. **Models-as-code approach:** Prefer Structurizr DSL (one model → multiple views that stay consistent) over single hand-authored Mermaid file.
2. **Validation:** Before trusting any AI-generated diagram, run through validation step (check every node maps to real file/directory/service that exists).
3. **QA gate:** Extend "gate on exit code, not intent" principle to diagrams — stamp all generated diagrams with commit hash + timestamp, explicitly mark "unverified," require human sign-off before treating as ground truth.

### Mermaid vs. D2 Decision

- **Default:** Mermaid for in-repo docs (best LLM fluency, native GitHub rendering).
- **Exception:** D2 with TALA layout for architecture maps where Mermaid's dagre layout mangles clean topology (commit rendered SVG next to .d2 source since no doc platform renders D2 natively).

### Diagram Legend (Write Once, Use Everywhere)

- **Scope:** Document this workspace's own legend covering:
  - Tool-call edge (MCP)
  - Agent-to-agent delegation/handoff edge (A2A)
  - Trust boundary (autonomous vs. human-approved)
  - Decision loop / conditional routing
  - Semantic color meanings (fixed color = fixed meaning rule)
  - Error/guardrail pathway notation
  - Memory subsystem styling

### If Rendering OTel Traces as Diagrams

- **Span naming:** Use OTel GenAI vocabulary (`invoke_agent`, `execute_tool`, `chat`, `invoke_workflow`, `mcp.*` attributes) rather than custom event names. Gives path to reuse existing OTel-compatible viewers instead of building bespoke trace renderer.
- **Distinguish:**  Deterministic QA-gate steps (`bash -n`, `test -f`) as workflow/scripted nodes; PO delegation/escalation decisions as agent/reasoning nodes.

### CI/QA Gate Pattern (Inherited from Diagram-as-Code Tools)

- **Syntax validation:** `mmdc -i x.mmd -o /dev/null` (Mermaid), `plantuml -checkonly` (PlantUML), `d2 validate`/fmt (D2).
- **Structural validation (if Structurizr):** MCP server inspection tools (no Component at Container level, etc.).
- **Visual-derived validation:** Skip "have a model read the rendered picture and judge it" per SADU benchmarks (~70% best-case accuracy). Instead, validate against text source.

### PO+Swarm Model Classification

- **Explicit terminology:** "Orchestrator-worker" topology (not "swarm" in peer-agent sense per 2026 taxonomy). Current `.agent-dashboard` naming and "swarm subagents" vocabulary risks miscommunicating topology as peer-to-peer.
- **Diagram vocabulary:** Hierarchical, orchestrator (PO) delegates to workers (subagents). Visually distinct from peer-swarm (all agents equal, no central control) and supervisor (tightly controlled workers).

---

## Part 8: Tool Policy Summary (Narrow, Durable)

| Category | Recommended Tool | Rationale | Rendering |
|----------|-----------------|-----------|-----------|
| **In-repo docs / README** | Mermaid fenced blocks | Native GitHub, best LLM fluency, no build step | Client-side `mermaid.min.js` or pre-rendered SVG |
| **Complex architecture maps** | D2 with dagre/ELK | Better auto-layout than Mermaid; vendor `d2` binary | Pre-rendered SVG in CI, commit alongside .d2 |
| **C4-model rigor (if needed)** | Structurizr DSL + MCP validation | Single model → multiple views, AI-friendly with guardrails | Rendered to HTML via Structurizr CLI |
| **Formal UML** | C4-PlantUML (stable) or PlantUML core | Deep UML support, C4-compatible; PlantUML now has no-Java options | Pre-rendered or CI validation via `-checkonly` |
| **Hand-drawn / collaborative** | Excalidraw (MCP, local-first) | MCP v2.0 compatible, zero API keys, JSON format diffable | Standalone or embedded in FigJam |
| **Multi-database schema** | ChartDB (open-source) or dbdiagram.io (DBML) | Reverse-engineer live DB, export DDL across 9+ dialects | Exported DDL stays in git as source of truth |
| **Unified rendering backend** | Kroki (self-hosted Docker) | 30+ engines behind one API, no per-tool CLI maintenance | PNG/SVG/PDF output from single container |

---

## Part 9: Sources (By Research Date & Topic)

### 2026-09-07: Tools Overview
- Mermaid C4 experimental support, offline rendering (`mermaid.min.js`, `mmdc`), D2 vs PlantUML vs Mermaid comparison, Structurizr 2026.07.03 state, agent-driven generation pattern, Excalidraw MCP/JSON format.

### 2026-09-08 Batch (Tools & MCP Servers)
- Mermaid MCP server (official), PlantUML MCP/core, draw.io AI generation docs, Mermaid new diagram types (fishbone, venn, wardley, treeview, event modeling, cynefin, railroad, swimlane), SVG accessibility (WCAG 2.2, sketchy-filter guidance), "diagram as code" in CI pattern, WCAG 3.0 draft status.

### 2026-09-08 (D2 & Excalidraw & Wardley)
- D2 native Go renderer, ELK.js 0.12.0 layout, Excalidraw MCP improvements (autoshape, semantic coloring, high-res), AWS Diagram MCP deprecation (replaced by Skills), ArcKit v4.3.0 (grounded diagram generation), LLM hallucination research (error-compounding, prompt-complexity), Wardley Mapping Claude Skill (interactive React + OWM DSL + commentary).

### 2026-09-09 Batch 2 (Excalidraw, D2 TALA, Amazon Case Study)
- Excalidraw Public API beta, excalidraw-diagram skill (visual pattern library), D2 TALA layout engine for architecture, Amazon Bedrock AgentCore case study (live .NET codebase → diagrams → searchable KB + CodePipeline).

### 2026-09-09 Batch 3 (Figma, Mermaid MCP, draw.io, C4-PlantUML, Drift)
- Figma `generate_diagram` MCP tool (Mermaid → FigJam, 6 types), Mermaid official MCP server docs, draw.io official AI generation spec (uncompressed XML, no comments, relative coords), C4-PlantUML v2.13.0 (maintained, no format changes), "architecture diagram drift" thesis (68% teams >6 months stale, AI agents calibrate to stale systems), diagram drift mitigation (NL regeneration ~30s, PR checklist, quarterly audits), sketchy SVG not recommended for technical docs.

### 2026-09-09 Batch 4 (Benchmarks, Figma, LikeC4, IcePanel)
- SADU benchmark (70.18% best VLM accuracy on diagram understanding), SAKE benchmark (89–94% LLM accuracy on architectural concepts), Figma generate_diagram MCP, LikeC4 DSL (AI-agent MCP/API exposure), IcePanel "death of architecture diagrams" (model as source of truth, diagrams are views, CI-driven freshness).

### 2026-09-09 (Eraser, Kroki, ER Tools)
- Eraser DiagramGPT (Terraform/IaC input, DSL output), Kroki unified 30+ engines HTTP API (deflate+base64 URL, POST JSON), MediaWiki Kroki extension, DrawSQL (NL-to-schema), ChartDB (live DB reverse-engineer ~15s, DDL export 9+ dialects), dbdiagram.io (DBML code-first).

### 2026-09-10 (A2A Gaps, Graph Engineering, Galileo)
- OTel trace → Mermaid converter gap (unfilled, recognized want in Jaeger/Tempo), A2A protocol Linux Foundation governance v1.0.1 (May 2026), Agent Card (`/.well-known/agent.json`), "graph engineering" terminology (TrueFoundry, explainx.ai), Galileo Agent Graph visualization, IETF draft Multi-Agent Delegation (draft-sato-soos-mad-03, December 2026 expiry).

### 2026-09-10 (Fitness Functions & Drift Detection)
- Architecture fitness functions (ArchUnit, NetArchTest, dependency-cruiser), ~68% teams with stale docs (Thoughtworks), ratchet pattern (block new violations only), lightweight process (ARCHITECTURE.md + PR checklist + quarterly owner audits), AI regeneration speed (~30s) as friction reducer, Claude Code hub-and-spoke delegation model, "no distinct diagram convention for agent delegation yet" (teams reuse flowchart/sequence tooling).

### 2026-09-10 (Trace-Driven Visualization)
- OpenTelemetry + OpenInference as common trace schema (Arize, LangSmith, Langfuse, Braintrust), LangGraph + LangSmith (static topology + live execution), Langfuse (MIT, OpenTelemetry-based, LangGraph native graph view), Conductor dashboard (interactive DAG, live streaming, TUI), "no off-the-shelf OTel→Mermaid converter" gap, Mermaid as distributed agent skill (slash-command invocation).

### 2026-09-11 (A2A Diagramming & Protocol Visualization)
- A2A = horizontal (agent-to-agent), MCP = vertical (agent-to-tool), Linux Foundation governance (confirmed), Agent Card state models (four-state: pending/in-progress/completed/failed streamed via SSE; eight-state: submitted/working/input_required/auth_required/completed/failed/canceled/rejected — sources disagree, unverified against primary spec), "no formal notation yet for A2A" (ad-hoc layered stacks + arrows + text labels), MCP/A2A/ACP/UCP four-protocol stack proposal, Excalidraw skill self-validation loop (generate JSON → render → visually inspect → iterate), semantic color meanings (fixed color = meaning), D2/Mermaid/PlantUML layout limitations (TALA paid-only, Mermaid minimal layout control, PlantUML awkward for complex).

### 2026-09-11 (Agentic-System Conventions)
- No universal notation standard yet; converging on shared elements (decision loops, tool registries, memory stores, trust boundaries), MCP as distinct edge type, LangGraph nodes/edges/shared-state model (auto-renders to Mermaid), required diagram elements (decision loops, trust boundaries, failure pathways, core component vocabulary: orchestrator/planner, tool registry, sub-agents, human gates, state store, guardrail layer), memory as subsystem (durable stores + retrieval policy + context assembly + write-back).

### 2026-09-11 v2 (MCP, Excalidraw, Azure, A2A Governance)
- Excalidraw MCP v2.0 (2026-07-28, 26 tools, Node ≥20, Mermaid-to-Excalidraw conversion local), Azure Architecture Diagram Builder MCP `render_diagram` tool (SVG with grouped zones, cost badges), "agent lives with your diagram" (MCP servers let agents edit live canvases, not regenerate from scratch), Mermaid vs D2 LLM fluency consensus (Mermaid stays default), A2A governance primary source (Linux Foundation, no "v1.0" in spec — described as "evolving"; corrected from aggregator sources), no diagram-as-code standard yet for A2A, vendor-specific observability dashboards only (Galileo Agent Graph).

### 2026-09-11 (Code-Driven Diagram Generation)
- Swark (VS Code extension, ~1.7k stars, AGPL-3.0, scans folder → Copilot → Mermaid preview), agentic C4 skill (Heuel, interactive HTML explorer, commit hash + timestamp stamp, "must be validated by someone who knows project"), "C4 Models Are Brilliant. AI Coding Is Breaking Them" (AI-agent code changes outpace manual diagram updates), Structurizr "models as code" with source-control drift detection, fitness functions as "more durable than diagrams," Mermaid Studio 2026.1.x+ (MCP tools for AI generation/validation), arXiv papers on diagram generation (Paper2SysArch, Text2Arch, Query2Diagram, Code2UML) — titles only, PDFs not confirmed.

### 2026-09-12 (Topology Graphs & Live Derived)
- Langfuse Agent Graphs (Aggregated mode: steps collapse with counters, loops as cycles; Expanded: every call its own node, loops unrolled into DAG; shipped July 2026), swarm-test CLI (real system topology as force-directed D3, single points of failure flagged red, exports Mermaid/DOT/PNG, GitHub Action for CI gate), LaunchDarkly agent graphs (performance metrics overlaid on nodes), three production patterns (supervisor/hierarchical, orchestrator-worker ~70%, peer-swarm), AgenticSwimlanes.com (BPMN 2.0 swimlanes, vendor-neutral reference, April 2026).

### 2026-09-12 (OTel GenAI & C4 Architecture Skill)
- OTel GenAI semantic conventions v1.41+ (moved to dedicated repo v1.42.0, June 2026), span types (`invoke_agent`, `execute_tool`, `chat`, `invoke_workflow`), MCP trace attributes (`mcp.method.name`, `mcp.session.id`, W3C Trace Context propagation nests server-side under client-side), major observability vendors + frameworks support (Datadog, Honeycomb, New Relic; LangChain, CrewAI, AutoGen, AG2), agentic C4 skill (Claude Code, C4-PlantUML, local interactive HTML explorer, timestamp + commit-hash stamps, "not a decision-maker, helps humans inspect").

### 2026-09-14 (Models-as-Code & Validation)
- Structurizr MCP server v2026.06.28 (DSL validation, prevents component-at-container-level violations), models-as-code (one model → multiple consistent views, diff-friendly, version-controllable, well-suited to LLMs), D2 three layouts (dagre default, ELK, TALA architecture-specific), Inkscape extension (Mar 2026), VPasCode support (Aug 2026), Mermaid 2026.3.1 (Cynefin, Railroad, Swimlane, inline docs, architecture-specific formatting), AI-diagram value in format conversion + code-to-diagram (not prose-to-diagram), BCS May 2026 event on C4/Structurizr/AI "common problems with AI-generated diagrams."

