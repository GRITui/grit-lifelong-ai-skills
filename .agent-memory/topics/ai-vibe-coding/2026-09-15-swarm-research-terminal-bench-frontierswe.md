# Research: Terminal-Bench and Frontier-SWE (2026 state)

> ✅ QA-gated by PO batch 2026-09-15 · spot-check: "Terminal-Bench v2.1 top score 91.4% (Claude Fable 5.1)" ✓ (independently re-fetched from artificialanalysis.ai/evaluations/terminalbench-v2-1, matched exactly)

## TL;DR
- Terminal-Bench has fragmented into multiple incompatible major versions in 2026 (2.1, 3.0, 4.0), each testing harder task sets — scores are NOT comparable across versions, and version 2.1 is already near-saturated (top models 84-91%) while 3.0/4.0 pull scores back down to 40-60%, mirroring the SWE-bench Verified -> Pro saturation pattern already noted in this workspace's prior research.
- FrontierSWE (Epoch AI / Proximal Labs), now on v2 (September 2026), is a distinct benchmark from Terminal-Bench: 34 real-world, ultra-long-horizon tasks (e.g. "reimplement git in Zig," "decode speech from MEG brain recordings," "train a medium-range weather forecasting model") with up to 20 hours of compute per task and 5 trials per model.
- OpenAI has publicly stated it no longer evaluates against SWE-bench Verified, framing it as no longer discriminating frontier capability — consistent with the saturation story across all three benchmark families (SWE-bench Verified, Terminal-Bench 2.1, and even early Terminal-Bench 3.0 tiers).
- Current top performers cluster around the same model family across benchmarks: "Claude Fable 5.1" leads Terminal-Bench v2.1 (91.4% max-effort) and reportedly leads the published FrontierSWE snapshot (88.2% mean@5 dominance), while "Claude Opus 5"/"GPT-6 Astra" lead the harder Terminal-Bench 3.0/4.0 tiers (34-58% range) — suggesting the same top model tier is being re-tested at progressively harder task sets as older versions saturate.
- Confidence is medium overall: version numbers, task counts, and score bands are corroborated across at least two sources per benchmark, but exact leaderboard snapshots move fast and were captured via search-engine-aggregated secondary summaries in several cases (see per-finding confidence).

## Findings

**What:** Terminal-Bench v2.1 (89 curated tasks: software engineering, sysadmin, data processing, model training, security) is run by third-party evaluator Artificial Analysis using the "Terminus 2" agent harness in an e2b sandbox, scored pass@1 averaged over 3 repeats. Top scores: Claude Fable 5.1 at 91.4% (max effort), 91.0% (xhigh effort), 89.9% (high effort).
**Why it matters:** This is a near-saturated tier (many models above 84%) — a benchmark stops discriminating agent capability once top scores cluster near ceiling, which is exactly the pattern this workspace already flagged for SWE-bench Verified.
**Confidence: high** (fetched directly from artificialanalysis.ai, which discloses its own harness/scoring methodology; independently re-verified by PO during QA gate).

