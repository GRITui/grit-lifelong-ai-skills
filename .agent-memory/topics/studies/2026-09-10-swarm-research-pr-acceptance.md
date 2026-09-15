# Study: Code Review Agent Merge Outcomes & Task-Stratified PR Acceptance (2026)

> ✅ QA-gated by PO batch 2026-09-10 · spot-check: "CRA-only merge rate 45.20% vs human-only 68.37% (arXiv 2604.03196)" ✓

## TL;DR

- Code-review agents (CRAs) acting alone on GitHub PRs merge at a much lower rate than human-only review (45.20% vs 68.37%), and their feedback is mostly noise: 12 of 13 studied CRAs average <60% "signal" (useful, actionable comments).
- Task type matters more than which coding agent you use: a large PR-acceptance study across 5 agents (Codex, Cursor, Claude Code, Copilot, Devin) found a 29-point acceptance-rate swing by task category (chore/docs ~82-84% vs performance ~55%), while agent-vs-agent differences were mostly not statistically significant after correction.
- Claude Code specifically led on documentation (92.3% acceptance) and features (72.6%) in that dataset, despite having the smallest sample size (139 PRs) of the five agents studied.
- Devin was the only agent showing a real learning-curve trend (+0.77%/week acceptance improvement over 32 weeks); the other four agents' acceptance rates were flat over time.
- Both studies used the AIDev / large-scale GitHub PR mining approach rather than lab RCTs — real production adoption data, not synthetic benchmarks.

## Findings

**What:** PRs reviewed only by automated Code Review Agents merge at 45.20% (127/281) vs 68.37% (804/1,176) for human-only reviewed PRs — a 23.17-point gap, chi-squared p<0.001.
**Why it matters:** Directly contradicts vendor claims that CRAs are a drop-in replacement for human review; CRA-reviewed PRs are also abandoned/closed-without-merge more often (34.88% vs 21.60%).
**Confidence:** high (re-verified exact figures against the primary arXiv HTML source).

**What:** Signal-to-noise analysis of closed CRA-only PRs shows 60.2% of CRA review comments fall in the 0-30% "signal" range (mostly noise); only 18.4% reach 80-100% signal. 12 of 13 individual CRA tools average below 60% signal ratio.
**Why it matters:** Suggests most automated review comments on real PRs are low-value/noisy, which is a concrete argument for treating CRA output as a filtered first pass, not a merge gate, in any pipeline (including this repo's own agent QA gates).
**Confidence:** high (same primary source, numbers confirmed on refetch).

**What:** Across 7,156 PRs from 5 agents (AIDev dataset), overall acceptance: Codex 77.9%, Cursor 74.5%, Claude Code 71.9%, Copilot 68.0%, Devin 61.6% — but task category explains a 29-point swing (chore 84.0%, docs 82.1%, features 66.1%, performance 55.4%), dwarfing agent-choice effects.
**Why it matters:** Of 64 stratified agent-vs-agent comparisons, only 6 survived Bonferroni correction — meaning most "agent X beats agent Y" headline claims in this space are not statistically robust; task framing/scoping is the bigger lever.
**Confidence:** high (numbers pulled directly from arXiv HTML, arXiv:2602.08915v2).

**What:** Claude Code led its cohort on documentation tasks (92.3% acceptance) and features (72.6%), Codex led on fixes (83.0%) and was most consistent across categories (59.6%-88.6% range), Cursor excelled at fixes (80.4%).
**Why it matters:** Per-task specialization patterns are visible even in a noisy comparative sample; useful signal for choosing which agent to route which PR-shaped task to, though Claude Code's sample (139 PRs) is much smaller than Codex's/Devin's (~2,000+ each), so its numbers are less statistically stable.
**Confidence:** med (small-sample caveat explicitly reduces confidence in the Claude Code figures specifically, even though the source numbers themselves are directly verified).

**What:** Devin was the only one of the five agents with a statistically visible temporal improvement trend (+0.77% acceptance/week over 32 weeks of observation); Codex, Cursor, Claude Code, and Copilot showed flat/stable acceptance from their first observed week onward.
**Why it matters:** Counters a common assumption that all agentic coding tools are rapidly improving in the wild — most show no measurable in-production learning curve over months of real usage; improvement claims should be checked against real merge-outcome data, not just capability benchmarks.
**Confidence:** med (single dataset, single time window; trend direction is clear but effect size is modest).

## For This Workspace

- Treat any future "code review agent" or automated QA-comment tool the harness adopts as a noisy first-pass filter, not a merge authority — the 45.20%/68.37% and signal-ratio numbers are a concrete argument for keeping the PO's human/agent merge decision as the actual gate, consistent with "PO QA gate verifies... BEFORE moving knowledge into topics/".
- When delegating PR-shaped work to swarm subagents, expect acceptance/quality to vary far more by task type (chore/docs vs performance/features) than by which model backs the subagent — bias task routing (e.g., give docs/chore tasks to any capable agent, reserve performance-sensitive tasks for more scrutiny) rather than assuming one agent is uniformly best.
- Don't extrapolate small-sample per-agent leaderboard claims (e.g., "Claude Code is best at X") without checking sample size — apply the same statistical-significance skepticism this repo already applies to fabricated-stats rejections (see the SlopCodeBench/HarnessFix rejection note) to comparative agent studies too.
- If this workspace ever benchmarks its own subagents' output quality over time, don't assume improvement is automatic — the AIDev PR study found 4 of 5 production agents showed no measurable week-over-week acceptance-rate improvement; track this repo's own swarm output quality explicitly rather than assuming it improves with more runs.

## Sources

https://arxiv.org/html/2604.03196
https://arxiv.org/pdf/2602.08915
https://arxiv.org/html/2602.08915v2
https://2026.msrconf.org/details/msr-2026-mining-challenge/54/From-Industry-Claims-to-Empirical-Reality-An-Empirical-Study-of-Code-Review-Agents-i
