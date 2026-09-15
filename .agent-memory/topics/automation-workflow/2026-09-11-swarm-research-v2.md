# Automation Workflow — Swarm Research (new material, 2026-09-11)

> ✅ QA-gated by PO batch 2026-09-11 · spot-check: MCP 2026-07-28 spec is stateless at transport layer (removes initialize/initialized handshake + Mcp-Session-Id) and introduces MRTR + CIMD deprecating DCR ✓ (verified via WebFetch against blog.modelcontextprotocol.io/posts/2026-07-28/)


Builds on `.agent-memory/topics/automation-workflow/2026-09-11-swarm-research.md` (A2A protocol, n8n CVE-2026-21858, idempotency patterns, orchestration-overhead counter-evidence). This draft covers genuinely new ground: the MCP 2026-07-28 spec, n8n's newer AI-agent-specific features, and 2026 agent-observability practice.

## TL;DR

- MCP shipped a major spec revision (2026-07-28): the protocol is now **stateless** at the transport layer (no more sticky sessions/handshake state), adds Multi Round-Trip Requests (MRTR) for mid-call clarification, header-based routing, cacheable list results with TTL, and hardened OAuth (RFC 9207 issuer binding, CIMD replacing Dynamic Client Registration).
- MCP formally deprecated Roots, Sampling, Logging, and legacy HTTP+SSE transport, with a 12-month minimum support window — anything built against the old primitives has a migration deadline, not an indefinite grace period.
- n8n's 2026 feature line (beyond the CVE already logged) rebuilt the AI Agent node with cross-provider tool calling (Claude, GPT-4o, Gemini, Mistral, Groq) and added four memory node types plus **per-node retry with exponential backoff** — directly relevant to this repo's n8n-driven dashboard regeneration.
- Agent observability in 2026 has consolidated around OpenTelemetry GenAI semantic conventions (`gen_ai.*` attributes) as the vendor-neutral tracing standard, with hierarchical trace models needed to localize failure root-cause across multi-agent/subagent chains.
- Tail-based sampling (keep full traces for errors, sample the rest) is the recommended default for production LLM/agent pipelines, over pure head-based sampling.

## Findings

**What:** MCP's 2026-07-28 spec removed session/handshake state from the protocol core: every request now carries its own protocol version, client identity, and capabilities, so a remote MCP server can sit behind a plain round-robin load balancer instead of needing sticky sessions or a shared session store.
**Why it matters:** Any MCP server this workspace stands up or depends on (e.g. the per-site Hostinger content MCP, future custom MCP tools) can now be scaled/deployed more simply; existing assumptions about session affinity in MCP client code should be re-checked against the new stateless model.
**Confidence: high**

**What:** Multi Round-Trip Requests (MRTR) replace server-initiated requests over open streams: a server can now return `resultType: "input_required"` and the client retries the same call with the missing answer, enabling mid-call confirmation or parameter collection without holding a persistent connection open.
**Why it matters:** Useful pattern for any future MCP tool needing human-in-the-loop confirmation (e.g. a destructive-action tool) — avoids the older long-lived-SSE-stream approach.
**Confidence: high**

**What:** MCP formally deprecated Dynamic Client Registration (DCR) in favor of Client ID Metadata Documents (CIMD), and deprecated Roots, Sampling, Logging, and the legacy HTTP+SSE transport — all continue working for at least 12 months but are on a removal track. Authorization was hardened with RFC 9207 issuer validation and issuer-bound credentials to prevent token reuse across authorization servers.
**Why it matters:** If this workspace or any dependency authenticates MCP clients via DCR or relies on Sampling/Logging primitives, there's a bounded window (≤12 months from 2026-07-28) before those break; worth a grep of any custom MCP client config for these primitives.
**Confidence: high**

