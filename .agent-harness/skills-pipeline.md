# Skill Delegation Pipeline — v1

State-driven pipeline: any skill request (from research, a lesson, or a backlog
card) flows through these stages. No one ever installs a draft directly.

```
S1 Intake (PO)  →  S2 Draft (swarm → .agent-memory/skills-inbox/<name>/)
  →  S3 Audit (PO gate)  →  S4 Equip (~/.claude/skills/)  →  S5 Invoke (on-demand)
  →  S6 Retire (/skill-doctor audit → trash + MEMORY note)
```

- **S1 Intake (PO):** open card; require QA-gated topic sources. No ungated research enters a skill.
- **S2 Draft (swarm):** build swarm writes ONLY to `skills-inbox/<name>/`. Skeleton: frontmatter `name` (== dir), trigger-style `description` (≤100 tok), `sources:` line; body ≤150 lines, decision rules not prose. Draft swarm invokes the equipped `writing-for-agents` skill to distill the draft: description = context pointer (front-loaded trigger word, one trigger per branch, no identity the body already carries); body split by the information hierarchy (in-file step → in-file reference → disclosed reference, pushed to a sibling file only when a branch needs it); prune duplication, no-ops, and sediment before handoff to S3.
- **S3 Audit (PO):** ① schema/name-match ② ≤150 lines ③ grep-audit `curl|exec\(|eval\(|sudo` ④ every rule traceable to a source line ⑤ description = trigger, sharpened per `writing-for-agents` (leading word, one branch per trigger clause) ⑥ invocation choice justified — model-invoked only if the PO or another skill must reach it unprompted, else `disable-model-invocation: true`. REJECT → note reason → back to S2 (2 strikes → discard).
- **S4 Equip (PO):** copy PASS folders to `~/.claude/skills/`; verify frontmatter; daily-log.
- **S5 Invoke (any agent):** ON-DEMAND ONLY — never preload a SKILL.md body; match by description, then load when executing the procedure.
- **S6 Retire (PO):** unused/bloated skills (via /skill-doctor) → trash + note.

`writing-for-agents` (S2/S3 distillation method) is equipped from
https://github.com/mattpocock/skills (MIT), `skills/productivity/writing-for-agents`
— added 2026-09-09.

## Rationale — lazy vs always-equip (measured 2026-09-09)

- Always-equip: Σ 31,434 tok for 9 existing bodies + ~4,800 planned ≈ **36,200 tok in every session** (~18% of a 200K window even unused).
- Pipeline lazy: descriptions ≤100 tok each, S3-gated bodies ≈ **1,500–1,900 tok/session**; bodies load only on invocation. **Delta ≈ 34.5K tok/session (~19×).**
- Matches arXiv 2602.11988: oversized always-on context raises inference cost ~20% and *degrades* task success via dilution. S3 cap + S6 retirement keep the baseline flat as the library grows.
