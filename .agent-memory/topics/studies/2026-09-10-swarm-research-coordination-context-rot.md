# Studies Research: Multi-Agent Coordination Gains vs. Noise Floor, and Context Rot as Premature Termination

> ✅ QA-gated by PO batch 2026-09-10 · spot-check: "arXiv:2606.20695 — 7/10 papers below noise floor, +5pp pooled Wilson CI [-2,+12], envelope [-3,+18]pp" ✓ (verified via WebFetch of abstract page, exact match)

---
topic: studies
angle: multi-agent coordination effectiveness + context rot in long-horizon agent sessions
date: 2026-09-10
---

## TL;DR

- A 2026 methodology paper (paired noise-floor protocol) finds that **7 of 10** recent multi-agent coordination architectures report headline gains that fall *below* the measured noise floor of running the same model twice with no coordination — the "coordination gain" may often be statistical noise, not architecture.
- ClawArena-Team shows the real bottleneck in subagent orchestration isn't task execution, it's **privilege/permission delegation**: no model exceeds 50% workspace-permission precision when granting subagents access.
- Context rot in long-horizon search agents is dominated by **premature termination**, not forgetting — agents increasingly give up or guess despite having context budget left, and the termination rate rises with context length.
- Context-isolation via sub-agent folding (FoldAgent) was the single best mitigation tested, giving up to a 19-point accuracy gain over baseline on BrowseComp.
- Cost and orchestration quality are decoupled: API cost varies >100x across models on the same orchestration benchmark while scores vary <4x — cheap models are Pareto-competitive.

## Findings

