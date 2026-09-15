---
name: code-review
description: Use when asked to review a diff since a fixed point (commit, branch, tag, HEAD~N), a swarm build lane's output, or a PR before merge. Two-axis review run as parallel sub-agents: Standards (repo rules plus a smell baseline) and Spec (fidelity to the originating contract). Pairs with qa-gate, which owns the deterministic checks this skill must not redo.
sources:
  - /Users/grit/ops/vendor/mattpocock/skills/skills/engineering/code-review/SKILL.md
pairs-with:
  - qa-gate
---
# audited: PASS 2026-09-10 (S3 PO audit)
# status: S2-draft 2026-09-10

## Prime rules

- Two axes, ALWAYS separate: **Standards** (how it is written) and **Spec** (what it was asked to do). Never merge or rerank across axes; one axis must not mask the other.
- Run each axis as its own sub-agent so neither pollutes the other's context.
- qa-gate runs FIRST and must already be green. This skill judges; it does not re-run exit-code checks.

## Fixed point

- Use the point the requester names (SHA, branch, tag, `HEAD~N`). None given: ask, or if unanswerable, default to the DELEGATION-CONTRACT's base ref.
- Pin once: `git diff <fixed>...HEAD` (three-dot, merge-base) plus `git log <fixed>..HEAD --oneline`.
- Fail fast here if `git rev-parse <fixed>` fails or the diff is empty. Never discover a bad ref inside a sub-agent.

## Spec source, in order

1. The DELEGATION-CONTRACT block of the task brief that commissioned this work.
2. A task/contract file under `.agent-memory/` named in the brief.
3. Issue refs in commit messages.
4. Nothing found: ask. Still none: skip the Spec axis, report "no contract available".

## Standards sources

- This workspace's `AGENTS.md`, `CLAUDE.md`, and the project's own `CLAUDE.md` (code style, red lines, comment/emoji rules, no-em-dash prose rule).
- Repo-documented standard always overrides the smell baseline below.
- Skip anything tooling already enforces (lint, shellcheck, formatters).
- Every smell finding is a JUDGEMENT CALL with the hunk quoted, never a hard violation.

## Smell baseline (what it is -> fix)

| Smell | Fix |
|---|---|
| Mysterious Name | rename; no honest name means murky design |
| Duplicated Code | extract shared shape, call from both |
| Feature Envy | move method onto the data it reaches into |
| Data Clumps | bundle the travelling fields into one type |
| Primitive Obsession | give the domain concept its own small type |
| Repeated Switches | polymorphism or one shared map |
| Shotgun Surgery | gather scattered edits into one module |
| Divergent Change | split module so each changes for one reason |
| Speculative Generality | delete; inline until a real need shows |
| Message Chains | hide the walk behind one method |
| Middle Man | cut the delegator, call the target direct |
| Refused Bequest | drop inheritance, use composition |

## Sub-agent briefs

**Standards agent gets**: diff command, commit list, paths of standards files, the smell table pasted IN FULL (sub-agent has no other access). Brief: per hunk, (a) documented-standard breaches citing file+rule, (b) baseline smells named and quoted; state which are judgement calls; under 400 words.

**Spec agent gets**: diff command, commit list, contract path/content. Brief: (a) requirements missing or partial, (b) scope creep beyond the contract, (c) implemented-but-likely-wrong behaviour; quote the contract line per finding; under 400 words. Skip entirely if no spec exists (report that, do not improvise one).

## Aggregate

- Report under `## Standards` and `## Spec`, verbatim or lightly cleaned. No merging, no reranking.
- Close with one line per axis: total findings + worst issue within THAT axis. Never declare a single overall winner.

## Why two axes

A change can pass one axis and fail the other: standards-clean but implements the wrong thing (Spec fail), or contract-exact but violates repo conventions (Standards fail). Separate reporting keeps both visible; that is the whole point.
