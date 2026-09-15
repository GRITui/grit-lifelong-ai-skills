> ✅ QA-gated by PO batch 2026-09-11 · spot-check: AIDev security-smell study (arXiv 2607.12428) headline figures ✓ (38.9% PRs w/ ≥1 smell = 1,563/4,022; 23.6% files flagged = 3,807/16,112; 8,701 total smells; supply-chain=82.3%; 253 critical, 99.6% hard-coded creds; judge precision 0.908/F1 0.836 — all confirmed verbatim against arxiv.org/html/2607.12428v1)

## TL;DR
- Empirical study of 4,022 agent-generated PRs (AIDev dataset) finds 38.9% contain at least one security smell, dominated by supply-chain issues; hard-coded credentials are 99.6% of critical-severity smells.
- A controlled benchmark shows product-context retrieval ("Brief"-style augmentation) lifts an agent's compliance with team-specific product decisions from 46% to 95% (+49 points) on 41 weighted decision points across 8 tasks — the baseline agent hits 100% on decisions visible in code but only 0-33% on decisions that live outside the codebase.
- Microsoft Agent Framework (converged AutoGen + Semantic Kernel) reached 1.0 GA April 2, 2026, and BUILD 2026 introduced "Agent Harness" as a first-class concept: shell/filesystem access, human-in-the-loop approval, and long-session context management — validates this repo's own harness-as-layer approach.
- Developer trust in agent output has risen but stays split: one 2026 survey finds 85.5% trust agent outputs "at least somewhat" (24.7% fully), while other 2026 data still shows most developers manually re-verify AI-written code.
- New context-engineering research directions beyond what's already tracked: "Mise en Place" (deliberate pre-task preparation as a methodology) and self-adaptive/rubric-based context pruning for long-horizon coding agents.

## Findings

1. **What**: AIDev-dataset study (arXiv 2607.12428) analyzed 16,112 file changes across 4,022 autonomous-agent PRs using an LLM judge (0.908 precision, 0.836 F1 vs. human-annotated gold set). 38.9% of PRs had ≥1 security smell; 23.6% of files (3,807/16,112) were flagged; 8,701 distinct smells found. Supply-chain integrity issues were 82.3% of all smells; over-privileged execution 9.6%; secrets/identity 3.4%. Of 253 critical-severity issues, hard-coded credentials were 99.6%. Notably, humans (not agents) introduced 67.6% of genuine leaked secrets, and 81.1% of those went undetected by reviewers before merge.
   **Why it matters**: Directly extends the existing "agent misalignment failure modes" and "security debt" thread with hard numbers — and complicates the narrative: the largest credential-leak risk in this corpus was human-introduced, not agent-introduced, though agents still produce plenty of supply-chain smells.
   **Confidence**: high (numbers pulled directly from arxiv.org/html/2607.12428v1).

2. **What**: Context-Augmented Code Generation benchmark (arXiv 2605.08112): Claude Code with codebase-only access scored 46% decision compliance across 41 weighted product-decision points in 8 SWE tasks; adding a product-context retrieval layer (specs, mid-build consultation, recorded decisions, persona/customer signals, competitive intel) raised compliance to 95% — a 49-point jump. The baseline was already at 100% for decisions visible in source code; the entire gap was in decisions that exist only outside the repo.
   **Why it matters**: Quantifies exactly why AGENTS.md/CLAUDE.md-style context files matter, and specifically that the value is concentrated in "invisible" product/business context, not code-visible logic — a sharper claim than generic context-engineering advice.
   **Confidence**: high (numbers pulled directly from arxiv.org/abs/2605.08112 abstract page).

3. **What**: Microsoft Agent Framework (merger of AutoGen + Semantic Kernel) hit 1.0 GA on 2026-04-02; BUILD 2026 added "Agent Harness" (shell/filesystem access + human-in-the-loop approval + long-session context mgmt), Hosted Agents, and CodeAct as named platform primitives.
   **Why it matters**: A major vendor now treats "harness" as a distinct architectural layer (model reasoning vs. execution/approval/context), which is conceptually identical to this repo's PO+swarm+DELEGATION-CONTRACT model — useful as external validation and as a vocabulary/feature reference.
   **Confidence**: med (from devblogs.microsoft.com, official but not independently cross-checked for exact GA date elsewhere).

