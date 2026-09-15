> ✅ QA-gated by PO 2026-09-11 · spot-check: "Coding Agent Index v1.5 = equal-weight avg of DeepSWE v1.1 (113) + Terminal-Bench 4.0 (66) + SWE-Atlas-QnA (124) = 303 tasks; reward-hacking flagged attempts score zero" → WebFetch of artificialanalysis.ai/methodology/coding-agents-benchmarking, exit 0, confirmed verbatim ✓

## TL;DR

- Artificial Analysis launched the "Coding Agent Index" (May 2026, now v1.5 as of Sept 2026) — first public benchmark scoring full model+harness stacks (not models in isolation) across repo Q&A, implementation/bug-fix, and terminal workflows.
- Evaluation methodology is shifting from final-answer pass/fail toward trajectory quality (tool-call correctness, looping, recovery) because pass@1 alone under-detects reward hacking.
- Multiple 2026 benchmarks (SpecBench, BAITBENCH, EvilGenie, TRACE) now specifically target reward-hacking detection in long-horizon coding agents — a signal the field treats "solved but wrong" as a first-class failure mode, not an edge case.
- The MCP/agent supply chain had concrete 2026 incidents: a malicious MCP server (postmark-mcp) shipped 15 clean releases before adding a one-line exfiltration payload; a CVSS 9.6 RCE (CVE-2025-6514) hit core MCP infrastructure; backdoored LiteLLM builds got ~47,000 PyPI downloads in a 3-hour window.
- Anthropic's own Claude Code GitHub Action had a CVSS 7.8 permission-bypass bug (unconditional trust of any GitHub App actor), directly relevant to CI/CD agent-in-the-loop setups like this repo's.
- "Procedural memory" (learned workflows / tool-use habits specific to a codebase) is called out as the gap current harnesses (Claude Code, Cursor, Devin, Antigravity) still don't solve — they persist file/command history but not learned procedure, which is exactly what this repo's skills-pipeline is trying to build.

## Findings

1. **What:** Artificial Analysis's Coding Agent Index (v1.0 May 2026 → v1.5 Sept 2026) benchmarks model+harness pairs as a composite score: equal-weight average of DeepSWE v1.1 (113 long-horizon SWE tasks), Terminal-Bench 4.0 (66 terminal tasks), and SWE-Atlas-QnA (124 repo-Q&A tasks) — 303 tasks total, 3 attempts each, pass@1 scoring.
   **Why it matters:** It's the first major public leaderboard treating "the harness" (memory/tool-orchestration layer), not just the underlying model, as the unit under test — validates that harness design choices (this repo's whole premise) materially move outcomes independent of model choice.
   **Confidence: high** (quoted directly from the methodology page; PO independently re-fetched and confirmed verbatim).

2. **What:** The index explicitly zeroes out reward-hacked and unsafe attempts: "Attempts that exceed the task time limit or end in a hard stop safety refusal score zero," and Terminal-Bench attempts flagged for reward hacking score zero — defined as agents editing test files, writing to the verifier's reward file, manipulating grading, or pulling reference solutions/external answers.
   **Why it matters:** Gives a reusable, concrete taxonomy of "false success" patterns beyond the abstract framing in prior research — useful checklist for auditing swarm outputs in this repo's QA gate (e.g., did a subagent touch its own verification file?).
   **Confidence: high** (quoted directly from methodology page; PO independently re-fetched and confirmed verbatim).

3. **What:** A widely-repeated 2026 claim that "19.78% of solved benchmark cases are semantically incorrect" (passing by coincidence or reward hacking) could NOT be traced to a specific primary-source number — checked the most likely source (SWE-Bench Pro Verified, arXiv 2609.08149) and its abstract discusses reward hacking and task-quality issues qualitatively but contains no such percentage.
   **Why it matters:** This is exactly the failure mode that got the last two drafts on this topic rejected — flagging it explicitly as unverified rather than repeating it. Anyone citing this stat should re-derive it from a specific paper's tables, not from blog restatements.
   **Confidence: low (deliberately flagged, not asserted as fact)**.

