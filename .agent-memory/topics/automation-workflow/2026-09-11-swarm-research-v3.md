## automation-workflow research — 2026-09-11
> ✅ QA-gated by PO 2026-09-11 · spot-check: Reflexion 91% pass@1 vs 80% GPT-4 baseline on HumanEval ✓ (arxiv.org/abs/2303.11366)

## TL;DR
- Multi-agent coordination in 2026 collapses to four mechanisms: shared state ("blackboard" pattern — i.e. a shared JSON file like this repo's `board.json`), message passing, explicit handoffs, or typed state transitions (LangGraph-style state machines) — the board/handshake-file approach used here is a named, recognized pattern, not an ad-hoc hack.
- "Self-healing" for LLM agent pipelines in 2026 means Reflexion-style verbal self-critique stored in memory and retried on the next attempt, not full autonomous remediation — Reflexion reports 91% pass@1 on HumanEval vs ~80% baseline from this alone.
- 2026 consensus architecture for automated remediation is "controlled autonomy": agents compress investigation/root-cause work, but irreversible or high-risk actions stay behind policy-based human approval — directly applicable to any dashboard action that could touch prod/deploys.
- n8n's Code nodes now run in isolated Task Runner processes by default (2026), so a runaway/infinite-loop JS snippet in a workflow can no longer crash the whole n8n instance — relevant if this workspace's n8n does any Code-node scripting for dashboard regeneration.
- LLM-as-a-judge (a secondary model evaluating a primary agent's output) is described as the standard 2026 design pattern for catching agent errors before they propagate downstream.

## Findings

1. What: Multi-agent orchestration literature groups coordination into four mechanisms — shared state (blackboard), message passing (AutoGen-style), explicit handoffs (OpenAI Agents SDK / Claude Code sub-agents), and typed state transitions (LangGraph state machines).
   Why it matters: This repo's `.agent-dashboard/board.json` + n8n regeneration loop is literally the "blackboard" pattern with a named lineage in 2026 orchestration writing, not a bespoke workaround — useful framing if extending or defending the design.
   Confidence: med (aggregated blog/vendor sources, not a single authoritative spec)

2. What: Fan-out/scatter-gather (parallel agents on independent subtasks, merged after) and sequential pipeline are called out as the two dominant orchestration topologies for production multi-agent systems in 2026.
   Why it matters: Matches this repo's PO + parallel swarm model directly (PO fans out research/build tasks, merges only after its own QA gate) — confirms the current operating model aligns with what's considered production-grade elsewhere.
   Confidence: med

3. What: Reflexion — an agent generates a verbal self-critique of a failed attempt, stores it in memory, and retries conditioned on that critique — is the most concretely evidenced self-healing mechanism cited for 2026 (91% pass@1 HumanEval vs ~80% GPT-4 baseline).
   Why it matters: Gives a lightweight, non-infrastructural way to add "self-healing" to headless `claude -p` cron runs: on failure, feed the previous error/output back into the next invocation's context instead of just blind-retrying.
   Confidence: med (single-technique citation, not independently reverified here)

4. What: 2026 self-healing pipeline architectures for infra/data are described as closed loops of drift detector → root-cause analyzer → remediation generator → post-remediation validator, but explicitly keep "controlled autonomy": irreversible/high-risk/business-sensitive actions require policy-based human approval even when the rest of the loop is automated.
   Why it matters: A template for hardening any future automated-fix step in this repo's QA gate or dashboard — auto-diagnose and propose, but require explicit approval before anything destructive (matches the harness's existing "PO never merges unverified work" rule).
   Confidence: med

5. What: LLM-as-a-Judge (a secondary, specialized model scoring/validating the primary agent's output) is cited as the standard 2026 pattern for catching agent errors before they propagate.
   Why it matters: Directly maps onto this repo's existing PO QA-gate concept — a second LLM pass reviewing a delegated subagent's draft before it's merged into `.agent-memory/topics/` is exactly this pattern already in place informally; formalizing it as an explicit judge step is a natural next step.
   Confidence: med

6. What: n8n's Code nodes in 2026 run via Task Runners by default — isolated processes so a memory leak or infinite loop in a JS/Python snippet doesn't crash the main n8n instance; n8n also added an execution-replay debugger (June 2026) for line-by-line variable tracing in failed Code-node runs.
   Why it matters: If this workspace's n8n instance uses Code nodes to regenerate `.agent-dashboard/data.js` or process board.json, this reduces the blast radius of a bad script and gives a concrete debugging path for failures.
   Confidence: med (third-party changelog aggregators, not n8n's own primary release notes verified directly here)

7. What: n8n's AI Agent node (2026) enforces JSON schema validation on every tool-call response and auto-retries when an LLM returns malformed data, specifically to prevent infinite loops and hallucinated API requests.
   Why it matters: A concrete guardrail pattern worth mirroring in any custom orchestration code in this repo that parses LLM output as structured data (e.g., board card updates) — validate against schema before acting, retry on mismatch rather than trusting the first response.
   Confidence: med

## For This Workspace
- Formalize the existing informal PO review as an explicit "LLM-as-judge" step in `.agent-harness/DELEGATION-CONTRACT.md`: require a second-pass validation (schema/claim check) on every research/build draft before it's promoted from `.agent-memory/inbox/` into `topics/`, matching the 2026 standard pattern rather than relying on PO judgment alone.
- For headless `claude -p` cron jobs (per `memory/webblog-cron-scheduling.md`), add a lightweight Reflexion-style retry: on a failed/errored run, feed the prior run's error output back into the next invocation's prompt context rather than a blind identical retry — cheap to add, evidenced to improve pass rate.
- If n8n Code nodes are used anywhere in the dashboard-regeneration pipeline (`.agent-dashboard/src/dashboard-server.swift` or its n8n triggers), confirm Task Runners are enabled (should be default in 2026 n8n) so a bad script can't take down the whole n8n instance that also drives cron-triggered agent jobs.
- When/if any automated remediation is added to the QA gate (e.g., auto-fixing a broken symlink or malformed board.json), keep it to "propose fix, require explicit approval" for anything that touches git history, deploys, or deletes files — consistent with both the 2026 "controlled autonomy" pattern and this repo's existing PO-never-merges-unverified rule.

## Sources
- https://www.digitalapplied.com/blog/multi-agent-orchestration-5-patterns-that-work
- https://beam.ai/agentic-insights/multi-agent-orchestration-patterns-production
- https://apptad.com/insights/multi-agent-orchestration-architecture-patterns/
- https://www.developersdigest.tech/blog/how-to-coordinate-multiple-ai-agents
- https://www.taskade.com/blog/ai-agent-error-recovery
- https://arxiv.org/abs/2605.06737
- https://arxiv.org/html/2608.01955v1
- https://novaaiops.com/self-healing-infrastructure
- https://optimumpartners.com/insight/how-to-architect-self-healing-ci/cd-for-agentic-ai/
- https://nodesify.com/blog/n8n-workflow-automation-guide-2026
- https://www.softomatesolutions.com/blog/n8n-updates-2026-whats-new/
- https://docs.n8n.io/release-notes
