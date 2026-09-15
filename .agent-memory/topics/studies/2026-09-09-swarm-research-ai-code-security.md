> ✅ QA-gated by PO batch 2026-09-09 · spot-check: Veracode 2026 GenAI Code Security Report 56% pass rate, 44% vuln-introduction rate, GPT-5.5 68% pass rate ✓ (independently re-searched, corroborated by BusinessWire/TheNextWeb/SD Times/vmblog)

# AI-Generated Code Quality & Security: 2026 Empirical Findings

Sub-topic within "studies": empirical research on AI-generated code quality and
security trends (distinct from the existing Aider benchmarks, context
engineering, skill atrophy, and METR/Kiro topics). Focus: what large-scale
2026 studies actually measured in production/benchmark code, not vendor
marketing claims.

## TL;DR

- AI-generated code security has **stalled, not improved**: Veracode's 2026
  GenAI Code Security Report puts the average pass rate at 56%, "virtually
  unchanged" from the prior year despite much stronger models.
- Independent production-code evidence agrees: SIG's State of Software 2026
  report (400B+ lines, 30,000+ systems) found AI-generated code carries
  roughly **2x the security-risk violations** of human-written code, with
  more than half containing vulnerabilities.
- Language matters a lot: Java is the worst-performing language in Veracode's
  tests (mean 30% pass rate) despite showing the clearest improvement trend;
  the best model (GPT-5.5) still fails ~32% of security tasks.
- Developer trust is low and largely rational: most developers say the
  top AI-era skill is "reviewing/validating AI-generated code," and a
  majority report spending more time debugging AI output, not less.
- Caveat: AI-written code is still a small fraction of enterprise production
  code (SIG puts it at 1.9%), so today's aggregate risk exposure is smaller
  than the per-line risk multiplier suggests — but that share is growing.

## Findings

1. **What:** Veracode's 2026 GenAI Code Security Report (100+ models tested,
   Summer 2026 dataset) found the average security pass rate for AI-generated
   code is 56%, essentially flat year-over-year despite large jumps in
   model coding capability.
   **Why it matters:** Confirms capability gains (benchmark scores, coding
   agent adoption) are decoupled from secure-coding outcomes — "smarter" is
   not making models "safer" by default.
   **Confidence:** high (vendor report, but corroborated by SD Times,
   TheNextWeb, and vmblog coverage; methodology described as 100+ models
   across languages and vulnerability categories with no security-specific
   prompting).

