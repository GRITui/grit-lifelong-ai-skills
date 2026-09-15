# Studies Research: Boundary Metadata Collapse in Multi-Agent Handoffs

> ✅ QA-gated by PO 2026-09-12 · spot-check: "boundary marker survival σ_b ≈ 0.80 uncompressed → ≈0.57 at 25-word budget; 73%/50% leakage GPT-5-mini/DeepSeek-R1-32B, <15% with explicit constraints" ✓ (arxiv.org/abs/2608.29028 abstract, WebFetch exit 0)

## TL;DR

- New primary source (arXiv 2608.29028, Sept 2026): multi-agent LLM handoffs suffer "boundary metadata collapse" — summaries preserve the facts a downstream agent needs but drop the usage-scope constraints attached to those facts (e.g. "for the scheduler only," "don't put this in the report").
- Compressing a handoff to a 25-word summary cut boundary-marker survival from σ_b ≈ 0.80 (uncompressed) to σ_b ≈ 0.57, while the operational facts themselves survived compression essentially intact.
- Vague boundary language leaked protected info in 73% of GPT-5-mini cases and 50% of DeepSeek-R1-32B cases; explicit constraints cut leakage to under 15%.
- The single mitigation that nearly eliminated leakage was an "audience allowlist" derived from ground truth — i.e., naming who may see a fact, not just what the fact is; prompt-only phrasing fixes and redaction were only partial.
- Secondary corroborating source (arXiv 2512.03262, SUSVIBES benchmark): the best coding-agent config (SWE-Agent + Claude 4 Sonnet) hit 57% functional correctness on real-world feature-request tasks, but only 11.8% of those passing solutions were actually secure — correctness and safety diverge sharply, and hinting at the vulnerability in the prompt did not fix it.

## Findings

1. **What:** Multi-agent handoff summaries systematically strip "boundary metadata" (scope/usage constraints on a fact) while keeping the fact itself, a failure the authors name "boundary metadata collapse."
   **Why it matters:** In any PO→swarm→PO handback pattern (this repo's operating model), a subagent's report can silently lose the caveats attached to a finding ("verify before merging," "unconfirmed," "test env only") even when the finding text itself survives faithfully — the PO reads a clean fact with no attached risk flag.
   **Confidence: high** (directly quoted from fetched abstract, numeric results reported).

2. **What:** Marker survival dropped from σ_b ≈ 0.80 uncompressed to σ_b ≈ 0.57 at a 25-word compression budget, tested on GPT-5-mini and DeepSeek-R1-32B on a controlled coordination testbed with human-validated labeling (κ = 0.74 inter-rater agreement).
   **Why it matters:** The failure is a direct, measured function of summary length/compression pressure, not a rare edge case — any workflow that asks a subagent to "keep the handoff short" is trading away exactly the constraint metadata that governs safe reuse of the information.
   **Confidence: high** (specific effect size + methodology confirmed in fetched abstract).

3. **What:** Vague boundary phrasing ("internal only," "be careful with this") leaked protected content in 73% of GPT-5-mini runs and 50% of DeepSeek-R1-32B runs; switching to explicit, structured constraints reduced leakage to <15%.
   **Why it matters:** Natural-language caveats in delegation briefs are much weaker than they feel — a subagent brief that says "sensitive, handle carefully" is closer to no constraint at all than to a hard rule.
   **Confidence: high** (numeric, from fetched abstract).

4. **What:** The one mitigation that "nearly eliminated" leakage was an explicit audience allowlist (naming exactly who/what may consume a given fact) derived from ground truth — not prompt engineering or output redaction, which gave only partial protection.
   **Why it matters:** Suggests the fix for handoff/context-loss failures is structural (an explicit access/scope field attached to each fact) rather than stylistic (better wording of the instruction).
   **Confidence: med** (abstract-level claim; full paper's allowlist mechanism and its false-negative/utility tradeoffs weren't verified beyond the abstract).

5. **What:** SUSVIBES benchmark (186 real-world feature-request SE tasks with known historical vulnerabilities) found the top-performing agent config (SWE-Agent + Claude 4 Sonnet) reached 57% functional correctness, but only 11.8% of those correct solutions were secure.
   **Why it matters:** Functional-correctness gates (the kind this repo's QA gate emphasizes: exit code 0, tests pass) do not catch security regressions — "it works" and "it's safe" are nearly independent outcomes at current agent skill levels.
   **Confidence: high** (numeric, directly from fetched abstract).

6. **What:** In the same benchmark, augmenting the feature request with an explicit vulnerability hint did not meaningfully improve the secure-solution rate.
   **Why it matters:** Telling an agent "watch out for X vulnerability class" in the brief is a weak control, analogous to finding 3 above (vague caveats don't hold) — reinforces that soft in-prompt warnings are not a reliable safety mechanism for either privacy-boundary or security-vulnerability failures.
   **Confidence: med** (stated in abstract as a summary conclusion, not broken out with its own separate number).

## For This Workspace

- **Treat delegation-brief caveats as structured fields, not prose.** The DELEGATION-CONTRACT (`.agent-harness/DELEGATION-CONTRACT.md`) and per-task briefs should carry scope/caveat constraints (write-scope, "unverified — confirm before merge," data sensitivity) as an explicit, separately-checked field the PO greps for on handback — not just a sentence buried in the subagent's free-text report, which the handoff-collapse finding suggests degrades under compression.
- **When merging swarm output into `.agent-memory/topics/`, distrust omission as much as content.** Boundary-collapse research implies a clean, confident-sounding digest from a subagent may have silently dropped its own hedges. The PO QA gate should specifically ask "did the subagent's original working notes carry a caveat that isn't in the final digest?" not just fact-check the claims that remain.
- **Do not let "tests/build pass" QA-gate exit codes stand in for a security check.** SUSVIBES shows correctness and security are nearly decoupled (57% vs 11.8%); if any swarm work involves security-relevant code, the QA gate needs a distinct security-review step, not an assumption that green CI implies safe code.
- **Avoid relying on soft prompt-level warnings for anything safety-critical in a brief.** Both sources converge on the same lesson: vague natural-language cautions ("be careful," "watch for vulnerabilities") are weak; prefer explicit, checkable constraints (allowlists, named forbidden actions, specific write-scope paths) — consistent with this repo's existing DELEGATION-CONTRACT approach, and a reason to keep tightening it toward hard/structured constraints rather than prose reminders.

## Sources

- https://arxiv.org/abs/2608.29028
- https://arxiv.org/html/2608.29028
- https://arxiv.org/abs/2512.03262
- https://arxiv.org/pdf/2512.03262
