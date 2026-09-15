# Swift on Apple Silicon — Consolidated Research Digest (2026-09-08 to 2026-09-11)

> Canonical digest consolidating three QA-gated research passes (2026-09-08, 2026-09-10, 2026-09-11-v2) into a single authoritative reference for Swift development on M1 with zero-dep builds, Foundation Models, MCP, MLX serving, and launchd automation.

## TL;DR

- **Swift 6.3.3 (CLT)** is the stable, fast baseline; single-file `swiftc -O` builds remain seconds-fast on M1.
- **Foundation Models** (macOS 26+) expose Apple's ~3B on-device LLM via `LanguageModelSession` + `SystemLanguageModel.availability` probe; 4096-token context window per session (verified via `contextSize` API in 26.4+); `fm` CLI (macOS 27) adds interactive/scripted access without Swift.
- **MCP Swift SDK 0.12.1** (May 2026) is frozen on the 2025-11-25 spec while MCP moved to stateless 2026-07-28 — pin stdio transport, don't expose HTTP.
- **MLX serving** consolidated into three interchangeable OpenAI-compatible endpoints: `mlx-lm` 0.31.3, Ollama MLX (Mar 2026), `mlx-serve` (native Zig) — replace the "embedding MLX in swiftc builds" plan with pointing to `localhost:8080/v1`.
- **Agent packages** (SwiftAgentCore, SwiftAgent) now exist for zero-dep headless loops; Swift Testing (toolchain-bundled, no SwiftPM needed) is ready for dashboard-server coverage.

## Zero-Dep Swift Architecture

### Toolchain & Compilation
- **Swift 6.3.3** (latest as of this digest, released 2026-03-24) is the stable target; ships with built-in `@c` C-interop, Embedded Swift gains, SE-0466 (nonisolated async default for servers), and `swift package show-traits`.
- **Single-file builds**: `swiftc -O file.swift -o tool` remains seconds-fast on M1 (single-core serial stages favor M1 per 2021 measurements; parallel C++ stages would favor more cores, but swiftc stays fast). Avoid SwiftPM + framework dependencies unless HTTP routing/middleware is essential.
- **Framework upgrade path**: If HTTP/routing features become necessary, **Hummingbird 2** (SwiftNIO-based, swift.org-endorsed) is the designated next step — costs SwiftPM + 8+ transitive deps but is lighter than Vapor.
- **Concurrency default**: Keep `nonisolated` for highly-concurrent servers (SE-0466 text explicitly flags MainActor default as wrong for server workloads). Swift 6.0/6.1 Sendable errors were pervasive (forums: hundreds per large project); 6.2+ (approachable concurrency) and 6.3.3 shrink errors dramatically. Use strict Swift 6 mode — it's practical.

### Testing
- **Swift Testing** (`@Test`, `@Suite`, `#expect`, `#require`) ships bundled with Swift 6.3.3 toolchain — zero SwiftPM dependency required.
- **No current coverage** on dashboard-server or MCP tooling (QA gate only checks `bash -n` / file existence).
- **Agent-oriented tooling**: 2026 saw dedicated "AI agent skills" for writing Swift Testing suites; public "Swift Testing Playbook" examples exist aimed at feeding agents. Use this to close the coverage gap without added toolchain complexity.

## Foundation Models: On-Device LLM Access

### API & Availability
- **Framework**: `FoundationModels` (macOS 26+); requires Apple Intelligence enabled and device support (M-series qualifies).
- **Availability probe** (mandatory first step):
  ```swift
  SystemLanguageModel.availability  // returns an AvailabilityReason
  ```
  On macOS 27 and `fm` CLI environments, use: `fm` command with no Swift needed.
- **Classes**: `LanguageModelSession` (streaming), `@Generable` for guided generation, `Tool` protocol for tool-calling, guardrails (`.default`, `.permissiveContentTransformations`) that throw `guardrailViolation`.

