# Skill Delegation Pipeline — v1

State-driven pipeline: any skill request (from research, a lesson, or a backlog
card) flows through these stages. No one ever installs a draft directly.
Every delegated run is bounded by `.agent-harness/DELEGATION-CONTRACT.md`
(temporary, minimum toolset, scoped).

```
S1 Intake (PO)  →  S2 Draft (swarm → .agent-memory/skills-inbox/<name>/)
  →  S3 Audit (PO gate)  →  S4 Equip (~/.claude/skills/)  →  S5 Invoke (on-demand)
  →  S6 Retire (/skill-doctor audit → trash + MEMORY note)
```

- **S1 Intake (PO):** open card; require QA-gated topic sources. No ungated research enters a skill.
- **S2 Draft (swarm):** build swarm writes ONLY to `skills-inbox/<name>/`. Skeleton: frontmatter `name` (== dir), trigger-style `description` (≤100 tok), `sources:` line; body ≤150 lines, decision rules not prose. Draft swarm invokes the equipped `writing-for-agents` skill to distill the draft: description = context pointer (front-loaded trigger word, one trigger per branch, no identity the body already carries); body split by the information hierarchy (in-file step → in-file reference → disclosed reference, pushed to a sibling file only when a branch needs it); prune duplication, no-ops, and sediment before handoff to S3. **Tool grants per `.agent-harness/DELEGATION-CONTRACT.md`** (researcher for research-stage swarms, builder for skill distillation).
- **S3 Audit (PO):** ① schema/name-match ② ≤150 lines ③ grep-audit `curl|exec\(|eval\(|sudo` ④ every rule traceable to a source line ⑤ description = trigger, sharpened per `writing-for-agents` (leading word, one branch per trigger clause) ⑥ invocation choice justified — model-invoked only if the PO or another skill must reach it unprompted, else `disable-model-invocation: true`. PASS **is recorded**: append `# audited: PASS <date>` as the first body line. REJECT → note reason → back to S2 (2 strikes → discard).
- **S4 Equip (PO):** copy PASS folders to `~/.claude/skills/`; verify frontmatter; **regenerate `.agent-harness/SKILLS-INDEX.md`**; daily-log.
- **S5 Invoke / auto-equip (any agent — PROACTIVE):** before any non-trivial task, `grep` `.agent-harness/SKILLS-INDEX.md` for trigger matches. Equipped match → invoke the skill tool (lazy load). **Staged match already `audited: PASS` → the agent MAY SELF-EQUIP** (copy `skills-inbox/<name>/` → `~/.claude/skills/`, verify frontmatter, regenerate index) rather than run the task without it. Staged without audit → don't install; flag to the PO on the board. Never preload a SKILL.md body.
- **S6 Retire (PO):** unused/bloated skills (via /skill-doctor) → trash + note.

`writing-for-agents` (S2/S3 distillation method) is equipped from
https://github.com/mattpocock/skills (MIT), `skills/productivity/writing-for-agents`
— added 2026-09-09.

## Tools track (T) — distill knowledge as a tool when leaner than a skill

**Decision rule:** procedure = judgment + branching → *Skill*. Procedure =
one deterministic command sequence with an exit code → **Tool**. Tools cost
~0 session context, are chmod-capable, and are composable from other tools/skills.

```
T1 Intake (PO, same card as S1; add `type: tool`)  →
T2 Draft (builder swarm → .agent-harness/tools/<name> staged in skills-inbox)  →
T3 Audit (PO: S3 checks + syntax gate `bash -n`/`python -m py_compile` +
   `--help` output present + no hardcoded secrets/absolute user paths beyond
   the documented repo + exit codes on failure paths)  →
T4 Equip (install to `.agent-harness/tools/`, chmod 755, list in SKILLS-INDEX.md
   under `tool` status)  →
T5 Use (any agent: check the index/tool list BEFORE hand-writing a command
   sequence that a tool already implements)  →
T6 Retire (broken/superseded → trash + note, same as S6)
```

Usage directive (all agents): if you are about to hand-run a draw sequence of
≥3 commands that an equipped tool already performs — run the tool instead;
if the tool has drift, flag it on the board (T6 candidate), don't silently fix it.

## Rationale — lazy vs always-equip (measured 2026-09-09)

- Always-equip: Σ 31,434 tok for 9 existing bodies + ~4,800 planned ≈ **36,200 tok in every session** (~18% of a 200K window even unused).
- Pipeline lazy: descriptions ≤100 tok each, S3-gated bodies ≈ **1,500–1,900 tok/session**; bodies load only on invocation. **Delta ≈ 34.5K tok/session (~19×).**
- Matches arXiv 2602.11988: oversized always-on context raises inference cost ~20% and *degrades* task success via dilution. S3 cap + S6 retirement keep the baseline flat as the library grows.
