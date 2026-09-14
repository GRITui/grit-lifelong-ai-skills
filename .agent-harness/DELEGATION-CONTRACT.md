# Delegation Contract v2 — the software house (temporary tool grants for sub-agents)

Rule: every delegated task receives the **minimum** toolset for its task shape,
for **that run only**, scoped to **one declared output directory**, with a call
budget and a mandatory exit-check. Escalation beyond the grant goes back to the
PO — a sub-agent never widens its own permissions.

## MVP 3 — the software-house roster

Each profile below is a role in a small software house, not a generic label.
The grant is picked to be the *tightest fit* for what that role actually does
day to day — a QA engineer probes and reports, a designer never touches
implementation code, an SRE is the only one with real system access. Every
role still has one door to tools outside its own lane: **Global Tool
Escalation**, below.

## Profiles (role → grant)

| Profile   | House role                        | Tools granted                                   | Write scope                  | Budget (tool calls) | Spawned by |
|-----------|------------------------------------|--------------------------------------------------|------------------------------|---------------------|------------|
| researcher| Research Analyst                   | WebSearch, WebFetch, Read, Glob, Grep, Write      | `.agent-memory/inbox/` only  | ≤12                 | PO / batch |
| builder   | Software Engineer                  | Read, Write, Edit, Glob, Grep, Bash (project-safe) | ONE named project dir       | ≤20                 | PO / batch |
| auditor   | QA Engineer                        | Read, Glob, Grep, Bash (read-only + curl probes) | none — reports only          | ≤10                 | PO only    |
| ops       | DevOps / SRE                       | Bash full (launchctl, sqlite3, plutil, brew, npm), Read, Glob | system/config paths | ≤15                 | PO only    |
| designer  | Product Designer                   | Read, Write, Glob, Grep                          | ONE named design-output dir  | ≤15                 | PO / delegator |
| writer    | Technical Writer                   | Read, Write, Glob, Grep                          | ONE named docs dir           | ≤12                 | PO / delegator |
| delegator | Engineering Manager (delegation)   | Task, Read, Glob, Grep, TodoWrite                | none — spawns do the writing | ≤8 spawns           | PO only    |

## Prompt block — append to every Task brief (portable floor)

```
- Granted tools: <profile> (<explicit list>)
- Write scope: <single dir> — any write outside it is a violation; report and stop
- FORBIDDEN everywhere: git push, rm outside declared dirs, plist/launchd/system
  edits (unless ops profile), installing packages, contacting credentials
- Output: single file or single dir named above
- Validate: '<exit-code check>' must pass before you report success —
  self-reported success without exit codes is not evidence
```

## Tool bindings (profile → .agent-harness/tools/)

Bindings are picked per role: each profile gets the scripts that match what it
actually does, not the full catalog.

| Profile   | Bound tools                                  | Selection rule |
|-----------|-----------------------------------------------|----------------|
| researcher| (none)                                        | inbox-only writes; tools unnecessary |
| builder   | skills-index, board, build_tokens_css.py     | run equipped tools instead of hand-typing their sequences; token builds are a build-time step |
| auditor   | skills-index (read-only), a11y-probe, qa-gate, qa-structure | probe/verify tools only — matches "reports, never fixes" |
| ops       | all tools (+ anything added later)           | on equip, ops grant is automatic — SRE owns the toolbox |
| designer  | a11y-probe (read-only)                       | spot-check a11y on specs/mockups before handoff to builder |
| writer    | skills-index (read-only), script-handoff-brief | assembling docs/handoffs is this role's core output |
| delegator | skills-index, board (read-only)              | reads to assemble briefs; never runs mutating tools itself |

Selection is by profile, not by search: the spawner includes the bound tools in
the grant; the sub-agent never hunts for tools. `SKILLS-INDEX.md` `tool` entries
exist for humans/equipped agents and T5 drift reports.

## Global Tool Escalation (the "still need a global tool" door)

Every role above is scoped tight on purpose. When a brief genuinely needs a
tool or skill outside a profile's bound list — including the standing 8 in
`.agent-harness/tools/` a role isn't bound to, or an `equipped`/`staged` skill
from `SKILLS-INDEX.md` — the sub-agent does **not** reach for it itself. It:

1. States the gap in its report: which tool/skill, why the bound set doesn't
   cover the brief.