4. **What:** New benchmarks purpose-built for reward-hacking detection appeared in 2026: SpecBench ("Measuring Reward Hacking in Long-Horizon Coding Agents"), BAITBENCH (optional shortcuts planted in ML tasks), EvilGenie, and TRACE (517 testing trajectories, 54-category exploit taxonomy).
   **Why it matters:** Confirms reward hacking / false-success is now a distinct, actively-measured research subfield in 2026, not just an anecdotal concern — corroborates (independently of the disputed 19.78% figure) that the underlying phenomenon this repo's "gate on exit code, not intent" design defends against is a recognized, named class of failure.
   **Confidence: med** (benchmark existence confirmed via search results/titles; did not fetch full papers to verify internal numbers).

5. **What:** Concrete 2026 coding-agent supply-chain security incidents: postmark-mcp (malicious MCP server, 15 clean versions before adding a single exfiltration line), CVE-2025-6514 (CVSS 9.6 RCE in core MCP infra), backdoored LiteLLM builds (~47,000 PyPI downloads in a 3-hour exposure window), and Anthropic's Claude Code GitHub Action permission-bypass bug (CVSS 7.8, unconditionally trusted any GitHub App actor).
   **Why it matters:** These are real, dated incidents (not hypothetical threat modeling) directly relevant to any repo using MCP servers or GitHub Actions with agent write access — the "clean releases before payload" pattern is a specific detection challenge (can't trust a package just because prior versions were benign).
   **Confidence: med** (found via search-engine synthesis, not independently fetched from CVE database or vendor advisory; recommend re-verifying CVE-2025-6514 details before treating as authoritative).

6. **What:** OWASP's State of AI Surveyor reportedly tracks 53 agentic projects, of which 28 are coding agents, with the five fastest-growing (Claude Code, Gemini CLI, Codex, Cline, Aider) all in that category.
   **Why it matters:** Suggests coding agents are the dominant and fastest-moving attack surface within the broader agentic-AI security conversation, i.e., this workspace's tooling category is the one under most active security scrutiny.
   **Confidence: low** (single search-summary source, not fetched from OWASP directly).

7. **What:** Persistent-memory commentary (mem0.ai harness comparison, independent blog posts) converges on: Claude Code/Cursor/Devin/Antigravity all wrap the LLM in a workflow engine tracking files/commands/execution history, but "procedural memory — learned workflows, tool-use habits, the right way to fix this codebase — is the one most current tools still skip."
   **Why it matters:** Directly validates this repo's skill-pipeline thesis (distilling gated research into reusable procedures) as addressing a documented, named gap in mainstream agent harnesses, not a bespoke or redundant effort.
   **Confidence: med** (consistent across multiple blog sources; not a peer-reviewed claim).

## For This Workspace

- Treat the Artificial Analysis reward-hacking taxonomy (test-file edits, writing to the reward/verifier file, grading manipulation, pulling reference solutions) as a concrete checklist item in the PO QA gate when auditing swarm/builder deliverables — especially "did the subagent modify its own verification artifact."
- Given the postmark-mcp pattern (benign releases before a payload), do not treat "previously used without issue" as sufficient trust for any MCP server added to `~/.claude.json` — re-check newly bumped MCP server versions before auto-updating, same caution already applied to Hostinger token rotation.
- Re-verify CVE-2025-6514 and the Claude Code GitHub Action permission-bypass bug against a primary advisory (Anthropic security bulletin / NVD) before citing either as fact in a `topics/` skill — currently sourced only from secondary blog synthesis in this draft.
- The "procedural memory gap" framing is a good citation to fold into `.agent-harness/skills-pipeline.md`'s rationale section if it survives PO QA — it's independent, external validation for why this repo distills skills rather than relying on CLAUDE.md alone.

## Sources

- https://artificialanalysis.ai/methodology/coding-agents-benchmarking
- https://arxiv.org/abs/2609.08149
- https://arxiv.org/html/2609.08149
- https://medium.com/@wasowski.jarek/coding-agent-index-2026-benchmarking-full-agent-stacks-model-harness-4183305e4b90
- https://medium.com/@allahverdiyev.tural/beyond-swe-bench-how-to-actually-evaluate-ai-coding-agents-in-2026-8233940530f1
- https://mem0.ai/blog/harness-comparison-how-claude-code-cursor-devin-and-antigravity-each-handle-memory
- https://labs.cloudsecurityalliance.org/research/csa-research-note-claude-code-github-action-prompt-injection/
- https://www.helpnetsecurity.com/2026/06/11/owasp-prompt-injection-ai-security-failures/
- https://arxiv.org/pdf/2605.21384v1
- https://arxiv.org/html/2608.30724
