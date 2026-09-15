> ✅ QA-gated by PO 2026-09-11 · spot-check: "AMA-Bench: GPT 5.2 72.26% accuracy; AMA-Agent beats HippoRAG2 by 11.16pp" ✓ (WebFetch of arxiv.org/html/2602.22769v1 confirms 0.7226/72.26% and 0.5722 vs 0.4480 = 11.16pp exactly)

## TL;DR

- Multi-agent failures split into three recovery tiers: tool faults recover fully, delegation ambiguity partially recovers, semantic/latent faults (context pollution, conflicting outputs) never recover via retry.
- Cascade radius (how far an error propagates through a pipeline) grows sharply with pipeline depth — from ~0.93 at depth 3 to ~4.67 at depth 7 in one benchmark.
- Model-driven routing for detecting/handling faulty agent outputs vastly outperforms keyword-heuristic routing on adversarial cases (100% vs 0% accuracy in one study).
- Agent memory benchmarks show current systems bottleneck on architecture, not model size — scaling 8B→32B params gives only marginal gains; even a strong general model (GPT 5.2) tops out at ~72% accuracy on a long-horizon memory benchmark.
- A large-scale real-world study (20,574 coding-agent sessions) exists specifically characterizing developer-agent misalignment patterns, but the public excerpt available did not surface specific percentage breakdowns — treat root-cause percentages from secondary sources as unverified.

## Findings

1. **What:** OrchestraBench identifies a three-tier fault-recovery split in multi-agent orchestration: tool-invocation faults are "fully recovered" (agents recompute manually when a tool fails, cascade radius 0); ambiguous-delegation faults are only partially recovered (~30% success, cascade radius ~1.4 stages); latent/semantic faults (context pollution, conflicting outputs, premature action) are never recovered (0% success, full cascade propagation) and retry does not help.
   **Why it matters:** Confirms that blind retry logic in an orchestration harness is a false safety net specifically for semantic-level errors — those need detection/attribution, not resubmission.
   **Confidence: high** (directly read from fetched abstract/summary of arxiv.org/html/2608.05263)

2. **What:** In the same benchmark, cascade radius (how many downstream pipeline stages an error corrupts) increases from about 0.93 at pipeline depth 3 to about 4.67 at pipeline depth 7.
   **Why it matters:** Deeper agent pipelines (more handoffs/sub-agents) amplify blast radius of a single fault non-linearly — argues for shallower delegation chains or checkpoints between stages.
   **Confidence: high** (read directly from fetched source)

3. **What:** Model-driven routers (used to classify/handle failures) reached 100% accuracy on adversarial test cases in OrchestraBench, versus 0% for keyword-flag heuristic routers.
   **Why it matters:** Simple keyword/regex-based error classification in a delegation harness is likely to miss adversarial or subtle failure signatures entirely; an LLM-based classifier step is worth the extra cost for critical routing decisions.
   **Confidence: high** (read directly from fetched source)

4. **What:** AMA-Bench (long-horizon agent memory benchmark) reports GPT 5.2 achieving 72.26% average accuracy, while the proposed AMA-Agent framework (built on the smaller Qwen3-32B model with a causality-graph + tool-augmented retrieval architecture) reaches accuracy that outperforms the strongest existing baseline (HippoRAG2) by 11.16 percentage points.
   **Why it matters:** Architecture (causal structure + hybrid retrieval) beats raw model scale for long-horizon agent memory tasks — pure similarity/embedding retrieval and naive compression underperform because agent trajectories are causally dense, not redundant prose.
   **Confidence: high** (read directly from fetched arxiv.org/html/2602.22769v1 page)

5. **What:** AMA-Bench's dataset spans 2,496 real-world QA pairs across six domains (web navigation, text-to-SQL, software engineering, gaming, embodied AI, open-world QA) plus 1,200 synthetic QA pairs stratified across trajectory lengths from 8K to 128K tokens.
   **Why it matters:** Gives a concrete sense of what "long-horizon" means in current agent-memory research (up to 128K-token trajectories) — a useful reference point when sizing this workspace's own topic-memory / inbox retention windows.
   **Confidence: high** (read directly from fetched source)

6. **What:** A large-scale empirical study ("How Coding Agents Fail Their Users") analyzed 20,574 real-world coding-agent sessions to categorize developer-agent misalignment symptom patterns, root causes, and co-occurrence relationships between failure types.
   **Why it matters:** This is the largest known real-usage dataset (as of this search) specifically about coding-agent failures, directly relevant to an agent-harness workspace that runs many delegated coding subagents — but the fetched excerpt only confirmed the dataset size and study framing, not specific percentage findings.
   **Confidence: med** (session count of 20,574 confirmed directly from fetch; the deeper root-cause statistics were not present in the fetched excerpt and are therefore not reported here)

7. **What:** Existing agent memory compression techniques (iterative summarization/edit-style approaches like MEM1, Mem0, MemAgent) are reported by search-result summaries as underperforming on causally-dense agent trajectories compared to structured/graph-based memory.
   **Why it matters:** Suggests plain "summarize and truncate" memory compaction (a tempting default for a topic-memory system) loses causal/dependency information that later retrieval needs.
   **Confidence: low** (this claim came from WebSearch snippet synthesis only — not independently verified by fetching a full source page in this session; treat as a qualitative lead, not a citable statistic)

## For This Workspace

- Treat blind retry of a failed subagent delegation as safe only for tool-level faults; for anything that looks like context pollution or conflicting sub-agent outputs, escalate to PO review rather than auto-retrying — matches the OrchestraBench recovery-tier finding.
- When chaining sub-agents (e.g., researcher → auditor → builder), prefer shallow, checkpointed handoffs over deep pipelines; the cascade-radius growth curve is a concrete argument for adding a verification gate every 2-3 hops rather than letting delegation chains run long uninterrupted.
- If/when this workspace builds any automated classifier for triaging failed swarm runs, use an LLM-based check rather than keyword/regex matching on error text — the 100%-vs-0% adversarial-accuracy gap is a strong argument against heuristic-only routing.
- For `.agent-memory/topics/`, consider that pure text summarization of old research digests may be lossy for anything causally structured (e.g., "X failed because Y, which was caused by Z") — a lightweight structured note (cause/effect list) alongside prose summary may retrieve better than prose alone, per the AMA-Bench causality-graph result.

## Sources

https://arxiv.org/pdf/2605.29442
https://arxiv.org/html/2608.05263
https://arxiv.org/html/2602.22769v1
