# MVP 3 — Software-House Delegation Roster (Handoff)

Source: `.agent-harness/DELEGATION-CONTRACT.md`

## 1. The 7 profiles

Every delegated task gets the minimum toolset for its task shape, for that
run only, scoped to one declared output directory, with a call budget and a
mandatory exit-check (`DELEGATION-CONTRACT.md:3-6`).

| Profile    | House role                       | Tools granted                                                      | Write scope                    | Budget (tool calls) | Spawned by       |
|------------|-----------------------------------|----------------------------------------------------------------------|---------------------------------|----------------------|-------------------|
| researcher | Research Analyst                  | WebSearch, WebFetch, Read, Glob, Grep, Write                        | `.agent-memory/inbox/` only     | ≤12                  | PO / batch        |
| builder    | Software Engineer                 | Read, Write, Edit, Glob, Grep, Bash (project-safe)                   | ONE named project dir           | ≤20                  | PO / batch        |
| auditor    | QA Engineer                       | Read, Glob, Grep, Bash (read-only + curl probes)                     | none — reports only             | ≤10                  | PO only           |
| ops        | DevOps / SRE                      | Bash full (launchctl, sqlite3, plutil, brew, npm), Read, Glob         | system/config paths             | ≤15                  | PO only           |
| designer   | Product Designer                  | Read, Write, Glob, Grep                                              | ONE named design-output dir     | ≤15                  | PO / delegator    |
| writer     | Technical Writer                  | Read, Write, Glob, Grep                                              | ONE named docs dir              | ≤12                  | PO / delegator    |
| delegator  | Engineering Manager (delegation)  | Task, Read, Glob, Grep, TodoWrite                                     | none — spawns do the writing    | ≤8 spawns             | PO only           |

(`DELEGATION-CONTRACT.md:19-27`)

Each grant is the tightest fit for the role's actual day-to-day work: a QA
engineer (auditor) probes and reports only, a designer never touches
implementation code, and an SRE (ops) is the only profile with real system
access (`DELEGATION-CONTRACT.md:10-15`).

This is also engine-enforced, not just a prompt convention: Claude Code's
`.claude/agents/<persona>.md` frontmatter `tools:` is a runtime allowlist —
a spawned sub-agent's tool table physically omits unlisted tools (e.g.
`researcher` has no `Bash`/`Edit`/`Task`/`TodoWrite` in its registry at all)
(`DELEGATION-CONTRACT.md:84-113`).

## 2. Global Tool Escalation

Every role's grant is scoped tight on purpose. When a brief genuinely needs
a tool or skill outside a profile's bound list — including one of the
standing 8 scripts in `.agent-harness/tools/` the role isn't bound to, or an
`equipped`/`staged` skill from `SKILLS-INDEX.md` — the sub-agent does not
reach for it itself. Instead it states the gap in its report (which
tool/skill, why the bound set doesn't cover the brief) and stops there: no
self-widening, no working around the gate with raw Bash or a hand-rolled
equivalent. The PO then decides: either re-spawn the same brief as a profile
that already carries that tool bound (e.g. a deeper a11y question goes to
`auditor`, not a `designer` improvising), or grant the specific tool for
that single run, noted in the PO's daily log. Grants made this way never
persist past the run that requested them — the profile's default bound list
in the contract's table is what ships next time unless the contract itself
is edited (`DELEGATION-CONTRACT.md:60-82`).

## 3. Relationship to the Ghost rule

Global Tool Escalation is the same mechanism the `ops` "Ghost rule" already
used for one-off permissions (e.g. running `VACUUM`), generalized to every
profile and to skills/tools — not just Bash subcommands (`DELEGATION-CONTRACT.md:77-82, 128-130`).
