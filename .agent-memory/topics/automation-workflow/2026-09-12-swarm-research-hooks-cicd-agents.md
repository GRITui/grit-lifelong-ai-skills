> ✅ QA-gated by PO 2026-09-12 · spot-check: Claude Code hooks fire on PreToolUse/PostToolUse/Stop lifecycle events ✓

## TL;DR
- Claude Code **hooks** (deterministic shell commands fired on lifecycle events — PreToolUse, PostToolUse, etc.) are the 2026-recommended mechanism for anything that must *always* happen (formatting, safety gates, audit logging) — CLAUDE.md/skills are requests, hooks are guarantees. Not yet used in this repo's harness.
- Temporal has become the dominant "durable execution" substrate for agentic workflows in 2026: automatic state capture + resume-on-failure, an official OpenAI Agents SDK integration, and adoption inside OpenAI's own production infra.
- GitHub shipped **Agentic Workflows** (Feb 2026) — natural-language-defined agents running inside GitHub Actions, triggered by issues/PRs/CI events, with a mandatory human-approval gate before any Actions run triggered by an agent-authored PR.
- A new vulnerability class, **PromptPwnd**, targets agentic CI: untrusted text (an issue title, a PR body) gets interpolated into an agent's prompt inside a privileged CI job, letting hidden instructions trigger privileged tool calls.
- Confidence-threshold gating (agent acts autonomously above ~0.70–0.90 confidence, escalates to human below it) is emerging as a named pattern for where to draw the "controlled autonomy" line in CI/agent pipelines.

## Findings

1. **What**: Claude Code hooks are shell commands bound to lifecycle events (PreToolUse, PostToolUse, Stop, etc.); 2026 guidance frames the rule as "if it must be enforced, use a hook or permission; if it's contextual knowledge, use a skill or CLAUDE.md — instructions are requests, hooks are guarantees."
   **Why it matters**: This repo currently enforces everything (delegation contract, write-scope limits, no-emoji, QA gates) through CLAUDE.md prose and subagent honor-system compliance. Hooks are the concrete mechanism to make a subset of those rules unbypassable rather than merely instructed.
   **Confidence**: high (multiple independent 2026 guides converge on the same framing)

2. **What**: Best-practice guidance explicitly warns that a bad `PreToolUse` hook can lock you out of Claude entirely, so hooks should be tested on a throwaway repo first, kept as simple one-line shell commands (not large embedded bash scripts inside JSON), and never used to silently bypass permission prompts (e.g. wrapping `--no-verify` into a hook).
   **Why it matters**: Directly relevant if this repo ever adds hooks to enforce the DELEGATION-CONTRACT write-scope rule — the failure mode (self-lockout) is severe enough to warrant a sandbox test first.
   **Confidence**: high