**What:** Terminal-Bench versions 3.0 and 4.0 exist as harder successor task sets released later in 2026, explicitly stated as not comparable to 2.1 scores. Terminal-Bench 3.0 top score: Claude Opus 5 at 42.7%. Terminal-Bench 4.0 top score: "GPT-6 Astra" at 58.2%, followed by "Claude Fable 5.1" at 57.9%.
**Why it matters:** Terminal-Bench is following the same versioning strategy as SWE-bench (Verified -> Pro): once a version saturates, a harder version replaces it rather than the same version being trusted long-term. Anyone citing a "Terminal-Bench score" must cite the version, or the number is close to meaningless.
**Confidence: med** (figures come from a secondary aggregator, CodingFleet's blog, surfaced via search snippet rather than directly fetched; not cross-verified against a primary leaderboard for 3.0/4.0).

**What:** FrontierSWE (Proximal Labs, hosted/tracked by Epoch AI) v2 (Sept 2026) contains 34 tasks spanning implementation, performance engineering, scientific computing, visual reasoning, and AI research — explicitly designed as "ultra long-horizon": each task gets up to 20 hours of agent compute time, run 5 trials, scored 0-100 with mean@5, best@5, average rank, and "dominance" as the reported metrics. All models are run inside Proximal's own minimal agent scaffold, "Proximus," at max reasoning effort.
**Why it matters:** This is a materially different benchmark shape from Terminal-Bench or SWE-bench: it targets multi-hour-to-day agentic work (echoing this workspace's existing RoadmapBench/SWE-EVO findings on the long-horizon capability cliff) rather than single-session terminal or PR-fix tasks. It complements, doesn't duplicate, that prior research.
**Confidence: high** on methodology (fetched directly from epoch.ai); **medium** on the specific "Claude Fable 5.1 leads at 88.2% mean@5 dominance" figure (only surfaced via search-engine synthesis of benchlm.ai, not independently fetched/verified against Epoch AI's own leaderboard table).

**What:** OpenAI published a statement ("Why SWE-bench Verified no longer measures frontier coding capabilities") announcing it has stopped using SWE-bench Verified as an internal frontier-capability evaluation.
**Why it matters:** A direct methodology critique from a frontier lab, not just third-party leaderboard commentary — corroborates the saturation/contamination concerns already logged in this workspace's SWE-bench Pro research, and signals the whole "single-PR-fix" benchmark family (Verified, and arguably early Terminal-Bench tiers) is being deprecated by labs in favor of harder, longer-horizon suites like FrontierSWE and SWE-bench Pro.
**Confidence: low-med** (the page returned HTTP 403 on fetch; this finding is based only on the article title and the fact that it appeared as a top, on-domain result — content was not directly readable this session).

**What:** Scale AI hosts a public SWE-bench Pro leaderboard (labs.scale.com/leaderboard/swe_bench_pro_public) as a third-party, independently-run tracker distinct from the morphllm.com/codeant.ai sources already logged in this workspace's prior SWE-bench Pro research.
**Why it matters:** A second, independent leaderboard host for SWE-bench Pro increases confidence that the ~25-57% score band (vs 80%+ on Verified) already logged in this workspace is not an artifact of a single reporting source; worth a follow-up fetch to cross-check exact current numbers.
**Confidence: low** (only the existence and URL of this leaderboard were confirmed via search; page was not fetched this session, so no scores were verified from it directly).

**What:** Cognition has published "FrontierCode," a related/competing long-horizon benchmark or product announcement (found via search alongside FrontierSWE), suggesting multiple labs are independently converging on "long-horizon, real-world engineering task" as the next benchmark frontier beyond single-PR-fix suites.
**Why it matters:** Signals this isn't one lab's idiosyncratic framing — at least three organizations (Proximal Labs/Epoch AI with FrontierSWE, Cognition with FrontierCode, and the RoadmapBench/SWE-EVO academic authors already logged in this workspace) are building similar long-horizon evaluation infrastructure in the same period, which raises confidence that "long-horizon capability cliff" is the real, converging signal for 2026 rather than noise from any single benchmark's construction.
**Confidence: low** (title and existence only, from a search snippet; content of the Cognition blog post was not fetched this session).

## For This Workspace
- When citing a "Terminal-Bench score" in board notes, skill drafts, or model-selection decisions, always cite the version number (2.1 vs 3.0 vs 4.0) alongside the score — the numbers are explicitly non-comparable across versions, and a stale "88% on Terminal-Bench" claim from an older version will read as far stronger than a current 4.0-tier ~55-58% for the same model class.
- FrontierSWE's 20-hour-per-task, 5-trial, mean@5/best@5/dominance scoring methodology is a good template to borrow for this workspace's own long-horizon swarm tasks: rather than a single pass/fail exit-code check on a large multi-file build task, consider running/spot-checking a small sample of repeated trials on genuinely long-running delegated work to get a variance signal, not just one binary result.
- Add a follow-up research card to independently fetch labs.scale.com/leaderboard/swe_bench_pro_public and epoch.ai/benchmarks/frontierswe's live leaderboard tables directly (both returned only secondary/aggregated numbers this session) before treating any specific score in this digest as citation-grade for external-facing claims.
- The OpenAI "no longer evaluate SWE-bench Verified" framing (even unverified past the headline) is a useful prompt to periodically re-check whether this workspace's own default benchmark references (SWE-bench Pro, Terminal-Bench) are still the ones frontier labs are actually using to make claims about their own models — benchmark relevance in this space appears to have a lifespan of months, not years.

## Sources
https://artificialanalysis.ai/evaluations/terminalbench-v2-1
https://epoch.ai/benchmarks/frontierswe
https://pricepertoken.com/leaderboards/benchmark/terminalbench
https://benchlm.ai/benchmarks/terminal-bench-2
https://llm-stats.com/benchmarks/terminal-bench
https://codingfleet.com/blog/terminal-bench-3-leaderboard-2026/
https://codingfleet.com/blog/terminal-bench-4-leaderboard-2026/
https://codingfleet.com/blog/terminal-bench-leaderboard-2026/
https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/
https://github.com/Proximal-Labs/frontier-swe
https://labs.scale.com/leaderboard/swe_bench_pro_public
https://www.proximal.ai/blog/frontierswe/
https://benchlm.ai/benchmarks/frontierswe
https://cognition.com/blog/frontier-code
