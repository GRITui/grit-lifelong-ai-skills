# software-development — Swarm Research (2026-09-07)

> ✅ QA-gated by PO 2026-09-07 · sources verified present · load-bearing claims spot-checked (Spec Kit 1.0 confirmed; n8n 2.x claims validated by live debugging) · merged from swarm inbox

# software-development — Swarm Research Draft (2026-09-07)

## TL;DR
- Consensus across 2026 sources: treat AI-written output as untrusted by default; the single most cited failure mode is a model writing both implementation and its own tests from the same prompt ("tautological tests", "false greens"). Independent oracles are load-bearing.
- Line coverage is widely called a broken gate for AI-generated code (generated tests execute without asserting); mutation score and behavioral/contract tests are the recommended replacements — though one source still recommends 85–90% coverage, a noted conflict.
- Spec-driven development is now mainstream tooling: GitHub Spec Kit hit 1.0.0 (Aug 2026), Spec → Plan → Tasks → Implement, and academic work shows validating intermediate artifacts (not just final code) catches hallucinated paths/APIs early.
- AGENTS.md is the de facto agent-context standard (60k+ projects; read natively by Claude Code, Codex, Copilot, Cursor, Gemini CLI), but research says keep it short (<150–300 lines) and index-style — verbose/auto-generated files measurably hurt.
- Repo hygiene findings validate this workspace's choices: allowlist `.gitignore` (`/*` + `!` negations) is the documented pattern for fixed-scope repos; symlinks in git store only the target path and break on clone.

## Findings
1. **What:** Verification-first testing for AI code: define the contract/spec *before* generation; write test descriptions first; never let one model author both sides from the same prompt; treat the agent's bundled tests as "candidate tests," not evidence. The recurring question: "What mistakes can still pass all my tests?" (Shiplight 7-layer model; Total Shift Left; QASkills SDET playbook; OrbitTest).
   **Why it matters:** This workspace's QA gate (bash -n, test -f, git status scope) is exactly the "cheap deterministic gate" layer these sources describe — the research suggests the missing piece is *independent* acceptance criteria, not heavier tooling.
   **Confidence: high** (4+ independent 2026 sources converge).

2. **What:** Coverage vs mutation-score conflict. Total Shift Left (2026-08): line coverage "stops meaning anything" for AI-generated tests — gate on mutation score (Stryker/Mutmut/PIT) instead; coverage climbing while mutation score stays flat = suite growing without strengthening. ContextQA (2026-04) contradicts: recommends *raising* coverage thresholds to 85–90% for AI-written files.
   **Why it matters:** For a no-test-runner knowledge repo, this favors simple behavioral assertions ("file exists AND parses AND follows template") over any coverage metric.
   **Confidence: high** on the conflict existing; **med** on which side applies to non-code repos.

3. **What:** Spec Kit 1.0.0 (github/spec-kit, Aug 2026): MIT-licensed `specify` CLI; `/speckit.specify|plan|tasks|implement|analyze|checklist`; works with 30+ agents; community extensions (CI Guard, Architecture Guard) add compliance gates. An arXiv study (arXiv:2604.05278) adds phase-level "context-grounding + validation hooks" that check SPEC/PLAN/TASKS artifacts *against the repo* (paths exist, deps installed) before implementation — improved judged quality (+3.0%, p<0.05) and caught hallucinated paths early. Cost: ~20–40% more tokens per feature (fundesk, Apr 2026).
   **Why it matters:** The workspace's "write to topics/ only after QA passes" is already artifact-gated; a lightweight analogue is validating *topic drafts* (template conformance, no dangling refs) before promotion.
   **Confidence: high** on tool facts; **med** on applicability to a docs-only repo.