**What:** n8n's 2026 feature set (independent of the CVE already logged) rebuilt the AI Agent node with tool-calling support spanning Claude, GPT-4o, Gemini, Mistral, Groq, and OpenAI-compatible endpoints; added four memory node types (in-memory, Redis, Postgres, Motorhead); replaced the flat workflow builder with a Canvas UI; and — notably — added **per-node retry logic with exponential backoff**.
**Why it matters:** Per-node backoff retry is a built-in answer to part of the "naive retry" anti-pattern flagged in the prior digest; worth checking whether the n8n flow that regenerates `.agent-dashboard/data.js` is using this feature or still relying on default/no retry.
**Confidence: med** (aggregator/blog sources — releasebot.io, softomatesolutions.com — not n8n's own changelog verbatim; cross-check against `docs.n8n.io/changelog` before relying on specifics)

**What:** Agent observability in 2026 has standardized on OpenTelemetry's GenAI semantic conventions (`gen_ai.*` span attributes) as the vendor-neutral tracing layer, with native adapters for OpenAI Agents SDK, LangGraph, Mastra, Pydantic AI, LangChain, CrewAI, and Vercel AI SDK, and OTel instrumentation as the fallback for anything without a native adapter.
**Why it matters:** This workspace's headless `claude -p` cron jobs and swarm subagents currently have no structured tracing — logs are ad hoc (`memory/YYYY-MM-DD.md`, board.json). If failure diagnosis across a multi-swarm run becomes painful, OTel GenAI conventions are the standard target rather than inventing a bespoke log format.
**Confidence: med** (aggregated from multiple 2026 vendor/blog sources — MLflow, Braintrust, digitalapplied — directionally consistent but vendor-authored, so treat specifics as marketing-adjacent)

**What:** Recommended production sampling strategy for LLM/agent traces is tail-based (capture full traces for errored/anomalous runs, sample the rest at a lower rate) rather than pure head-based sampling, because agent failures are often only identifiable after the full trace completes (e.g., a late tool-call failure invalidates an otherwise-normal-looking early trace).
**Why it matters:** If/when this workspace adds tracing to swarm dispatch, tail-based sampling is the right default so a rare DELEGATION-CONTRACT violation or budget overrun isn't sampled away.
**Confidence: low** (single-topic aggregation across marketing blogs, no primary vendor spec or benchmark cited)

## For This Workspace

- Grep any custom MCP client/server config in this repo (or in `~/.claude.json` mcpServers blocks) for reliance on Dynamic Client Registration, Sampling, Logging, or Roots — these are on a ≤12-month deprecation clock from 2026-07-28 and should migrate to CIMD / the newer primitives before removal.
- Check whether the n8n workflow regenerating `.agent-dashboard/data.js` uses per-node retry-with-backoff (a 2026 n8n feature) instead of no-retry or a naive immediate retry — cheap fix that directly closes the "naive retry" anti-pattern already flagged against this repo's n8n usage.
- Confirm the n8n instance version is current enough to include the rebuilt AI Agent node / per-node retry features (separately from the CVE-2026-21858 ≥1.121.0 security floor already tracked) — check `docs.n8n.io/changelog` directly rather than aggregator sites for the exact version that shipped per-node retry.
- If swarm-dispatch failures become hard to diagnose from `memory/YYYY-MM-DD.md` alone, consider OpenTelemetry GenAI semantic conventions (`gen_ai.*`) as the structured-tracing target rather than a bespoke log schema — but this is a "when it hurts" investment, not an immediate priority given the current PO+swarm model already has an explicit QA gate.

## Sources

https://blog.modelcontextprotocol.io/posts/2026-07-28/
https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/
https://blog.modelcontextprotocol.io/posts/mcp-roadmap/
https://itdaily.com/news/software/mcp-2026-update-specs/
https://blog.cloudflare.com/mcp-v2/
https://aaif.io/blog/mcp-is-growing-up
https://docs.n8n.io/changelog/release-notes-2.x
https://blog.mean.ceo/n8n-news-september-2026/
https://releasebot.io/updates/n8n
https://releases.sh/n8n
https://www.softomatesolutions.com/blog/n8n-updates-2026-whats-new/
https://mlflow.org/articles/what-is-agent-observability-a-2026-developer-guide/
https://mlflow.org/articles/setting-up-llm-observability-pipelines-in-2026/
https://www.braintrust.dev/articles/agent-observability-complete-guide-2026
https://openobserve.ai/blog/opentelemetry-for-llms/
https://www.digitalapplied.com/blog/ai-agent-observability-2026-tracing-monitoring-stack-guide
