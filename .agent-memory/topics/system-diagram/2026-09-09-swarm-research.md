# System-diagram research: Eraser.io, Kroki, AI ER-diagram tools

> ✅ QA-gated by PO 2026-09-09 · spot-check: Kroki wraps 30+ diagram engines with deflate+base64 GET / POST API ✓

## TL;DR
- Eraser.io's DiagramGPT + Eraser MCP server is a mature, previously-uncovered AI diagram tool: it accepts natural-language prompts, existing diagram code, image/PDF attachments, *and Git repos* (Terraform/IaC) as input, and returns editable DSL + PNG across 6 diagram types (sequence, ERD, cloud architecture, flowchart, BPMN, freeform).
- Kroki fills a real gap in prior research: a single self-hostable HTTP API that wraps 30+ diagram engines (Mermaid, PlantUML, D2, GraphViz, Excalidraw, DBML/Erd, WaveDrom, C4-PlantUML, and more) behind one consistent request/response contract — one Docker container instead of installing `mmdc`, PlantUML jar, D2 binary, etc. separately.
- Database-schema/ER diagramming has its own fast-moving AI sub-niche not yet covered: DrawSQL (NL-to-schema AI design), ChartDB (open-source, 20k+ GitHub stars, imports a live DB schema in ~15s via one query, exports SQL DDL across 9+ dialects), and dbdiagram.io (DBML-as-source, code-first).
- Kroki's diagram-source-in-URL model (deflate+base64 GET, or POST with `Content-Type`) makes diagrams embeddable as plain links in Markdown/wikis (MediaWiki has a native Kroki extension) with zero client-side rendering — a different tradeoff than Mermaid's client-side-JS or a pre-render build step.
- All three tool families reinforce the same 2026 pattern already logged in this topic: diagram-as-code text (DSL/DBML/Terraform) is the durable, diffable artifact; AI features (DiagramGPT, DrawSQL AI, ChartDB AI) are convenience layers for *generating* that text, not a replacement for keeping it in version control.

## Findings

### Eraser.io DiagramGPT + Eraser MCP server
- What: Eraser's "Prompt → Diagram" API and MCP server (usable from Claude, Cursor, VS Code, ChatGPT) generate/search/read/update/export diagrams across sequence, ERD, cloud-architecture, flowchart, BPMN, and freeform types. Input can be a plain-text prompt, an `inlineCodeEdit` (existing Eraser DSL passed back for editing without prior request history), an uploaded PNG/JPEG/PDF (base64, up to 10MB), or a Git repo reference (public/private) so it can generate architecture diagrams straight from Terraform/IaC source. Output is Eraser DSL (editable text) plus PNG at 1–3x quality, or a binary file stream. There's a "standard" vs "premium" model tier (premium is default).
- Why it matters: This is the most input-flexible AI diagram generator found across all research batches so far — specifically the "point it at a Git repo of Terraform and get an architecture diagram" path is a capability not documented for Mermaid AI, draw.io's AI generator, or Excalidraw's MCP in prior files. It also syncs to GitHub and embeds into Confluence/Notion, positioning it as a hybrid AI-generation + doc-embedding tool rather than pure code-to-image.
- Confidence: high (official Eraser docs page fetched directly; feature list matches consistently across search snippets).