### Context Budget & Model Details
- **On-device context**: **4096 tokens per session** (unchanged on OS 27; confirmed via docs, TN3193, InfoQ Mar 2026).
- **Runtime APIs** (macOS 26.4+): `SystemLanguageModel.contextSize` + `tokenCount(for:)` allow runtime context management without hardcoding 4096.
- **Overflow handling**: Exceeding context throws `.exceededContextWindowSize` / `contextSizeExceeded`.
- **Model refresh**: On-device model is **replaced in macOS point updates** (e.g., 26.4 refresh) — re-test prompts after OS updates.
- **Guardrails**: Refined from 26.4 → 27 to reduce false positives.

### Architecture Implications
- **Single-shot / small-schema design** required due to 4096 budget — no multi-turn conversations without external state.
- **PCC (Private Cloud Compute) escape hatch**: macOS 27 added `PrivateCloudComputeLanguageModel` with 32K context + reasoning, free tier covers <2M first-time downloads, higher with iCloud+. This is a cloud path; use only when on-device 4K budget is exhausted.
- **New in OS 27**: Image inputs (Vision OCR/barcode tools callable directly from FM), Dynamic Profiles (swap model/tools/instructions mid-session), `LanguageModel` protocol allowing Claude/Gemini/custom providers (closes the "one model at a time" limitation from 26.x).

### fm CLI & Python SDK
- **`fm` command** (pre-installed macOS 27): `fm chat` (interactive, resumable sessions), `fm respond` (one-shot + `--model pcc` switch + structured output), pipe-into-shell-script usage (e.g., rename files from image content).
- **Python SDK**: `apple-fm-sdk` on PyPI (`pip install apple-fm-sdk`, Apache-2.0, created Feb 2026). Requires macOS 26.0+ / Xcode 26+ / Python 3.10+ / Apple Intelligence. Mirrors Swift features (streaming, tool calling, guided generation via `@fm.generable`).
- **Community wrappers**: `brianwestphal/apple-fm`, `systemsoftware/foundationmodels-cli`, `sohail288/apple-fm-cli` add HTTP-server shapes for eval pipelines and shell integration.
- **Fastest prototyping route**: `fm` CLI for prompts/automations on this Mac without writing Swift; ready-made pattern for cron/headless jobs.

## MCP (Model Context Protocol)