4. **What:** AGENTS.md conventions. Red Hat (2026-07-27): keep <150 lines, use as an index (orientation table pointing to docs/), review anything auto-generated — ETH Zurich found auto-generated context files can hurt performance and add >20% inference cost. Atlan docs: <300 lines, "Always / Ask first / Never" boundaries section, nearest-file-wins precedence in monorepos. BuildBetter (2026-05): 200–500 lines sweet spot (conflicts with Red Hat).
   **Why it matters:** Direct guidance for how the workspace's repo AGENTS.md and topic files should be structured and sized.
   **Confidence: high** on best practices; note the length-band disagreement (150 vs 300 vs 500).

5. **What:** Allowlist `.gitignore` mechanics (git-scm docs; TheLinuxCode playbook, 2026-02): start with `*`, then `!/dir/` to un-ignore *parent directories* (git won't descend into ignored dirs), then `!/dir/file`; verify with `git check-ignore -v`; ignore rules never untrack already-tracked files (use `git rm --cached`); git's own doc example uses `/*` (not bare `*`) for the top-level deny-all.
   **Why it matters:** This is exactly the repo's pattern; the two gotchas (parent-dir traversal, tracked-file stickiness) are the likely silent-failure modes for a public repo.
   **Confidence: high** (official docs).

6. **What:** Symlinks in git (Stack Overflow canonical answer; gitignore/git docs; BinaryLoader 2026-02): git stores only the link's target path as file content (mode 120000); clones on machines where the target doesn't exist produce dangling links; `core.symlinks=false` checks out links as plain text files; a symlinked *directory* is replaced by a real dir on some pulls. Practitioner split on dotfiles strategy: GNU Stow symlink-farms vs copy-based deployment (shinyaz 2026-03 argues copies: symlinks break when repo moves) vs bare-repo-with-alias (Trevor Lauder 2025-08).
   **Why it matters:** macOS agent workspace with dotfiles/symlinks nearby; a public repo should never ship a symlink pointing outside the repo.
   **Confidence: high** on git behavior; **med** on which dotfiles strategy is "best" (sources disagree).

7. **What:** CI for solo/agent-driven projects: GitHub Actions is free for public repos; minimal viable pipeline is lint + typecheck + a few behavioral tests on every push, with branch protection requiring the status check (heathschweitzer 2026-04; welikeremotestack 2026-03). For agent-in-CI: `deep-agent-action` (github.com/dipjyotimetia, Jun 2026) runs a coding agent in-process on the runner with allow-listed secret-free shell, human-approval gates (`require_push_approval`), and cost caps; `three-body-agent` (a7t-ai) shows a full autonomous implement→fix→merge pipeline using only `gh`/`jq`/shell. Caveat: PRs from `GITHUB_TOKEN` don't trigger other CI workflows without a GitHub App.
   **Why it matters:** The repo is public with no build system — a 10-line Actions workflow re-running the existing primitive QA gate server-side is the cheapest tamper-evident verification layer.
   **Confidence: high**.

8. **What:** Monorepo vs small repos for 1-person/small teams: near-consensus that monorepo/default-single-repo wins until a component has a genuinely independent lifecycle (different runtime, release cadence, or hard access boundary); plain workspace scripts beat Turborepo/Nx below ~3 people; git submodules are a known footgun for small teams (dev.to/libme 2026-08; smitparekh 2026-06; ztabs 2026-02).
   **Why it matters:** Confirms keeping knowledge content in one dedicated repo rather than splitting per-topic repos or vendoring via submodules.
   **Confidence: high** on solo/small-team guidance (3 concordant sources).

## For This Workspace
1. **Codify the QA gate into one runnable script** (e.g. `scripts/qa.sh`: `bash -n` on scripts, `test -f` on required files, `git status --porcelain` scope check, plus `git check-ignore -v` spot-checks on the allowlist). Same primitives, single invocation — reusable by agents, humans, and CI (Finding 5, 7).
2. **Add two public-repo hygiene checks to the gate:** (a) fail on any tracked symlink whose target is outside the repo (`git ls-files -s | grep ^120000` + readlink check) — prevents dangling links on clone; (b) fail on already-tracked-but-ignored files (`git ls-files -i --exclude-standard`) — catches allowlist drift (Finding 5, 6).
3. **Wire a minimal GitHub Actions workflow** running that QA script on every push to main (free for public repos, ~10 lines YAML); enable branch protection requiring the check. This gives server-side verification without adding a build system or test runner (Finding 7).
4. **Independent-oracle rule for topic files:** acceptance criteria for new `.agent-memory/topics/` entries should be written *before* the content (template checklist: required sections, no TODO placeholders, working relative links), and validated by a separate review pass — not by the same agent turn that wrote the file (Findings 1, 2).

## Sources
- https://www.shiplight.ai/blog/testing-strategy-for-ai-generated-code — Shiplight AI (2026-05), 7-layer testing model for AI code
- https://totalshiftleft.ai/blog/testing-ai-generated-code — Total Shift Left (2026-08), gates/mutation-score vs coverage
- https://contextqa.com/blog/what-is-ai-generated-code-testing-checklist/ — ContextQA (2026-04), 6-layer checklist (conflict source on coverage)
- https://qaskills.sh/blog/testing-ai-generated-code-sdet-playbook — QASkills.sh (2026-02), SDET playbook, independent oracles
- https://www.orbittest.dev/blog/how-to-test-ai-generated-code — OrbitTest (2026-07), boundary/contract testing for AI code
- https://github.com/github/spec-kit — GitHub Spec Kit (v1.0.0, 2026-08), spec-driven development toolkit
- https://arxiv.org/pdf/2604.05278 — arXiv, Spec Kit Agents: context-grounding/validation hooks study
- https://www.fundesk.io/spec-driven-development-github-spec-kit-guide — Fundesk (2026-04), Spec Kit workflow + token cost
- https://agents.md/ — agents.md, open AGENTS.md spec
- https://developers.redhat.com/articles/2026/07/27/standardize-project-context-agentsmd-and-agent-skills — Red Hat Developer (2026-07), AGENTS.md + Agent Skills best practices
- https://docs.atlan.com/agents/how-tos/write-an-agents-md-file — Atlan docs, AGENTS.md authoring guide
- https://blog.buildbetter.ai/agents-md-complete-guide-for-engineering-teams-in-2026/ — BuildBetter (2026-05), AGENTS.md guide (length-band conflict source)
- https://git-scm.com/docs/gitignore — Git official docs, ignore semantics + allowlist example
- https://thelinuxcode.com/ignore-everything-track-only-what-matters-a-practical-gitignore-playbook/ — TheLinuxCode (2026-02), allowlist .gitignore playbook
- https://stackoverflow.com/questions/954560/how-does-git-handle-symbolic-links — Stack Overflow, git symlink behavior
- https://blog.binaryloader.io/en/development/scm/git/sync-files-with-symlink/ — BinaryLoader (2026-02), symlinked config files
- https://shinyaz.com/en/blog/2026/03/15/modern-dotfiles-guide — shinyaz (2026-03), copy-vs-symlink dotfiles tradeoffs
- https://trevorlauder.dev/blog/2025/08/09/macos-dotfiles-bare-git-setup/ — Trevor Lauder (2025-08), bare-repo dotfiles on macOS
- https://heathschweitzer.com/blog/ci-cd-for-solo-developers-github-actions-without-the-complexity — Heath Schweitzer (2026-04), minimal solo CI/CD
- https://github.com/dipjyotimetia/deep-agent-action — deep-agent-action (2026-06), agent-in-CI with allowlisted shell + approval gates
- https://dev.to/libme/monorepo-or-polyrepo-for-a-three-person-startup-a-decision-framework-51nd — DEV (2026-08), small-team repo decision framework
- https://www.smitparekh.co.in/blog/monorepo-vs-polyrepo-a-decision-framework-for-small-teams — Smit Parekh (2026-06), monorepo vs polyrepo for small teams
