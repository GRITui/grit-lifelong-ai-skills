---
name: token-build
description: Use when the local HTML/Swift dashboards need design tokens — compiles the vendored DTCG token JSON into a single namespace-prefixed CSS variables file (base + dark-theme delta block) via a deterministic script. Triggers on "tokens", "CSS variables", "theme file", "dark palette" for dashboard UI work.
sources:
  - /Users/grit/ops/vendor/ux-ui-agent-skills/.claude/skills/token-build/SKILL.md
  - /Users/grit/ops/vendor/ux-ui-agent-skills/.claude/skills/design-tokens/SKILL.md
  - /Users/grit/ops/vendor/ux-ui-agent-skills/workflows/token-build.md
  - /Users/grit/ops/vendor/ux-ui-agent-skills/tokens/*.json
---
# audited: PASS 2026-09-10 (PO audit)
# Token Build (local dashboard variant)

Deterministic TOOL distilled from the vendor kit. The DTCG token JSON is the
source of truth; CSS output is generated, never hand-edited.

## Use

```sh
python3 ~/.agent-memory/skills-inbox/token-build/build_tokens_css.py -o dashboard.css
python3 .../build_tokens_css.py --no-validate          # warn-only build
python3 .../build_tokens_css.py <custom-token-dir> -o t.css
```

## What it does

- Flattens all `tokens/*.json` (colors, typography, spacing, shadows, borders,
  motion, gradients, opacity, blur, sizing, states, theming, data-viz,
  breakpoints) into dotted paths → `--ops-<path>` CSS vars.
- Resolves `{alias}` references across the full set; unresolved alias = exit 1
  (same rule as vendor `scripts/validate_tokens.py`).
- Emits `:root` (base) + `:root[data-theme="dark"]` (delta-only overrides from
  `colors.json` `dark` tier). Dark-first is fine: set `data-theme="dark"` on
  `<html>` — our dashboards are dark by default.

## Conventions (adapted, non-negotiable)

- Namespace is `--ops-` (rename with `--prefix`); keep it stable across
  dashboards so copy-paste between them works.
- Components reference **semantic** vars (`--ops-semantic-surface-card`) or
  component vars — never primitives (`--ops-primitive-gray-500`) and never raw
  hex/px/duration. That is the same no-hardcode rule as vendor `design-qa`.
- Regenerate on token change; a stale CSS file next to fresh JSON is a bug.
- Dark overrides stay a delta — never duplicate the full light set.

## Pairs with

- `frontend-design` (aesthetic direction) — consumes these vars.
- `a11y-audit` (this folder) — verifies the rendered result meets contrast.
- Vendor depth if ever needed: `scripts/validate_tokens.py`,
  `workflows/token-build.md` (Style Dictionary / multi-platform targets we do
  not use locally).

## Verification

`python3 -m py_compile build_tokens_css.py` passes; script exit 0 = valid
tokens + all aliases resolved. Check the generated file starts `/* GENERATED`
and contains both `:root` blocks before wiring a dashboard to it.
