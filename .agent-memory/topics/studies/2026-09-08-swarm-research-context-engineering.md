> ✅ QA-gated by PO batch 2026-09-08 · spot-check: fetched platform.claude.com/docs memory-tool page directly — confirmed tool type `memory_20250818`, six commands (view/create/str_replace/insert/delete/rename), persists /memories dir across sessions, matches draft ✓

# Case Study: Anthropic's Context Editing + Memory Tool (server-side context engineering)

Angle (a): a production context-engineering technique — Anthropic's server-side
**context editing** API paired with the **memory tool**, both shipped for
Claude models and now a reference design other coding-agent harnesses (Claude
Code, OpenCode, Codex) converge on.

## TL;DR

- Anthropic shipped a server-side **Context Editing API** (beta header
  `context-management-2025-06-27`) that auto-clears old tool-use/result pairs
  and thinking blocks *before* they hit the token count and the model, without
  the client losing the full history.
- Paired with the `memory_20250818` **memory tool** (shipped alongside Sonnet
  4.5, released September 29, 2025), agents persist notes to a `/memories`
  directory and re-read them on demand instead of keeping everything in-context.
- Anthropic's internal 100-turn web-search benchmark: context editing alone
  cut token consumption **84%** and lifted task performance **29%**; editing +
  memory tool together gave **39%** performance improvement over baseline.
- Default trigger: fires once the prompt passes **100,000 input tokens**,
  keeping the 3 most recent tool results and replacing older ones with a
  placeholder so the model knows content was removed.
- Claude Code itself (the coding-agent product) layers its own client-side
  compaction on top: tool-result trimming, prompt-cache-friendly formatting,
  and a 9-section structured LLM summary when a session nears its limit.

## Findings

1. **What**: The Context Editing API strips old tool_use/tool_result pairs and
   extended-thinking blocks server-side, before token counting and after the
   prompt-cache lookup, replacing them with placeholder text.
   **Why it matters**: Cleared tokens never hit the bill, and the technique is
   cache-friendly — unlike client-side truncation, it doesn't require the app
   to re-manage cache breakpoints itself.
   **Confidence**: high (Anthropic's own platform docs).

2. **What**: Default clearing threshold is 100,000 input tokens, with the 3
   most recent tool results always preserved.
   **Why it matters**: Gives a concrete, tunable number for anyone building a
   similar auto-prune policy in a homegrown harness — you don't have to
   guess a threshold from scratch.
   **Confidence**: high (platform docs + corroborated by Channel.tel writeup).

3. **What**: The memory tool (`memory_20250818`) gives Claude filesystem-like
   `view`/`create`/`str_replace`/`insert`/`delete`/`rename` operations against
   a `/memories` directory that persists **across API calls/sessions**, not
   just within one context window. When present in a request, the API
   auto-injects an instruction telling the model to check memory before
   acting.
   **Why it matters**: This is functionally identical in spirit to this
   workspace's `.agent-memory/topics/` pattern — Anthropic is standardizing
   "write what you learn to files, read back on demand" as the recommended
   cross-session memory architecture, not RAG/vector search.
   **Confidence**: high (platform docs; SDK ships `BetaAbstractMemoryTool`
   Python / `betaMemoryTool` TypeScript helpers to subclass for custom storage
   backends).

4. **What**: Anthropic's official "Effective context engineering for AI
   agents" guide frames four core levers: writing context out, selecting only
   what's relevant, compressing (compaction), and isolating context via
   sub-agents.
   **Why it matters**: Sub-agent isolation — each sub-agent gets its own
   context window, system prompt, and tool permissions, then reports a
   synthesized result back to the lead agent — is exactly the "swarm"
   pattern this workspace's PO+swarms operating model already uses.
   **Confidence**: high (Anthropic engineering blog, primary source).

5. **What**: Compaction (distinct from context editing) is triggered
   client/session-side: when a conversation nears its context-window limit,
   the system summarizes it and reinitiates a fresh window from that summary
   rather than surgically clearing old tool calls.
   **Why it matters**: Editing (surgical, automatic, cheap) and compaction
   (holistic summarization, lossier) are complementary, not the same
   mechanism — a harness may want both: cheap auto-pruning for tool noise,
   periodic summarization for narrative continuity.
   **Confidence**: med (multiple third-party writeups agree; exact Claude
   Code internal implementation details are less officially documented than
   the API-level context editing feature).

6. **What**: Third-party analysis (justin3go.com, April 2026) describes
   Claude Code's own compaction as a "three-tier progressive mechanism": tool
   result trimming, prompt-cache-friendly restructuring, and a 9-section
   structured LLM summary, compared against similar approaches in Codex and
   OpenCode.
   **Why it matters**: Shows the pattern converging across multiple
   independent coding-agent products in 2026, not just Anthropic's — worth
   treating as an emerging industry-standard shape for "how coding agents
   survive long sessions," useful precedent for this repo's own harness
   design.
   **Confidence**: med (single third-party source, not Anthropic-official;
   worth independent verification before citing exact tier names elsewhere).

## For This Workspace

- **Adopt an explicit "read memory before acting" instruction pattern**: this
  repo's CLAUDE.md Step 1 (Recall) already mirrors what Anthropic's memory
  tool auto-injects into the system prompt. Consider making that instruction
  even more mechanical/first-line (e.g., a literal checklist step at the very
  top of every swarm agent's prompt) rather than prose buried in Step 1.
- **Consider a numeric threshold analog for `.agent-memory/inbox/` pruning**:
  Anthropic's 100k-token / keep-last-3 default suggests a concrete rule this
  repo could borrow — e.g., "PO only keeps the N most recent inbox drafts
  in active review context; older ones get archived or summarized" — instead
  of an unbounded inbox.
- **Formalize sub-agent isolation as a stated design goal**, not just an
  incidental effect of using the Agent tool: each swarm worker already gets
  an isolated context and restricted write scope (inbox-only) — this matches
  Anthropic's documented "functional context isolation" pattern almost
  exactly and is worth naming explicitly in the harness docs as the reason
  swarms outperform a single long-running session.
- **Distinguish "editing" vs "compaction" as two separate future levers**:
  if this workspace ever needs the PO session itself to survive very long
  multi-swarm days, note that surgical clearing (drop old raw tool output,
  keep recent) and holistic summarization (compact the narrative) are
  different tools solving different problems — don't conflate them when
  designing any future auto-prune logic for board.json or session logs.

## Sources

- https://platform.claude.com/docs/en/build-with-claude/context-editing
- https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool
- https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- https://www.channel.tel/blog/agent-context-editing-memory-tool-token-cost
- https://justin3go.com/en/posts/2026/04/09-context-compaction-in-codex-claude-code-and-opencode
- https://www.leoniemonigatti.com/blog/claude-memory-tool.html
- https://platform.claude.com/docs/en/build-with-claude/compaction
