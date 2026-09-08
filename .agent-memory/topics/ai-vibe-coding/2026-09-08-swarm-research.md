> ✅ QA-gated by PO batch 2026-09-08 · spot-check: Claude Code changelog v2.1.257 added "Claude Fable 5.1" (claude-fable-5-1) as default Fable model, 1M context — verified directly against code.claude.com/docs/en/changelog ✓

## TL;DR

- Claude Code's official changelog (Sep 1–6, 2026) shipped `/skill-doctor` (skill context-cost diagnostics), `/diff` panel, prompt-cache-miss diagnostics, a new default "Claude Fable 5.1" model (1M context), and new containment/egress-evasion protections for auto mode.
- Vibe-coding security is now a documented, recurring failure mode: independent scans across 2025-2026 found large fractions of publicly deployed AI-generated apps expose secrets/data (e.g., ~40% of ~5,000 scanned apps per one 2026 report; 300+/1,072 apps leaking DB keys client-side in another).
- Two new benchmarks (Vibe Code Bench v1.1, ViBench) now specifically measure end-to-end "prompt-to-working-app" agentic coding rather than isolated code completion — and even top models (Opus, GPT-5.2) only hit 42-46% Pass@1 on ViBench's realistic tasks, versus much higher scores on narrower benchmarks.
- 2026 workflow consensus (Sourcegraph, Anthropic-adjacent sources) has shifted from "prompt engineering" to "context engineering": scoped tool surfaces per (sub)agent, writer/reviewer session separation, and treating agent memory as typed data architecture rather than free-text chat history.
- Tooling landscape consolidated: Cursor acquired Continue.dev; Windsurf rebranded to "Devin Desktop" (windsurf.com now redirects to devin.ai); Codex ships a cross-platform desktop multi-agent command center.

## Findings

### Claude Code Sep 2026 release cadence
- What: Official changelog shows near-daily point releases (2.1.252 → 2.1.263, Aug 31–Sep 6 2026) adding `/skill-doctor`, `/diff`, prompt-cache diagnostics, `bashOutputMaxChars`/`taskOutputMaxChars` (up to 128K), `--append-subagent-system-prompt-file`, `CLAUDE_CODE_SUBAGENT_MODEL_FORCE`, and a one-time warning before reading files outside the working directory.
- Why it matters: `/skill-doctor` and the subagent-prompt-file flag directly affect this workspace's swarm-based skill/subagent design — worth checking whether unused skills are bloating context here. The file-read warning and containment/egress-evasion auto-mode rule are relevant to how much this repo trusts agents to roam outside cwd.
- Confidence: high (fetched directly from code.claude.com/docs/en/changelog).

### New model: "Claude Fable 5.1" as Claude Code default
- What: As of 2.1.257 (Sep 1 2026), Claude Code's default model became "Claude Fable 5.1" — 1M token context, $10/$50 per Mtok, $0.25/Mtok cache reads.
- Why it matters: Larger default context window changes the calculus for how much of `.agent-memory/topics/` can be loaded per session vs. relying on targeted grep/glob recall.
- Confidence: high (official changelog).

