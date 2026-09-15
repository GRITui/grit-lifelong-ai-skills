> ✅ QA-gated by PO batch 2026-09-08 · spot-check: CVE-2025-53773 (GitHub Copilot RCE via prompt injection, CVSS 9.6) ✓

# software-development — Swarm Research (2026-09-08, angle: agent/MCP security)

## TL;DR
- 2026 is the year AI-coding-agent security became a named discipline: OWASP shipped both a **Top 10 for Agentic Applications (Dec 9 2025)** and a separate **OWASP MCP Top 10**, formalizing risks like tool misuse, identity/privilege abuse, memory poisoning, and supply-chain compromise.
- **CVE-2025-53773** (CVSS 9.6): prompt injection hidden in public repo *code comments* tricked GitHub Copilot into flipping a config setting that enabled code execution without user approval — proof that untrusted repo content (not just chat input) is an attack surface for coding agents.
- The **"lethal trifecta"** framing (private-data access + external communication ability + exposure to untrusted content) is the dominant mental model for when an agent setup becomes exploitable; all three conditions co-occurring is the red flag, not any single one.
- MCP specifically is under active attack research: 30+ CVEs filed against MCP servers/clients Jan–Feb 2026, and Unit 42 measured a **78.3% attack success rate** when 5 MCP servers were chained to one agent — malicious/impersonating MCP servers (e.g., a fake Postmark server silently forwarding emails) are a real, documented pattern, not theoretical.
- Consensus defense-in-depth stack: input validation + instruction-hierarchy enforcement, least-privilege tool scoping (small blast radius per credential), output validation, runtime/behavioral monitoring, and periodic adversarial testing — explicitly "no single control fully prevents prompt injection."

## Findings

1. **What:** OWASP Top 10 for Agentic Applications (2026), published Dec 9 2025 by the OWASP GenAI Security Project, ranks 10 risk categories: planning manipulation, tool use, identity, supply chain, code execution, memory, inter-agent communication, cascading failures, human-agent trust, and rogue agents.
   **Why it matters:** Gives this workspace a checklist vocabulary for reasoning about its own PO+swarm agent model — e.g. "memory poisoning" maps directly onto the `.agent-memory/topics/` write path, and "supply chain" maps onto the Hostinger/GitHub MCP servers already wired into `~/.claude.json`.
   **Confidence:** high (OWASP is a primary, citable standards body; corroborated by multiple independent write-ups).

2. **What:** A separate, dedicated **OWASP MCP Top 10** now exists alongside the LLM-app and Agentic-app lists, because MCP's client-server-tool topology has distinct failure modes from generic LLM apps. Guidance: apply both the Agentic and LLM lists when using third-party MCP servers/agent platforms, not just one.
   **Why it matters:** This workspace connects to multiple third-party MCP servers (Hostinger content/API MCP, GitHub MCP, plus various claude.ai connectors visible in this session). Each one is technically in scope for MCP-specific threat modeling, not just generic "API integration" hygiene.
   **Confidence:** high (OWASP primary source referenced consistently across Cycode, Aikido, NHIMG summaries).

3. **What:** CVE-2025-53773 — prompt injection embedded in public GitHub repository code *comments* (not chat/PR text) instructed GitHub Copilot to modify its own settings to enable code execution without user approval. CVSS 9.6. Separately, a "triple CVE chain" in Cursor IDE combined a shell-builtin bypass (CVSS 9.8), a git-hook escape, and a TOCTOU race condition — together showing AI coding assistants are now the most heavily targeted product category for prompt injection (7 of 21 documented multi-stage attacks in the source dataset target this category).
   **Why it matters:** Directly relevant to any workspace practice of having agents read/act on untrusted third-party repo content (e.g. cloning external code, reading issues/PRs, or ingesting web-fetched pages into context) — the attack surface is *content the agent reads*, not just prompts a human types.
   **Confidence:** high (CVE + CVSS score are verifiable primary facts; corroborated by vectra.ai writeup).

