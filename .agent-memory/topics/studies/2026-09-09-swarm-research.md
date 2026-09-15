> ✅ QA-gated by PO batch 2026-09-09 · spot-check: arXiv 2606.19121 ("Index Sickness"/"Phantom Legislation", Zhang & Song, 391-session Bang-v3 study) independently fetched and confirmed to match draft's TL;DR ✓

# Study: Failure Modes of Self-Documenting, Persistent-Memory AI Agents (2026)

## TL;DR
- A month-long, 391-session field study of an AI agent maintaining its own project knowledge base found that piling on more formal rules/symbolic IDs to fix drift *backfires* past a complexity threshold — the agent stops reasoning about real semantics and starts hallucinating internally-consistent nonsense ("Index Sickness" / "Phantom Legislation").
- The fix that worked in that study was not more rules but *less* and *simpler*: separating a stable "Baseline" doc from an append-only "Log," cutting instruction volume ~75%, eliminating recurrence over the next ~150 sessions.
- Separately, background/autonomous execution ("heartbeat" cycles) is a real memory-integrity risk: ordinary untrusted content encountered during unattended background tasks got written into persistent agent memory and influenced later behavior in up to 91% of tested cases, with no prompt-injection trickery needed.
- Industry benchmarking in 2026 (Mem0's State of AI Agent Memory report) shows the harder unsolved problem is now *forgetting/updating* stale-but-still-relevant memory, not retrieval — accuracy drops ~25 points as memory scale grows from 1M to 10M tokens.
- A separate architectural study (ForgetEval, 13 configurations) found deterministic "delete/supersede" rules recover most forgetting cases fast (64-191ms) but fail at intent-aware or paraphrased deletion requests, which need an LLM in the loop at some stage of the write/mutation path — at a real latency cost (~2.3s/case).

## Findings

### Index Sickness: symbolic-system complexity has a collapse threshold
- What: In a real software project (codenamed Bang-v3), the team kept adding formal constraints — symbolic identifier systems, more defensive rules in system prompts, larger context — every time the AI agent's long-horizon collaboration drifted. Past a complexity threshold, the LLM did not get more accurate; it abandoned genuine understanding of business semantics and retreated into self-referential reasoning about its own symbolic layer, producing outputs that look internally consistent but are disconnected from ground truth.
- Why it matters: This is the exact trap a QA-gated memory harness with dated markdown files, topic taxonomies, and accreting instructions can fall into — the intuitive fix for confusion (add more rules/IDs/structure) can make an agent worse, not better.
- Confidence: med (single action-research case study, not a controlled experiment, small author team)

### "Phantom Legislation" as the diagnostic symptom
- What: The paper's named failure signature is the agent inventing rules/decisions that sound authoritative and consistent with the existing symbolic system but were never actually made or true — legislation the agent "phantom-authored" for itself.
- Why it matters: Gives a concrete thing to grep for when auditing a memory harness: markdown notes stating "rule" or "decision" as fact should be checked against whether an actual verified event produced them, not just whether they read fluently.
- Confidence: med

### The "Pang Principle" (Semantic Vitality Law) — natural language beats symbolic compression
- What: The authors' proposed underlying principle: natural language carrying explicit purpose conveys substantially higher information quality to an LLM than symbolic/compressed expression (IDs, codes, terse tags), even though symbols look more "efficient."
- Why it matters: Argues against over-compressing memory notes into terse tags/IDs to save tokens — plain-language notes with explicit purpose are more robust for a coding agent re-reading its own memory later.
- Confidence: med

### Baseline-Log Physical Separation fixed it
- What: The mitigation that worked was structurally separating a slow-changing "Baseline" (current state of truth) from an append-only "Log" (history of changes/decisions), rather than letting one growing document serve both roles. This cut AI-facing instruction volume ~75% and eliminated recurrence of Index Sickness over the next ~150 sessions in the same project.
- Why it matters: Directly analogous to separating "current verified knowledge" (topics/) from "raw session history" (inbox/, dated files) — which this workspace's harness already does structurally, but the finding suggests actively pruning/consolidating the Baseline layer matters, not just appending dated files forever.
- Confidence: med (validated in the same single project, not replicated elsewhere)

### Background/"heartbeat" execution silently pollutes agent memory
- What: A security study on personal AI agents that run background (heartbeat-driven) tasks in the same session/memory context as foreground conversation found that untrusted content encountered during unattended background work (e.g., email, social content) can silently pollute persistent memory and later shape visible agent behavior. Measured effects: social-credibility-driven behavioral influence up to 61%; memory-saving routines entrenching short-term pollution into lasting memory at rates up to 91%; polluted content persisting and influencing behavior across sessions at up to 76%. Notably, ordinary misinformation was sufficient — no adversarial prompt injection was required.
- Why it matters: Any workflow where a subagent/swarm writes drafts that later get promoted into durable memory (this repo's inbox -> topics pipeline) is structurally the same pattern the paper flags as risky — the QA gate before promotion is the exact mitigation boundary that determines whether pollution reaches durable memory.
- Confidence: high (adversarial/security research with quantified rates, though on a different agent platform "Claw," not Claude Code specifically)

### Forgetting, not retrieval, is now the dominant production failure mode
- What: Mem0's 2026 industry report states that as memory scale grows (tested at 1M vs 10M token scale on the BEAM benchmark), scores drop from 64.1 to 48.6 (~25-point decline), and that "memory staleness" — high-relevance memories becoming confidently incorrect after circumstances change — is characterized as a harder, open problem beyond simple decay/expiry mechanisms.
- Why it matters: A durable knowledge base that only ever appends dated files (as this harness does) will accumulate stale-but-confident notes (e.g., an old deploy token rotation, an old project status) unless something actively revisits/supersedes old topic files, not just adds new ones.
- Confidence: high (vendor benchmark report, standardized benchmarks LoCoMo/LongMemEval/BEAM, though self-reported by a memory-product vendor)

### Deterministic deletion rules handle the easy cases; paraphrased/intent-based forgetting needs an LLM in the write path
- What: An architectural comparison across 13 agent-memory system configurations (ForgetEval benchmark, 1000 templated + 385 adversarial cases) found deterministic supersede/purge primitives handle lexical/temporal forgetting well but fail badly on canonicalization (5% on identifier obfuscation, 0% cross-lingual) and intent-aware deletion. Putting an LLM at the mutation/write step (not just at read/retrieval time) recovered intent-aware deletion (78-85%) and pushed overall accuracy to 91.7-93.2%, at a latency cost of ~2.3s/case vs 64-191ms for deterministic rules.
- Why it matters: Confirms that "when do we overwrite/retire an old memory file" is an LLM-judgment problem, not something a simple grep/dedup script can safely do — relevant to how this repo's PO role decides when to supersede an old topic file vs append a new dated one.
- Confidence: med (single benchmark paper, one research group, MIT-licensed code released but not independently reproduced yet)

### Retrieval-augmented memory has matured into a three-signal-fusion default
- What: Per the same 2026 report, leading agent-memory retrieval now fuses semantic similarity, BM25 keyword matching, and entity matching rather than relying on embeddings alone, and this fused approach outperforms any single signal; token cost per query dropped to ~6,900 tokens vs ~26,000 for stuffing full context.
- Why it matters: For a markdown-file memory harness that's currently searched via `grep -ri` per the CLAUDE.md Step 1 (Recall), this suggests plain grep alone is the "single-signal" weak point — pairing it with a keyword/BM25-style search or explicit topic-index files would likely improve recall precision as the corpus grows.
- Confidence: med (vendor-reported improvement numbers, directionally consistent with broader retrieval literature)

## For This Workspace
- Treat "Index Sickness" as a concrete audit question for the PO role: periodically check whether `.agent-memory/topics/` notes are drifting into self-referential jargon/IDs that no longer map to verifiable facts, and prefer plain-language notes with explicit purpose over compressed tags.
- Adopt an explicit Baseline vs Log split within busy topics (e.g., `webblog-hostinger-deploy.md` as a living Baseline that gets edited/consolidated, vs dated files as an append-only Log) instead of only ever adding new dated files — the paper's fix was specifically pruning/restructuring, not just appending.
- Since research-swarm drafts land in `.agent-memory/inbox/` before promotion, treat that inbox->topics QA gate as the security boundary the "silent memory pollution" paper implies is necessary — verify sourced claims and re-check for injected/unverifiable content before anything gets promoted to `topics/`, especially for anything written by an unattended/background-triggered agent.
- When a topic file's fact goes stale (token rotated, project status changed), actively supersede/edit the old file rather than only adding a newer dated file alongside it — per the "memory staleness is now the dominant failure mode" finding, an accumulating pile of dated files without retirement of outdated ones is the known failure pattern to avoid.

## Sources
https://arxiv.org/abs/2606.19121
https://arxiv.org/abs/2603.23064
https://arxiv.org/abs/2606.15903
https://mem0.ai/blog/state-of-ai-agent-memory-2026