### Swift SDK Status
- **Current**: `modelcontextprotocol/swift-sdk` v0.12.1 (May 7, 2026), still latest on Swift Package Index as of Aug 2026; `main` branch untouched ~4 months.
- **Spec parity**: Implements 2025-11-25 spec (includes `initialize` handshake, `Mcp-Session-Id` header, `Content.text(_:)` API).
- **MCP moved on**: 2026-07-28 final spec went stateless (no initialize, no session headers, cross-call state via explicit "handle" returns). Full JSON Schema 2020-12 for tool schemas. Tier-1 SDKs (Python, TypeScript, Go, C#) shipped day one; Python SDK broke to v2.0.0 (breaking changes); Swift is listed as "requires attention for Apple ecosystem support" — **NOT a Tier-1 SDK**.

### Practical Guidelines
- **Stdio transport only**: Swift MCP servers remain correct on the 2025-11-25 stdio shape. Safe to use today for stdio-based tool servers.
- **HTTP transport forbidden**: Do not expose MCP over HTTP from Swift — stateless 2026-07-28 is unsupported. If an HTTP-exposed MCP endpoint is ever needed, front it with a Tier-1 SDK sidecar (Python/TS/Go proxy).
- **Migration path**: If Swift SDK updates to 0.13.x or later, check release notes for stateless support. Until then, pin 0.12.1 + clear `Content.text(_:)` deprecations (stdio Content now uses `text(text:annotations:_meta:)`; FocusRelay #75 documents the checklist).
- **Verification**: `swift build -c release` + `swift test` on 6.3.3.

## MLX: Local Inference

### Previous Plan (No Longer Valid)
- **Old problem**: MLX Swift's Metal shaders cannot compile from plain swiftc/SwiftPM (needs xcodebuild) — embedding MLX in CLI tools was a dead end.
- **Workaround** (remains valid): Run MLX as a separate OpenAI-compatible HTTP server.

### Current Serving Parity (2026-09 ecosystem)
MLX is no longer a single tool but a **commodity OpenAI-compatible endpoint** with three interchangeable front doors:

1. **mlx-lm** (Python, PyPI):
   - Version: 0.31.3 (`mlx_lm.server`)
   - Install: `uv tool install mlx-lm` or `pip install mlx-lm`
   - Command: `mlx_lm.server --model <mlx-id> --port 8080`
   - API: OpenAI-compatible chat-completions on `127.0.0.1:8080/v1`
   - Default choice for simplicity

2. **Ollama MLX backend** (native, Rust + Zig):
   - Release: Mar 30, 2026 (stable, production-tested)
   - Features: M5 GPU Neural Accelerators support, NVFP4 parity with production, cross-conversation cache reuse, intelligent checkpoints
   - Port: 11434 (drop-in replacement for `ollama` if already in stack)
   - Use if: Raycast / Open WebUI / ollama-client already in use

3. **mlx-serve** (native Zig, one binary):
   - Install: `brew install mlx-serve`
   - Port: 11234 (default) or 11434 (Ollama drop-in)
   - APIs: OpenAI + Anthropic Messages + Ollama formats
   - Extra features: Speculative decoding, KV-cache quantization, menu-bar app
   - Use if: Claude Code or other Anthropic-Messages client needs native support

### Impact on Dashboard
- **No embedded inference**: Swift dashboard-server does NOT embed MLX directly.
- **HTTP-only interface**: Dashboard speaks plain OpenAI chat-completions to `127.0.0.1:8080/v1` (or configurable base URL).
- **Backend swap**: Change MLX backend without touching dashboard code (all three serve the same OpenAI API shape).

### Foundation Models Protocol (New, OS 27)
- **WWDC26 update**: Model choice now behind a `LanguageModel` protocol; Apple ships `MLXLanguageModel` backend that pulls Hugging Face MLX models.
- **Same call sites**: Works the same as `SystemLanguageModel`, meaning a single `LanguageModelSession` API can dispatch to either on-device or MLX models.
- **Status**: Requires verification against WWDC26 docs re: availability from CLT-only (non-Xcode) builds. Not yet independently cross-checked in this digest.

### MLX Core Versions
- MLX core: 0.32.0 (as of July 7, 2026)
- MLX Swift: 0.31.6 (as of July 7, 2026)
- Static Linux SDK: Per-release bundles across 6.3–6.3.3 line; SBOM pins musl 1.2.5 + musl-fts.

## Agent-Oriented Swift Packages

Two zero-dep agent-loop packages emerged in 2026 for headless/server automation:

### SwiftAgentCore (MIT, Swift 5.9+)
- **Dependencies**: Zero external dependencies
- **Platforms**: macOS 13+ / iOS 16+
- **Features**:
  - Unified provider API for OpenAI-compatible / Anthropic / Gemini / MiniMax / Codex-OAuth
  - AsyncStream SSE streaming
  - Tool-calling emulation fallback (for models that don't natively support tools)
  - Safety-level confirmation gates (approval patterns for mutating tools)
  - Multi-directory SkillRegistry
- **Use case**: Provider-agnostic headless loops, launchd cron jobs, approval-gated tool invocation

### SwiftAgent (SwiftedMind, Swift 6)
- **Dependencies**: Foundation-based, FoundationModels-design philosophy
- **Features**:
  - `@Generable` structs as tools
  - Streaming snapshots of partially-generated structured output
  - Proxy-server + HTTP-fixture recording (for testing)
  - Per-turn authorization
- **Use case**: Foundation Models-native tool servers, guided generation workflows

**Confidence note**: Both are aligned with zero-dep dashboard-server ethos. Adoption signal is low (stars tiny, 4★/29 commits), so treat as experimental. Test before production use.

## Launchd & Headless Patterns

### One-Shot Invocation Pattern
- **Rationale**: Dashboard-server remains a zero-dep `swiftc`-built binary; unattended mode uses CLI invocation + scheduling, not a long-running daemon.
- **Implementation**:
  - CLI prompt input → agent loop runs → writes state file → exits
  - Next invocation reads persisted state file
  - launchd plist (or `headless cron`-style state dir) schedules repeats
  - Avoid long-lived in-memory daemon state

### Tool Approval Gates
- **Pattern**: SwiftAgentCore's safety-level confirmation for mutating tools
- **Implementation**: Prompt approval before executing delete/write/network tools; record decision in state file
- **No interactive daemon**: If approval is needed, queue the decision for the next invocation, don't block the current run

### Ecosystem Examples
- **headless-cli** (RobertTLange): One entrypoint over codex/claude/pi/opencode/gemini/acp backends; `--prompt`/`--json`/`--print-command` flags; per-user cron daemon under `~/.headless/cron`
- **Dapr DurableAgent**: Sidecar runtime, state-store persistence, `AgentRunner.serve()` REST + pub/sub, before_tool_call HITL hooks

## Cross-Platform Distribution

### On This Mac (Ad-Hoc Signing)
- `swiftc -O file.swift -o tool` produces a binary
- Ad-hoc-signed binaries run fine on the build Mac; zero friction

### External Distribution (Paid Developer ID)
- **Requirements**: Apple Developer Program (paid), Developer ID certificate, notarization
- **Process**:
  - `codesign --timestamp --options runtime <binary>`
  - `xcrun notarytool submit --wait <binary>`
- **Gotcha**: Standalone binaries cannot be stapled (Error 73) — Gatekeeper phones home on first run
- **Latency**: Apr 2026 forum reports 15+ hour notarization queues; budget for delays

### Static Linux SDK (musl)
- **Install**: `swift sdk install <bundle>` (get bundles from swift.org install pages, per-release across 6.3–6.3.3 + snapshots)
- **Build**: `swift build --swift-sdk aarch64-swift-linux-musl` (or `x86_64-...`)
- **Produces**: Fully static musl binaries from macOS
- **Testing**: Smoke-test per-dependency; musl/SIL compiler bugs exist (e.g., apple/swift-configuration#105)
- **API shim**: Use `canImport(Glibc) / canImport(Musl)` conditionals for C-library-touching deps
- **Network limitation**: Network.framework is Apple-only; macOS server code won't port as-is
- **Status** (2026-09): No discrete musl-breakage reports found for 6.3.x; static-Linux deploy remains routine

## M1 Performance Reality

- **Single-core**: M1 is competitive with large-core-count machines on serial workloads (2021 benchmark: full Swift compiler build 1686s M1 vs 1732s 10-core iMac Pro)
- **Incremental builds (Xcode)**: Feb 2026 forums report regression with macOS 26.4+ (10–70s "Planning/Emit Swift module" for one-line changes; macro-heavy files worst) — but this is Xcode/SwiftPM, not swiftc CLI
- **Single-file swiftc**: Stays seconds-fast, no known regressions
- **Implication**: The zero-dep single-file architecture is accidentally the fastest-compiling option on this machine

### M5 GPU Performance (Not Applicable Here)
- MLX on M5 GPU Neural Accelerators: 3.3–4.06x faster time-to-first-token vs M4 (Apple ML research, Qwen 1.7B–14B, GPT-OSS 20B)
- **This Mac (M1) reality**: Local MLX/Ollama inference is the "cheap, not fast" tier; keep latency-sensitive work on litellm/OpenRouter path

## For This Workspace

### Foundation Models
1. **Probe availability first**: `SystemLanguageModel.availability` (or `fm` if on macOS 27) before any FM feature depends on it
2. **Design around 4K context**: Single-shot architecture, small `@Generable` schemas, token bookkeeping via `contextSize` API (26.4+)
3. **FM availability matrix**: M1 + Apple Intelligence + macOS version decides everything (26.0+ for Python SDK, 26.4+ for `contextSize`, 27 for `fm` CLI)

### MCP
1. **Pin Swift SDK 0.12.1** on stdio transport; clear `Content.text` deprecations via FocusRelay #75 checklist
2. **No HTTP exposure**: If HTTP MCP is ever needed, proxy through a Tier-1 SDK (Python/TS/Go)
3. **CI validation**: `swift build -c release` + `swift test` on 6.3.3

### MLX Serving
1. **Default choice**: `mlx-lm 0.31.3` (`uv tool install mlx-lm` + `mlx_lm.server --port 8080`)
2. **Dashboard code**: OpenAI-compatible `127.0.0.1:8080/v1` with configurable base URL; backend-agnostic
3. **No embedded inference**: Keep MLX out of the Swift binary; serve as separate HTTP endpoint

### Agent Loops & Launchd
1. **One-shot invocation pattern**: CLI prompt → agent loop → exit + state file; launchd/cron schedules repeats
2. **Approval gates**: SwiftAgentCore safety-level pattern for mutating tools; queue approvals for next invocation
3. **Zero-dep binary**: Keep `swiftc` builds standalone; state persists in files, not in-memory daemon
4. **Test coverage**: Use Swift Testing (bundled, no SwiftPM); agent-oriented skills exist for writing test suites

### Distribution
1. **Local**: Ad-hoc signing, zero friction
2. **External**: Budget for Developer ID cert + notarization latency (15+ hours reported)
3. **Linux**: Static Linux SDK musl builds; test per-dependency

## Sources

### Swift Toolchain & Architecture
- 2026-09-08 digest: Swift 6.3 release notes, SwiftNIO server docs, Hacking with Swift, Swift Forums migration threads, compile-time benchmarks
- 2026-09-10 digest: swift.org "What's New in Swift — August 2026", GitHub Spec Kit placement
- 2026-09-11-v2 digest: swift.org install pages (Static Linux SDK bundles), Swift.org serverless/microservices positioning

### Foundation Models
- 2026-09-08 digest: Apple docs, Apple newsroom
- 2026-09-10 digest: Medium article on MLXLanguageModel protocol (single source, needs WWDC verification)
- 2026-09-11-v2 digest: WWDC26 sessions (#334 fm CLI, #241 Python SDK), Apple docs (contextSize, tokenCount, TN3193), InfoQ Mar 2026, macOS 27 community verification of context budget unchanged

### MCP Protocol & SDK
- 2026-09-08 digest: GitHub, Swift Package Index, MCP blog, SDK WG notes
- 2026-09-10 digest: MCP blog (2026-07-28 spec), MCP spec migrations, Swift Forums (MCP SDK deprecations)
- 2026-09-11-v2 digest: Swift Package Index (0.12.1 latest, May 7 2026), MCP blog (SDK betas), PyPI (Python SDK versions), FocusRelay #75 (Swift 6.3.3 migration checklist)

### MLX & Local Inference
- 2026-09-08 digest: mlx-swift README, WWDC26 transcripts, Hugging Face blog, examples
- 2026-09-10 digest: Apple ML research (M5 GPU Neural Accelerators benchmark, machinelearning.apple.com)
- 2026-09-11-v2 digest: mlx-lm PyPI, Ollama MLX blog (Mar 30 2026), mlx-serve API docs (OpenAI + Anthropic APIs), mlx-openai-server (model types, reasoning parser), Hugging Face model pages

### Agent Packages & Testing
- 2026-09-10 digest: GitHub (SwiftAgentCore, SwiftedMind/SwiftAgent), Swift Testing avanderlee.com, public Swift Testing Playbook gist
- 2026-09-11-v2 digest: SwiftAgentCore/SwiftAgent READMEs, headless-cli, Dapr DurableAgent patterns

### Distribution & Signing
- 2026-09-08 digest: Apple notarization docs, akrabat.com, ddev/signing_tools, Apple Forums (notarization queue latency)
- 2026-09-11-v2 digest: swift.org install pages, musl SBOM (1.2.5 + musl-fts), May 2026 nondeterminism report, musl-import shim pattern (canImport Glibc/Musl)
