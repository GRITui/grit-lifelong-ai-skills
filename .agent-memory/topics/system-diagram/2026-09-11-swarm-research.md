> ✅ QA-gated by PO 2026-09-11 · spot-check: Swark repo is AGPL-3.0, 1.7k stars/106 forks, uses GitHub Copilot via VS Code Language Model API ✓

## TL;DR
- LLM-driven "diagram from code" tooling has moved from novelty to a small ecosystem: VS Code extensions (Swark), IDE-integrated diagram languages (Mermaid Studio, JetBrains 2026.2), and agent "skills" (Claude Code / Codex C4 skills) all now generate diagrams directly from a repo, not from hand-written descriptions.
- The C4 model is being explicitly re-engineered for AI-coding workflows: practitioners report that fast, AI-driven code churn breaks manually-maintained C4 diagrams, and the emerging fix is agent skills that regenerate diagrams on demand rather than humans updating them.
- Structurizr (the C4 reference "diagrams as code" tool) is being used less as a static rendering tool and more as a drift-detection layer, pairing DSL models with source-control integration.
- Fitness functions continue to be framed as the durable alternative to diagrams for architecture governance — "automated architecture tests" that run in CI and fail the build on violation, rather than documentation that can silently go stale.
- Human-in-the-loop review is a deliberate design choice in the newest agentic diagram skills (e.g. Heuel's c4-diagrams skill) — they auto-generate but explicitly warn diagrams must be validated by someone who knows the project, and stamp diagrams with commit-hash/timestamp provenance rather than claiming full automation.

## Findings

**What:** Swark (VS Code extension, AGPL-3.0, ~1.7k GitHub stars / 106 forks per its repo page) generates architecture diagrams from source by scanning a selected folder, building a prompt from the retrieved files, invoking GitHub Copilot via VS Code's Language Model API, and rendering the result as a Mermaid diagram in a markdown preview.
**Why it matters:** It's a concrete, shipped example of the "LLM reads repo → diagram-as-code output" pipeline with no external API dependency (code stays within GitHub Copilot), which is the pattern other tools in this space are converging on.
**Confidence: high** (sourced directly from the project's GitHub README)

**What:** Stephan Heuel (Resilens) published an "agentic skill" (`c4-diagrams`, built on C4-PlantUML) for Claude Code/Codex that renders system-context, container, component, deployment, and sequence C4 views from a repo and bundles them into a single interactive HTML explorer, tagged with generation timestamp and commit hash.
**Why it matters:** It's a working template for "skills that generate diagrams" applicable directly to this workspace's own skill-pipeline model — it packages instructions/scripts/templates as a reusable local workflow rather than a one-off prompt, and deliberately keeps a human review gate ("diagrams are auto-generated... must be validated by someone who knows the project") instead of claiming autonomous sync.
**Confidence: high** (sourced directly from the author's blog post)

**What:** An ITNEXT piece ("C4 Models Are Brilliant. AI Coding Is Breaking Them.") frames the core 2026 problem as: AI-agent-driven code changes now land in large batches, and no one manually updates architecture diagrams to match — the industry response is diagrams that regenerate from the "living codebase" automatically rather than being hand-maintained.
**Why it matters:** This directly names the failure mode this workspace should design against: diagrams drifting from an AI-agent-modified codebase faster than a human can keep up.
**Confidence: med** (summarized from search snippet of the article; not independently fetched in full)

**What:** Structurizr, Simon Brown's C4 reference implementation, is described (per a 2026 architecture-tools roundup) as a "models as code" system where a single Structurizr DSL model renders multiple diagram types, supports flow-step annotations for runtime interactions, and integrates with source control for drift detection.
**Why it matters:** Reinforces the "one model, many views" principle (consistent with C4's own philosophy) as the preferred alternative to maintaining several disconnected diagram files — relevant if this workspace consolidates its own diagram sources.
**Confidence: med** (from search-result summary of Catio's "Best Software Architecture Tools in 2026" post; not independently fetched)

**What:** Mermaid Studio's 2026 release notes show incremental but steady tooling investment: 2026.1.x added full support for all 22 native Mermaid diagram types plus MCP tools for AI-assisted diagram generation and validation; 2026.2.x added a free "Mermaid Studio Core" edition, a visual flowchart editor, and a class-diagram overhaul (inline docs, inlay hints, structure view); 2026.3.3 added railroad-diagram language support for JetBrains 2026.2 compatibility.
**Why it matters:** Mermaid now has native MCP tool support for AI-assisted generation/validation — meaning agent-driven Mermaid diagram creation and correctness-checking can be delegated to first-party tooling rather than ad hoc LLM prompting.
**Confidence: med** (from search-result summaries of mermaidstudio.dev "what's new" pages; not independently fetched, but titles/version numbers are consistent and specific)

**What:** Fitness-function framing in 2026 sources (Medium/platformtoolsmith/architectviewmaster posts) consistently describes fitness functions as executable, CI-integrated architecture checks that "fail the build when architectural rules are violated — before code reaches the main branch," explicitly positioned as more durable than diagrams because they "survive after meetings are ended or diagrams that are or are not maintained."
**Why it matters:** Confirms the existing workspace note on fitness functions (2026-09-10 batch) is still the dominant framing a year on — diagrams are for human comprehension, fitness functions are for enforcement, and the two should be treated as complementary rather than either one substituting for the other.
**Confidence: med** (search-result summary across multiple blog posts; none individually fetched in full)

**What:** Multiple 2026 arXiv papers target LLM-driven diagram/architecture generation as an active research area: Paper2SysArch (structure-constrained system architecture generation from scientific papers), Text2Arch (a dataset for generating scientific architecture diagrams from NL descriptions), Query2Diagram (answering developer queries with UML diagrams), and Code2UML (agentic LLMs with context engineering for scalable software visualization, using specialized agents to transform structured intermediate representations into UML).
**Why it matters:** Signals the field is moving from single-prompt diagram generation toward structured intermediate representations and multi-agent pipelines for diagram fidelity — relevant if this workspace wants more reliable diagram output than a single LLM call.
**Confidence: low** (titles/topics only, from search snippets; PDF fetch of Code2UML failed to render as text so no verbatim figures could be confirmed — do not cite specific accuracy numbers from these papers without a follow-up fetch)

## For This Workspace
- Adopt the "skill + human review gate + provenance stamp" pattern from Heuel's c4-diagrams skill: any diagram-generation skill added to `.agent-harness/tools/` should stamp output with commit hash + generation timestamp and carry an explicit "unverified, needs human review" marker, matching this workspace's existing QA-gate philosophy (never treat AI-generated diagrams as auto-verified truth).
- Treat diagrams and fitness functions as two separate, non-substitutable outputs: if/when this workspace builds an architecture-fitness-function tool (per the existing 2026-09-10 research), do not let it double as the diagram source — keep diagram generation (human comprehension) and fitness functions (CI enforcement) as separate pipelines per the "diagrams go stale, fitness functions don't" argument above.
- If this workspace generates Mermaid diagrams via agents, check whether Mermaid's native MCP tooling (AI-assisted generation/validation per Mermaid Studio 2026.1.x notes) can replace ad hoc prompt-based Mermaid generation — worth a follow-up spike since it would give schema-validated output instead of freeform LLM text.
- Before citing Code2UML/Paper2SysArch/Text2Arch numeric results in a future skill or memory doc, do a dedicated fetch of the arXiv HTML/abstract pages (the PDF binary could not be parsed by WebFetch here) — do not carry forward any specific accuracy/benchmark figures from this digest, as none were confirmed verbatim.

## Sources
- https://github.com/swark-io/swark
- https://blog.heuel.org/2026/02/an-agentic-skill-for-interactive-c4-architecture-diagrams/
- https://itnext.io/c4-models-are-brilliant-ai-coding-is-breaking-them-heres-what-we-re-doing-about-it-a92490fff5f6
- https://www.catio.tech/blog/software-architecture-tools
- https://mermaidstudio.dev/whatsnew/2026-1-2/
- https://mermaidstudio.dev/whatsnew/2026-1-4/
- https://mermaidstudio.dev/whatsnew/2026-1-5/
- https://mermaidstudio.dev/whatsnew/2026-1-6/
- https://mermaidstudio.dev/whatsnew/2026-1-8/
- https://mermaidstudio.dev/whatsnew/2026-1-9/
- https://mermaidstudio.dev/whatsnew/2026-2-1/
- https://mermaidstudio.dev/whatsnew/2026-2-3/
- https://mermaidstudio.dev/whatsnew/2026-2-4/
- https://mermaidstudio.dev/whatsnew/2026-3-3/
- https://cosmin-vladutu.medium.com/fitness-functions-and-architectural-tests-why-code-reviews-arent-enough-e805be1d41e2
- https://platformtoolsmith.com/blog/operationalizing-adrs-fitness-functions/
- https://www.architectviewmaster.com/blog/architecture-fitness-functions-catch-drift-before-prod/
- https://arxiv.org/pdf/2511.18036
- https://arxiv.org/pdf/2604.14941
- https://arxiv.org/pdf/2605.24453
- https://arxiv.org/pdf/2604.23816
