> ✅ QA-gated by PO 2026-09-12 · spot-check: Veracode 2026 GenAI Code Security Report — AI-generated code averages 56% security pass rate, stalled despite model capability gains ✓

## TL;DR
- Google's 2026 multi-agent design-pattern guidance formalizes patterns this workspace already uses informally (Coordinator/Dispatcher ≈ PO+swarm, Parallel Fan-Out/Gather ≈ parallel research swarms, Generator+Critic/Iterative Refinement ≈ build swarm + PO QA gate) — useful vocabulary and a checklist of patterns not yet adopted (Reflection loops, Hierarchical Decomposition).
- AI-generated code security has plateaued, not improved: Veracode's 2026 GenAI Code Security Report finds AI-generated code passes security checks only 56% of the time even as models get more capable at other tasks — "smarter but not safer."
- SAST finding volume explodes with agentic coding: Cloud Security Alliance/Apiiro Fortune-50 data shows monthly static-analysis findings climbing ~10x (roughly 1,000 → 10,000+) in repos with active AI-generated code — a triage/tooling bottleneck, not just a code-quality one.
- AI-recommended dependencies are unreliable: Endor Labs research finds only 1 in 5 AI-recommended dependency versions is safe, and 34% are outright hallucinated (non-existent packages/versions) — directly relevant to any swarm that resolves or adds dependencies unsupervised.
- AI code review tooling has matured into a standard CI/CD stage in 2026 (Cursor, Codex, Copilot, Augment Code, Qodo, Sourcegraph-class tools running as bot reviewers on every PR push), with human reviewers repositioned toward judgment/architecture calls rather than line-by-line diffs.

## Findings

**What:** Google published formal guidance (via InfoQ, Jan 2026) naming eight core multi-agent design patterns: Sequential Pipeline, Coordinator/Dispatcher, Parallel Fan-Out/Gather, Hierarchical Decomposition, Generator and Critic, Iterative Refinement, Human-in-the-Loop, and Composite (combinations of the above). Google's stated rationale: "Reliability comes from decentralization and specialization."
**Why it matters:** This workspace's PO+swarm model maps almost exactly onto Coordinator/Dispatcher (PO delegates to specialized subagents) plus Human-in-the-Loop (PO QA gate before merge to `.agent-memory/topics/`) plus Parallel Fan-Out/Gather (parallel research swarms merged by the PO). The two named patterns this workspace does *not* yet formally use are Generator-and-Critic as a dedicated in-task role (a build agent produces, a *separate* critic agent reviews, before the PO even sees it) and Reflection (an agent re-evaluates its own prior output before finalizing) — both are candidate additions to `.agent-harness/DELEGATION-CONTRACT.md` for build-swarm tasks.
**Confidence:** med (single aggregator/news source summarizing a Google Cloud Architecture Center doc, not the primary doc itself)

**What:** Veracode's 2026 GenAI Code Security Report (published July 2026) found AI-generated code security has "stalled" at a 56% pass rate on security checks, despite base model capability continuing to climb on other benchmarks — the headline framing is "LLMs are getting smarter, but not safer."
**Why it matters:** A concrete, named-source counterpoint to any assumption that newer/bigger models auto-fix security quality; security pass rate is decoupled from general capability gains, so security verification must stay a separate, explicit gate regardless of which model a swarm uses.
**Confidence:** med (press-release-level summary of the Veracode report; primary report not read directly)

**What:** Cloud Security Alliance research (citing Apiiro Fortune-50 telemetry) found monthly SAST findings in repos with active AI-generated code jump roughly tenfold — from ~1,000 to 10,000+ findings/month — as agentic coding output scales.
**Why it matters:** Static analysis tooling and triage capacity, not just code-generation quality, becomes the bottleneck at scale; a QA gate that runs a linter/SAST tool once per PR may not survive the finding-volume increase agentic workflows produce. Relevant if this workspace's build swarms ever scale beyond small scripts/tools.
**Confidence:** low-med (single research-note citing proprietary vendor telemetry, not independently reproducible)

