> ✅ QA-gated by PO batch 2026-09-09 · spot-check: GitHub Spec Kit is a real intent-driven SDD harness with EARS-syntax-templated specs and a Spec→Plan→Tasks→Implement phased workflow ✓

## TL;DR
- Spec-Driven Development (SDD) went mainstream in 2026 as the direct answer to "vibe coding" drift: specs become the executable source of truth, code is a generated/verified artifact.
- Every major AI coding tool now ships an SDD flavor: GitHub Spec Kit, AWS Kiro, Claude Code (cc-sdd), Cursor Plan Mode, Tessl, BMAD-METHOD, OpenSpec.
- Canonical workflow is a 7-phase pipeline with human review gates: Constitution → Specify → Clarify → Plan → Tasks → Implement → Analyze — never jump straight from spec to code.
- Three maturity levels exist: Spec-First (low overhead, prototypes), Spec-Anchored (specs+code co-evolve, test-enforced — the production recommendation), Spec-as-Source (aspirational, humans edit only specs).
- Adjacent trend: "Continuous Agentic/Continuous Deployment" (CA/CD) — agents reason about and adapt pipelines, not just run inside them, using tiered autonomy matched to risk level.

## Findings

**What:** SDD's core failure mode it fixes is AI agents producing "plausible code that drifts from intent, hallucinates APIs, and decays as projects scale" under ad-hoc prompting ("vibe coding").
**Why it matters:** This is precisely the failure mode a QA-gated memory/harness system is designed to prevent — SDD is the code-generation-side analog of this workspace's "verify before persist" principle.
**Confidence:** high

**What:** GitHub reports teams using Spec Kit internally ship features with roughly an order-of-magnitude fewer "regenerate from scratch" cycles than ad-hoc prompting; AWS reports Kiro customer cases where 40-hour features shipped in under 8 hours of human time when spec-authored first.
**Why it matters:** Concrete (if vendor-reported, so treat as directional) evidence that spec-first structuring reduces rework — relevant when deciding whether to draft a spec before delegating a build task to a swarm.
**Confidence:** med (vendor-sourced claims, not independently audited)

**What:** Specifications are commonly written in EARS syntax (Easy Approach to Requirements Syntax) — templated statements like "WHEN [event] THE system SHALL [action]" — which map directly to executable acceptance tests.
**Why it matters:** Gives a lightweight, testable format for writing task/board cards or acceptance criteria that agents can self-verify against, rather than freeform prose specs.
**Confidence:** high

**What:** Teams commit a "constitution" file (project-wide rules: language, frameworks, testing standards) before writing the first spec — commonly an `AGENTS.md` or similar — and every task/commit cites the spec clause it satisfies (e.g. `feat(auth): refs specs/004-magic-link/spec.md`).
<br>**Why it matters:** This maps almost exactly onto this repo's existing `CLAUDE.md`/`AGENTS.md` constitution pattern and board-card structure; the missing piece here is per-task traceability links from commits/deliverables back to a spec clause.
**Confidence:** high

**What:** "Drift detection" is done via executable tests that continuously validate alignment between specification and implementation, not via manual doc review.
**Why it matters:** Directly analogous to this workspace's QA gate (exit-code-0 verification) — SDD generalizes the same idea to feature specs, suggesting the harness could add a lightweight "does the deliverable still match its board-card spec" check for longer-running swarm tasks.
**Confidence:** med

**What:** In agentic CI/CD, the dominant 2026 architectural pattern is "tiered autonomy" — matching an agent's decision authority to the risk level of the action (e.g., auto-merge low-risk fixes, human gate for high-risk changes) — and GitHub's Feb 2026 technical preview lets engineers write agentic workflow logic in plain Markdown instead of YAML ("Continuous AI" / Agentic Workflows).
**Why it matters:** Tiered autonomy is a reusable pattern for this workspace's PO+swarm model — research swarms (low risk, write to inbox only) vs. build swarms (higher risk, still PO-gated) already mirror this, confirming the design choice rather than requiring a change.
**Confidence:** med

**What:** Despite AI adoption in DevOps crossing ~90% among individual developers by early 2026, only ~13% of teams have deployed agents across the *full* delivery lifecycle (commit through production) — most usage is still point-solution (review, test generation) rather than end-to-end.
**Why it matters:** Useful calibration: full autonomous pipelines are still rare in practice even where individual AI tool adoption is near-universal; don't over-index on "agentic CI/CD" marketing claims as describing typical practice.
**Confidence:** med

## For This Workspace
- Adopt a lightweight EARS-style acceptance-criteria line on board cards in `.agent-dashboard/board.json` (e.g. "WHEN swarm completes THE deliverable SHALL exist at inbox path X and pass QA gate Y") so the PO QA gate has an explicit, testable target rather than an implicit one.
- Add a traceability convention: when moving a research draft from `.agent-memory/inbox/` to `topics/`, reference the originating board card ID in the commit message (mirrors SDD's `refs specs/...` commit convention) — cheap, and makes `git log` a searchable audit trail.
- Consider a "constitution" cross-check step before dispatching new swarms: confirm the task references relevant existing `CLAUDE.md`/`AGENTS.md` rules explicitly, the way SDD's "Constitution" phase precedes "Specify" — reduces rediscovery of rules mid-task.
- The "tiered autonomy" framing is a good vocabulary match for documenting *why* research swarms write only to inbox/ while build swarms get scoped output dirs — worth citing if the operating model section of CLAUDE.md is ever revised.

## Sources
https://www.augmentcode.com/tools/best-spec-driven-development-tools
https://levelup.gitconnected.com/beyond-vibe-coding-a-guide-to-spec-driven-development-with-ai-agents-00f41cb44738
https://www.augmentcode.com/guides/what-is-spec-driven-development
https://dev.to/krlz/spec-driven-development-in-2026-what-it-is-the-tooling-and-how-teams-actually-use-it-2fk2
https://arxiv.org/pdf/2606.04967
https://arxiv.org/pdf/2606.27045
https://www.thebcms.com/blog/spec-driven-development/
https://www.productbuilder.net/learn/spec-driven-development
https://codeant.ai/blogs/best-ai-code-review-tools-github-ci-cd
https://www.augmentcode.com/guides/cicd-ai-agents-pipeline-integration
https://arxiv.org/pdf/2508.11867
https://arxiv.org/pdf/2605.07062
https://www.augmentcode.com/guides/ai-code-review-ci-cd-pipeline
https://blog.barecheck.com/development-integrations/the-agentic-revolution-reshaping-cicd-pipelines-in-2026/
https://zylos.ai/research/2026-05-12-agentic-cicd-ai-driven-delivery-pipelines/
https://intuitionlabs.ai/articles/spec-driven-development-spec-kit
https://medium.com/@visrow/comprehensive-guide-to-spec-driven-development-kiro-github-spec-kit-and-bmad-method-5d28ff61b9b1
https://github.com/aws-samples/sample-specship
https://geshan.com.np/blog/2026/05/aws-kiro/
https://learn.microsoft.com/en-us/training/modules/spec-driven-development-github-spec-kit-enterprise-developers
