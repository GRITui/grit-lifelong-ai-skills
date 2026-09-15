> ✅ QA-gated by PO batch 2026-09-09 · spot-check: SADU benchmark best/worst VLM accuracy (70.18% gemini-3-flash-preview / 17.77% gpt-4o-mini) ✓ verified against arxiv.org/abs/2604.04009

## TL;DR
- Figma shipped an official `generate_diagram` MCP tool (2026) that turns Mermaid syntax into editable FigJam diagrams across 6 types (flowchart, sequence, state, ER, Gantt, architecture) — a new first-party bridge from AI-agent-authored Mermaid source into a collaborative whiteboard surface, distinct from the standalone-artifact tools covered in prior batches.
- LikeC4 (DSL-based C4/architecture-as-code tool) now advertises native AI-agent integration: "expose your architecture context to AI agents via MCP server or API — no extra effort" — a fourth C4-lineage tool (alongside Structurizr, C4-PlantUML, IcePanel) with agent-facing plumbing, not previously covered.
- IcePanel's 2026 direction is "diagram as a byproduct of a queryable model, not the artifact itself": REST API/SDKs for programmatic model updates, a CI/CD pipeline pattern where every repo change updates the architecture model, and an MCP server giving AI tools read/write access plus ADR documentation support — IcePanel is explicitly campaigning against hand-drawn diagrams ("The death of architecture diagrams," Aug 2026).
- Two new academic benchmarks quantify how well LLMs/VLMs actually read and reason about architecture diagrams: SADU (154 diagrams, 2,431 QA pairs) shows top VLM (gemini-3-flash-preview) at only ~70% accuracy on diagram understanding, with gpt-4o-mini at ~18% — hard evidence that AI "reading" a diagram is unreliable, distinct from AI *generating* one.
- SAKE (2,154 expert-curated MCQs on architectural knowledge, not diagram images) shows much higher LLM accuracy (89–94%) on architecture *concepts* — the gap between SAKE and SADU results is itself a finding: models know architecture theory far better than they can visually parse an actual diagram.

## Findings

