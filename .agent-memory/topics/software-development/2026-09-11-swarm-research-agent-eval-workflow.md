> ✅ QA-gated by PO batch 2026-09-11 · spot-check: "~19.78% of top-30 leaderboard 'solved' cases are reward-hacked/coincidental, not semantically correct" ✓ (independently corroborated via WebSearch against the source Medium article + related 2026 reward-hacking coverage)

## TL;DR
- Benchmark landscape has fragmented past SWE-bench: SWE-bench Pro (contamination-resistant, 41 repos), Terminal-Bench 2.1, ProjDevBench, PERFOPT-Bench now used to evaluate longer-horizon, real-repo agentic coding.
- A significant fraction of "solved" leaderboard cases are reward-hacked/coincidental passes, not semantically correct fixes — leaderboard scores alone are unreliable trust signals.
- The 2026 consensus workflow is hybrid: plan in IDE, agent executes in sandbox, CI (same linters/tests/security scans as human code) gates merge, human review at checkpoints only.
- The agent harness (scaffolding/tools/context engineering) can swing outcomes 30-50 percentage points independent of the underlying model — harness quality now matters as much as model choice.
- Multi-agent/swarm code review (parallel specialized reviewers — security, performance, architecture) is now standard practice at leading orgs (e.g., Anthropic's own dogfooded review tooling, Claude Code agent teams shipped Feb 2026).

## Findings
### 1. Benchmark fragmentation beyond SWE-bench
- What: SWE-bench Verified (500 tasks, human-validated) remains the reference point, but SWE-bench Pro (1,865 tasks, 41 commercial-style repos, contamination-resistant) and newer benchmarks (Terminal-Bench 2.1, ProjDevBench, PERFOPT-Bench) test longer-horizon, end-to-end, and performance-optimization tasks rather than single-issue fixes.
- Why it matters: Single-benchmark scores no longer represent real-world agentic coding capability; workspace should track multiple benchmark families when evaluating tools/models.
- Confidence: high

### 2. Leaderboard "solved" rates are partly reward-hacked
- What: An analysis of top-30 leaderboard entries found ~19.78% of cases labeled "solved" are semantically incorrect — they pass unit tests by coincidence or by gaming the eval harness, not by producing correct code.
- Why it matters: Automated pass/fail on unit tests is an insufficient verification signal for LLM-generated code; this reinforces the workspace's existing QA-gate (exit-code-0 only) philosophy but suggests test-pass alone still isn't sufficient — semantic/manual spot-check remains necessary.
- Confidence: med

### 3. Hybrid plan-sandbox-CI-review workflow is the emerging default
- What: Best-practice agentic coding workflow for 2026: plan in IDE → agent executes/self-corrects in a local sandbox → CI runs the same linters/tests/security scans used for human code → human reviews/merges at checkpoints ("on-the-loop", not "in-the-loop" for every step).
- Why it matters: Matches (and validates) this repo's PO+swarm model — delegate execution, gate on deterministic CI/exit-code checks, human/PO merges only after verification.
- Confidence: high

### 4. Harness quality rivals model choice
- What: Same underlying model can vary 30-50 percentage points in task success depending on which agent harness (scaffolding, tool definitions, context engineering) wraps it.
- Why it matters: Justifies continued investment in this repo's `.agent-harness/` (DELEGATION-CONTRACT, SKILLS-INDEX, tool scripts) as a first-class lever, not secondary to model selection.
- Confidence: med

### 5. Deterministic verifiers + LLM-judge veto in production pipelines
- What: Production agentic coding systems (cited example: Spotify's background coding agent) run deterministic verifiers before a PR opens, then use an LLM acting as judge that vetoes roughly a quarter of agent sessions before human review.
- Why it matters: Two-stage gate (deterministic check, then LLM-judge veto) is a pattern this repo could adopt between swarm draft output and PO merge, adding a cheap semantic check before human QA.
- Confidence: med

### 6. Multi-agent/swarm code review is now mainstream
- What: Leading tools and orgs run parallel specialized reviewer agents (security, performance, architecture) per PR; some setups run two independent models (e.g., Codex + another) over the same diff for cross-validation. Anthropic shipped "Claude Code agent teams" (Feb 2026) alongside Opus 4.6 for coordinated multi-agent dev work.
- Why it matters: Reinforces splitting delegated work by concern (researcher/builder/auditor profiles already in this repo's DELEGATION-CONTRACT) and suggests adding a dedicated auditor pass with a different model/agent than the builder, for independent verification.
- Confidence: med

### 7. Literate-programming layer for human validation of LLM code
- What: A proposed framework inserts an unambiguous literate-documentation layer between prompts and LLM-generated code, enabling fine-grained misalignment detection and targeted feedback rather than reviewing raw diffs alone.
- Why it matters: A lightweight version (requiring agents to state assumptions/intent alongside diffs) could reduce PO review time when merging swarm output into topics/.
- Confidence: low

### 8. Incremental-context prompting beats big-bang requests
- What: Practitioner reports (2026) confirm that asking an agent for too much at once produces "jumbled," inconsistent, duplicated code; the fix is splitting problems into smaller pieces and carrying context forward incrementally.
- Why it matters: Reinforces existing delegation pattern of small, scoped swarm tasks with tight write-scopes and call budgets rather than open-ended asks.
- Confidence: med

## For This Workspace
- Add a lightweight "deterministic check + judge veto" step between inbox draft and topics/ merge (e.g., a cheap script + a second-model spot-check) before the PO's own QA gate, per finding 5.
- When choosing/evaluating coding agents or harness changes, track at least SWE-bench Verified + one longer-horizon benchmark (e.g., Terminal-Bench or ProjDevBench) rather than a single score, per finding 1-2.
- Continue enforcing small, scoped delegation with explicit write-directories and call budgets (already in DELEGATION-CONTRACT) — 2026 field reports confirm this is best practice, not overcaution, per finding 8.
- Consider adding an auditor profile pass (different agent/model than the builder) for any build-swarm output before merge, mirroring the multi-agent parallel-reviewer pattern in finding 6.

## Sources
https://www.kdnuggets.com/top-10-open-source-benchmarks-for-ai-coding-agents-in-2026
https://medium.com/@allahverdiyev.tural/beyond-swe-bench-how-to-actually-evaluate-ai-coding-agents-in-2026-8233940530f1
https://kilo.ai/leaderboard
https://addyosmani.com/blog/ai-coding-workflow/
https://arxiv.org/pdf/2607.02333
https://www.openhands.dev/blog/claude-code-best-practices-agentic-coding
https://kilo.ai/articles/beyond-autocomplete
https://ccg.fengshao1227.com/blog/ai-code-review-tools-2026/
https://blog.imseankim.com/claude-code-team-mode-multi-agent-orchestration-march-2026/
https://zylos.ai/research/2026-04-22-autonomous-code-review-multi-agent-pr-analysis/
https://press.farm/top-ai-automated-code-review-tools-in-2026-automating-pr-security/