3. **What**: Temporal's 2026 roadmap reached GA on Temporal Nexus and Multi-Region Replication (99.99% SLA), added an official OpenAI Agents SDK integration for durable orchestration, and is used in production by OpenAI itself for agentic-AI infrastructure; Gartner projects 40% of enterprise apps will have task-specific AI agents by end of 2026 (up from <5% in 2025).
   **Why it matters**: Temporal-style durable execution (automatic checkpointing, resume-without-loss on crash) is a heavier-weight alternative to this repo's simpler cron/launchd + board.json handshake pattern — worth knowing as the "what production teams reach for once scale/reliability requirements exceed a single-machine cron setup" reference point, not an immediate migration need.
   **Confidence**: med (aggregated from Temporal's own marketing pages + third-party summaries, not independently verified against a primary engineering blog post)

4. **What**: GitHub launched Agentic Workflows (Feb 2026) inside GitHub Actions — agents triggered by issues/PRs/CI events, described in natural language rather than YAML, that can triage bugs, write fixes/tests, and open PRs unattended. GitHub's stated safety decision: agent-authored PRs require explicit human approval before any Actions workflow runs against them.
   **Why it matters**: This repo just added an "AI agent QA gate" via GitHub Actions (per recent commit `7fcc59a`) — GitHub's own approval-before-run policy for agent PRs is a directly applicable pattern to mirror or compare against in that gate's design.
   **Confidence**: med (drawn from secondary write-ups of the GitHub announcement, not GitHub's primary docs page)

5. **What**: A named vulnerability class, "PromptPwnd," describes untrusted user-supplied text (issue titles, PR descriptions, comments) being interpolated directly into an agent's prompt when that agent runs inside a CI job with privileged tool access — hidden instructions in the untrusted text can cause the agent to invoke privileged tools it shouldn't.
   **Why it matters**: Any future automation here that lets an LLM read GitHub issues/PRs and act with repo-write or deploy privileges (e.g. auto-triage) must treat issue/PR body text as untrusted input, not as trusted instructions — a concrete injection risk to design against before adding such a flow.
   **Confidence**: med (single vulnerability-class writeup, not cross-confirmed by a second independent source)

6. **What**: 2026 CI/CD-for-agents writeups describe confidence-threshold gating — an agent acts autonomously when its self-reported/derived confidence is above roughly 0.70–0.90, and escalates to a human otherwise — as a concrete implementation of "controlled autonomy" inside pipelines.
   **Why it matters**: Gives a more specific, numeric version of the "controlled autonomy" pattern already noted in this topic's 2026-09-11 research (propose-fix-require-approval) — a threshold is something this repo's QA gate or delegation contract could actually encode rather than leaving the escalation decision qualitative.
   **Confidence**: low (single aggregator source citing thresholds without attribution to a primary study)

## For This Workspace
- Evaluate adding a small number of Claude Code **hooks** (not full replacement of CLAUDE.md) for the highest-value guarantees already stated as prose rules — e.g. a `PreToolUse` hook that blocks `Write`/`Edit` calls outside a subagent's declared write-scope directory, turning the DELEGATION-CONTRACT's "write scope" rule from an honor-system instruction into an enforced guardrail. Test on a throwaway repo first per the 2026 guidance in Finding 2 — a bad `PreToolUse` hook can self-lock the session.
- Treat GitHub's "approval required before Actions run on agent-authored PRs" policy as the reference design for the newly-added AI-agent QA gate (`7fcc59a`) — confirm the gate requires a human/PO approval step before any CI job with write/deploy privileges runs against a PR whose diff originated from an agent.
- If any future workflow here has an agent read GitHub issues/PR bodies and act on them (triage, auto-fix), explicitly sanitize/quote that text as untrusted data before it enters the agent's prompt — do not let issue/PR text be interpreted as instructions (PromptPwnd risk, Finding 5).
- Temporal-style durable execution is not a near-term need for this repo's scale (single-machine cron/launchd + board.json), but keep it as the named reference point if the automation-workflow topic ever needs to answer "what's the production-grade upgrade path beyond cron once reliability requirements grow."

## Sources
- https://www.datacamp.com/tutorial/claude-code-hooks
- https://promptessor.com/blog/best-claude-code-hooks-examples-for-safer-automated-coding-workflows-in-2026
- https://smartscope.blog/en/generative-ai/claude/claude-code-best-practices-advanced-2026/
- https://temporal.io/pages/durable-ai-agent-bundle
- https://olmecdynamics.com/news/temporal-durable-execution-agentic-workflows-2026
- https://intuitionlabs.ai/articles/agentic-ai-temporal-orchestration
- https://medium.com/@Micheal-Lanham/github-just-made-ai-agents-part-of-ci-cd-heres-how-to-build-your-first-agentic-workflow-d6f7d9fe62ff
- https://alexlavaee.me/blog/agent-operated-cicd-pipelines/
- https://gravitydevops.com/ai-agents-cicd-pipelines-2026/
- https://www.buildmvpfast.com/blog/ai-agents-ci-cd-pipeline-devops-automation-2026
