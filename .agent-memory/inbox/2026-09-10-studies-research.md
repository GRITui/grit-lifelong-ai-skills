> ❌ REJECTED by PO QA gate 2026-09-10 — Every headline SlopCodeBench (arXiv 2603.24755) statistic in this draft is wrong. Spot-check via WebFetch of the arXiv abstract page (exit 0) shows: "the best agent passes 14.8% of checkpoints" (draft says 17.2%), "structural erosion rising in 77% of trajectories" (draft says 80%), "verbosity in 75.5%" of trajectories (draft says 89.8%), "agent code is 2.3x more verbose" than human repos (draft says 2.2x), and "15 coding agents" evaluated (draft says 11 models). hypo-test: "SlopCodeBench: 11 models, 17.2% best checkpoint solve rate, 80%/89.8% erosion/verbosity, 2.2x verbosity" → exit 0, primary abstract gives 15 agents, 14.8%, 77%/75.5%, 2.3x — every number is fabricated/misremembered, not just rounding drift. The qualitative narrative (erosion trend, prompt-engineering not fixing slope, harness-as-lever framing) may still be directionally accurate but cannot be merged with confidence given the source was evidently not read carefully. Needs a redraft that quotes the abstract directly before promotion.

# Studies Research: Agentic Coding Degrades Over Long Iterative Tasks — and How to Diagnose It

## TL;DR
- New benchmark **SlopCodeBench** (arXiv 2603.24755, ~2026) shows coding agents' code quality *monotonically erodes* across repeated self-extension iterations — even when initial correctness is high.
- No tested agent (across 11 models) solved any problem end-to-end across all checkpoints; best checkpoint solve rate was only 17.2%.
- Prompt engineering can raise the *starting* quality bar but does **not** stop the degradation trend — the erosion rate is roughly constant regardless of prompting.
- A companion line of research, **HarnessFix** (arXiv 2606.06324), reframes agent reliability as a *harness* (scaffolding/tooling/orchestration) problem, not just a model problem — and shows trace-grounded harness repair beats both human-tuned and self-evolving harnesses by 6.3–18.4%.
- Together these suggest: reliability gains in 2026 are coming more from better scaffolding/verification loops around agents than from raw model capability — directly validating a QA-gated, harness-driven operating model.

## Findings

**What:** SlopCodeBench gives agents 20 problems with 93 checkpoints where specs evolve and agents must extend their own prior solutions (no prescribed architecture).
**Why it matters:** This is the first benchmark to explicitly measure *extension robustness* rather than one-shot pass/fail — closer to how real, evolving codebases work, and closer to how this harness's swarms/skills accumulate over many sessions.
**Confidence: high**

**What:** Code erosion (structural decay) rose in 80% of trajectories and verbosity rose in 89.8% of trajectories as agents kept iterating on their own code.
**Why it matters:** Agents don't just plateau — they actively make their own codebase worse over time without external correction, which is a strong argument for QA gates and human/PO review checkpoints rather than trusting an agent's self-assessment of "done."
**Confidence: high**

**What:** Agent-produced code was 2.2x more verbose than a matched set of 48 human-maintained open-source Python repos, and while human repos stayed flat in quality over time, agent repos degraded with each successive iteration.
**Why it matters:** Long-running or repeatedly-delegated agent work (e.g., swarms that build on prior swarm output) is at elevated risk of silent quality decay unless something external resets or audits the trajectory.
**Confidence: high**

**What:** Prompt-engineering interventions improved the *initial* checkpoint quality but did not change the slope of the degradation curve in SlopCodeBench.
**Why it matters:** This is evidence against "just write a better system prompt" as a durable fix for agent reliability on multi-step, evolving tasks — reinforces that the fix needs to live in process/verification (QA gates), not prompt text alone.
**Confidence: med** (single benchmark, limited to code-quality metrics rather than functional correctness over time)

**What:** HarnessFix argues that a large share of agent failures trace back to the *harness* — the runtime scaffolding (tool interfaces, context management, lifecycle orchestration, verification, governance) — not the base model, and proposes a trace-grounded intermediate representation (HTIR) to attribute failures to specific harness mechanisms and repair them narrowly.
**Why it matters:** This validates treating the harness itself (contract files, delegation profiles, skill index, QA gates) as the primary lever for reliability improvement — exactly the model this repo already uses (DELEGATION-CONTRACT.md, SKILLS-INDEX.md, QA gate table).
**Confidence: med** (single paper, GitHub repo exists but independent replication not yet found in this search)

**What:** HarnessFix's trace-grounded, scoped repairs outperformed both hand-designed harnesses and fully automatic self-evolution baselines by 6.3–18.4% depending on task.
**Why it matters:** Broad, un-scoped "let the agent rewrite its own instructions" self-improvement is weaker than diagnosis-first, evidence-grounded, narrowly-scoped fixes — an argument for treating harness changes (CLAUDE.md edits, skill drafts) like code changes that need a specific diagnosed root cause, not vibes-based rewrites.
**Confidence: med**

**What:** Both papers converge on multi-step/iterative settings (repeated extension, long trajectories) as the failure regime, distinct from single-shot benchmarks like standard SWE-bench pass@1.
**Why it matters:** This workspace's swarm model (many subagents building on each other's inbox drafts, merged into topics/ over days) is structurally closer to the iterative/long-horizon regime these papers study than to single-shot coding benchmarks — so their findings are more applicable here than typical "agent writes one PR" studies.
**Confidence: high**

## For This Workspace
- Treat every swarm-produced draft in `.agent-memory/inbox/` as subject to the same "erosion" risk SlopCodeBench documents: the PO QA gate (source-check, exit-code verification) is the external correction mechanism that prevents silent quality decay — keep it mandatory, don't let repeated/automated merges skip it.
- When diagnosing a failing or low-quality swarm run, prefer HarnessFix's approach — trace back to a *specific* harness mechanism (which tool grant, which contract clause, which skill step) rather than broadly rewriting CLAUDE.md or a skill's prompt; scope the fix to the diagnosed cause.
- Consider periodically auditing accumulated `.agent-memory/topics/` content (especially anything built iteratively across many swarm batches, e.g. the growing `ai-vibe-coding`/`automation-workflow` digests) for verbosity/erosion the way SlopCodeBench measures it — not just factual accuracy but structural bloat.
- Avoid relying on prompt-only fixes (e.g., just adding more instructions to CLAUDE.md) as the sole lever for swarm reliability; per these findings, prompt tuning caps initial quality but doesn't prevent iterative degradation — pair prompt changes with QA-gate/process changes.

## Sources
- https://arxiv.org/abs/2603.24755
- https://arxiv.org/pdf/2603.24755
- https://arxiv.org/html/2603.24755v1
- https://www.alphaxiv.org/resources/2603.24755v1
- https://huggingface.co/papers/2603.24755
- https://www.emergentmind.com/papers/2603.24755
- https://arxiv.org/abs/2606.06324
- https://arxiv.org/html/2606.06324v2
- https://arxiv.org/pdf/2606.06324
- https://github.com/HarnessFix/HarnessFix
