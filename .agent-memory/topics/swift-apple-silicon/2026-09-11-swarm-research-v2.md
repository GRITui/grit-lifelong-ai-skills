# swift-apple-silicon v2 — Swarm Research (2026-09-11)

> ✅ QA-gated by PO 2026-09-11 · machine+API spot-checks: swiftc 6.3.3/arm64 ✓, MCP swift-sdk latest=0.12.1 ✓, local macOS 26.2 (→ macOS-27 items noted future-gated) ✓

## TL;DR (≤5 bullets) — NEW angles only, nothing repeating the v1 file
- **fm CLI + Python SDK are the new FM on-ramps:** macOS 27 ships a pre-installed `fm` command (`fm chat`, `fm respond --model pcc`) and Apple published `apple-fm-sdk` on PyPI (`pip install apple-fm-sdk`, 1.2k★) — shell scripts and Python eval harnesses no longer need Swift/Xcode just to poke the on-device model.
- **Hard FM budget numbers confirmed:** on-device context window is **4096 tokens/session** (unchanged on OS 27; verify at runtime via `SystemLanguageModel.contextSize` + `tokenCount(for:)` from OS 26.4), PCC server model gives **32K + reasoning** free under 2M first-time downloads; OS 27 adds vision inputs, Dynamic Profiles, and a `LanguageModel` protocol for any provider.
- **Swift MCP SDK is frozen while the spec moved on:** SPI still shows **0.12.1 (May 2026)** as latest with `main` untouched ~4 months; all four Tier-1 SDKs (TS/Python/Go/C#) speak the stateless **2026-07-28** spec, Swift is explicitly flagged "requires attention" — pin stdio + `Content.text(text:annotations:_meta:)` and do not chase the stateless HTTP core in Swift yet.
- **MLX serving grew three interchangeable front doors:** `mlx-lm` 0.31.3 (`mlx_lm.server`), **Ollama-on-MLX preview** (Mar 2026, NVFP4, shared-prefix cache), and native-Zig **mlx-serve** (one binary, OpenAI+Anthropic+Ollama APIs) — any OpenAI/Anthropic/Ollama client (Pi, OpenClaw, Claude Code) can point at localhost unchanged.
- **Zero-dep Swift agent runtimes now exist as packages:** SwiftAgentCore (no external deps, multi-provider, streaming-first, tool fallback, skills) and SwiftAgent (FoundationModels-design philosophy, `@Generable` tools) give the dashboard-server a headless loop without inventing one; Static Linux SDK line stays on musl with per-release 6.3.x bundles.

## Findings (5-8, each What / Why it matters / Confidence high|med|low)

1. **What:** WWDC26 introduced the `fm` CLI (pre-installed, macOS 27) with `fm chat` (interactive, resumable sessions), `fm respond` (one-shot + `--model pcc` switch + structured output), and pipe-into-shell-script usage (e.g. rename files from image content). Companion session "Build AI-powered scripts with the fm CLI and Python SDK" demos eval pipelines.
   **Why it matters:** Fastest way to prototype FM prompts/automations on this Mac without writing Swift — and a ready-made pattern for cron/headless jobs that shell out to the on-device model instead of embedding it.
   **Confidence:** high

2. **What:** Apple open-sourced the Foundation Models SDK for Python (`github.com/apple/python-apple-fm-sdk`, Apache-2.0, created Feb 2026): `pip install apple-fm-sdk`, requires macOS 26.0+ / Xcode 26+ / Python 3.10+ / Apple Intelligence on; mirrors Swift features (streaming, tool calling, guided generation via `@fm.generable`, `SystemLanguageModel().is_available()`). Community wrappers (`brianwestphal/apple-fm`, `systemsoftware/foundationmodels-cli`, `sohail288/apple-fm-cli`) add CLI + local HTTP server shapes.
   **Why it matters:** Python eval/batch harness for Swift FM app features is now first-party; community HTTP-server wrappers preview what an FM-backed dashboard route could look like, but they need Apple-Intelligence hardware (M1 qualifies, OS version gates apply).
   **Confidence:** high

3. **What:** Concrete FM budgets: on-device = 4096 tokens/session (docs + TN3193 + InfoQ Mar 2026; OS 27 community verification says unchanged, larger-context claims refer to PCC only). OS 26.4 added `contextSize` + `tokenCount(for:)` (back-deployed) so code need not hardcode 4096; overflow throws `.exceededContextWindowSize` / `contextSizeExceeded`. Guardrails refined in 26.4 → 27 to cut false positives. OS 27 adds: rebuilt on-device model, image inputs (Vision OCR/barcode tools callable), Dynamic Profiles (swap model/tools/instructions mid-session), `LanguageModel` protocol (Claude/Gemini/custom providers), PCC `PrivateCloudComputeLanguageModel` 32K + reasoning, no keys, free <2M first-time downloads (higher with iCloud+).
   **Why it matters:** 4096 forces single-shot/small-schema design and token bookkeeping per session; PCC is the escape hatch for bigger context but is a cloud path with download-tier pricing — affects whether the dashboard-server stays pure on-device.
   **Confidence:** high (budgets/APIs from Apple docs; pricing from WWDC26 session excerpt — med on exact current tier terms)

4. **What:** MCP Swift SDK status: 0.12.1 (May 7, 2026) still latest on SPI (Aug 2026 snapshot; `main` modified ~4 months ago); 0.12.0→0.12.1 was OAuth/HTTP-transport/server-internals + `Content.text(_:)` → `text(text:annotations:_meta:)` deprecation (FocusRelay #75 documents the migration on Swift 6.3.3). Meanwhile MCP 2026-07-28 final (Jul 28, 2026): stateless core (no initialize handshake/session), full JSON Schema 2020-12 for tool schemas (oneOf/anyOf/$ref), Tier-1 SDKs shipped day one; Python SDK went v2 (`mcp` 2.0.0 Jul 28 → 2.1.1 Aug 25, breaking). Swift is non-tier-1, listed as "requires attention for Apple ecosystem support."
   **Why it matters:** Swift MCP servers remain correct on the **stdio** transport against the 2025-11-25 shape, but cannot speak stateless-HTTP 2026-07-28; any HTTP-exposed MCP surface should go through a Tier-1 SDK sidecar/proxy, not the Swift SDK.
   **Confidence:** high (versions/dates from SPI + MCP blog + PyPI; "frozen" inferred from 4-month main inactivity — med)

5. **What:** MLX serving parity: `mlx-lm` 0.31.3 on PyPI (`mlx_lm.server --model <id> --port 8080`, OpenAI-compatible); Ollama MLX preview (Mar 30, 2026 blog: MLX backend on Apple Silicon, M5 GPU Neural Accelerators, NVFP4 parity with production, cross-conversation cache reuse + intelligent checkpoints); `mlx-serve` (native Zig, `brew install mlx-serve`, port 11234 default / 11434 Ollama drop-in, OpenAI + Anthropic Messages + Ollama APIs, speculative decoding, KV-cache quant, menu-bar app); `mlx-openai-server` 1.8.1 (model types lm/multimodal/image/embeddings/whisper, `--reasoning-parser`/`--tool-call-parser` flags). HF model pages now print `mlx_lm.server` + Pi/OpenClaw wiring verbatim.
   **Why it matters:** The "MLX server route" is no longer one tool but a commodity OpenAI-compatible endpoint — the Swift dashboard-server can treat local LLM as HTTP (`localhost:8080/v1` or `:11434`) and swap backends without code changes.
   **Confidence:** high (mlx-lm version + Ollama blog + mlx-serve API docs; perf claims like "35%+ faster than LM Studio" are vendor-reported — low)

6. **What:** Swift-native agent-loop packages appeared in 2026: **SwiftAgentCore** (MIT, Swift 5.9+, macOS 13+/iOS 16+, zero external deps; unified OpenAI-compatible/Responses + Anthropic + Gemini + MiniMax + Codex-OAuth providers; AsyncStream SSE streaming; tool-calling emulation fallback; safety-level confirmation gates; multi-dir SkillRegistry) and **SwiftedMind/SwiftAgent** (Swift 6, FoundationModels-design API, `@Generable` structs as tools, streaming snapshots incl. partially-generated structured output, proxy-server + HTTP-fixture recording, per-turn authorization).
   **Why it matters:** Both are closer to this workspace's zero-dep dashboard-server ethos than pulling a Python agent framework — SwiftAgentCore for provider-agnostic headless loops, SwiftAgent where FM-style guided generation is the interface.
   **Confidence:** med (feature lists from READMEs; no independent adoption/QA signal — stars tiny, 4★/29 commits)

7. **What:** Headless/cron patterns converged: `headless-cli` (one entrypoint over codex/claude/pi/opencode/gemini/acp backends, `--prompt/--json/--print-command`, per-user cron daemon under `~/.headless/cron`) and Dapr's DurableAgent "headless agents" pattern (sidecar runtime, state-store persistence, `AgentRunner.serve()` REST + pub/sub, before_tool_call HITL hooks). Swift server side: Swift.org positions Swift (fast cold start, low memory) for serverless/microservices; `swift-aws-lambda-runtime` tutorial path exists.
   **Why it matters:** Template for the dashboard-server's unattended mode: CLI-invoked one-shot runs + launchd/cron scheduling + approval-gated tools, rather than a bespoke scheduler.
   **Confidence:** med

8. **What:** Static Linux SDK (musl) status: Swift.org install pages ship per-release Static SDK bundles across the 6.3–6.3.3 line plus `main`/`release/6.4.x` snapshots; SBOM pins musl 1.2.5 + musl-fts; documented porting shim is `canImport(Glibc)/canImport(Musl)` with `swift build --swift-sdk x86_64|aarch64-swift-linux-musl`. One known 2026 papercut: bundle-ID + explicit `--triple` selection nondeterminism (May 2026 report).
   **Why it matters:** No musl-breakage news found for 6.3.x — static-Linux deploy of a server stays routine; only C-library-touching deps need the Musl import shim, and SDK selection should use the plain triple form.
   **Confidence:** low (absence-of-news + install-page listings; no discrete "musl fix" release located)

## For This Workspace (2-4 concrete items for: macOS M1/6.3.3 zero-dep Swift dashboard-server, Foundation Models availability, MCP Swift SDK, MLX server route, launchd services)
- **FM availability gate first:** M1 + Apple Intelligence + OS version decides everything — `fm` CLI needs macOS 27, Python SDK needs 26.0+/Xcode 26+, `contextSize`/`tokenCount` need 26.4+. Before writing any FM code, probe `SystemLanguageModel().is_available()` (or `fm` if on 27) and record the measured `contextSize`; keep 4096 as fallback constant, never as hardcoded assumption. Design FM features single-shot with small `@Generable` schemas against the 4096 budget; reserve PCC (32K) for a later, explicitly-cloud step.
- **MCP: pin Swift SDK 0.12.1 on stdio, migrate `Content.text`:** set the dependency floor to 0.12.1, clear the `text(text:annotations:_meta:)` deprecations, verify with `swift build -c release` + `swift test` on 6.3.3 (FocusRelay #75 checklist pattern). Do not expose MCP over HTTP from Swift (stateless 2026-07-28 unsupported); if an HTTP MCP endpoint is ever needed, front it with a Tier-1 (Python/TS) proxy.
- **MLX route = OpenAI-compatible localhost, three options:** default `uv tool install mlx-lm` + `mlx_lm.server --model <mlx-id> --port 8080` (0.31.3); alternative Ollama MLX build on `:11434` for Raycast/Open WebUI/ollama-client compat; `mlx-serve` only if Anthropic-Messages compat (Claude Code drop-in) is needed. Dashboard-server speaks plain OpenAI chat-completions to `127.0.0.1:8080/v1` with a swappable base URL — no embedded inference, no Python in the Swift binary.
- **launchd + headless discipline:** one-shot invocations (CLI prompt → run → exit) scheduled via launchd plist (or `headless cron`-style state dir if a second scheduler is ever wanted — not both); keep the dashboard-server binary zero-dep `swiftc`-built, put tool-approval gates (SwiftAgentCore safety-level pattern) on any mutating tool, and persist run state in files the next invocation re-reads rather than a daemon held in memory.

## Sources (URLs one per line)
https://developer.apple.com/videos/play/wwdc2026/334
https://developer.apple.com/videos/play/wwdc2026/241
https://developer.apple.com/documentation/foundationmodels
https://developer.apple.com/documentation/Updates/FoundationModels
https://developer.apple.com/documentation/foundationmodels/managing-the-context-window
https://developer.apple.com/documentation/technotes/tn3193-managing-the-on-device-foundation-model-s-context-window
https://github.com/apple/python-apple-fm-sdk
https://github.com/brianwestphal/apple-fm
https://github.com/systemsoftware/foundationmodels-cli
https://swiftpackageindex.com/modelcontextprotocol/swift-sdk
https://blog.modelcontextprotocol.io/posts/sdk-betas-2026-07-28
https://pypi.org/project/mcp/2.1.1
https://github.com/deverman/FocusRelayMCP/issues/75
https://pypi.org/project/mlx-lm
https://ollama.com/blog/mlx
https://mlxserve.com/api
https://github.com/ml-explore/mlx/discussions/3796
https://pypi.org/project/mlx-openai-server
https://github.com/herrkaefer/SwiftAgentCore
https://github.com/SwiftedMind/SwiftAgent
https://github.com/RobertTLange/headless-cli
https://www.swift.org/documentation/articles/static-linux-getting-started.html
https://www.swift.org/install/linux/ubuntu/24_04
https://www.infoq.com/news/2026/03/apple-foundation-models-context
https://www.swift.org/blog/whats-new-in-swift-march-2026/