2. **What:** In the same Veracode dataset, ~44% of AI code-generation tasks
   introduced at least one risky security vulnerability; GPT-5.5 led at 68%
   pass rate while six of eleven tested models scored 50-53%.
   **Why it matters:** Even the best current model fails roughly 1 in 3
   security-relevant tasks — "pick a better model" is not a fix by itself.
   **Confidence:** high (same primary source as #1).

3. **What:** Java had the worst mean security pass rate of any language
   tested (30%) despite showing the clearest improvement trend of any
   language in the report.
   **Why it matters:** Security risk from AI-generated code is not uniform —
   language/ecosystem choice materially changes exposure, useful for setting
   per-language review rigor.
   **Confidence:** medium (single-source stat, not cross-verified elsewhere).

4. **What:** SIG's State of Software 2026 report, based on 400+ billion
   lines of code across 30,000+ production systems (not synthetic benchmark
   prompts), found AI-generated code carries roughly double the
   security-risk violations of human-written code, with over half containing
   vulnerabilities; AI-generated code is currently only ~1.9% of enterprise
   production code.
   **Why it matters:** This is real production telemetry, not a lab
   benchmark, and it independently corroborates Veracode's lab-style
   findings — two very different methodologies converge on the same
   direction (AI code = meaningfully higher security risk per line).
   **Confidence:** high for the directional finding (large sample, real
   deployments); the exact 2x multiplier is a secondary-source paraphrase of
   the SIG report, so treat the precise number as medium confidence.

5. **What:** SIG's framing: AI acts as an "amplifier" of existing engineering
   discipline — it accelerates productivity in well-governed codebases and
   accelerates technical-debt accumulation in poorly-governed ones (quoting
   SIG CEO Luc Brandts: "you cannot manage what you cannot measure").
   **Why it matters:** Reframes "is AI code good or bad" as "AI code quality
   is a multiplier on your existing review/governance process" — directly
   relevant to how much QA-gating matters.
   **Confidence:** medium (interpretive framing from the vendor, not a raw
   statistic).

6. **What:** SonarSource's 2026 State of Code Developer Survey reports that
   when developers were asked what skill matters most in the AI era, the
   top answer (47%) was "reviewing and validating AI-generated code for
   quality and security."
   **Why it matters:** Practitioner sentiment lines up with the hard data —
   the emerging core skill is verification, not generation.
   **Confidence:** medium (could not fetch full PDF content directly; figure
   taken from search-result summary of the report, not independently
   re-verified against the primary document).

7. **What:** Secondary aggregation (SecondTalent, citing Stack Overflow 2025
   survey + SWE-bench + peer-reviewed sources) reports 67% of developers
   spend more time debugging AI-generated code, 71% refuse to merge AI
   output without manual review, and only 3% "highly trust" AI-generated
   code; also notes HumanEval scores (90%+) diverge sharply from real-world
   SWE-bench performance (~39.6%).
   **Why it matters:** Explains the gap between headline benchmark scores
   and lived developer experience — the benchmarks agents are marketed on
   are not the benchmarks that predict real-task reliability.
   **Confidence:** low-medium (aggregator site rolling up multiple
   third-party sources; treat as directionally useful, not a primary
   citation — verify against Stack Overflow's own 2025/2026 survey or
   SWE-bench leaderboard before citing hard numbers elsewhere).

## For This Workspace

- The QA gate in this harness (`bash -n`, symlink checks, markdown link
  checks) is exactly the right shape given finding #1/#2: model output
  quality plateaus around a ~50-60% real-world pass rate on
  security-sensitive tasks, so gating on exit code rather than intent is
  well justified, not overcautious.
- Finding #5 (AI as an "amplifier" of existing discipline) is a direct
  argument for keeping the PO+swarms split: swarms draft to `inbox/`,
  PO verifies before promotion to `topics/` — undisciplined merge-on-write
  would be exactly the failure mode SIG describes.
- If this workspace ever generates code (not just markdown/config), treat
  language choice as a risk lever per finding #3 — e.g. prefer languages/
  frameworks with better observed AI-code security track records, or add
  extra review weight for Java-equivalent stacks.
- Flag the SonarSource and SecondTalent figures (findings #6, #7) as
  "medium/low confidence, needs primary-source re-verification" if reused
  elsewhere — they were read via search snippets / aggregator summaries,
  not the original PDF/survey report, unlike the Veracode and SIG findings
  which have multiple independent corroborating write-ups.

## Sources

https://www.veracode.com/blog/2026-genai-code-security-report-ai-risk/
https://www.veracode.com/resources/analyst-reports/2026-genai-code-security-report/
https://www.businesswire.com/news/home/20260728207685/en/LLMs-Are-Getting-Smarter-But-Not-Safer-Veracode-2026-GenAI-Code-Security-Report-Finds-AI-Generated-Code-Security-Has-Stalled-at-56-Pass-Rate
https://sdtimes.com/agentic-security/veracode-finds-ai-generated-code-security-has-barely-improved-since-last-year/
https://thenextweb.com/news/veracode-2026-genai-code-security-56-percent-pass-rate
https://www.veracode.com/blog/spring-2026-genai-code-security/
https://vibegraveyard.ai/story/sig-state-of-software-2026-ai-code-security-study/
https://www.sonarsource.com/state-of-code-developer-survey-report.pdf
https://www.secondtalent.com/resources/ai-generated-code-quality-metrics-and-statistics-for-2026/
https://sqmagazine.co.uk/ai-coding-security-vulnerability-statistics/
