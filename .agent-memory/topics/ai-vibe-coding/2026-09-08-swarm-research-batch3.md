> ✅ QA-gated by PO batch 2026-09-08 · spot-check: Veracode Spring 2026 security pass rate ~55% (independently found 56% pass rate / 45% flaw rate, Java worst) ✓

## TL;DR

- Context engineering (not prompt engineering) is now the dominant skill: more tokens ≠ better — targeted 5K-token retrieval beat a 100K-token codebase dump in benchmarks.
- AI-generated code security is stagnant-to-worse: ~45% of generation tasks still introduce known flaws; AI-assisted devs at Fortune 50s ship 3-4x more commits but 10x more security findings.
- "Workslop" (polished-but-hollow AI output that creates downstream review burden) is a named, measured 2026 workplace problem — 66% of workers spend 6+ hrs/week fixing AI mistakes.
- Skill atrophy is now empirically measured, not just anecdotal: Anthropic's 2026 study found a 17-point comprehension-quiz gap for AI-assisted devs learning new libraries.
- Claude Code's own ecosystem has matured into three orchestration tiers (subagents / Agent Teams / external orchestrators) — subagents cover ~80% of needs; Agent Teams add genuine cross-agent negotiation but cost multiplies per agent.

## Findings

1. **What:** Anthropic's 2026 Agentic Coding report calls context engineering "the load-bearing skill of 2026." Teams with well-maintained context files (CLAUDE.md-style repo memory) reportedly ship with 40% fewer errors and complete tasks 55% faster.
   **Why it matters:** Directly validates this repo's own QA-gated `.agent-memory/` design — persistent, curated repo context is treated as the highest-leverage lever in the field, not a nice-to-have.
   **Confidence:** med (vendor-reported figures, not independently replicated; but corroborated by Sourcegraph's separate benchmark finding).

2. **What:** Sourcegraph benchmarked coding agents on identical tasks and found agents given a 100K-token full codebase summary performed *worse* than agents given 5K tokens of targeted retrieval.
   **Why it matters:** Confirms "more context = worse," a specific, actionable finding for anyone building retrieval/memory into an agent harness — favors selection/compression/pruning over dumping.
   **Confidence:** med (single-source benchmark, but methodologically concrete and widely cited).

3. **What:** Veracode's Spring 2026 GenAI Code Security study (150+ LLMs) found only ~55% of AI code-generation tasks produce secure code; Java fails worst (72% failure rate). Separately, 35 new CVEs were disclosed from AI-generated code in March 2026 alone (up from 6 in January).
   **Why it matters:** Security has not improved despite vendor claims — code review / secure-coding gates remain mandatory even (especially) for agent-written code.
   **Confidence:** high (large longitudinal industry study + CVE tracking data, cross-corroborated by CSA Vibe Security Radar).

4. **What:** An empirical study across Fortune 50 enterprises found AI-assisted developers commit 3-4x faster than peers but introduce security findings at 10x the rate.
   **Why it matters:** Quantifies the speed/safety tradeoff — supports gating merges on verification (exactly this repo's QA-gate model) rather than trusting agent velocity alone.
   **Confidence:** med (single study, enterprise-specific, exact methodology not verified firsthand).

5. **What:** Anthropic's 2026 comprehension study: developers who used AI assistance while learning a new library scored ~50% vs. 67% (a 17-point gap) on an immediate comprehension quiz vs. unassisted developers. Follow-on research distinguishes "accept-without-reading" users (measurably worse at debugging unfamiliar code over time) from "draft-then-review-carefully" users (who ship more without losing skill).
   **Why it matters:** Skill atrophy is real but *conditional on usage pattern* — the mitigation is workflow discipline (review/understand before accept), not avoiding AI tools.
   **Confidence:** med (Anthropic self-reported study; independently-run follow-up work is emerging but thinner).

6. **What:** Stanford/BetterUp-linked 2026 research coined and measured "workslop": AI output that looks polished but is riddled with errors/hallucinations. 40% of workers received workslop in the last month; 66% say reviewing others' AI output creates extra work; ~$9M/year estimated correction cost per 10,000 employees; 95% of orgs report no measurable AI ROI (MIT Media Lab).
   **Why it matters:** Directly relevant to swarm-based agent workflows — unreviewed subagent output can become "workslop" for the PO to clean up, which is exactly what a QA gate is meant to prevent.
   **Confidence:** med-high (Stanford-affiliated study widely picked up by HBR/CNBC; MIT ROI figure is a separate, frequently-cited but debated report).

7. **What:** GitHub's January 2026 study on agent-authored pull requests found agent-generated code introduces more redundancy and technical debt per change than human-written code; Copilot code review has processed 60M+ reviews (10x growth in under a year), and practitioner guidance is converging on "review agent PRs like a new hire's, not like a trusted senior's."
   **Why it matters:** Reinforces that agent output — even code review by agents — needs a human/PO-level trust boundary; matches this repo's "PO never merges unverified work" rule.
   **Confidence:** med (GitHub self-reported usage stats are solid; the "more tech debt" claim is a single study).

8. **What:** Claude Code's multi-agent tooling has stratified into three tiers by 2026: in-session subagents (fire-and-forget workers), the built-in "Agent Teams" feature (parallel Claude Code instances with a shared task list and direct messaging, good for genuine deliberation), and external orchestrators (Gas Town, Multiclaude, etc.) for cross-repo/cross-team runs. Guidance: subagents cover ~80% of needs; Agent Teams multiply token cost per agent added.
   **Why it matters:** Useful vocabulary/decision framework for this repo's own "PO + swarms" model — confirms subagents (current approach) are the right default, and flags that scaling to Agent-Teams-style peer coordination has a real cost multiplier.
   **Confidence:** low-med (blog/vendor-content sources, not primary Anthropic docs; treat as directional).

## For This Workspace

- **Keep context files lean, not exhaustive.** The Sourcegraph finding (5K targeted > 100K dump) argues against ever letting `.agent-memory/topics/` sprawl into unpruned mega-files — favor many small, focused topic files (which this harness already does) over consolidated ones.
- **Treat subagent/swarm output as "workslop risk" by default.** Since unreviewed AI output measurably creates downstream cleanup burden, the existing PO QA gate (spot-check claims, verify exit-0 builds before merging into `topics/`) is doing exactly the right job — don't relax it for speed.
- **If any future task involves AI-generated code changes to this repo's own scripts,** add a lightweight secure-coding check to the QA gate table (beyond `bash -n`/`shellcheck`) given the 45%+ insecure-code base rate reported in 2026 — e.g. grep for hardcoded secrets/unsafe eval patterns before writing verified memory about a script.
- **When delegating to subagents, require they show their sources/verification inline** (as this task's own format does) rather than a bare summary — mitigates the "accept without reading" skill-atrophy pattern for the PO/human reviewing swarm output.

## Sources

- https://sourcegraph.com/blog/context-engineering
- https://www.heyuan110.com/posts/ai/2026-06-16-context-engineering-2026/
- https://www.veracode.com/blog/spring-2026-genai-code-security/
- https://labs.cloudsecurityalliance.org/research/csa-research-note-ai-generated-code-vulnerability-surge-2026/
- https://sqmagazine.co.uk/ai-coding-security-vulnerability-statistics/
- https://learn.senwitt.com/blog/anthropic-coding-skill-study-what-developers-should-take-away/
- https://vucense.com/ai-intelligence/agentic-ai/when-vibe-coding-breaks-the-brain-ai-productivity-and-the-risk-of-skill-atrophy/
- https://dev.to/tanishka_karsulkar_ec9e58/the-skill-atrophy-crisis-how-ai-is-quietly-de-skilling-developers-in-2026-129j
- https://workplaceinsight.net/ai-generated-workslop-is-destroying-productivity-say-researchers/
- https://hbr.org/2026/01/why-people-create-ai-workslop-and-how-to-stop-it
- https://www.cnbc.com/2025/09/23/ai-generated-workslop-is-destroying-productivity-and-teams-researchers-say.html
- https://github.blog/ai-and-ml/generative-ai/agent-pull-requests-are-everywhere-heres-how-to-review-them/
- https://sourcegraph.com/blog/ai-code-review
- https://www.tembo.io/blog/claude-code-multi-agent-orchestration
- https://addyosmani.com/blog/code-agent-orchestra/
