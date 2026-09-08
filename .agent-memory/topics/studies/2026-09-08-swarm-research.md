> ✅ QA-gated by PO batch 2026-09-08 · spot-check: GitHub API for doobidoo/mcp-memory-service confirmed stars=1928, forks=303, latest release v11.11.0 published 2026-09-05T09:57:42Z — matches draft ✓

# Study: Henry (Heinrich) Krupp / doobidoo — mcp-memory-service

## TL;DR
- Henry Krupp (GitHub `doobidoo`, Kreuzlingen, Switzerland) builds and maintains **mcp-memory-service**, an open-source MCP server giving AI agents persistent, local-first semantic memory.
- Project is large and active: 1,928 stars, 303 forks, 3,330+ commits, latest release v11.11.0 shipped Sept 5, 2026 (three days before this research).
- Architecture directly parallels this workspace's own goals: knowledge-graph memory with typed edges (causes/fixes/contradicts), autonomous consolidation (decay + compression), hybrid BM25+vector search, and a documented `AUTHORSHIP.md`/`SECURITY.md` governance pattern.
- Supports 25+ clients (Claude Desktop, Claude Code, VS Code, Cursor, LangGraph, CrewAI, AutoGen, claude.ai Remote MCP) via one self-hosted backend — explicit anti-vendor-lock-in design.
- Bio frames him as a "Senior DevOps Engineer transitioned to AI Infrastructure Product Leader" — this is a practitioner building memory infra as his primary focus, not a side skill collection (contrast with chakrit's skills/prompt-pipeline focus).

## Findings

1. **What**: `mcp-memory-service` (github.com/doobidoo/mcp-memory-service) is a Python MCP server that persists agent memories with local ONNX embeddings (all-MiniLM-L6-v2, 384-dim) and exposes them via REST API (76 endpoints), MCP protocol, OAuth 2.0, CLI, and a web dashboard.
   **Why it matters**: it's a working, shipped answer to exactly the "agent amnesia across sessions" problem this workspace's own `.agent-memory/` harness is trying to solve by hand with markdown files.
   **Confidence**: high (verified via repo README and GitHub profile directly; star/fork/release counts independently reverified via GitHub API).

2. **What**: Storage backends are pluggable — SQLite-vec (local default), Cloudflare D1 (hybrid sync), or Milvus (vector DB) — chosen so embeddings and search can run fully offline with no cloud dependency by default.
   **Why it matters**: models a "privacy-first, sync-optional" pattern relevant to any future decision to make this repo's memory syncable across machines.
   **Confidence**: high.

3. **What**: Typed knowledge-graph edges (`causes`, `fixes`, `contradicts`) auto-extracted from `@mentions` and `#tags`, plus autonomous consolidation that decays/compresses old memories and surfaces "insight cards."
   **Why it matters**: this is a more structured evolution of what our flat `topics/<topic>/*.md` files do manually — worth studying if the inbox/topics split ever needs relationship tracking (e.g., "this fix contradicts that earlier note").
   **Confidence**: medium (feature exists per README/changelog notes, did not independently test the extraction behavior).

4. **What**: The project moved its primary development from Codeberg back to GitHub as of v11.11.0 (Sept 2026), and that same release closed three documented security advisories (filesystem tool exposure, SSE auth bypass, DCR token scope).
   **Why it matters**: shows an MCP server maintainer actively treating an agent-memory tool as security-sensitive surface — a useful cautionary note since this workspace's own harness is exactly the kind of tool (arbitrary file read/write via memory) that could have analogous exposure.
   **Confidence**: medium (mentioned in fetched summaries of the repo/wiki, not independently diffed against the CVE/advisory text).

5. **What**: Author documents authorship/licensing explicitly via `AUTHORSHIP.md` (Apache 2.0), and maintains a public roadmap wiki page ("13 Development Roadmap").
   **Why it matters**: a lightweight governance pattern (explicit authorship + security policy + public roadmap) that a small solo-maintainer project can adopt without heavyweight process — directly portable to this repo's own `.agent-harness/INSTRUCTIONS.md` conventions.
   **Confidence**: high (file names/wiki page title confirmed present in repo).

6. **What**: Krupp's GitHub bio also lists adjacent projects — `shodh-cloudflare` (device-synced AI memory on Cloudflare edge), `MCP-Context-Provider` (static MCP server to prevent context loss between chats), and `SecondBrain Pro` (iOS/Watch voice-capture knowledge app).
   **Why it matters**: shows the same "memory/context persistence" problem being attacked from three angles (server-side MCP, edge sync, personal capture app) by one builder — a useful map of the solution space if this workspace wants prior art beyond the primary repo.
   **Confidence**: medium (pinned-repo names/descriptions read from profile page, not individually opened/verified).

7. **What**: Reported benchmark numbers — 80.4% Recall@5 on LongMemEval, 91.1% on DevBench — are cited in the README as evidence the memory/retrieval design actually works, not just architecturally interesting.
   **Why it matters**: gives a concrete bar (recall on standard memory benchmarks) to think about if this workspace ever wants to evaluate whether its own grep-based `.agent-memory/topics/` recall step is "good enough" vs. a real vector/hybrid retrieval system.
   **Confidence**: low (numbers only seen via a secondary summarization pass of the README, not the raw benchmark table itself).

## For This Workspace
- Adopt the **typed-relationship idea** loosely: when writing new `.agent-memory/topics/*.md` files, consider a lightweight "relates-to / supersedes / contradicts" front-matter line pointing at prior topic files — cheap version of Krupp's knowledge-graph edges without needing a DB.
- Adopt the **AUTHORSHIP.md + SECURITY.md pattern**: this repo's harness (which reads/writes files based on agent output) has similar blast radius to an MCP memory server; a short `SECURITY.md` stating what an agent with write access to `.agent-memory/` and `.agent-dashboard/` can and can't do would be cheap insurance.
- **Watch** `doobidoo/mcp-memory-service` as a reference implementation if this workspace ever outgrows flat markdown + grep recall — it's a proven, actively-maintained (commit as recent as Sept 5, 2026) example of the next tier (real vector search + consolidation) rather than a toy.
- Do **not** copy the multi-backend (SQLite/Milvus/Cloudflare) complexity wholesale — this workspace's scale (a handful of contributors, markdown files) doesn't yet justify it; the governance and relationship-tagging ideas are the portable parts, not the storage architecture.

## Sources
https://github.com/doobidoo/mcp-memory-service
https://github.com/doobidoo
https://raw.githubusercontent.com/doobidoo/mcp-memory-service/main/README.md
