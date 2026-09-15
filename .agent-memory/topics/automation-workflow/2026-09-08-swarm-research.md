> ✅ QA-gated by PO batch 2026-09-08 · spot-check: MCP 2026-07-28 spec made the protocol core stateless (no sticky sessions/session store needed) ✓ confirmed against https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/

## TL;DR

- n8n's AI Agent node (v1.28, Jan 2026) added structured tool calling, four memory backends (in-memory/Redis/Postgres/Motorhead), and a ReAct mode — its 2026 default pattern is a centralized orchestrator with specialized sub-agents.
- Multi-agent orchestration has consolidated around six named patterns (orchestrator-worker, pipeline, fan-out, debate, swarm, blackboard); orchestrator-worker/supervisor is the "2026 production workhorse," but ~40% of multi-agent pilots still fail within 6 months from picking the wrong topology.
- MCP's 2026-07-28 spec made the protocol core stateless (no more sticky sessions/session store needed for remote servers), which directly simplifies running multiple MCP servers behind a plain load balancer.
- Temporal is now a common durable-execution backbone for long-running agent workflows (used by Replit Agent 3, Cursor, OpenAI's Codex web agent); its OpenAI Agents SDK integration hit GA in March 2026.
- Claude Code's own subagent fan-out now has built-in guardrails (default concurrency limit 20 since v2.1.217, nested-subagent depth capped at 5) — relevant directly to this workspace's swarm pattern.

## Findings

**What:** n8n's AI Agent node reached its most substantial update in v1.28 (Jan 2026): structured tool calling to prevent infinite loops, 4 memory options (in-memory, Redis, Postgres, Motorhead), and a new ReAct execution mode. n8n also added an AI Workflow Builder that turns natural-language prompts into draft workflows.
**Why it matters:** For a solo operator already running n8n for board/dashboard regeneration, upgrading to a version with structured tool calling + persistent memory backends removes a common failure mode (agent loops) and enables cross-run state without hand-rolled state files.
**Confidence:** med (aggregated from multiple SEO/blog sources, not n8n's own changelog directly — worth confirming version numbers against n8n's official release notes before relying on the exact "1.28"/date claim).

**What:** The AI agent orchestration landscape has converged on six named topologies — orchestrator-worker, pipeline, fan-out, debate, swarm, blackboard — with orchestrator-worker (supervisor) called the "2026 default and production workhorse" due to the widest framework support (Claude Agent SDK, LangGraph, OpenAI Agents SDK, CrewAI hierarchical).
**Why it matters:** Validates this workspace's existing PO + swarms model (main session as supervisor, parallel research/build swarms) as the mainstream-recommended pattern rather than a bespoke one.
**Confidence:** high (multiple independent 2026 sources converge on the same taxonomy).

**What:** Despite growing adoption (Gartner: 1,445% increase in multi-agent inquiries Q1 2024→Q2 2025, orgs averaging 12 agents), roughly 40% of multi-agent pilots fail within six months in production — commonly because teams pick the wrong orchestration pattern for the problem, or the right one without understanding its failure mode.
**Why it matters:** Argues for deliberately choosing the simplest topology that fits each task (per the source's advice: "start simple, add agents only when the problem genuinely decomposes") rather than defaulting to swarms for everything — directly actionable for this repo's PO to be selective about when to fan out research swarms vs. just doing a task directly.
**Confidence:** med (the 40% figure traces to secondary blog aggregation of a Gartner-adjacent claim, not a primary Gartner report link).

**What:** The MCP specification's 2026-07-28 release made the protocol core stateless: remote MCP servers no longer need sticky sessions or a shared session store, can run behind a plain round-robin load balancer, and clients can cache `tools/list` responses per a server-specified `ttlMs`. Input schemas also gained composition support (`oneOf`/`anyOf`/`allOf`, `$ref`/`$defs`).
**Why it matters:** Directly relevant to this workspace's Hostinger content MCP + API MCP layering (per global CLAUDE.md) — stateless MCP servers are simpler to scale/retry and cache tool lists, reducing per-call overhead for repeated automation runs.
**Confidence:** high (sourced from the official Model Context Protocol blog).

**What:** Temporal has become a common durable-execution layer for long-running agentic workflows in 2026 — journaling every workflow step so a crashed process can resume from the last completed step rather than restarting. Its OpenAI Agents SDK integration reached GA on March 23, 2026; adopters cited include Replit Agent 3, Cursor's long-running automation, and OpenAI's Codex web agent.
**Why it matters:** For any future move beyond cron (which can't resume mid-run or survive sleep/crash), Temporal-style durable execution is the documented 2026 upgrade path — worth evaluating if unattended `claude -p` runs grow longer or need resumability instead of the current self-removing one-shot cron pattern.
**Confidence:** med (vendor-adjacent sources; the GA date and named adopters should be verified against Temporal's own changelog if this becomes a real dependency).

**What:** Best-practice guidance for unattended/scheduled AI agent jobs in 2026 converges on: idempotency keys on every side-effecting call, explicit "did I already do this?" checks before acting, mandatory strict timeouts (a few minutes) to stop stuck processes from burning credit, and a log entry (timestamp, actions, outcome) per scheduled run for debuggability.
**Why it matters:** Reinforces and extends the existing cron lessons already in this workspace's memory (dedup pitfall, self-removing one-shot jobs) — the idempotency-key and mandatory-timeout points aren't yet captured in the existing `webblog-cron-scheduling` memory and are worth folding in.
**Confidence:** med (aggregated from multiple 2026 how-to blogs, consistent with general distributed-systems practice, no single authoritative primary source).

**What:** Claude Code's subagent fan-out now ships with explicit guardrails: a default concurrent-subagent limit of 20 (since v2.1.217) and nested-subagent depth capped at 5, alongside support for a lead agent fanning out "tens to hundreds" of parallel subagents via "Dynamic Workflows."
**Why it matters:** Sets a concrete ceiling to plan around when this workspace's PO dispatches parallel research/build swarms — useful to know the platform itself will throttle over-eager fan-out rather than needing to hand-roll a concurrency limiter.
**Confidence:** med (specific version number and limit came from a single blog aggregation, not Anthropic's own release notes — worth a quick primary-source check before treating "20" as authoritative).

## For This Workspace

- When dispatching PO swarms (per this repo's Operating Model), default to the orchestrator-worker/supervisor topology already in use, but explicitly ask "does this decompose?" before fanning out — the 40%-pilot-failure finding suggests over-swarming trivial tasks is itself a risk, not just a cost.
- Add idempotency keys and a mandatory per-run timeout to the existing cron/`claude -p` pattern (extends `webblog-cron-scheduling` memory) — e.g., a run-id file checked before any side-effecting Hostinger/n8n call, and a hard wall-clock cutoff in the wrapper script.
- If n8n is upgraded, check for the v1.28+ AI Agent node's Postgres/Redis memory backends as a lower-effort alternative to hand-rolled state files for anything that needs cross-run memory beyond what `.agent-memory/` provides.
- Track the MCP 2026-07-28 stateless-core spec change when adding or debugging MCP servers (Hostinger content/API MCPs, n8n MCP) — if a server claims to need sticky sessions going forward, that's now a smell worth double-checking against the current spec.

## Sources

https://medium.com/@angelosorte1/n8n-in-2026-latest-updates-practical-use-cases-ethical-automation-11af4cb4b455
https://medium.com/@angelosorte1/multi-agent-orchestration-with-n8n-in-2026-from-concept-to-real-world-ai-systems-bae68fa7ba03
https://hatchworks.com/blog/ai-agents/n8n-guide/
https://chronexa.io/blog/n8n-ai-agent-features-2026
https://beam.ai/agentic-insights/multi-agent-orchestration-patterns-production
https://www.glukhov.org/ai-systems/architecture/multi-agent-orchestration-patterns/
https://www.digitalapplied.com/blog/multi-agent-orchestration-5-patterns-that-work
https://gurusup.com/blog/agent-orchestration-patterns
https://appamass.com/en/blog/multi-agent-orchestration-production-patterns-2026-e431zfbjmelmwyup1ts7
https://singhajit.com/multi-agent-ai-swarms-system-design/
https://blog.modelcontextprotocol.io/posts/2025-11-25-first-mcp-anniversary/
https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/
https://blog.modelcontextprotocol.io/posts/mcp-roadmap/
https://blog.modelcontextprotocol.io/posts/2026-07-28/
https://dev.to/x4nent/complete-guide-to-mcp-model-context-protocol-in-2026-architecture-implementation-and-4a11
https://temporal.io/pages/durable-ai-agent-bundle
https://intuitionlabs.ai/articles/agentic-ai-temporal-orchestration
https://jacar.es/en/durable-agent-execution-with-temporal/
https://olmecdynamics.com/news/temporal-durable-execution-agentic-workflows-2026
https://www.reactify-solutions.com/articles/durable-ai-agents-2026
https://callsphere.ai/blog/temporal-ai-agent-workflows-durable-execution-workflow-as-code
https://fast.io/resources/ai-agent-job-scheduling/
https://www.mindstudio.ai/blog/claude-code-cron-jobs-schedule-agents
https://dev.to/toji_openclaw_fd3ff67586a/the-complete-guide-to-ai-agent-cron-jobs-and-scheduling-2c3f
https://moclaw.ai/blog/ai-cron-jobs-2026-guide
https://hermes-agent.ai/blog/hermes-agent-cron-jobs
https://www.mindstudio.ai/blog/sub-agents-claude-code-context-management
https://www.mindstudio.ai/blog/code-with-claude-2026-new-agent-features
https://hidekazu-konishi.com/entry/claude_code_subagents_and_orchestration_guide.html
https://www.digitalapplied.com/blog/claude-code-subagent-depth-limits-budget-caps-2026
https://alexop.dev/posts/claude-code-workflows-deterministic-orchestration/
https://getaitopia.io/blog/claude-subagents-explained-multi-agent-orchestration
https://www.totalum.app/blog/claude-code-subagents-totalum
https://www.totalum.app/blog/claude-agent-sdk-totalum-2026
