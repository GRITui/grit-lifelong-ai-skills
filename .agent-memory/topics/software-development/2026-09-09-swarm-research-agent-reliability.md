> ✅ QA-gated by PO batch 2026-09-09 · spot-check: paper at arxiv.org/pdf/2605.29442 is titled "How Coding Agents Fail Their Users: A Large-Scale Analysis of Developer-Agent Misalignment in 20,574 Real-World Sessions" and covers the failure taxonomy (incorrect solutions, incomplete implementations, code-quality issues, misunderstood context, codebase incompatibility) — confirmed via independent WebFetch ✓

## TL;DR

- Autonomous coding agents fail less on syntax and more on **social/organizational fit**: code that compiles and runs but is silently wrong, or doesn't match how a team actually works.
- Large real-world audits (33,596 PRs; 20,574 developer-agent sessions) find that **less than half of agent-authored code survives into final commits**, even though agents now author "more than half" of committed code in some codebases.
- Standard benchmarks (SWE-bench and family) systematically **overstate reliability**: leaked/overly detailed issue descriptions, single-language bias, confounded model-vs-scaffold effects, and dataset defects in ~30% of tasks per a 2026 OpenAI audit.
- Enterprise deployments show a **~37% gap between lab benchmark scores and real-world production performance**, with up to 50x cost variation for similar accuracy across agent stacks.
- Newer benchmarks (SWE-bench Pro, SWE-Compass) and evaluation approaches try to fix this by adding multi-file/multi-language tasks, contamination resistance, and trajectory-level (not just pass/fail) scoring.

## Findings

1. **What:** A forensic audit of 33,596 real-world agent-authored pull requests (across repos with real maintainers) catalogs where autonomous coding agents actually fail in practice, not in benchmarks.
   **Why it matters:** Shifts the failure conversation from "does it pass the test" to "does a human maintainer accept it" — a much higher and more realistic bar for any workspace using agents to write production code.
   **Confidence:** med (could not fully re-fetch source; found via search snippet + title, blocked by 403 on direct fetch).

2. **What:** A separate large-scale study of 20,574 real developer-agent sessions ("How Coding Agents Fail Their Users") finds a taxonomy of failure types — incorrect solutions, incomplete implementations, code-quality issues, misunderstood context/requirements, and solutions incompatible with the existing codebase — and reports that a substantial share of agent output never survives as a commit.
   **Why it matters:** Confirms failure is dominated by *context/requirements misunderstanding* and *codebase incompatibility*, not raw code-generation ability — meaning better prompting/spec work (not a bigger model) is often the higher-leverage fix.
   **Confidence:** high (fetched full PDF via WebFetch).

3. **What:** "What Breaks When LLMs Code?" and related 2026 papers describe a critical failure mode: code that is **syntactically correct and executes successfully but is silently wrong** — plausible-looking but incorrect output that agents don't flag with any error signal.
   **Why it matters:** This is the most dangerous failure class for autonomous/unattended agent runs (e.g., headless `claude -p` in cron) because there's no exit-code signal to catch it — only human or independent-agent review does.
   **Confidence:** med (from search synthesis, not independently fetched).

4. **What:** A taxonomy paper ("Why AI Agents Fail") derived 14 distinct failure modes from 1,642 execution traces across five multi-agent frameworks; framework choice mattered a lot — one specialized two-agent framework reached 98.1-100% success while general-purpose frameworks (AutoGen, CrewAI) scored ~89-93% on the same tasks.
   **Why it matters:** Architecture/scaffold choice is itself a major reliability lever, independent of the underlying model — relevant when choosing how to structure PO+swarm delegation patterns.
   **Confidence:** med (search synthesis only).

5. **What:** SWE-bench, the de facto standard for coding-agent evaluation, has well-documented limitations: overly detailed issue descriptions that inflate resolution rates, single-language (mostly Python) bias, and confounded model-vs-scaffold effects. A 2026 OpenAI audit found dataset quality issues (broken or overly strict tests) in roughly 30% of tasks.
   **Why it matters:** Headline "SWE-bench %" scores used to pick or trust a coding agent/model should be treated skeptically — they likely overstate real capability by a meaningful margin.
   **Confidence:** high (consistent across multiple 2026 sources in search results).

6. **What:** Enterprise agentic AI systems reportedly show a ~37% gap between lab benchmark scores and real-world deployment performance, with up to 50x cost variation among agents/stacks achieving similar accuracy.
   **Why it matters:** Cost-efficiency and benchmark score are decoupled — worth benchmarking your own actual task mix (and cost) rather than trusting published leaderboard numbers.
   **Confidence:** med (single-source figure, not cross-verified against a second independent source).

7. **What:** Newer/harder benchmarks are emerging specifically to counter these gaps: SWE-bench Pro (harder, multi-file, contamination-resistant tasks) and SWE-Compass (extends to eight programming languages and multiple task types). Best-practice guidance ("Establishing Best Practices for Building Rigorous Agentic Benchmarks," arXiv 2507.02825) argues evaluation should score trajectory quality, tool-call correctness, looping/recovery behavior — not just final pass/fail.
   **Why it matters:** If this workspace ever needs to self-evaluate an agent/workflow, a pass/fail-only QA gate (like the current shell-exit-code gate) is a reasonable floor but misses looping/recovery/trajectory issues that matter for autonomous runs.
   **Confidence:** high (multiple corroborating 2026 sources).

## For This Workspace

- The QA gate here already treats exit-code-0 as the bar, which is correct for catching hard failures — but per finding #3, **silently-wrong-but-passing** output is the more insidious failure mode for background/cron `claude -p` runs. Consider adding a lightweight second-agent review step (not just exit code) for any unattended run that touches production content or deploys.
- Per findings #1-#2, the biggest real-world agent failure category is *context/requirements misunderstanding and codebase incompatibility*, not raw generation quality — reinforces this repo's Step-1-Recall discipline (grep `.agent-memory/topics/` before acting) as a directly relevant mitigation, and argues for writing sharper task specs in swarm-agent prompts.
- Don't cite raw SWE-bench-style leaderboard percentages as a trust signal for model/agent choice in future memory entries (finding #5) — flag such scores as "benchmark, not real-world" if referenced.
- Given finding #4 (framework/scaffold materially changes success rate independent of model), if this workspace ever evaluates alternative swarm-orchestration approaches, treat orchestration design as a first-class reliability variable, not an implementation detail.

## Sources

https://medium.com/@vivek.babu/where-autonomous-coding-agents-fail-a-forensic-audit-of-real-world-prs-59d66e33efe9
https://arxiv.org/pdf/2605.29442
https://arxiv.org/html/2605.30777v1
https://papers.ssrn.com/sol3/Delivery.cfm/6572478.pdf?abstractid=6572478&mirid=1
https://www.kdnuggets.com/top-10-open-source-benchmarks-for-ai-coding-agents-in-2026
https://arxiv.org/pdf/2604.03515
https://arxiv.org/pdf/2507.02825
https://kili-technology.com/blog/ai-benchmarks-guide-the-top-evaluations-in-2026-and-why-theyre-not-enough
https://www.morphllm.com/ai-agent-evaluation
https://futureagi.com/blog/evaluating-coding-agents-2026/
