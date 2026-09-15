---
name: llm-eval-harness
description: Use when judging LLM-generated output quality over a DATASET rather than gating a single deliverable — designing input/expected pairs, choosing scorers (heuristic vs AI-graded), caching responses to avoid re-billing, or wiring vitest-based `.eval.ts` files. Complements qa-gate, which handles deterministic code gates.
sources:
  - /Users/grit/ops/vendor/mattpocock/evalite/readme.md
  - /Users/grit/ops/vendor/mattpocock/evalite/CLAUDE.md
  - /Users/grit/ops/vendor/mattpocock/evalite/packages/example/src/example.eval.ts
---
# audited: PASS 2026-09-10 (S3 PO audit)

# LLM eval harness

Distilled from evalite (TypeScript-native, local-first LLM eval tool on Vitest).
When the output under test is model-generated, exit-code gates and mutation scores
don't apply — you need a graded signal over a dataset.

## Prime rule

- qa-gate gates CODE deterministically (exit 0 or fail). LLM output needs a
  DATASET + SCORERS producing a score you can trend. Never judge one cherry-picked
  example and call it an eval; never replace the eval harness with "looks good to me".

## Setup (one-time, per project)

```bash
npm i -D evalite vitest
```

- Evals live in `*.eval.ts` files, discovered and run like tests (`npx evalite`,
  `npx evalite watch` for watch mode; local web UI for result browsing).
- Config in `evalite.config.ts` (vitest.config.ts is legacy-supported only).
- Results persist to a local SQLite db (`evalite.db`) — past runs are comparable,
  which is the whole point: trend the score, don't eyeball it.

## Eval file anatomy

```ts
import { evalite } from "evalite";
import { Factuality, Levenshtein } from "autoevals";

evalite("Name of the eval", {
  data: async () => [
    { input: "...", expected: "..." },   // one object per case
  ],
  task: async (input) => {
    // the LLM call under test — may return a string OR a stream
    return callModel(input);
  },
  scorers: [Factuality, Levenshtein],
});
```

- `data()` returns input/expected pairs; each case runs concurrently.
- `task` is EXACTLY the production interaction (same system prompt, same model) —
  if the eval task drifts from production, the score measures a fiction.
- Optional `columns` for custom per-case display data in the UI.

## Scorer selection ladder (cheap → expensive)

1. **Exact / string distance** (`Levenshtein`): verbatim or near-verbatim answers
   (IDs, names, extraction tasks). Free, deterministic.
2. **AI-graded vs expected** (`Factuality` and siblings from autoevals): semantic
   correctness of free-form answers against a known-expected value. Costs tokens.
3. **Custom scorer**: domain rules as plain functions (e.g. "output must contain
   zero forbidden phrases", "JSON must parse and match schema"). Write these before
   reaching for an LLM judge — most domain constraints are checkable deterministically.
- A `no-scorers` eval is legal (raw output inspection in the UI) but produces no
  score — use only while designing, never as a standing suite.
- One eval per behavior, not one mega-eval: "answers capitals", "refuses
  nonexistent countries" are separate `evalite()` calls with separate datasets.

## Dataset design

- Include adversarial and edge cases IN the dataset, not as hopes: the vendor
  example deliberately adds "country does not exist → 'Unknown'" and "no capital →
  '<country> has no capital'" alongside the happy-path capitals.
- `expected` is a CONTRACT, not a hint: it defines what "right" means for scorers.
  If you can't write `expected`, you don't understand the behavior yet — fix that
  before automating judgment.
- Keep datasets small but pointed; every case re-runs (and re-bills) on every eval.

## Cost discipline

- Cache model responses keyed on (model, prompt) so re-runs during scorer/dataset
  iteration don't re-bill (vendor example wraps the model in a cache layer backed
  by local file storage).
- Cheap model for development loops; expensive model only for final verification.
- Trace nested LLM calls (`traceAISDKModel` pattern) so a bad score is attributable
  to the failing sub-call, not mystery-shopped.

## Verdicts and regression flow

- Verdict per eval: score vs its own history (did this change regress the dataset?)
  and vs a threshold you set per behavior. A score without a threshold is trivia.
- Run the harness as part of the merge gate whenever the change touches prompts,
  models, or scoring-relevant code — deterministic gates (qa-gate) and graded evals
  TOGETHER, each covering what the other can't see.
- Failing case → add it to the dataset permanently. Datasets grow monotonically;
  that's the harness compounding.

## Pairing in this workspace

- `qa-gate` = per-deliverable binary gates. This skill = dataset-level quality
  signal for model output. Use both; one never substitutes for the other.
- Runs of agents (`agent-run-contract`) can emit structured-output tags — the
  schema-validated payload is a natural `input` for an eval dataset.