### Kroki — unified diagram-rendering API
- What: Kroki (kroki.io, OSS) is an HTTP service that wraps 30+ diagramming engines — BlockDiag family, BPMN, C4 (via PlantUML), D2, DBML, Ditaa, Erd, Excalidraw, GraphViz, Mermaid, Nomnoml, Pikchr, PlantUML, SvgBob, UMLet, Vega/Vega-Lite, WaveDrom, WireViz, and experimental draw.io/diagrams.net support — behind one consistent API. GET requests encode the diagram source into the URL itself (deflate + base64); POST requests send source as JSON or plain text with `Content-Type`/`Accept` headers to pick output format (SVG/PNG/PDF/JPEG/Base64). Free hosted instance is donated by Exoscale; self-hosting is a documented Docker/Linux setup.
- Why it matters: Every prior research batch in this topic treated diagram engines as separate tools each needing their own CLI/binary (`mmdc`, PlantUML jar, D2 binary, Graphviz `dot`). Kroki collapses that into one container and one request format — directly useful if this workspace's CI/QA-gate ever needs to render more than one diagram-source type without maintaining N separate toolchains. It also enables "diagram as a URL" embedding (no client JS, no build step) which MediaWiki natively supports via a Kroki extension — a third rendering pattern alongside "client-side JS" (Mermaid in Markdown) and "pre-rendered SVG in CI" already logged in earlier batches.
- Confidence: high (official kroki.io site + docs.kroki.io fetched directly, consistent with GitHub repo description; PO spot-check confirmed engine count, GET/POST behavior via direct fetch of kroki.io).

### AI-assisted ER/database-schema diagramming (DrawSQL, ChartDB, dbdiagram.io)
- What: This sub-niche wasn't covered in prior batches despite ERD being one of the diagram-design skill's supported types. DrawSQL lets users paste SQL, describe a schema in plain English (AI designs tables/columns/relationships/constraints), or draw manually, with MySQL/PostgreSQL/SQL Server support. ChartDB (OSS, 20k+ GitHub stars) imports a live database schema via a single generated query (~15s, no direct DB connection needed), offers an AI ER-diagram generator from natural-language descriptions, exports to SQL DDL across 9+ dialects (Postgres, MySQL, SQL Server, SQLite, MariaDB, ClickHouse, CockroachDB, Oracle, Snowflake, BigQuery), and embeds into Notion/Miro/Confluence. dbdiagram.io remains the code-first option, using DBML as its plain-text source format (analogous to Mermaid/D2 for architecture diagrams).
- Why it matters: For any future task needing a database schema diagram from an actual live DB (vs. hand-authoring an ERD), ChartDB's "one query, no connection, ~15s" reverse-engineering approach plus DDL export in 9+ dialects is a concrete, low-friction option; DBML (dbdiagram.io) is the direct ERD analog to this topic's established "keep the text source in git" pattern.
- Confidence: med (search-snippet-level detail for DrawSQL/dbdiagram.io; ChartDB detail came from a direct site fetch, but exact AI-generation quality/accuracy wasn't independently tested).

## For This Workspace
- If a future task needs to render diagram source types beyond what's already scripted (Mermaid via `mmdc`), consider a self-hosted Kroki Docker container as a single rendering backend for D2/PlantUML/GraphViz/Excalidraw/DBML instead of installing each CLI separately — it fits the existing "QA gate renders from text source, never judges the picture" model from batch4, since Kroki's contract is text-in/image-out with no AI in the loop.
- If a task ever needs an ERD/database-schema diagram from a real project database, ChartDB (open-source, self-hostable, one-query reverse-engineering, DDL export) or dbdiagram.io's DBML format are better fits than hand-drawing one — DBML source should be committed to git the same way this topic already recommends for Mermaid/D2 sources.
- Eraser's MCP server (Git-repo-to-architecture-diagram, via Terraform/IaC scanning) is worth a spike if this workspace ever needs to auto-generate an infra diagram directly from a Terraform-managed project, without an agent hand-authoring the DSL.

## Sources
https://www.eraser.io/diagramgpt
https://www.eraser.io/product/ai-diagrams
https://docs.eraser.io/reference/generate-diagram-from-prompt
https://kroki.io/
https://docs.kroki.io/kroki/
https://github.com/yuzutech/kroki
https://www.mediawiki.org/wiki/Extension:Kroki
https://cloudairyhq.medium.com/top-5-ai-er-diagram-generators-for-database-architects-in-2026-8f0767286e7c
https://drawsql.app/er-diagram
https://docs.dbdiagram.io/
https://dbdiagram.io/home
https://chartdb.io
