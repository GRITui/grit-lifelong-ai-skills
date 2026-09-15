> ✅ QA-gated by PO batch 2026-09-09 · spot-check: "SWE-bench Pro top score" ✓ — corrected from a single "~57%" figure (rejected in a prior pass) to the verified range below; independent search confirms scores vary 51.9%-81.2% by evaluation harness/vendor (Scale AI public set: GPT-5.4 xHigh 59.1%, Claude Opus 4.6 51.9%; vendor-aggregate leaderboards: Claude Fable 5.1 81.2%), so no single number is meaningful without naming the harness.

## TL;DR
- Context engineering — curating what an agent sees, not raw context size — is now treated as the primary lever for coding-agent quality; benchmarks show more tokens can make agents perform *worse* if the extra tokens are low-signal.
- The "scratchpad/structured-note" memory pattern (write notes to files outside the context window, re-read on demand) is emerging as the standard architecture for long-running coding agents — directly analogous to this repo's `.agent-memory/` design.
- SWE-bench (the dominant coding-agent benchmark) is fragmenting into harder, contamination-resistant variants (SWE-bench Pro, SWE-Compass) because the original benchmark is saturating near ~80% for frontier models.
- Testing AI-generated code is shifting from "more unit tests" to targeted defect-class testing (error handling, concurrency, security boundaries, edge cases) plus property-based testing, because AI-authored bugs cluster in predictable categories.
- AI code review is now a first-class CI step (GitHub Copilot code review, CodeRabbit, Cursor review agents) doing line-level PR comments, but 2026 sources note it's best used for style/consistency enforcement, not a substitute for behavioral verification.

## Findings

