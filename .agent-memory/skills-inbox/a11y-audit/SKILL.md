---
name: a11y-audit
description: Use when auditing agent-built HTML dashboards or UI for accessibility — WCAG 2.2 AA contrast, keyboard navigation, focus visibility, target size, screen-reader semantics, reduced-motion. Triggers on "a11y", "accessibility check", "contrast", "keyboard", "WCAG" for any rendered HTML artifact before it ships.
sources:
  - /Users/grit/ops/vendor/ux-ui-agent-skills/.claude/skills/a11y-audit/SKILL.md
  - /Users/grit/ops/vendor/ux-ui-agent-skills/accessibility/wcag-checklist.md
  - /Users/grit/ops/vendor/ux-ui-agent-skills/accessibility/aria-patterns.md
---
# audited: PASS 2026-09-10 (PO audit)
# Accessibility Audit (rendered-HTML gate)

Adapted from the vendor skill for our artifacts: standalone dark-theme HTML
dashboards. Checkable here because our surfaces are real HTML files.

## Steps

1. Read the vendor `accessibility/wcag-checklist.md` (POUR-organized,
   P0/P1/P2) and `accessibility/aria-patterns.md` for the element being
   audited. Do not paraphrase from memory.
2. **P0 set per component** (fail = findings table entry):
   - Keyboard navigable; Tab order logical; no focus trap unless a modal
     (then Escape releases it).
   - Focus visible with ≥3:1 contrast against adjacent colors.
   - Screen-reader name/role/state correct (use native elements first:
     `<button>`, `<input>`, `<table>` — ARIA only to fix, never to re-invent).
   - Contrast: 4.5:1 text, 3:1 large text + UI borders/icons.
   - Target size ≥24×24.
   - No color-only signaling (status dots get text or `aria-label` too).
3. **Dark-theme specifics for our dashboards:** muted grays on dark surfaces
   are the top contrast failure; check `--ops-*` semantic text vars, not
   guessed hex. Reduced motion: honor `prefers-reduced-motion` (vendor
   `tokens/motion.json` has a `reducedMotion` tier).
4. WCAG 2.2 additions: Focus Not Obscured (2.4.11), Target Size (2.5.8).
5. **Measure, never eyeball.** Never state a ratio you did not compute: run
   the vendor's real-render gate `node /Users/grit/ops/vendor/ux-ui-agent-skills/scripts/measure_render.mjs <file> --dark`
   (every text element) and `verify_states.mjs <file> --dark` (default/hover/
   focus per control) when Node+Playwright exist; for loose pairs compute
   contrast in Python (relative luminance) and report the computed number.
   If a gate cannot run, say "not verified" — do not claim pass.

## Output

A findings table: WCAG criterion (e.g. 1.4.3) · severity (P0/P1/P2) ·
what fails · specific fix (token or code-level). Confirm passes explicitly.
Accessibility is never traded for aesthetics; a contrast failure means the
color changes, not the requirement.

## Pairs with

- `qa-gate` (deterministic gates) — this is the a11y lens on top of it.
- `frontend-design` (aesthetics) — contrast findings override its color picks.
- `token-build` (this workspace) — fix dark-theme contrast at the token layer,
  regenerate CSS, re-audit.

## Vendor depth (load on demand, read-only)

`accessibility/cognitive.md`, `i18n-rtl.md`, `vision.md`, `wcag-aaa.md` —
only when the artifact actually needs them.
