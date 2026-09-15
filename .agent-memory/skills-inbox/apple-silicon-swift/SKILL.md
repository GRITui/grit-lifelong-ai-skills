---
name: apple-silicon-swift
description: Use when writing, compiling, or distributing Swift on this Apple Silicon (M1, CLT-only) Mac — choosing zero-dep single-file builds vs frameworks, using the Foundation Models on-device LLM, MCP Swift SDK transports, MLX integration, Static Linux SDK cross-builds, or code-signing/notarization for externally shared binaries.
sources:
  - /Users/grit/.agent-memory/topics/swift-apple-silicon/2026-09-08-swarm-research.md
---
# audited: PASS 2026-09-10

## Default architecture

- Default: zero-dep single-file `swiftc -O file.swift -o tool` (NWListener / Foundation) — fastest builds on CLT 6.3.3 / M1; single-file compiles stay seconds-fast.
- Add a framework ONLY IF HTTP routing/middleware is truly needed → Hummingbird 2 (SwiftNIO, swift.org-endorsed, lighter than Vapor); costs SwiftPM + 8+ transitive deps.
- Concurrency: keep the `nonisolated` default for servers (SE-0466); strict Swift 6 mode is practical on 6.2+ toolchains.

## On-device LLM

- Foundation Models needs macOS 26 + Apple Intelligence enabled — run a 3-line `SystemLanguageModel.availability` probe BEFORE any feature depends on it.
- On-device model ≈3B params and is REPLACED in OS point updates (e.g. 26.4) — retest prompts after updates; guardrails throw `guardrailViolation`.
- Preferred route: OpenAI-compatible wrapper exposing a local endpoint (apfel / maclocal-api style) → slot into the litellm :4000 router as a `local-free` tier. Bridge by endpoint, never embed.

## MCP / MLX

- MCP Swift SDK 0.12.1 (Swift 6, zero data-race errors) is solid for stdio servers — PIN stdio transport + the 2025-11-25 spec; do NOT adopt the 2026-07-28 HTTP/stateless semantics yet.
- NEVER embed MLX in CLT/swiftc builds — SwiftPM cannot compile its Metal shaders (needs xcodebuild). Use the separate `mlx-lm` OpenAI-compatible server instead.

## Cross-platform / distribution

- Linux binaries: Static Linux SDK — `swift sdk install <...static-linux-0.1.0.artifactbundle.tar.gz>`, build with `--swift-sdk aarch64-swift-linux-musl` (or x86_64); smoke-test every dependency (musl/SIL compiler bugs exist, e.g. apple/swift-configuration#105). Network.framework is Apple-only — macOS server code won't port.
- Distribution friction tiers: on this Mac, ad-hoc-signed binaries run as-is, zero friction. External sharing = paid Developer ID + `codesign --timestamp --options runtime` + `xcrun notarytool submit --wait`; standalone binaries cannot be stapled — budget for queue latency.

Validate: `swiftc --version` — prints the CLT version (6.3.x expected); nonzero = toolchain missing, do not compile.
