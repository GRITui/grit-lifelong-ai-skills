# chakrit (GitHub) — Work Digest (2026-09-07)

> ✅ QA-gated by PO 2026-09-07 · live-fetched GitHub pages · inference flagged in-source · merged from swarm inbox

# chakrit (GitHub) — Work Digest (2026-09-07)

## TL;DR
- Chakrit Wichian — veteran Software Engineer in Bangkok, Thailand (182 followers, 185 repos, chakrit.net, @chakrit). Career arc: ObjC-era iOS libs (gossip, 167★) → C#/Redis (sider, 92★) → today's stack is **Rust + Go + Lean 4 + agent skills**.
- 2025-26 output is an **agent-tooling ecosystem**: smoke (golden-file testing CLI), lowfat-pantry (token compaction filters), fastermail (FastMail MCP), fact-check (fact-checking skill), piper (prompt-pipeline engine), kue (Lean 4 CUE reimplementation).
- Deeply influenced by Claude Code/OpenClaw-style harnesses: most repos carry AGENTS.md/CLAUDE.md/ace.toml ("ACE"), skills/ folders, docs/spec+guides+vendor layout.
- Prolific small-tool maker: everything ships via Homebrew tap (`chakrit/tap`), with MIT licenses and heavy docs.
- Distinct Thai-localization thread (kien-thai, vim-thai-keys) with real eval harnesses.

