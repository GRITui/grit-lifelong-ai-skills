---
name: qa-gate
description: Use when verifying any deliverable before merge, promotion, or equip — shell scripts, required files, commit scope, allowlist .gitignore hygiene, tracked-symlink safety, research-draft claims, or test suites. Enforces exit-code-0 deterministic gates, independent-oracle review, and mutation-score-over-coverage verdicts. Never accept agent self-reported success.
sources:
  - /Users/grit/.agent-memory/topics/software-development/2026-09-07-swarm-research.md
  - /Users/grit/.agent-memory/topics/software-development/2026-09-08-swarm-research.md
  - /Users/grit/.agent-memory/topics/software-development/2026-09-08-swarm-research-benchmarks.md
  - /Users/grit/.agent-memory/topics/software-development/2026-09-09-swarm-research.md
  - /Users/grit/.agent-memory/topics/software-development/2026-09-09-swarm-research-agent-reliability.md
---
# audited: PASS 2026-09-10

## Prime rule

- The gate passes ONLY on exit code 0 — never on intent, never on "should work".

## Deterministic primitives (pick by what changed)

| Changed | Gate |
|---|---|
| Shell script | `bash -n <script>` (+ `shellcheck <script>` if installed) |
| Required files / harness | `test -f <each required path>` |
| Markdown / memory | exists, non-empty, headers + relative links resolve |
| Commit scope | `git status --porcelain` shows only intended files |
| Allowlist hygiene | `git check-ignore -v <path>` spot-checks return the expected rule |
| Tracked symlinks | `git ls-files -s \| grep ^120000` then `readlink` each target — fail if target missing or outside the repo |
| Tracked-but-ignored | `git ls-files -i --exclude-standard` — fail on ANY output (allowlist drift) |

- Why `bash -n`: parse-only syntax check — exits 0 when the script parses, nonzero on any syntax error; it never executes the script, so it safely gates untrusted code.
- `git ls-files -i --exclude-standard` non-empty means tracked files were later ignored — untrack (`git rm --cached`) or fix the rule before merge.
- Allowlist `.gitignore`: git won't descend into ignored dirs — every `!` negation needs its parent dirs un-ignored first.

## Independent-oracle rule (judgment gates)

- Write acceptance criteria BEFORE producing the content; validate against them in a separate pass.
- Never let the producing agent/turn grade its own output — self-reported success and passed-own-tests are the documented failure modes.
- Use the `fact-check` skill (`~/.claude/skills/fact-check`) to verify claims; independently spot-check at least ONE load-bearing claim per research draft.
- For unattended/cron runs touching production content or deploys: add a second-agent review step beyond exit codes.
- Probe error paths and edge cases, not just the happy path — AI-authored bugs cluster there.

## Verdicts

- Research drafts: FAIL if sources missing, any claim untraceable, or the spot-check contradicts the draft. PASS → merge with QA-gated header; FAIL → reject with reason.
- Code suites: gate on mutation score, not line coverage — coverage rising while mutation score stays flat = suite growing without strengthening.
- No-test-runner (docs/knowledge) repos: behavioral assertions (file exists AND parses AND matches template) beat any coverage metric.

Validate: `bash -n <script>` — exit 0 = parses clean; ANY nonzero = gate fails (syntax error); never run the script itself to "check" it.