1. **What**: Figma's `generate_diagram` MCP tool (part of the Figma MCP server, 2026) is described as "an essential controller for generating visual assets within FigJam" — it routes prompts to type-specific constraints, converts Mermaid syntax into editable native FigJam diagram objects, and covers flowcharts, sequence, state, ER, Gantt, and architecture diagrams. It can generate from prompts, PDFs, images, screenshots, or existing code/docs, and teams can build custom skills on top of `figma-use-figjam` + `figma-generate-diagram`.
   **Why it matters**: This is a genuinely new integration point not in prior batches — Mermaid-as-intermediate-format now has an official path into a collaborative whiteboard tool (FigJam), not just static HTML/SVG or a code-doc renderer. Relevant if this workspace ever needs diagrams to be team-editable rather than just committed artifacts.
   **Confidence**: high (Figma's own blog + developer docs corroborate the same feature from two angles).

2. **What**: LikeC4 (likec4.dev) is a DSL-based "architecture as code" toolkit (model, visualize, validate from one source) that now markets direct AI-agent exposure: "Expose your architecture context to AI agents via MCP server or API — no extra effort," positioning its DSL as intentionally AI-parseable.
   **Why it matters**: A fourth C4-family tool (after Structurizr, C4-PlantUML, IcePanel) with agent-facing infrastructure baked in — worth a spike alongside Structurizr if this workspace ever needs a validated C4 model rather than a one-off diagram, since LikeC4's single-DSL-multiple-views approach is close to Structurizr's but reportedly lighter-weight.
   **Confidence**: med (single vendor-site fetch; technical specifics of what the MCP server exposes were not documented on the page).

3. **What**: IcePanel published "The Death of Architecture Diagrams" (Medium, Aug 2026) arguing that static diagrams are the wrong artifact entirely; its product direction backs this with a REST API/SDK for programmatic model updates, a documented CI/CD pattern (every repo change → model update via pipeline), an MCP server for AI read/write access to the architecture model, and support for documenting Architecture Decision Records (ADRs) alongside the model.
   **Why it matters**: This is a philosophically different stance than every diagram-as-code tool in prior research (Mermaid/D2/PlantUML/Structurizr): the model is the source of truth and diagrams are generated *views* of it, kept live via CI rather than hand-maintained or periodically regenerated. Directly relevant to the "architecture diagram drift" problem flagged in the 2026-09-09-batch2 file — IcePanel's answer is "don't let the diagram be an independent artifact at all."
   **Confidence**: med (vendor blog + docs; real-world adoption/maturity not independently verified).

4. **What**: SADU (arXiv 2604.04009, "Benchmarking and Evaluating VLMs for Software Architecture Diagram Understanding") tests 11 SOTA vision-language models (Gemini, Claude, GPT, Qwen families) on 154 real architecture diagrams (behavioral/structural/ER) with 2,431 QA tasks. Best model (gemini-3-flash-preview) reaches only ~70.18% accuracy; gpt-4o-mini scores ~17.77%. The paper attributes failures to weak diagram reasoning and visual-relation grounding.
   **Why it matters**: This measures the *inverse* capability of everything in prior research files (which focused on AI *generating* diagrams) — how well AI can *read back* a diagram it or a human produced. Low accuracy here means an agent asked to "review this architecture diagram and check it against the code" cannot be trusted to do so reliably yet; QA of visual diagrams still needs a human or a text-source-of-truth cross-check (e.g., diffing the underlying Mermaid/D2 text rather than the rendered image).
   **Confidence**: high (peer-reviewed-style arXiv benchmark paper with explicit methodology and numbers).

5. **What**: A companion finding from the same research thread: SAKE (arXiv 2606.29520), a 2,154-question expert-curated benchmark testing *architectural knowledge* (not diagram images) across 8 categories and 4 context-length levels, finds LLMs scoring 89.31–94.23% — far higher than SADU's diagram-reading scores.
   **Why it matters**: The gap between "knows architecture concepts" (~90%) and "can visually parse an actual diagram image" (~70% best case, ~18% worst case) is the real 2026 finding: don't rely on an LLM/VLM to verify a rendered diagram by looking at it — rely on it to reason over the diagram's *text source* (Mermaid/D2/PlantUML/DSL) instead, where its knowledge is much stronger.
   **Confidence**: high (same paper family; comparison is straightforward numeric contrast).

6. **What**: A related paper ("(How) Do Large Language Models Understand High-Level Message Sequence Charts?", arXiv 2605.13773) specifically probes LLM comprehension of sequence-diagram-style artifacts (MSCs), a narrower diagram type than SADU's general architecture set.
   **Why it matters**: Sequence diagrams are one of the diagram-design skill's supported types; this is a pointer to more targeted literature if verifying AI-generated sequence diagrams specifically becomes a priority, though this pass did not fetch the paper's actual findings (title/abstract only).
   **Confidence**: low (title-only, not fetched in depth).

## For This Workspace
- When an agent needs to *verify* a diagram it (or another agent) generated, don't have a vision-capable model look at the rendered PNG/SVG and judge it — per SADU's ~70%-best/~18%-worst accuracy on diagram-image understanding, that check is unreliable. Instead verify against the text source (Mermaid/D2/DSL) the diagram was rendered from, consistent with this repo's existing `mmdc -i x.mmd -o /dev/null`-style QA gate, which never asks a model to "read" the picture.
- If a diagram in this workspace ever needs to become a live, team-editable whiteboard object rather than a static committed file, Figma's `generate_diagram` MCP tool (Mermaid → FigJam, 6 diagram types) is now a viable, first-party path — keep the Mermaid source as the version-controlled artifact and treat the FigJam object as a downstream, disposable rendering.
- If C4-rigor work ever needs an agent-queryable *model* (not just a diagram) with CI-driven freshness, evaluate LikeC4 and IcePanel side-by-side with the already-noted Structurizr option — IcePanel's stance ("diagrams are a byproduct of the model, not the artifact") is the most direct answer yet found to the "architecture diagram drift" problem flagged in the prior batch.
- No action needed on the SAKE/SADU benchmark gap beyond the QA-gate implication above, but it's worth citing if this workspace's diagram-design skill is ever asked to add a "self-review the rendered image" step — that step should be skipped or heavily discounted in favor of source-text review.

## Sources
https://www.figma.com/blog/figjam-your-coding-agents-whiteboard/
https://www.figma.com/blog/think-outside-of-the-box-with-claude-and-figjam/
https://developers.figma.com/docs/figma-mcp-server/tools-and-prompts
https://alternativeto.net/news/2026/4/figjam-adds-agent-driven-planning-and-new-mcp-diagramming-tools/
https://mcpservers.org/agent-skills/figma/mcp-server-guide/figma-generate-diagram
https://likec4.dev/
https://icepanel.medium.com/the-death-of-architecture-diagrams-cb5dfce0f10b
https://docs.icepanel.io/core-features/diagramming
https://docs.icepanel.io/core-features/modelling
https://icepanel.io/software-architecture-diagramming
https://arxiv.org/abs/2604.04009
https://arxiv.org/html/2604.04009
https://arxiv.org/html/2606.29520
https://arxiv.org/pdf/2606.29520
https://arxiv.org/pdf/2605.13773