2. Stops there — no self-widening, no working around the gate with raw Bash
   (which most roles don't have anyway) or a hand-rolled equivalent.
3. The PO decides: either re-spawn the same brief as a profile that already
   carries that tool bound (e.g. an a11y question that needs deeper probing
   goes to `auditor`, not a `designer` improvising), or grant the specific
   tool for that single run under the Ghost rule below, noted in the PO's
   daily log.

This is the same mechanism the `ops` "Ghost rule" already used for one-off
permissions (e.g. VACUUM) — Global Tool Escalation is that rule generalized to
every profile and to skills/tools, not just Bash subcommands. Grants under
this door never persist past the run that requested them; the profile's
default bound list in the table above is what ships next time unless the PO
edits this contract.

## The hard gate, defined (what makes it "hard")

**Mechanism:** `.claude/agents/<persona>.md` frontmatter `tools:` is a runtime
allowlist, enforced by the Claude Code engine at spawn. A spawned
`subagent_type: researcher` receives a tool registry containing ONLY the
listed tools — `Bash`, `Edit`, `TodoWrite`, `Task` etc. are **absent from its
tool table**, so the agent cannot even attempt them. This is categorically
stronger than the prompt block, which is a rule the model could ignore.

**Per-persona gate matrix:**

| Persona | Hard-allowed | Hard-absent (impossible to call) |
|---------|--------------|----------------------------------|
| researcher | WebSearch, WebFetch, Read, Glob, Grep, Write | **Bash, Edit, Task, TodoWrite** — cannot shell out, mutate files, or re-spawn sub-swarms |
| builder | Read, Write, Edit, Glob, Grep, Bash | WebSearch/WebFetch (no unsupervised web), Task — brief-bound Bash only |
| auditor | Read, Glob, Grep, Bash | Write, Edit, **Task** — physically cannot remediate or re-delegate (pure findings) |
| ops | Bash, Read, Glob | WebSearch, Write, Edit, Task — mutations only through reviewed shell commands |
| designer | Read, Write, Glob, Grep | Bash, Edit, WebSearch/WebFetch, **Task** — spec/copy writer only, cannot execute code or re-delegate |
| writer | Read, Write, Glob, Grep | Bash, Edit, WebSearch/WebFetch, **Task** — docs/handoff writer only, cannot execute code, fetch live sources, or re-delegate |
| delegator | Task, Read, Glob, Grep, TodoWrite | **Write, Edit, Bash, WebSearch/WebFetch** — can only spawn the other profiles, cannot touch files or shell directly itself |

**Remaining soft layer (still enforced in persona bodies):** Bash SUBCOMMAND
scope (auditor: read-only/probe-only; ops: brief-named targets only) cannot be
expressed in frontmatter — enforced by the persona's brief template + the PO
reviewing ops commands. Everything else above is engine-enforced.

**Registration & verification:** personas register at Claude Code session
startup. Verify once registered: `Task(subagent_type=auditor)` then ask it to
run `Write` — hard gate proof = tool absent from its inventory. Unregistered
sessions → fall back to `general` + the persona's brief block (portable floor).

## Grant line — one line inside every Task brief

`- Granted: <profile> — tools: <list>; scope: <dir>; budget: ≤N calls; tools bound: <names or none>`

## Hard-gating (evidence-backed personas registered 2026-09-10)

| Runtime      | Mechanism |
|--------------|-----------|
| Claude Code  | **`.claude/agents/{researcher,builder,auditor,ops,designer,writer,delegator}.md`** — native `tools:` frontmatter HARD-restricts spawns; each persona body embeds its brief template (scope lock, budget, mandatory Validate). Use `subagent_type: researcher\|builder\|auditor\|ops\|designer\|writer\|delegator` in Task calls; fall back to `general` + the prompt block only when the persona file is absent on that machine or the session predates registration. `delegator` is the only profile with `Task` — it may spawn the other six, never itself (no nested delegators) |
| headless CLI | `--allowedTools` on `-p` runs (unlisted tools silently no-op — list everything the task needs, including its Validate command's tool) |
| opencode     | `opencode.json` agent `tools:{...}` per agent |
| Other        | the persona prompt block IS the enforcement |

Ghost rule: when a profile needs a temporary extra permission (e.g. `ops` running
VACUUM), the PO grants it in the brief for that single task and notes it in the
daily log — grants never persist beyond the spawned run.

## Hypothesis tests (empirical spot-check instrument)

All profiles have standing authority to run ONE-CLASS hypothesis tests during
build/research/QA work:

- Write scope extension: a throwaway directory `/tmp/hypo-<slug>/` (scripts,
  scratch files, compiled probes) — the ONLY sanctioned write outside the
  declared scope. Self-clean when done; never commit it anywhere.
- Procedure: state the claim as a falsifiable line ("X happens in ≤N"), write the
  minimal script that would falsify it, run it, capture exit code + key output.
- Evidence rule: PASSED hypothesis tests may be cited in place of (or alongside)
  a source spot-check in QA gates — record `hypo-test: <claim> → exit X, <fact>`
  in the report. A FAILED test falsifies the claim regardless of what the
  sources said; the finding goes in the report even when the draft must change.
