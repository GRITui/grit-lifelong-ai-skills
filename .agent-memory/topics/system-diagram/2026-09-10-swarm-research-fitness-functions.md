# System-diagram research: diagram drift & architecture fitness functions (Sep 2026)

> ✅ QA-gated by PO 2026-09-10 · spot-check: dependency-cruiser (npm) exists, latest v18.2.0, validates dependency rules ✓

## TL;DR
- Architecture diagram staleness is a named, measured problem in 2026: ~68% of teams reportedly run on architecture docs >6 months stale (Thoughtworks, cited via ArchitectureDiagram.ai).
- The emerging fix pattern is NOT auto-diagram-from-code, but "architecture fitness functions" (ArchUnit, NetArchTest, dependency-cruiser) that run in CI and fail builds on undeclared new dependencies/boundary crossings — catching drift at the *code* level before diagrams even go stale.
- A second, lighter-weight pattern: keep a canonical `ARCHITECTURE.md` (diagram-as-code source, e.g. Mermaid/D2) in the repo root, require its update in the PR checklist, and rotate a quarterly "diagram owner" for audits — process discipline, not tooling.
- AI-assisted regeneration (natural-language description -> diagram in ~seconds) is being marketed (e.g. ArchitectureDiagram.ai) as the low-friction alternative to manual redraws, but full automated code-to-diagram drift detection is explicitly stated as "not yet a fully automated process."
- No tool found (again) that ingests this repo's shape of artifact (Claude Code subagent delegation via `.agent-harness/DELEGATION-CONTRACT.md` + `.agent-dashboard/board.json`) and outputs a diagram automatically — the gap from prior research rounds persists, but the CI-fitness-function pattern is directly adoptable here as a *cheaper* substitute.

## Findings

1. **What**: "Architecture diagram drift" is now a defined term with a checklist (deprecated services still shown, missing integrations, diagrams >90 days old, AI agents making false assumptions from stale docs).
   **Why it matters**: Gives this workspace a concrete self-audit checklist for `.agent-dashboard/` diagrams and any topic-file diagrams instead of vague "keep docs updated" advice.
   **Confidence: med** (single vendor blog, but cites Thoughtworks stat).

2. **What**: "Architecture fitness functions" — automated CI tests (ArchUnit for Java, NetArchTest for .NET, dependency-cruiser for JS/TS) that assert structural rules (allowed dependency directions, layer boundaries) and fail the build on violation.
   **Why it matters**: This is a drift-*prevention* mechanism that doesn't require a diagram-generation tool at all — it encodes the diagram's rules as executable tests. Directly portable pattern for any repo with declared structure (e.g., "researcher agents must not write outside inbox/").
   **Confidence: high** (well-established tool names, consistent across multiple 2026 sources).

3. **What**: Some fitness-function setups only block *new* violations ("ratchet" pattern) so existing drift can shrink over time but never silently grow.
   **Why it matters**: Useful CI philosophy for a fast-changing repo like this one — don't require a big-bang fix, just stop the bleeding going forward.
   **Confidence: med**.

4. **What**: Recommended lightweight process fix: canonical `ARCHITECTURE.md` (diagram-as-code source) in repo root, PR checklist item to update it, rotating quarterly diagram-owner audits.
   **Why it matters**: Zero new tooling required; matches this repo's existing "diagram-as-code" findings (Mermaid/D2/Structurizr) from 2026-09-07 research — closes the loop from "which tool to draw with" to "how to keep it current."
   **Confidence: med** (process advice, not empirically validated at scale in the source).

5. **What**: AI natural-language-to-diagram regeneration (describe the change in plain English, get an updated diagram in ~30 seconds) is positioned as the friction-reducer, with the stated bottleneck being "the description, not the drawing."
   **Why it matters**: Reframes the drift problem — if regenerating is cheap, staleness is a discipline failure, not a tooling gap. Relevant for whether this repo should invest in diagram *generation* speed vs. diagram *validation* (fitness functions).
   **Confidence: low** (vendor marketing content, unverified benchmark).

6. **What**: Fully automated "codebase vs. architecture description" drift detection is explicitly described as not yet mature/automated as of writing.
   **Why it matters**: Confirms (again) the gap flagged in prior rounds — no tool auto-diffs actual system structure against a diagram for arbitrary/agentic codebases; this remains an open space.
   **Confidence: high** (explicit statement in source, consistent with two prior research rounds finding no OTel-trace-to-diagram or A2A-card-to-diagram tool).

7. **What**: Claude Code's own delegation model is documented as a "hub-and-spoke"/orchestrator-worker pattern (main agent = manager, subagents isolated with own context/tools/permissions, returning only final output to parent) — this is the closest thing to a "convention" for depicting agent-to-agent delegation, but it's described in prose/guides, not as a standardized diagram notation.
   **Why it matters**: No distinct diagram convention (arrows/notation) for agent delegation has crystallized yet beyond generic hub-and-spoke flowcharts; teams appear to just reuse existing flowchart/sequence-diagram tooling rather than adopt anything delegation-specific.
   **Confidence: med** (consistent across multiple guide/blog sources, but none propose new notation).

## For This Workspace

1. Treat the harness's own rules as fitness functions where possible: e.g., write a small CI/pre-commit check (dependency-cruiser-style, but a simple shell/grep check is fine given this isn't a compiled codebase) that fails if a researcher/builder subagent's output lands outside its declared write directory from `DELEGATION-CONTRACT.md` — this is cheaper than trying to keep a diagram of "who can write where" perpetually accurate.
2. Add a single canonical `ARCHITECTURE.md` (or reuse `.agent-harness/INSTRUCTIONS.md`) with an embedded Mermaid/D2 diagram of the PO → swarm → inbox → topics pipeline, and add "update ARCHITECTURE.md diagram" as an explicit line item whenever `DELEGATION-CONTRACT.md` or the PO/swarm model changes — matches the recommended PR-checklist pattern.
3. Apply the "≤90 days" staleness checklist from Finding 1 to `.agent-dashboard/` visuals specifically: since `board.json`/`data.js` regenerate autonomously via n8n but the *diagram/legend* explaining the pipeline is hand-maintained, schedule a recurring (quarterly, per Finding 4) manual check that the dashboard's static explanatory diagram still matches the current DELEGATION-CONTRACT/SKILLS-INDEX shape.
4. Do not invest yet in building/adopting an automated OTel-trace-to-diagram or delegation-manifest-to-diagram generator for this repo (confirmed still not mature, Finding 6) — cheaper ROI right now is the fitness-function/checklist approach above; revisit this specific gap in a future research round if a new tool surfaces.

## Sources
- https://architecturediagram.ai/blog/architecture-diagram-drift
- https://www.xopsschool.com/tutorials/drift-detection/
- https://atlan.com/know/context-drift-detection/
- https://techdebt.guru/ai-architecture-drift/
- https://www.envzero.com/blog/drift-detection-in-iac-prevent-your-infrastructure-from-breaking
- https://medium.com/@richardhightower/claude-code-subagents-and-main-agent-coordination-a-complete-guide-to-ai-agent-delegation-patterns-a4f88ae8f46c
- https://hatchworks.com/blog/claude/claude-sub-agents-and-agent-teams/
- https://hidekazu-konishi.com/entry/claude_code_subagents_and_orchestration_guide.html
- https://www.anthropic.com/engineering/multi-agent-research-system
