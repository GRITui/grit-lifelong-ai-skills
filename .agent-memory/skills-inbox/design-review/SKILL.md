---
name: design-review
description: Use when reviewing or scoring agent-built UI — a dashboard, admin screen, or HTML artifact — before it ships. Scores 6 weighted dimensions, applies Nielsen's 10 heuristics and anti-slop checks, and runs the local design-QA gate list. Triggers on "review this UI", "design review", "is this good", "audit my dashboard".
sources:
  - /Users/grit/ops/vendor/ux-ui-agent-skills/.claude/skills/design-review/SKILL.md
  - /Users/grit/ops/vendor/ux-ui-agent-skills/.claude/skills/design-qa/SKILL.md
  - /Users/grit/ops/vendor/ux-ui-agent-skills/workflows/design-review.md
  - /Users/grit/ops/vendor/ux-ui-agent-skills/workflows/design-qa.md
---
# audited: PASS 2026-09-10 (PO audit)
# Design Review (scored) + Design QA (gate list)

Absorbs the vendor `design-review` scoring rubric AND the `design-qa` gate
pyramid, adapted to a no-design-team, no-Figma workspace where the UI is
agent-built dark-theme HTML/Swift dashboards.

## Steps — scored review

1. Read vendor `workflows/design-review.md` for the rubric and scoring guide.
2. Gather context: which dashboard, who reads it, what decisions it drives.
3. Score 6 dimensions — Visual Hierarchy 20%, Consistency 20%, Accessibility
   20%, Usability 20%, Responsiveness 10%, Performance 10% — and compute the
   weighted overall. Consistency = all values trace to `--ops-*` token vars.
4. Run the accessibility lens (P0 checklist) per the `a11y-audit` skill in
   this workspace; use measured contrast numbers, never eyeballed ones.
5. Check the anti-slop tells from vendor `taste/design-taste.md`: emoji as
   icons (banned — use inline SVG `currentColor` or plain words), generic
   gradient-purple defaults, lorem-like placeholder copy, decorative cards
   with no data, "AI-empty filler" layouts.
6. Apply Nielsen's 10 heuristics; cite violations by number.

## Steps — QA gate list (fast gates first)

Run these on the artifact before or after the scored review; report actual
output, not claims:

1. Token discipline: grep the HTML/CSS for raw hex/px/magic durations outside
   the generated token file (vendor rule: `lint_hardcodes.py`). Everything
   traces to a `--ops-*` var.
2. Tokens valid: `python3 build_tokens_css.py` (token-build skill) exits 0 —
   no unresolved aliases.
3. Contrast: measured per a11y-audit (real-render gate if Node exists,
   otherwise computed).
4. States, not just resting: hover/focus/active/disabled all render correctly
   and are visually distinct (the classic failure: focus ring invisible on
   dark surfaces).
5. No horizontal overflow at narrow widths (280/320px) — dashboards still
   get opened on small windows.
6. Render AND look: screenshot the page, click each control, confirm state
   changed. Gates prove correctness, not pixels; a human/agent read of the
   screenshot is part of the gate. Note honestly what was NOT verified.

## Output

- The 6-dimension scored table + weighted overall.
- A prioritized findings table: # · severity (Critical → Major → Minor →
  Enhancement) · finding · recommendation (token-referenced where possible).
- The actual gate results (pass/fail per gate), including "not verified"
  where a gate could not run.

## Pairs with

- `qa-gate` — the generic verification harness; this supplies the
  design-specific gates it should run for UI artifacts.
- `frontend-design` — used at build time; this reviews the result against it.
- `a11y-audit` + `token-build` (this workspace) — the fix loop for contrast
  and consistency findings.

## Vendor depth (read-only, on demand)

`taste/design-taste.md` (full banned-defaults list), `workflows/design-qa.md`
(visual-regression + CI wiring we do not run locally).
