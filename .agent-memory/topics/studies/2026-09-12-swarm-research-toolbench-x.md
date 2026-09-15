# Studies Research: Tool-Use Reliability Under Injected, Recoverable Hazards (ToolBench-X)

> ✅ QA-gated by PO 2026-09-12 · spot-check: "five hazard types (Specification Drift, Invocation Error, Execution Failure, Output Drift, Cross-source Conflict); each instance solvable via a valid recovery path; failures driven by limited hazard diagnosis/recovery, not tool-call volume/inference budget; recovery hints beat test-time scaling" ✓ (arxiv.org/abs/2606.25819 abstract, WebFetch exit 0, quotes verbatim)

## TL;DR
- New primary source: ToolBench-X (arXiv 2606.25819, Tian/Shi/Zhou/Zhao, submitted June 2026) — a tool-use reliability benchmark that injects recoverable environment hazards rather than just testing raw accuracy.
- Core finding: agents that do well under reliable tools often fail once recoverable hazards are injected — the gap is a distinct failure mode from accuracy.
- Failures trace mainly to poor hazard diagnosis and ineffective recovery, not tool-call volume or inference budget.
- Targeted recovery hints recover many failed tasks; simply scaling test-time compute gives much smaller gains.
- Implication: reliability under unreliable/adversarial tool environments needs to be measured and engineered separately from task accuracy.

## Findings

**What:** ToolBench-X evaluates tool-using agents on executable multi-step tasks (sequential, parallel, and mixed workflows) across diverse domains, injecting five structured hazard types: Specification Drift, Invocation Error, Execution Failure, Output Drift, and Cross-source Conflict.
**Why it matters:** This is a more realistic stress test than standard function-calling benchmarks — it models the actual failure surface of MCP-style tool ecosystems (drifted specs, flaky execution, conflicting sources) that a PO+swarm harness like this repo's is exposed to.
**Confidence: high** (directly from abstract).

**What:** Every injected hazard scenario is designed to remain solvable through at least one valid recovery path (retry, fallback, verification, or cross-checking).
**Why it matters:** The benchmark isolates recovery competence rather than measuring unsolvable-task failure — a cleaner signal for whether an agent/harness handles adversity gracefully.
**Confidence: high**.

**What:** Agents that perform well under reliable tool conditions often fail once recoverable hazards are introduced.
**Why it matters:** Standard "does it work" benchmarks (clean tool environments) systematically overstate real-world reliability; a harness relying on accuracy-only benchmarks for tool selection is measuring the wrong thing.
**Confidence: high**.

**What:** Failures are driven less by tool-use volume or inference budget than by limited hazard diagnosis and ineffective recovery strategy.
**Why it matters:** More tool calls or more reasoning tokens does not fix reliability — the bottleneck is whether the agent recognizes something went wrong and picks a correct recovery action, a qualitatively different capability from raw capability scaling.
**Confidence: high**.

**What:** Targeted recovery hints (explicit guidance on how to detect/handle a hazard) substantially recover failed tasks, while test-time scaling (more inference compute/turns) yields comparatively limited gains.
**Why it matters:** Investment in explicit recovery instructions/playbooks in a harness's tool-calling layer likely beats investment in bigger context windows or more retries alone.
**Confidence: high**.

**What:** The paper frames its contribution as moving tool-use evaluation "beyond function calling" — beyond accuracy metrics toward task completion under unreliable tool environments.
**Why it matters:** Complements this repo's existing SUSVIBES (security-vs-correctness gap) and test-oracle-gaming findings: correctness metrics alone (or passing gated tests) don't capture resilience to degraded/adversarial tool conditions, which is exactly the situation delegated subagents face (flaky MCP servers, expired tokens, transient 503s per this repo's own Hostinger notes).
**Confidence: med** (interpretive link to this repo, not stated in paper).

## For This Workspace
- The DELEGATION-CONTRACT / researcher-profile pattern already forces call budgets and scoped tools; add an explicit "hazard recovery" expectation to sub-agent briefs — e.g., name the retry/fallback path expected for known-flaky calls (Hostinger 503s, MCP session drops) rather than assuming clean tool execution.
- When auditing swarm output for the QA gate, treat "task appeared to succeed once" as weak evidence; ToolBench-X's finding that clean-environment success doesn't predict hazard-condition success argues for spot-checking behavior under at least one injected failure (expired token, malformed response) before trusting a build/research swarm's tool-use claims.
- Prefer writing recovery hints directly into skill/tool procedures (`.agent-harness/tools/`) over relying on bigger context or more retries — this matches the paper's finding that hints beat test-time scaling for recovery.
- Candidate new topics/studies entry angle for a follow-up: track whether MCP-layer flakiness (Hostinger 401/503, session-id drops) documented in this repo's own memory maps onto ToolBench-X's five hazard categories — could seed a harness-specific hazard checklist.

## Sources
https://arxiv.org/abs/2606.25819
https://arxiv.org/pdf/2606.25819
https://arxiv.org/html/2606.25819v1
