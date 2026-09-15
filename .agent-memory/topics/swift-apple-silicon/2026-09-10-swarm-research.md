# Swift on Apple Silicon — Swarm Research (2026-09-10)

> ✅ QA-gated by PO 2026-09-10 · spot-check: Swift Testing (`import Testing`) parses with plain swiftc, no SwiftPM package needed → hypo-test exit 0 ✓

## TL;DR
- WWDC26 made Foundation Models model-agnostic: a new `LanguageModel` protocol + `MLXLanguageModel` backend now let Swift apps run any Hugging Face MLX model (not just Apple's on-device model) through the same API — closes the "MLX can't embed in CLT builds" gap by putting MLX behind the *same* framework instead.
- MLX core hit v0.32.0 and MLX Swift hit 0.31.6 (both 2026-07-07); Ollama 0.19 (2026-03-30) shipped a native MLX backend, giving a third local-server option beyond `mlx-lm`/LM Studio.
- The MCP 2026-07-28 spec (already flagged as "not yet in the Swift SDK" on 2026-09-08) is now confirmed to delete `initialize`/`Mcp-Session-Id` entirely in favor of per-request `_meta` fields, and formally deprecates Roots/Sampling/Logging (12-month removal window) — no Swift SDK release news found yet, so the lag is now more consequential, not less.
- Swift.org's "What's New in Swift — August 2026" post exists (no MCP/MLX content found in it during this pass, but it's the next toolchain-status checkpoint after the 6.3.3/July digest already on file).
- Swift Testing (bundled with Swift 6 toolchain, no SwiftPM dependency needed) is gaining AI-agent-oriented tooling in 2026 (agent skills for writing `@Test`/`@Suite`/`#expect` tests) — relevant since this workspace already builds agent tooling and has zero test coverage on the dashboard server.

## Findings
1. **What:** WWDC26 Foundation Models update: model choice is now behind a `LanguageModel` protocol, and Apple ships `MLXLanguageModel` as a built-in backend that pulls open-source models from Hugging Face's MLX community and runs them via Swift's GPU/Neural Engine path — same call sites as `SystemLanguageModel`.
   **Why it matters:** Previously this workspace's plan was "Foundation Models for Apple's on-device model, separate mlx-lm HTTP server for anything else." This narrows that gap — worth re-checking macOS version/availability requirements before assuming it's usable from a CLT-only (non-Xcode) build.
   **Confidence: med** (single Medium article, not yet cross-checked against Apple docs/WWDC session transcript)
2. **What:** MLX core reached v0.32.0 and MLX Swift reached 0.31.6, both dated 2026-07-07 (same release week). Ollama 0.19 (2026-03-30) added a native MLX backend for Apple Silicon.
   **Why it matters:** Version-pins worth using if/when this Mac stands up an MLX-based local model server; Ollama+MLX backend is a lower-friction alternative to hand-rolling `mlx-lm` if Ollama is already in the stack (litellm router).
   **Confidence: med** (aggregator blog post, not swift-mlx/ollama release notes directly)
3. **What:** M5 GPU Neural Accelerators benchmark (Apple ML research): 3.3x–4.06x faster time-to-first-token vs M4 across Qwen 1.7B–14B and GPT-OSS 20B, per Apple's own published numbers.
   **Why it matters:** Not directly actionable on this M1 Mac, but sets expectation: MLX perf gains going forward are increasingly M5-specific (Neural Accelerator silicon), so M1 local-inference speed is a fixed ceiling — favor the existing server-based (not on-device) LLM tier for anything latency-sensitive.
   **Confidence: high** (Apple Machine Learning Research blog, machinelearning.apple.com)
4. **What:** MCP spec 2026-07-28 confirmed details beyond what the last digest captured: no `initialize` handshake, no `Mcp-Session-Id` header, cross-call state must be carried explicitly as a returned "handle" argument; Roots, Sampling, and Logging are formally deprecated with a 12-month removal clock; TypeScript/Python/Go/C# SDKs already updated. No mention of an updated Swift SDK in this search pass.
   **Why it matters:** Confirms the 2025-09-08 digest's "spec-lag" flag was correct and the lag is now spec-vs-SDK, not just spec-vs-spec — if this workspace ever needs HTTP-transport MCP (not stdio), the official Swift SDK is likely still on the old handshake model. Re-check swift-sdk releases before building anything HTTP-based.
   **Confidence: high** for spec content (modelcontextprotocol.io blog, Appwrite/Cloudflare corroboration); **low** for "Swift SDK still lagging" (absence of evidence, not evidence of absence — didn't check GitHub releases directly this pass)
5. **What:** swift.org published "What's New in Swift — August 2026" as the next monthly digest after the July one already cited in the 2026-09-08 research.
   **Why it matters:** Marks the next toolchain checkpoint to check for CLT/swiftc-relevant changes (build-system, concurrency, packaging) beyond 6.3.3 — not yet read in depth this pass, flagged for a future research cycle.
   **Confidence: low** (title/existence only, content not fetched)
6. **What:** Swift Testing (the `@Test`/`@Suite`/`#expect`/`#require` framework) ships with the Swift 6 toolchain and needs no SwiftPM dependency to use — confirmed still true in 2026, and 2026 is seeing dedicated "AI agent skills" built specifically to write Swift Testing suites (e.g. a GitHub issue tracking an agent skill for this, and a public "Swift Testing Playbook" gist explicitly aimed at feeding agents).
   **Why it matters:** Zero-dependency test coverage is achievable on this CLT-only Mac today with no new tooling — directly fills a gap (the dashboard server and MCP tooling currently have no automated tests per the QA-gate table in CLAUDE.md, which only checks `bash -n`/existence, not correctness).
   **Confidence: high** for framework being toolchain-bundled (github.com/swiftlang/swift-testing, avanderlee.com); **med** for "actively growing agent-tooling ecosystem" claim (anecdotal GitHub issue/gist, not a maintainer announcement)
7. **What:** Embedded Swift is described in 2026 sources as still in early/experimental stages for some targets (e.g. WebAssembly compilation for tiny web UI binaries), separate from the more mature embedded-microcontroller use case already noted in the 6.3 release notes on file.
   **Why it matters:** Not directly relevant to this Mac's server/dashboard/MCP tooling today, but flags that Embedded Swift's WASM path is not yet a turnkey option if this workspace ever wants a browser-side Swift component.
   **Confidence: low** (single course/tutorial-site source, not swift.org or swift-evolution)

## For This Workspace
1. **Before building any HTTP-transport MCP server in Swift, check `github.com/modelcontextprotocol/swift-sdk` releases directly** — this pass found strong spec-side confirmation of the 2026-07-28 stateless changes but no confirmation the Swift SDK has caught up; don't assume parity with the TS/Python/Go/C# SDKs.
2. **Re-verify Foundation Models' new `LanguageModel`/`MLXLanguageModel` protocol against Apple's actual WWDC26 session doc (not just the Medium summary) before relying on it** — if it holds up, it may let this Mac call open-source MLX models through the same `LanguageModelSession` API already planned for Apple's on-device model, simplifying the litellm `local-free` tier design noted in the 2026-09-08 digest.
3. **Add a Swift Testing suite for the dashboard-server / MCP tooling** — it's zero-dependency (bundled in the toolchain, no SwiftPM package needed), directly strengthens the QA gate beyond `bash -n`/file-existence checks, and fits the "single-file swiftc" pattern this workspace already favors.
4. **Pin MLX version expectations to M1 reality, not M5 marketing** — the 3–4x M5 Neural Accelerator gains (Qwen/GPT-OSS benchmarks) don't apply to this machine; keep treating local MLX/Ollama inference as the "cheap, not fast" tier and route latency-sensitive work through the existing litellm/OpenRouter path.

## Sources
https://www.swift.org/blog/swift-6.3-released/
https://www.swift.org/blog/whats-new-in-swift-august-2026/
https://medium.com/@nuthalapativarun/mlx-is-now-a-first-class-citizen-in-apples-ai-stack-run-any-hugging-face-model-through-foundation-9dfb8dad2191
https://machinelearning.apple.com/research/exploring-llms-mlx-m5
https://www.digitalapplied.com/blog/apple-mlx-framework-local-ai-developers-2026-guide
https://blog.modelcontextprotocol.io/posts/2026-07-28/
https://appwrite.io/blog/post/mcp-goes-stateless-in-the-2026-07-28-specification
https://blog.mcpservers.org/posts/mcp-spec-2026-07-28
https://techcommunity.microsoft.com/blog/appsonazureblog/mcp-just-went-stateless-%E2%80%94-what-the-2026-spec-changes-about-scaling-on-app-servic/4530222
https://blog.cloudflare.com/mcp-v2/
https://github.com/swiftlang/swift-testing
https://www.avanderlee.com/swift-testing/modern-unit-test/
https://gist.github.com/steipete/84a5952c22e1ff9b6fe274ab079e3a95
https://github.com/nimblehq/ios-templates/issues/657
https://durellwilson.github.io/swift-2026-course/swift6/testing.html