### Context engineering supersedes "bigger context window"
- What: Sourcegraph's 2026 benchmarking found agents given a 100K-token codebase summary performed worse than agents given 5K tokens of targeted retrieval — 20x the context with worse results.
- Why it matters: Directly validates minimal, curated context over dumping full history/files at an agent — relevant to how much this repo's swarm agents should be handed vs. told to look up.
- Confidence: med (single vendor blog benchmark, not independently replicated, but consistent with Anthropic's own guidance).

### Structured note-taking / scratchpad memory pattern
- What: Coding agents increasingly write persistent notes/scratchpads to a file outside the model's context window and re-read them on demand, rather than keeping everything in-context or relying on vector-DB long-term memory.
- Why it matters: This is architecturally identical to this repo's `.agent-memory/topics/` + inbox + QA-gate design — external validation that file-based, human-auditable memory is a live 2026 pattern, not a workaround.
- Confidence: med (pattern reported across multiple secondary sources; traces back to Anthropic's context-engineering guidance).

### Tool Search / curated tool sets over large tool lists
- What: 2026 best practice is to expose a small, high-signal set of tools per agent by default and use a "Tool Search"-style mechanism to load additional tool schemas on demand, rather than loading a large static tool list into context up front.
- Why it matters: This mirrors the deferred-tool mechanism already in use in this session (ToolSearch loading WebSearch/WebFetch schemas on demand) — confirms it's a deliberate, current design pattern worth relying on for future swarm agent configs.
- Confidence: med.

### SWE-bench is saturating and fragmenting into harder variants
- What: As of ~April 2026, frontier models (Claude Opus 4.6, Gemini 3.1 Pro, Claude Opus 4.5) score 80-81% on SWE-bench Verified. New benchmarks — SWE-bench Pro (1,865 tasks, 41 repos, Python/Go/TS/JS, private codebases to resist contamination) and SWE-Compass (8 languages, multiple task types) — were built because the original single-language, GitHub-issue-style benchmark is no longer discriminating between top models. SWE-bench Pro scores vary sharply by evaluation harness: on Scale AI's standardized public set the top score is ~59% (GPT-5.4 xHigh, with Claude Opus 4.6 around 52%), while vendor-aggregate leaderboards report 80%+ for top models — the same benchmark name, very different numbers depending on who ran it.
- Why it matters: A benchmark score quoted for a coding model/agent must specify *both* the SWE-bench variant *and* the evaluation harness/leaderboard — "SWE-bench Pro" alone is not a comparable number across sources. Useful when evaluating which model/agent to route a task to, but a single figure without harness context should be treated as unverified.
- Confidence: high (multiple corroborating sources; the harness-dependent spread itself independently confirmed via spot-check).

### Testing strategy for AI-generated code targets specific defect classes, not just more tests
- What: 2026 QA guidance recommends establishing a behavior baseline *before* letting an agent touch code, then layering static analysis, edge-case unit tests, property-based testing, and infrastructure-fault testing (network partitions, queue delays) specifically because AI-generated bugs cluster in error handling, concurrency, and security-boundary code — reported as needing roughly 30-50% more testing time than hand-written code, but qualitatively different testing, not just more of the same.
- Why it matters: Directly actionable for QA-gating agent output in this repo — the QA gate in CLAUDE.md ("exit code 0, never on intent") should specifically probe error paths and edge cases rather than just running the happy path.
- Confidence: low-med (sourced mostly from SEO-style QA vendor blogs — Skyramp, TestDino, Shiplight — rather than primary engineering sources; directionally plausible but treat specific % figures as unverified marketing claims).

### AI code review is now embedded in CI but scoped to style/consistency, not correctness sign-off
- What: GitHub Copilot code review, CodeRabbit, Cursor's review agent, and Augment Code's review agent post automated line-level PR comments (style, obvious bugs, security patterns) in 2026 workflows; GitHub Copilot CLI (Aug 2026) defaults to claude-sonnet-5 and supports BYOK providers for review.
- Why it matters: Useful as a cheap first-pass filter before a human/PO merges swarm output, but sources are consistent that it complements rather than replaces behavioral/functional verification — same principle as this repo's PO QA gate.
- Confidence: med.

### AI-to-AI PR review is an emerging research area
- What: A 2026 arXiv paper ("AI-to-AI Code Reviews of GitHub Pull Requests") studies cases where one AI agent opens a PR and another AI agent reviews it, examining review quality and failure modes.
- Why it matters: Directly relevant to this repo's swarm model (agents producing drafts that other processes must gate) — worth a future deeper-dive read if the PO wants agents cross-reviewing each other's inbox drafts before promotion to topics/.
- Confidence: low (single paper, not yet corroborated at scale).

## For This Workspace
- The scratchpad/structured-note and Tool Search patterns found here are already what this repo does (`.agent-memory/inbox` + deferred ToolSearch) — treat this as confirmation to keep swarm agents writing to files rather than trying to keep everything in one long-context session.
- When quoting a coding-agent benchmark score to justify a model choice for a swarm task, name both the specific SWE-bench variant (Verified vs. Pro vs. Compass) *and* the evaluation harness/leaderboard — Pro scores alone range from ~52% to 81%+ depending on who ran the eval, so a bare percentage is not comparable across sources and mixing them up would misinform model-routing decisions.
- Extend the QA gate in CLAUDE.md for any future code-generation tasks: beyond `bash -n` / exit-code checks, add at least one deliberate edge-case or error-path check (the 2026 literature's core claim is that AI-authored bugs cluster there specifically).
- Consider a light "AI-to-AI review" step for future research swarms: before a PO promotes an inbox draft to topics/, have a second, independent agent do a source spot-check pass — cheap and matches the emerging pattern in the cited AI-to-AI PR review research.

## Sources
https://sourcegraph.com/blog/context-engineering
https://epoch.ai/benchmarks/swe-bench-verified
https://codeant.ai/blogs/swe-bench-scores
https://github.com/swe-bench/SWE-bench
https://arxiv.org/pdf/2604.03515
https://arxiv.org/pdf/2605.05400
https://arxiv.org/pdf/2512.05470
https://arxiv.org/html/2608.21311v1
https://skyramp.dev/blog/testing-ai-generated-code
https://testdino.com/blog/how-to-test-ai-generated-code
https://www.shiplight.ai/blog/testing-strategy-for-ai-generated-code
https://daily.dev/blog/best-ai-coding-agents-comparison/
https://mightybot.ai/blog/coding-ai-agents-for-accelerating-engineering-workflows/