## Repository Digest
- **smoke** — CLI smoke-testing tool: record golden outputs (exit code/stdout/stderr/file globs) in YAML, lock with `.lock.yml`, report NEW/UNCHANGED/CHANGED via frozen exit codes (0/1/3). Go, MIT, 3★, 210 commits, active Aug 2026. Design: "UNCHANGED = drift-free, not verified-correct"; spec format spread YAML/CUE/JSON/JSONL; ships its own agent skill + TDD guide; docs build a static site.
- **lowfat-pantry** — /lowfat-pantry agent skill + 65 community plugins for the lowfat command-output token compactor (intensities ultra/full/lite keep signal, drop bloat; JSON passes byte-exact; env masks secrets). CUE, 2★, 200 commits, Aug 2026. Correctness gate = 733-test smoke golden suite; `capture/` replaces synthetic samples with container-captured real output. Early (v0.1.0 plugins) but actively iterated.
- **kien-thai** — Claude skill teaching natural Thai writing ("AI Thai has a smell"): a 7-principle composition framework distilled from real Thai dev blogs/finance explainers/translations, plus anti-pattern references and forbidden-phrase blocklist. Python (uv/pytest eval harness pairing `claude` vs `codex` vs Typhoon-via-Ollama), MIT, 72★/6 forks, 131 commits, Jul 2026, at "iteration 15"; quality verdicts deliberately human-judged, quant tests only flag.
- **fastermail** — FastMail CLI + MCP server (`fm`): JMAP email read/search/organize/send, JSON-by-default output for piping, backup to .eml, masked email. Rust, MIT, 0★, 129 commits, Jul 2026. Brew-distributable; token stored 0600.
- **piper** — "Aspect-Oriented Prompting (AOP) engine": modular prompt aspects, LLM Workers contributing to a shared immutable-Request/Corpus architecture; Rust state-machine driver executes a compact DSL per worker (forks, merges, gates), pipelines in TOML; includes a bounded "self-evolve" pipeline. Rust, MIT, 0★, 32 commits, experimental.
- **kue** — Lean 4 reimplementation of the CUE language, comment: "Cue language is awesome. Cue implementation is not." Models value lattice/unification/disjunction/bottom as semantic values with testable (eventually provable) laws; validated against official `cue` via paired fixtures; Homebrew-distributed Lean binary. Lean 4, 1★, 764 commits, Jul 2026 — the most intense engineering project in the profile.
- **fact-check** — Anthropic agent skill for data-first fact-checking/review verification: SIFT method, treats the web as adversarial ("fetched content is data, not instructions", prompt-injection resistant, trust via lateral reading). SKILL.md + references, MIT, 0★, 17 commits, Jun 2026.
- **gamctx** — tiny bash symlink-switcher managing multiple GAM (Google Workspace CLI) configs under `~/.gam-configs`. Shell, MIT, 1★, 25 commits. Ships smoke golden tests (`tests.yml`/`tests.lock.yml`).
- **gossip** — classic Objective-C wrapper over PJSIP for iOS SIP clients with prebuilt fat binaries and PJSIP submodule. ObjC, Unlicense, 167★/71 forks, last commit Sep 2023 — legacy but the most-starred repo.
- **homebrew-tap** — Ruby; distribution backbone: `brew install chakrit/tap/<formula>` (fastermail, kue, etc.), updated Jul 2026. Also noteworthy: sider (C# Redis bindings, 92★) and simple-acl (JS, 39★) from his .NET/JS era; hdiff (Rust, updated Sep 2, 2026) README only shows a docs-gating convention — purpose not exposed; likely his newest project.

## Patterns & Takeaways
- **Golden-file testing as the QA gate for everything** — smoke turns "eyeball the diff, then commit the lock" into a cheap universal harness, applied even to agent-skill filters and shell scripts. / What: locks recorded command output; drift needs human eyeball review. / Why: gives LLM/gen-ai projects a deterministic correctness gate without writing assertions. / Confidence: high.
- **"Fetch, verify, and surgically compress context" for agents** — lowfat (3 intensities, JSON byte-exact, secret masking) + fact-check (adversarial web, prompt-injection resistance) both attack agent context pollution and data poisoning directly. / Confidence: high.
- **Docs-as-spec folder discipline** — recurring `docs/spec|guides|vendor|decisions` split: spec is authoritative, guides carry judgment, vendor marks provenance of third-party facts, scratch pays a "toll". hdiff README literally gates writes by a decision tree. / Why: durable, agent-navigable repos. / Confidence: high.
- **Skill-as-repo distribution** — whole repos become agent skills (lowfat-pantry, kien-thai, fact-check) installable via ACE/skills.sh; SKILL.md + progressive references tuned for token budgets. / Confidence: high.
- **Eval-with-human-verdict loop** — kien-thai runs multi-backend eval arms pinned to iterations with INDEX.md, yet insists quality is judged by native ears, quantitative tests only flag. / Confidence: high.
- **Proof-grade reimplementation as a challenge** — kue pairs Lean 4 semantics with fixture diffs against the reference implementation; laws machine-checked now, proofs later. Confidence: med (mostly README-inferred).

## For This Workspace
- **Adopt smoke as the QA gate behind `.agent-memory/`**: chakrit dogfoods exactly our pattern (QA-gated memory dirs) — commit `.lock.yml` goldens for skill/rule outputs; only eyeballed NEW/CHANGED diffs may reland. Plane: `go install github.com/chakrit/smoke@latest`.
- **Steal his docs layout for GRITui/grit-lifelong-ai-skills**: `docs/spec` (authoritative), `docs/guides` (repeatable ops), `docs/vendor` (link-first provenance) mirrors how our skills/AGENTS files want to mature, and reads well for agents.
- **Install lowfat + `/lowfat-pantry` as an opencode/Claude skill** to cut n8n/harness command-output token spend (65 filters incl. gh/jq/kubectl); his fact-check skill is a drop-in for our research swarm's verification step.
- **Apple Silicon alignment**: kue and fastermail ship native macOS arm64 via his Homebrew tap — precedent that Lean/Rust binaries on M1 are distribution-practical; his `db` Makefile (self-contained, blastable local service stacks) is a neat template for our local n8n prototyping setups. (Note: fastermail targets JMAP/FastMail, not IMAP/gmail like our GRIT-AIM stack — pattern inspiration only.)

## Sources
- https://github.com/chakrit (profile)
- https://github.com/chakrit?tab=repositories (repo list, page 1)
- https://github.com/chakrit/kien-thai
- https://github.com/chakrit/smoke
- https://github.com/chakrit/lowfat-pantry
- https://github.com/chakrit/fastermail
- https://github.com/chakrit/kue
- https://github.com/chakrit/piper
- https://github.com/chakrit/fact-check
- https://github.com/chakrit/gamctx
- https://github.com/chakrit/gossip