**What:** Endor Labs research found only 1 in 5 AI-recommended dependency versions are actually safe (up-to-date, non-vulnerable), and 34% of AI-recommended dependencies are hallucinated — i.e., reference packages/versions that don't exist ("slopsquatting" risk surface).
**Why it matters:** Any build-swarm task that adds or updates a dependency (npm/pip/cargo install suggested by an agent) needs a mandatory existence + vulnerability check before it lands — this is a concrete, quantified reason to never let an agent's dependency suggestion go straight into a lockfile without verification.
**Confidence:** med (specific named-source stat, but summarized via a blog aggregator rather than the primary Endor Labs writeup)

**What:** AI-powered SAST ("AI SAST") is described as the 2026 default: tools now add LLM reasoning on top of traditional rule-based static analysis, tracing dataflow across files to judge whether a flagged pattern is actually exploitable in context, which cuts false-positive rates versus legacy scanners.
**Why it matters:** If this workspace ever adds a static-analysis QA-gate step, the 2026 baseline expectation is context-aware/dataflow-aware analysis rather than a bare pattern-matching linter — relevant to picking or building a `.agent-harness/tools/` static-analysis tool.
**Confidence:** low (vendor/aggregator framing across multiple blog sources, no primary benchmark data)

**What:** AI code review has standardized into a CI/CD pipeline stage in 2026: tools (Cursor's AI Code Review, Codex, GitHub Copilot, Augment Code's review agent, Qodo, Sourcegraph-class tools) run as a bot identity on every PR open/push, posting line-level feedback and PR summaries, with the stated shift being that humans now focus on judgment/architecture calls while the AI handles mechanical, cross-cutting review.
**Why it matters:** Validates (and gives external corroboration for) this workspace's existing `LineOA-middleware PR policy` (gate PRs on CI, auto-merge once green) — the described 2026 industry pattern is consistent with treating automated review/CI as sufficient for routine PRs and reserving human attention for architectural risk, not a workspace-specific idiosyncrasy.
**Confidence:** med (consistent claim across multiple 2026 vendor/aggregator sources, but all are vendor-adjacent, not independent research)

## For This Workspace
- Add a "dependency verification" step to `.agent-harness/DELEGATION-CONTRACT.md` for builder-role subagents: any newly suggested dependency/package version must be checked to exist and be non-vulnerable (e.g. `npm view <pkg>` / registry lookup) before it's added to a lockfile — directly motivated by the Endor Labs 1-in-5-safe / 34%-hallucinated stat above.
- Adopt Google's pattern vocabulary explicitly in `.agent-harness/DELEGATION-CONTRACT.md` or `skills-pipeline.md`: name the PO+swarm setup as Coordinator/Dispatcher + Human-in-the-Loop, and consider formally adding a Generator-and-Critic sub-pattern inside build-swarm tasks (a dedicated reviewer subagent before PO sees output), rather than relying solely on the PO as sole critic.
- If/when a static-analysis or security-scan tool is added under `.agent-harness/tools/`, budget for triage volume growth (the ~10x SAST-finding-surge pattern) rather than assuming linear scaling with codebase size — favor a dataflow/context-aware scanner over a bare pattern-matcher if choosing between tools.
- Treat "AI-generated code passed its tests / lint" as necessary but not sufficient for security specifically — the Veracode 56%-pass-rate finding means a separate security-focused check (not just functional QA) is warranted before merging build-swarm output that touches auth, secrets, or network calls, consistent with existing `Secrets` guidance in global CLAUDE.md.

## Sources
- https://www.infoq.com/news/2026/01/multi-agent-design-patterns/
- https://docs.cloud.google.com/architecture/choose-design-pattern-agentic-ai-system
- https://www.businesswire.com/news/home/20260728207685/en/LLMs-Are-Getting-Smarter-But-Not-Safer-Veracode-2026-GenAI-Code-Security-Report-Finds-AI-Generated-Code-Security-Has-Stalled-at-56-Pass-Rate
- https://labs.cloudsecurityalliance.org/research/csa-research-note-ai-generated-code-vulnerability-surge-2026/
- https://www.endorlabs.com/learn/sast-for-ai-generated-code-what-static-analysis-catches-and-misses
- https://cycode.com/blog/ai-sast/
- https://www.dryrun.security/blog/top-ai-sast-tools-2026
- https://sourcegraph.com/blog/automated-code-review-tools
- https://www.qodo.ai/blog/ai-code-review/