**What:** "How Much Coordination Gain Is Real? A Paired Noise-Floor Protocol for Multi-Agent LLM Benchmarks" (arXiv:2606.20695) measures the natural performance variance ("noise floor") of a single model run under configuration-equivalent, no-coordination conditions, then compares reported multi-agent coordination gains against it. On Claude Haiku 4.5, pooled paired gaps across two n=100 seeds averaged +5pp with a Wilson CI of [-2, +12] — not statistically significant — and the observed envelope of paired gaps spanned [-3, +18]pp.
**Why it matters:** Against this envelope, 7 of 10 recent multi-agent coordination papers report headline effects that sit below the local noise floor, and one more sits inside the envelope. That means most published "coordination works" claims in this space have not been shown to survive a same-model paired replication.
**Confidence: high** (numbers read directly from the paper's abstract/results text).

**What:** ClawArena-Team (arXiv:2606.31174) benchmarks a single "manager" LLM commanding a fixed pool of subagents via dynamic workflows, scoring both task correctness and how well the manager grants privileges/routes modalities to subagents.
**Why it matters:** The dominant failure mode is not perception or task competence but **privilege-granting precision** — no evaluated model exceeds 50% precision when deciding what workspace access to grant a subagent. Leaderboard scores cluster in a tight 9.9-point band even though the underlying orchestration *behavior* (how work is delegated) diverges by more than an order of magnitude, meaning similar-looking outcomes can hide very different (and very different quality) delegation strategies.
**Confidence: med** (WebFetch summarized rather than quoting exact table values; abstract-level numbers only).

**What:** The same ClawArena-Team benchmark found API cost spans over 100x across models while overall orchestration scores vary less than 4x, and the cheapest open-source models sit on the Pareto frontier.
**Why it matters:** Paying more for a "smarter" orchestrator model doesn't reliably buy better subagent management — cost is a weak proxy for orchestration quality.
**Confidence: med**.

**What:** "Diagnosing and Mitigating Context Rot in Long-horizon Search" (arXiv:2606.29718) tested search agents across three benchmarks. Baseline accuracy/premature-termination rates: BrowseComp 35.0% accuracy / 53.4% premature termination; BrowseComp-Plus 72.0% accuracy / 23.6% premature termination; xbench-DeepSearch 56.2% accuracy / 20.4% premature termination. Premature termination rate correlates positively with context length even controlling for query difficulty.
**Why it matters:** This reframes "context rot" — the dominant symptom in long-horizon agentic search isn't the model forgetting facts, it's the model **giving up early** (outputting an uncertain/incorrect answer) once context grows large, well before hitting the hard context limit.
**Confidence: high** (numbers read directly from fetched paper content).

**What:** The same paper tested 7 context-management interventions across three families — compaction (summarize on length/turn/semantic triggers), trimming (discard-all / keep-latest), and isolation (FoldAgent, spinning up sub-agents to isolate context). Isolation was the strongest: FoldAgent on BrowseComp reached 54.0% accuracy, a 19-point gain over the 35.0% baseline. Summarization methods produced smaller but still positive gains (paper reports 46.6% accuracy on average across datasets for summary methods), at a real cost — the best isolation method used 57.7 tool calls vs. 21.7 for baseline.
**Why it matters:** Context isolation (delegating to sub-agents to keep the "manager" context small) beats plain summarization for mitigating premature termination, but at roughly 2.7x the tool-call cost — a concrete throughput/reliability tradeoff for any harness using sub-agent delegation.
**Confidence: high**.

**What:** The same paper also tested parallel sampling with behavior-aware filtering (running multiple attempts and filtering by observed agent behavior rather than just majority vote) as a lower-cost alternative, yielding 2.6%–4.9% accuracy gains across aggregation methods.
**Why it matters:** When premature termination is less severe, cheap parallel sampling + filtering may be a better cost/benefit trade than full context-isolation architectures.
**Confidence: med** (numbers confirmed but methodology detail on "behavior-aware filtering" not independently verified beyond the fetched summary).

**What:** Related work (search hits, not independently fetched/read in full) — "Classifier Context Rot" (arXiv:2605.12366) reports recall for an Opus-4.6-based monitor dropping from 98.6% to 88% once 800k tokens of benign prior actions were prepended to context.
**Why it matters:** Corroborates that context rot affects not just task agents but safety/monitoring classifiers riding along in the same context — relevant to any harness relying on an LLM "gate" reviewing a long transcript.
**Confidence: low** (taken from search-result summary only; primary source not fetched/read directly, so treat as a pointer for follow-up, not a verified figure).

## For This Workspace

1. **Don't trust an "orchestration works" claim (including our own PO+swarm setup) without a no-coordination control.** Before crediting the PO+swarm model with a quality/speed win over a single-agent run, run the paired baseline (same model, same task, no delegation) at least once — arXiv:2606.20695's finding that most reported multi-agent gains sit inside a same-model noise envelope applies directly to any internal claim that "swarms beat solo agents here."
2. **Audit delegation contracts for privilege precision, not just task success.** ClawArena-Team's finding that privilege-granting is the real bottleneck (not task completion) maps onto `.agent-harness/DELEGATION-CONTRACT.md` — when auditing a sub-agent run, check whether the write-scope/tool-grant actually matched what the task needed (over-grant or under-grant), not just whether the deliverable looked right.
3. **Watch for premature termination, not just wrong answers, in long research swarm runs.** If a researcher subagent returns early with low confidence after a long multi-search session, that's the "context rot" failure mode (give-up, not forget) — a cheap mitigation per the paper is parallel sampling with a second short run rather than assuming the long run was thorough.
4. **When a sub-agent task needs long context (many search/tool calls), prefer sub-agent isolation over a single long-running agent with summarization** — the paper's ranking (isolation > summarization > trimming) suggests the existing pattern of delegating discrete legwork to fresh subagents (rather than one agent accumulating a huge transcript) is the right default, at the cost of more total tool calls — worth stating explicitly as a tradeoff when scoping delegation-contract call budgets.

## Sources

- https://arxiv.org/html/2606.29718 (Diagnosing and Mitigating Context Rot in Long-horizon Search)
- https://arxiv.org/abs/2606.20695 (How Much Coordination Gain Is Real? A Paired Noise-Floor Protocol for Multi-Agent LLM Benchmarks)
- https://arxiv.org/abs/2606.31174 (ClawArena-Team: Benchmarking Subagent Orchestration and Dynamic Workflows in Language-Model Agents)