### Vibe coding security failures are now a well-documented pattern, not anecdote
- What: Multiple independent 2026 write-ups (NordLayer, Arnica, IANS Research, OX Security, a Medium audit, VibeEval's "2026 AI Coding Security Report") converge on the same picture: AI-generated apps ship with client-side-exposed DB keys, missing auth checks, and broad data exposure at meaningful scale (one report: ~40% of ~5,000 scanned vibe-coded apps exposed sensitive data; another: 300+/1,072 apps leaked DB keys, 172 allowed unauthenticated deletes). Named incidents include a Lovable authorization bug (CVE-2025-48757) and the "Tea" app message-exposure incident.
- Why it matters: Directly relevant lesson for any "ship fast with an agent" workflow — auth/authz and secret-handling need an explicit QA gate step, not just "did it run."
- Confidence: med (numbers vary by source/methodology, but the qualitative pattern is corroborated across many independent outlets — worth treating as directionally solid, not exact).

### Realistic end-to-end benchmarks show agentic coding is far from solved
- What: ViBench (CAIS 2026), a new open benchmark for full natural-language-to-working-web-app tasks, found even leading models (Opus 4.6, GPT-5.2) only achieve 42-46% Pass@1 — much lower than these models' scores on narrower code-completion benchmarks. Vibe Code Bench v1.1 (a different, narrower benchmark) reports "Claude Fable 5" at 90.35%.
- Why it matters: The gap between narrow-benchmark scores and realistic end-to-end task success is a caution against over-trusting "vibe coded, it worked once" as sufficient QA — reinforces this repo's own QA-gate-before-memory principle.
- Confidence: med (benchmark methodology differs significantly between the two; treat absolute numbers loosely, trend is the useful signal).

### Shift from "prompt engineering" to "context engineering" / scoped subagent design
- What: 2026 sources (Sourcegraph blog, metacto, mem0.ai) describe a consensus practice: curate a small, scoped tool surface per agent/subagent rather than giving every agent every tool; use tool-search/on-demand tool loading for the long tail; separate "writer" and "reviewer" sessions so review isn't biased by the agent's own prior output; treat memory as typed/structured data tied to a business key rather than raw chat transcript.
- Why it matters: This matches (and validates) the existing PO+swarm / research-writes-to-inbox / QA-gate-then-promote-to-topics design already in this repo's CLAUDE.md — no architecture change needed, but confirms the pattern is current best practice, not idiosyncratic.
- Confidence: med (aggregated marketing/blog content, not primary research, but consistent across multiple independent vendors).

### Coding-tool market consolidation and rebrands
- What: Cursor acquired Continue.dev. Windsurf rebranded to "Devin Desktop" (windsurf.com redirects to devin.ai) as of June 2, 2026. OpenAI Codex ships a desktop multi-agent command center on macOS and Windows, bundled into ChatGPT Plus/Pro/$200 tiers rather than sold as a standalone subscription.
- Why it matters: If any future task in this workspace references "Windsurf" by name, note the rebrand — old docs/links may 404 or redirect.
- Confidence: med (multiple comparison-blog sources agree, but these are SEO/comparison content rather than primary vendor announcements — worth a spot-check before relying on exact dates).

### Adoption data point: AI coding tools in YC startups
- What: One 2026 source states roughly 40% of a recent Y Combinator batch used AI coding tools to build their MVPs, and frames the vibe-coding category as split into "agentic full-app builders" vs. "AI-first IDEs that accelerate developers."
- Why it matters: Useful directional signal for how mainstream agent-driven build workflows have become, though it's a single secondary-source claim.
- Confidence: low (single blog aggregation, no primary citation found for the YC statistic itself).

## For This Workspace

1. Run `/skill-doctor` (new in Claude Code 2.1.261) in this repo to check whether any of the many skills listed in the system context are unused dead weight inflating context per session.
2. Given the vibe-coding security pattern (exposed secrets/auth gaps), consider adding an explicit "secrets/auth check" line item to the Step 2 QA Gate table in `/Users/grit/CLAUDE.md` for any future task that touches deploy configs, DNS, or API tokens (the repo already handles Hostinger/token hygiene well, but this generalizes it).
3. If any topic files or automation reference "Windsurf," add a note that it rebranded to Devin Desktop (windsurf.com → devin.ai) as of June 2026, so future searches/links aren't stale.
4. Given the 1M-context "Claude Fable 5.1" default and larger `bashOutputMaxChars`/`taskOutputMaxChars`, it may be safe to loosen any conservative context-budgeting assumptions baked into swarm-agent prompts in this workspace — worth a small test before broadly adopting.

## Sources

https://code.claude.com/docs/en/changelog
https://blog.mean.ceo/claude-code-news-september-2026/
https://www.gradually.ai/en/changelogs/claude-code/
https://releasebot.io/updates/anthropic/claude-code
https://releasebot.io/updates/anthropic
https://arxiv.org/pdf/2510.12399
https://keyholesoftware.com/vibe-coding-trends-2026/
https://www.vals.ai/benchmarks/vibe-code
https://www.caisconf.org/program/2026/papers/vibench-a-benchmark-on-vibe-coding/
https://www.crewscale.com/blog/best-vibe-coding-tools-2026
https://benchlm.ai/benchmarks/vibecodebench
https://dev.to/pockit_tools/cursor-vs-windsurf-vs-claude-code-in-2026-the-honest-comparison-after-using-all-three-3gof
https://kingy.ai/news/codex-vs-claude-code-vs-cursor-vs-windsurf-vs-manus-a-practical-map-of-ai-coding-agents-for-2026/
https://www.frankx.ai/blog/cursor-vs-claude-code-vs-windsurf-2026
https://lushbinary.com/blog/ai-coding-agents-comparison-cursor-windsurf-claude-copilot-kiro-2026/
https://copilot-alternatives.com/blog/cursor-vs-windsurf-2026
https://nordlayer.com/blog/vibe-coding-security/
https://www.arnica.io/blog/vibe-coding-security-risks
https://www.iansresearch.com/resources/all-blogs/post/security-blog/2026/05/15/easy-to-build--easy-to-expose--how-vibe-coding-is-creating-new-data-risks
https://medium.com/developersglobal/the-vibe-coding-security-gap-9a1c3fb7fecf
https://www.ox.security/blog/vibe-coding-security/
https://vibe-eval.com/updates/2026-ai-coding-security-report/
https://www.metacto.com/blogs/context-rich-environments-ai-agents
https://www.make.com/en/blog/agent-workflow-memory
https://sourcegraph.com/blog/context-engineering
https://mem0.ai/blog/context-engineering-ai-agents-guide
https://www.futureproofing.dev/resources/ai-native-team/agentic-coding-workflow-2026