4. **What**: VS Code 1.109 (2026) is positioned as "the home for multi-agent development," adding Agent Merge and multi-root/multi-session agent organization for orchestrating parallel agent sessions plus PR review in-editor.
   **Why it matters**: Signals IDE-level convergence toward the same swarm/parallel-agent pattern this workspace already uses via delegation — relevant if this repo ever needs an IDE-integrated view of concurrent subagent runs.
   **Confidence**: med (single secondary source, not independently fetched from primary VS Code release notes).

5. **What**: Developer trust data is mixed across 2026 surveys: one report finds 85.5% of respondents trust agent output "at least somewhat" (24.7% completely, 60.8% somewhat) and 49.1% call agents "in production/core to how they ship"; another cites 96% of developers not fully trusting AI-generated code correctness, and 82%/71% split on speed vs. complex-problem-solving confidence.
   **Why it matters**: The spread between surveys (different populations/methodologies) suggests trust-in-agents claims should be sourced per-survey, not quoted as a single industry number — a caution for future digests in this topic.
   **Confidence**: low (secondary aggregator search results only; no primary survey report fetched, numbers not cross-verified).

6. **What**: New context-engineering papers not yet in this topic: "Mise en Place for Agentic Coding" (arXiv 2605.05400) frames deliberate pre-task preparation as a distinct methodology countering "vibe coding" speed-over-prep habits; "SWE-Pruner" (arXiv 2601.16746) and "Context Pruning for Coding Agents via Multi-Rubric Latent Reasoning" (arXiv 2605.15315) both target self-adaptive context trimming for long-horizon agent sessions.
   **Why it matters**: Distinct from the already-tracked AGENTS.md/CLAUDE.md context-file thread — these are runtime/session-level context management techniques (what to keep in the window over a long task), a gap in current topic coverage.
   **Confidence**: low (titles/abstracts only from search snippets, not fetched in full; no numeric claims taken from these).

7. **What**: "Context Engineering for AI Agents in Open-Source Software" (arXiv 2510.21413) studied AI context-file adoption across 466 open-source projects and identifies AGENTS.md as an emerging de facto standard format.
   **Why it matters**: Adds an adoption-rate data point to the existing human-curated-vs-AI-generated context-file thread, but the exact adoption percentage was not visible in search snippets and was not fetched — flagged as a follow-up, not a confirmed number.
   **Confidence**: low (not fetched; existence/framing only, no numbers cited).

## For This Workspace
- Add a lightweight secrets/credential-leak check to the PO QA gate (Step 2 primitives table) — the AIDev study shows humans, not agents, are the dominant source of leaked credentials in agent-touched PRs, so `git diff` scanning for hard-coded secrets before merge is worth codifying as a primitive alongside the existing shell/harness/memory checks.
- The 46%→95% product-context-compliance finding is a concrete argument for keeping this repo's CLAUDE.md/topic-memory discipline strict: decisions not visible in code (like the "answer first, no restating" output contract, or the DELEGATION-CONTRACT write-scope rules) are exactly the class of thing baseline agents miss 67-100% of the time without an explicit context layer.
- Track "Agent Harness" as a term Microsoft is now using publicly for the same concept this repo calls DELEGATION-CONTRACT/PO+swarm — worth a short cross-reference note next time `.agent-harness/DELEGATION-CONTRACT.md` is revised, so vocabulary stays legible to anyone comparing against MAF docs.
- Do not merge the developer-trust survey stats (finding 5) into topics/ as a single number — if a future digest wants trust data, it should fetch the primary Sonar/State-of-Code or similar report directly, since current secondary snippets disagree by double digits.

## Sources
- https://arxiv.org/html/2607.12428v1
- https://arxiv.org/abs/2605.08112
- https://devblogs.microsoft.com/agent-framework/microsoft-agent-framework-at-build-2026-announce/
- https://devblogs.microsoft.com/agent-framework/microsoft-agent-framework-at-build-2026/
- https://visualstudiomagazine.com/articles/2026/02/09/hands-on-with-new-multi-agent-orchestration-in-vs-code.aspx
- https://arxiv.org/abs/2605.05400
- https://arxiv.org/pdf/2601.16746
- https://arxiv.org/pdf/2605.15315
- https://arxiv.org/abs/2510.21413
