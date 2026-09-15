#!/usr/bin/env python3
"""Compile DTCG token JSON -> CSS custom properties for the ops dashboards.

Distilled from ops/vendor/ux-ui-agent-skills (token-build + design-tokens).
Reads the vendor tokens/*.json (DTCG $type/$value), resolves {alias}
references across the whole set, and emits one self-contained CSS file:

  :root                     -> all tokens (light/base), namespace-prefixed
  :root[data-theme="dark"]  -> delta overrides from colors.json "dark" tier

Dotted paths become kebab-case var names: semantic.surface.card ->
--ops-semantic-surface-card. Primitives are emitted but the convention is:
components reference SEMANTIC vars only, never primitives.

Usage:
  python3 build_tokens_css.py                          # default vendor tokens -> stdout
  python3 build_tokens_css.py -o dashboard.css         # write file
  python3 build_tokens_css.py --prefix app             # --app-... names
  python3 build_tokens_css.py /path/to/tokens -o t.css # custom token dir

Exit 0 = built (and, unless --no-validate, all aliases resolved);
exit 1 = unresolved alias or unreadable JSON.
"""
import argparse
import json
import re
import sys
from pathlib import Path

DEFAULT_TOKENS = Path("/Users/grit/ops/vendor/ux-ui-agent-skills/tokens")
ALIAS = re.compile(r"\{([^}]+)\}")


def flatten(obj, prefix=""):
    """Yield (dotted_path, node) for every DTCG leaf (a dict with $value)."""
    out = {}
    if isinstance(obj, dict):
        if "$value" in obj:
            out[prefix] = obj
        else:
            for k, v in obj.items():
                if k.startswith("$"):
                    continue
                out.update(flatten(v, f"{prefix}.{k}" if prefix else k))
    return out


def load_set(token_dir):
    """Load every *.json in the dir; return {dotted_path: node} merged.

    Mirrors the vendor validator's tolerant alias model: every token is
    registered under bare path (first-wins on cross-file collision), plus
    "<stem>.<path>" for each file, so {opacity.disabled}, {dataviz.*},
    and {semantic.feedback.error-border}-style refs all resolve. Two
    vendored aliases are genuinely broken (states.error.* -> feedback.error
    without the -border/-ring suffix; see BROKEN_ALIASES).
    """
    leaves, prefixed = {}, {}
    for f in sorted(token_dir.glob("*.json")):
        try:
            data = json.loads(f.read_text())
        except json.JSONDecodeError as e:
            sys.exit(f"FAIL invalid JSON: {f.name}: {e}")
        stem = f.stem
        flat = flatten(data)
        for path, node in flat.items():
            if path not in leaves:
                leaves[path] = node
            for ns in {stem, stem.replace("-", "")}:
                prefixed[f"{ns}.{path}"] = node
        for k, v in data.items():
            if k.startswith("$"):
                continue
            for path, node in flatten(v, k).items():
                for ns in {stem, stem.replace("-", "")}:
                    prefixed[f"{ns}.{path}"] = node
    leaves.update({k: v for k, v in prefixed.items() if k not in leaves})
    return leaves


# Vendored aliases that reference nonexistent tokens; redirected to the
# intended target so the build passes without editing the read-only source.
BROKEN_ALIASES = {
    "semantic.feedback.error": "semantic.feedback.error-border",
    "dataviz.diverging.positive-strong": "dataviz.diverging.positive-strong",
    "dataviz.diverging.negative-strong": "dataviz.diverging.negative-strong",
}


def css_str(val):
    """Coerce a resolved token value to a CSS-safe string (lists -> comma-join)."""
    if isinstance(val, list):
        return ", ".join(str(v) for v in val)
    return str(val)


def resolve(leaves):
    """Resolve {alias} refs against the merged set. Returns (resolved, unresolved)."""
    resolved, unresolved = {}, []
    for path, node in leaves.items():
        val = node["$value"]
        if isinstance(val, str):
            def sub(m):
                ref = m.group(1).lstrip("./")
                ref = BROKEN_ALIASES.get(ref, ref)
                tgt = leaves.get(ref)
                if tgt is None:
                    unresolved.append(f"{path} -> {{{m.group(1)}}}")
                    return m.group(0)
                return css_str(resolved.get(ref, tgt["$value"]))
            val = ALIAS.sub(sub, val)
        elif isinstance(val, list):
            val = [ALIAS.sub(lambda m: resolved.get(
                m.group(1), m.group(0)), v) if isinstance(v, str) else v
                for v in val]
        resolved[path] = val
    return resolved, unresolved


def var_name(dotted, prefix):
    return f"--{prefix}-" + dotted.replace(".", "-").replace("_", "-")


def emit_css(leaves, prefix):
    resolved, _ = resolve(leaves)
    base, dark = {}, {}
    for path, node in leaves.items():
        if path.startswith("dark.") and path != "dark" or ".dark." in path:
            # colors.json "dark" tier mirrors the semantic tiers (text,
            # surface, border, action) -> emit as semantic-var overrides.
            bare = path.removeprefix("colors.").removeprefix("dark.")
            mirror = "semantic." + bare
            dark[mirror if mirror in leaves else "dark." + bare] = resolved[path]
        else:
            base[path] = resolved[path]

    lines = ["/* GENERATED by build_tokens_css.py - do not hand-edit.",
             "   Source: ops/vendor/ux-ui-agent-skills/tokens/*.json (DTCG).",
             "   Conventions: reference semantic vars only; dark = delta block. */",
             ":root {"]
    for path in sorted(base):
        lines.append(f"  {var_name(path, prefix)}: {base[path]};")
    lines.append("}")
    if dark:
        lines.append("")
        lines.append(":root[data-theme=\"dark\"] {")
        for path in sorted(dark):
            lines.append(f"  {var_name(path, prefix)}: {dark[path]};")
        lines.append("}")
    return "\n".join(lines) + "\n", dark


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("token_dir", nargs="?", default=str(DEFAULT_TOKENS))
    ap.add_argument("-o", "--output", default=None)
    ap.add_argument("--prefix", default="ops")
    ap.add_argument("--no-validate", action="store_true",
                    help="skip unresolved-alias hard failure")
    args = ap.parse_args()

    token_dir = Path(args.token_dir)
    if not token_dir.is_dir():
        sys.exit(f"FAIL not a token directory: {token_dir}")
    leaves = load_set(token_dir)
    if not leaves:
        sys.exit(f"FAIL no tokens found in {token_dir}")

    if not args.no_validate:
        _, unresolved = resolve(leaves)
        if unresolved:
            for u in unresolved:
                print(f"UNRESOLVED {u}", file=sys.stderr)
            sys.exit(1)

    css, dark = emit_css(leaves, args.prefix)
    if args.output:
        Path(args.output).write_text(css)
        n_dark = len(dark)
        print(f"OK wrote {args.output} "
              f"({len(css.splitlines())} lines, {n_dark} dark overrides)")
    else:
        sys.stdout.write(css)


if __name__ == "__main__":
    main()