4. **What:** The "lethal trifecta" model: an agent becomes exploitable when it simultaneously has (a) access to private/sensitive data, (b) the ability to communicate externally (send emails, make API calls, push commits), and (c) exposure to untrusted content (web pages, third-party repos, PR descriptions). Recommended mitigation is breaking any one leg of the trifecta per agent/task rather than trying to filter all untrusted content perfectly.
   **Why it matters:** This is a fast, practical audit heuristic — for any given agent task in this workspace (e.g. "swarm reads web + writes to inbox + has git/deploy credentials"), check whether all three legs are present simultaneously and whether they need to be.
   **Confidence:** high (concept is now widely cited across the 2026 AI-security literature as the standard framing, e.g. Simon Willison's original formulation referenced across multiple 2026 sources).

5. **What:** MCP-specific supply-chain risk is empirically measured, not hypothetical: 30+ CVEs filed against MCP servers/clients/infrastructure between Jan–Feb 2026; Unit 42 (Palo Alto Networks) found a 78.3% attack success rate when chaining 5 MCP servers to a single agent; a documented real-world case involved a malicious MCP server impersonating the Postmark email service and silently forwarding outgoing emails to an attacker.
   **Why it matters:** Directly actionable for the `HOSTINGER_API_TOKEN`-scoped MCP servers already in `~/.claude.json` — the risk isn't just "token gets stolen," it's "a compromised or impersonating MCP server silently misuses a legitimately-scoped token." Argues for periodically verifying MCP server identity/source, not just rotating tokens on 401s.
   **Confidence:** medium-high (Unit 42 stat and CVE count are from a credible named source per the Cycode summary, but this research didn't fetch Unit 42's primary report directly — one level of indirection).

6. **What:** By 2026, agentic governance guidance (Cloudsmith, Augment Code, Cycode) treats AI coding agents as non-human identities requiring their own access policy: every agent action should be traceable to a specific model version + prompt, dependency selection is increasingly agent-driven (not human-reviewed) which raises hallucinated-dependency and typosquat risk, and industry estimates cited say autonomous agents will write/test/deploy nearly half of enterprise code by end of 2026.
   **Why it matters:** Reinforces (from a security angle, complementing the existing 2026-09-08 file's CI-testing angle) why this workspace's QA gate treats agent output as untrusted-until-verified by construction — the "half of enterprise code is agent-written" framing is exactly the threat model the gate exists for.
   **Confidence:** medium (the "half of code by 2026" figure is a widely-repeated industry estimate, not a measured statistic — treat as directional, not precise).

7. **What:** Recommended defense-in-depth stack across six layers, repeated consistently across sources: (1) input validation / separating system instructions from untrusted data at the architecture level, (2) instruction-hierarchy enforcement, (3) least-privilege tool/credential scoping so a successful injection has a small blast radius, (4) output validation before an agent's output is acted on, (5) continuous runtime/behavioral monitoring for anomalous tool use, (6) regular adversarial testing (red-teaming). Explicit caveat: "no single control can fully prevent prompt injection."
   **Why it matters:** Gives a concrete checklist to compare against this workspace's current controls, which today rely mostly on layer 3 (per-project-scoped MCP tokens) and human review — layers 1, 4, 5, 6 are largely absent.
   **Confidence:** high (this exact six-layer framing is directly quoted/paraphrased consistently across the fetched vectra.ai source and corroborated by the broader search results).

## For This Workspace

1. **Treat every third-party MCP server as in-scope for the "lethal trifecta" check.** Before wiring a new MCP server (or reusing an existing one for a new task), ask: does this agent invocation combine (a) access to secrets/private data, (b) an external-communication capability, and (c) exposure to untrusted content in the same turn? If yes, break one leg — e.g. don't let the same subagent that reads arbitrary web content also hold the Hostinger deploy token in the same call.
2. **Add an MCP-provenance check to the existing Hostinger token-rotation habit** (already documented in `.agent-memory/topics/`): when rotating a token after a 401, also spot-check that the MCP server package/endpoint hasn't changed (e.g. `npx --package=hostinger-api-mcp@latest` version, or the content-MCP domain) — the 78.3%-attack-chaining and Postmark-impersonation findings (Finding 5) suggest verifying *what* you're authenticating to, not just refreshing *how*.
3. **Extend the QA-gate table in `CLAUDE.md`** with an untrusted-content flag: any research swarm that ingests web content (WebFetch/WebSearch results) into `.agent-memory/inbox/` should be treated as reading untrusted data (Finding 3's "attack surface is content the agent reads" applies to fetched web pages, not just repo comments) — the PO's existing "spot-check claims" QA step already partially covers this, but it's worth noting explicitly as a security control, not just an accuracy control.
4. **Note OWASP's Agentic/MCP Top 10 as a reference framework** for future `.agent-memory/topics/` entries on this domain — if/when this workspace adds a new MCP integration or hands agents write-access to more systems, use the 10-category taxonomy (planning, tool use, identity, supply chain, code execution, memory, inter-agent comms, cascading failures, human-agent trust, rogue agents) as the review checklist rather than ad hoc reasoning.

## Sources
https://cycode.com/blog/owasp-top-10-agentic-applications/
https://cycode.com/blog/owasp-mcp-top-10/
https://www.vectra.ai/topics/prompt-injection
https://www.vectra.ai/topics/agentic-ai-security
https://cycode.com/blog/ai-security-vulnerabilities/
https://cloudsmith.com/blog/the-2026-guide-to-software-supply-chain-security-from-static-sboms-to-agentic-governance
https://www.augmentcode.com/guides/supply-chain-security-agentic-era
https://cycode.com/blog/securing-adlc/
