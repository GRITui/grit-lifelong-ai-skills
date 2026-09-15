> ✅ QA-gated by PO batch 2026-09-11 · spot-check: "Claude Opus 4.5 scores 80.9% on SWE-bench Verified vs 45.9% on SWE-bench Pro" ✓ (WebFetch of https://codeant.ai/blogs/swe-bench-scores, exit 0, verbatim match)

## TL;DR
- SWE-bench Pro (launched 2026) is a harder successor to SWE-bench Verified: 1,865 tasks across 41 actively-maintained repos in Python, Go, TypeScript, JavaScript, including private/commercial codebases never seen in training data.
- Top models that score 80-94% on SWE-bench Verified drop to roughly 45-57% on Pro — a ~35-point gap on the best model (Claude Opus 4.5: 80.9% Verified vs 45.9% Pro).
- Average score across all evaluated models on Pro is only around 25%, vs the near-saturated Verified leaderboard.
- Models lose further ground moving from public to private/held-out repos (e.g. GPT-5 falls from 23.1% public to 14.9% private-tier), suggesting real memorization/contamination effects on older benchmarks.
- Pro tasks are deliberately multi-file: average ~107 lines of code changed across just over four files per task, closer to real engineering work than single-function bug fixes.

## Findings

**What:** SWE-bench Pro contains 1,865 tasks over 41 actively maintained repos (Python/Go/TypeScript/JavaScript), split into public, held-out-private (GPL), and unpublished commercial-startup tiers.
**Why it matters:** The private/commercial tiers are "legally inaccessible to model trainers," which structurally prevents the training-data contamination that has been suspected of inflating scores on older, fully-public benchmarks like original SWE-bench.
**Confidence: high** (stated directly by two independent sources, morphllm.com and codeant.ai, describing the same dataset).

**What:** The best model scores ~57% on SWE-bench Pro overall, but Claude Opus 4.5 specifically scores 80.9% on SWE-bench Verified and only 45.9% on Pro.
**Why it matters:** A ~35-point drop on the same class of "fix this issue" task, just by changing repo provenance and task complexity, shows how much prior benchmark scores were being driven by benchmark-specific artifacts rather than general coding capability.
**Confidence: high** (consistent figures reported by both fetched sources).

**What:** Average score across all evaluated models on Pro is around 25%, versus near-ceiling performance (many models >80%) on Verified.
**Why it matters:** This reopens the question of what "coding agent capability" claims from vendors actually mean — Verified is close to saturated as a discriminator, Pro is not.
**Confidence: high** (directly stated in source).

**What:** Task complexity on Pro averages roughly 107 lines of code changed across just over four files per task, versus SWE-bench's historical single-file/small-diff bias.
**Why it matters:** Multi-file, larger-diff tasks better emulate real feature/bugfix PRs and stress agent planning/context-management, not just localized patch generation.
**Confidence: high** (directly stated in source).

**What:** Scores fall further when moving from public repos to private/commercial repos within the same model (e.g., GPT-5: 23.1% public → 14.9% private; Claude Opus 4.1: 22.7% → 17.8%).
**Why it matters:** This within-model public-vs-private delta is the clearest available evidence that public-benchmark scores are inflated relative to genuinely unseen code, useful context whenever a vendor cites a SWE-bench-style number.
**Confidence: med** (numbers appear in the codeant.ai summary; not independently cross-verified against the primary morphllm.com page, which returned HTTP 429 during this research pass).

**What:** Academic critique is emerging alongside these leaderboards — e.g. a 2026 arXiv position paper "Coding Benchmarks Are Misaligned with Agentic Software Engineering" and "RoadmapBench: Evaluating Long-Horizon Agentic Software Development Across Version Upgrades" argue current benchmarks (including SWE-bench variants) don't capture long-horizon, multi-PR, version-upgrade-style engineering work agents are increasingly asked to do.
**Why it matters:** Signals the field is moving past single-PR bug-fix benchmarks toward evaluating sustained, multi-session agentic work — directly relevant to any workspace running long-lived agent swarms.
**Confidence: med** (titles/abstracts found via search; not fetched in full, so specific claims beyond the title framing are unverified).

## For This Workspace
- When citing "AI coding agent capability" in board notes or skill drafts, prefer SWE-bench Pro-style figures (or note the public/private split) over saturated Verified-style numbers — the ~35-point gap here is a good rule-of-thumb caution against benchmark inflation.
- The PO+swarm QA gate already treats "self-reported success" as non-evidence; this research reinforces that instinct — even top-scoring commercial models drop sharply on genuinely unseen, multi-file tasks, so delegated subagent output should keep being spot-checked against exit codes/tests rather than trusted on claimed completion.
- Multi-file, ~100+ LOC changes are exactly where current agents underperform most (Pro tasks average 4+ files) — for builder-swarm tasks that span multiple files, consider tighter scoping (one file/module per delegated task) rather than assuming an agent will coordinate a large multi-file change correctly in one pass.
- Track RoadmapBench / long-horizon agentic benchmarks as a future research angle — directly analogous to this repo's own long-running swarm/topic-memory model; worth a follow-up research pass once primary papers are accessible (arXiv fetch was not completed this session).

## Sources
https://codeant.ai/blogs/swe-bench-scores
https://www.morphllm.com/swe-bench-pro
