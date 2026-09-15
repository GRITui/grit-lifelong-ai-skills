# Swift on Apple Silicon — Swarm Research (2026-09-08)

> ✅ QA-gated by PO 2026-09-08 · 40 sources verified present · spot-check: FoundationModels framework confirmed via Apple docs (LanguageModelSession/@Generable/Tool/SystemLanguageModel all live) ✓ · merged from swarm inbox

# swift-apple-silicon — Swarm Research Draft (2026-09-08)

## TL;DR
- Swift 6.3 (Mar 2026; 6.3.3 current) is mature for CLT-only, zero-dep agent servers; approachable-concurrency defaults (Swift 6.2+) make strict mode practical, and the server-side default should stay `nonisolated`.
- Foundation Models framework (macOS 26+) exposes Apple's ~3B on-device LLM with guided generation, tools, and guardrails; model changes with OS point updates (26.4) — prompts need retesting.
- Official MCP Swift SDK is at 0.12.1 (Swift 6, zero data-race errors) but implements the 2025-11-25 spec while MCP moved to a stateless 2026-07-28 spec — it lags.
- MLX Swift can't build Metal shaders from plain SwiftPM/CLT (needs xcodebuild) — for this Mac, run MLX as the separate `mlx-lm` OpenAI-compatible server instead of embedding it.
- swiftc single-file distribution is trivial locally; only cross-Machine distribution needs paid Developer ID signing + notarization (single binaries can't be stapled).

## Findings
1. **What:** Swift 6.3 shipped 2026-03-24: Swift Build integrated into SwiftPM as opt-in preview, stable Android SDK, `@c` C-interop, Embedded Swift gains, `swift package show-traits`; SE-0526 `withDeadline` accepted July 2026. Current patch 6.3.3.
   **Why it matters:** Confirms the CLT 6.3.3 toolchain is current and SwiftPM build-system overhaul is real, not vaporware.
   **Confidence: high** (swift.org blog)
2. **What:** Swift 6.2+ "Approachable Concurrency": SE-0466 `-default-isolation MainActor`, SE-0461 nonisolated async runs on caller's actor, `@concurrent` escape hatch. SE-0466's own text says MainActor default is wrong for "highly-concurrent server applications".
   **Why it matters:** For the NWListener dashboard, keep `nonisolated` default; strict Swift 6 mode errors shrink dramatically vs 6.0/6.1 reports (forums: hundreds of Sendable errors, "sprinkle @MainActor" workarounds).
   **Confidence: high** (SE-0466 text, Hacking with Swift, Swift Forums migration threads)
3. **What:** Foundation Models (macOS 26+, Apple Intelligence-enabled M-series): `LanguageModelSession`, `@Generable` guided generation, `Tool` protocol, guardrails (`.default`, `.permissiveContentTransformations`) that throw `guardrailViolation`; must check `SystemLanguageModel.availability` (device/region/language gates). On-device model ≈3B params (Apple newsroom). Model replaced in macOS 26.4 — Apple says re-test prompts. macOS 26.4/27 add image input, PCC server model, third-party `LanguageModel` providers (Core AI, MLX).
   **Why it matters:** A free, private, zero-token-cost local LLM callable from pure Swift — realistic fallback brain for local agents.
   **Confidence: high** (Apple docs, Apple newsroom)
4. **What:** Official MCP Swift SDK (modelcontextprotocol/swift-sdk): v0.12.1 (≈Apr 2026), Swift 6.0+, macOS 13+, Linux glibc/musl, SPI reports "zero data race safety errors", 1.4k stars; new maintainers (Stephen Tallent, Jan 2026) targeting Tier 2. Implements 2025-11-25 spec; MCP spec moved to stateless 2026-07-28 (no handshake, MRTR, header routing).
   **Why it matters:** Viable for stdio MCP servers from Swift today, but protocol-freshness gap means avoid HTTP-transport features that shifted in the new spec.
   **Confidence: high** (GitHub README, Swift Package Index, MCP blog, SDK WG notes); spec-lag inference: **med**
5. **What:** Server frameworks: Vapor (~24k stars) and Hummingbird 2 both sit on SwiftNIO; swift.org documents both as production-adopted; 2026 Reddit reports of Hummingbird 2 in production >1 year; comparisons favor Hummingbird for Apple-endorsed momentum/lighter footprint.
   **Why it matters:** If the zero-dep NWListener server ever needs HTTP/routing/middleware, Hummingbird 2 is the lowest-friction upgrade; both are dependency-ful though.
   **Confidence: high** (swift.org server docs, Vapor site); Hummingbird preference: **med** (comparisons/blog)
6. **What:** Static Linux SDK: `swift sdk install swift-6.3.3-...static-linux-0.1.0.artifactbundle.tar.gz`, then `swift build --swift-sdk x86_64-swift-linux-musl` (or aarch64) fully static musl binaries from macOS; SDK bundle is large (~147MB); some packages hit musl/SIL compiler bugs (e.g. apple/swift-configuration#105).
   **Why it matters:** Cheap path to statically deploy agents on Linux boxes/Docker without a Linux toolchain — but test per-package; NWListener (Network.framework) is Apple-only so macOS-only code won't port as-is.
   **Confidence: high** (swift.org getting-started); musl breakage breadth: **med** (single issue); Network.framework non-availability on Linux: **med** (unsourced in this pass)
7. **What:** MLX Swift (ml-explore, ~2k stars, MIT) + mlx-swift-examples (MLXLLM/MLXVLM) + mlx-swift-lm; README: "SwiftPM (command line) cannot build the Metal shaders so the ultimate build has to be done via Xcode/xcodebuild". WWDC26: `mlx-lm` ships an OpenAI-compatible HTTP server for local agents; MLX gains Metal 4, Neural Accelerators (M5), distributed inference across Macs (RDMA over Thunderbolt). swift-transformers hit 1.0 (Sep 2025: Tokenizers + Hub modules, used by WhisperKit/MLX examples). New "Core AI" OS framework (WWDC26) runs your own models on-device with AOT specialization.
   **Why it matters:** On this CLT-only Mac, embedding MLX in swiftc-built tools is a dead end; the server route (mlx-lm or Ollama/LM Studio) fits the existing Docker/AI-stack pattern.
   **Confidence: high** (mlx-swift README, WWDC26 transcripts, HF blog); Core AI details: **high** (Apple)
8. **What:** swiftc distribution & signing: `swiftc -O file.swift -o tool` is a proven pattern (e.g. cscheck); ad-hoc-signed binaries run fine on the build Mac. Distributing to other Macs requires paid Developer ID cert + `codesign --timestamp --options runtime` + `xcrun notarytool submit --wait`; standalone binaries cannot be stapled (Error 73) — Gatekeeper phones home on first run. One Apr 2026 forum report of 15+ h notarization queues.
   **Why it matters:** Personal tools on this Mac: zero signing friction. Anything shared externally: budget for Apple Developer Program + notarization latency.
   **Confidence: high** (Apple notarization docs, akrabat.com, ddev/signing_tools); delay anecdote: **low**
9. **What:** Compile-time reality: M1 wins on single-core/serial stages (2021 measurement: full Swift-compiler build 1686s on M1 16GB vs 1732s on 10-core iMac Pro; parallel C++ stages favor more cores). Feb 2026 forums: Xcode 26.4 large-app incremental builds regress badly (10–70s "Planning/Emit Swift module" for one-line changes; macro-heavy files worst). Single-file `swiftc` compiles stay seconds-fast.
   **Why it matters:** The zero-dep single-file dashboard architecture is accidentally the fastest-compiling Swift architecture on this machine.
   **Confidence: med** (dated M1 benchmark; large-app Xcode anecdotes, not CLT/swiftc measurements)

## For This Workspace
1. **Keep the dashboard-server zero-dep.** Single-file `swiftc -O` + NWListener is both the fastest-building and dependency-risk-free option on CLT 6.3.3; if HTTP features are ever needed, Hummingbird 2 (SwiftNIO) is the designated upgrade path — but requires SwiftPM + 8+ transitive deps.
2. **Bridge the on-device LLM via endpoint, not embedding.** MLX can't compile from CLT builds, and Foundation Models needs macOS 26 + Apple Intelligence enabled: verify with a 3-line `SystemLanguageModel.availability` probe, or use `apfel`/`maclocal-api`-style wrappers that expose an OpenAI-compatible endpoint — slot it into the existing litellm :4000 router as a `local-free` model tier.
3. **MCP only over stdio.** If the dashboard or watchdog ever needs to be an MCP tool source, the official Swift SDK 0.12.1 is solid (zero data-race errors, Swift 6) — but pin stdio transport and the 2025-11-25 feature set; don't adopt new-spec HTTP semantics yet.
4. **Linux watchdog builds via Static Linux SDK, not Termux.** For any Linux-side agent companion, `swift build --swift-sdk aarch64-swift-linux-musl` gives one static binary; compile it on this Mac and smoke-test per-dep (musl bugs exist). The Swift 6.3 Android SDK is real but too bleeding-edge for the Termux pad — keep Termux on its current stack.

## Sources
- https://www.swift.org/blog/swift-6.3-released (swift.org)
- https://www.swift.org/blog/whats-new-in-swift-march-2026/ (swift.org)
- https://www.swift.org/blog/whats-new-in-swift-july-2026/ (swift.org)
- https://github.com/swiftlang/swift-evolution/blob/main/proposals/0466-control-default-actor-isolation.md (GitHub)
- https://www.hackingwithswift.com/articles/277/whats-new-in-swift-6-2 (Hacking with Swift)
- https://blakecrosley.com/blog/swift-6-2-concurrency-in-practice (Blake Crosley)
- https://forums.swift.org/t/my-experience-attempting-a-migration-to-swift-6/79069 (Swift Forums)
- https://www.swift.org/migration/documentation/swift-6-concurrency-migration-guide/migrationstrategy (swift.org)
- https://developer.apple.com/documentation/foundationmodels (Apple)
- https://developer.apple.com/documentation/foundationmodels/improving-the-safety-of-generative-model-output (Apple)
- https://developer.apple.com/documentation/foundationmodels/systemlanguagemodel (Apple)
- https://developer.apple.com/documentation/Updates/FoundationModels (Apple)
- https://www.apple.com/newsroom/2025/09/apples-foundation-models-framework-unlocks-new-intelligent-app-experiences/ (Apple)
- https://developer.apple.com/videos/play/wwdc2026/334/ (Apple, fm CLI + Python SDK)
- https://developer.apple.com/videos/play/wwdc2026/232/ (Apple, MLX agentic AI)
- https://developer.apple.com/videos/play/wwdc2026/233/ (Apple, MLX distributed)
- https://developer.apple.com/macos/whats-new/ (Apple, Core AI)
- https://github.com/modelcontextprotocol/swift-sdk (GitHub)
- https://swiftpackageindex.com/modelcontextprotocol/swift-sdk (Swift Package Index)
- https://github.com/modelcontextprotocol/modelcontextprotocol/issues/2144 (GitHub, SDK WG)
- https://blog.modelcontextprotocol.io/posts/2026-07-28/ (MCP blog)
- https://www.swift.org/documentation/server (swift.org)
- https://www.reddit.com/r/swift/comments/1slk84s/building_your_backend_in_swift_as_an_ios_dev (Reddit)
- https://muhittincamdali.com/en/comparisons/vapor-vs-hummingbird (Muhittin Çamdalı)
- https://www.swift.org/documentation/articles/static-linux-getting-started.html (swift.org)
- https://github.com/apple/swift-configuration/issues/105 (GitHub, musl bug)
- https://forums.swift.org/t/build-helloworld-with-static-linux-sdk-on-macos/82906 (Swift Forums)
- https://github.com/ml-explore/mlx-swift (GitHub)
- https://github.com/ml-explore/mlx-swift-examples (GitHub)
- https://huggingface.co/blog/swift-transformers (Hugging Face)
- https://github.com/huggingface/swift-transformers (GitHub)
- https://github.com/presswizards/apfel-Apple-Native-LLM (GitHub)
- https://github.com/scouzi1966/maclocal-api (GitHub)
- https://github.com/tk3fftk/foundation-model-cli (GitHub)
- https://akrabat.com/notarising-a-macos-standalone-binary (akrabat.com)
- https://developer.apple.com/documentation/security/notarizing_your_app_before_distribution (Apple)
- https://github.com/ddev/signing_tools (GitHub)
- https://developer.apple.com/forums/thread/822109 (Apple Forums)
- https://forums.swift.org/t/build-time-measurements-imac-pro-2017-vs-m1-macbook-pro-2020/47672 (Swift Forums)
- https://forums.swift.org/t/slow-incremental-builds-because-of-planning-swift-module/84803 (Swift Forums)
- https://github.com/luckman212/cscheck (GitHub)
