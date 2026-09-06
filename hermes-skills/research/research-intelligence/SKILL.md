---
name: research-intelligence
description: Class-level research workflow for paper discovery, RSS/blog monitoring, knowledge-base building, prediction-market lookup, and research writing handoff.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [research, arxiv, rss, blogs, llm-wiki, polymarket, literature, monitoring, knowledge-base]
---

# Research Intelligence

Use this umbrella for discovering, monitoring, organizing, and synthesizing external information: arXiv search, paper triage, RSS/blog monitoring, durable markdown knowledge bases, prediction-market checks, and handoff into research writing.

## Default workflow

1. Define the research question and desired output: quick answer, source list, literature map, monitoring job, knowledge-base entry, or writing plan.
2. Select sources based on the question:
   - arXiv for academic papers and IDs;
   - blogs/RSS for ongoing technical monitoring;
   - LLM Wiki or markdown vaults for persistent interlinked notes;
   - Polymarket for market-implied probabilities and current event forecasts;
   - conference paper-writing workflows for manuscript structure and citations.
3. Collect source metadata with URLs/IDs and timestamps.
4. Synthesize rather than paste: group by claim, method, evidence, and uncertainty.
5. Save durable notes when the user asks for ongoing research memory.

## Labeled playbooks

### arXiv discovery

Search by keyword, author, category, or arXiv ID. Return title, authors, date, abstract gist, and link. For literature review, cluster papers by method and novelty.

### Blog/RSS monitoring

Use feed tooling for recurring source monitoring. Prefer explicit feed URLs, dedupe entries, and summarize only material changes. For cron-style monitoring, make the prompt self-contained.

### Knowledge-base building / LLM Wiki

Use markdown knowledge bases for persistent interlinked research. Prefer an explicit wiki path supplied for the task. Otherwise resolve and validate `OBSIDIAN_VAULT_PATH` through `local-knowledge-workbench` and discover an existing wiki within that vault. `_Wiki` is an example folder name, not a configured setting or required layout. Use `~/wiki` only when it actually exists; if the root remains unknown, discover a unique existing directory containing `index.md`, `log.md`, and either `SCHEMA.md` or `AGENTS.md`. Ask when multiple candidates remain; never initialize a new fallback silently.

For an existing wiki, orient before every ingest or query:

1. Read `SCHEMA.md`; if absent, read `AGENTS.md` and treat it as canonical local governance.
2. Read `index.md`, any secondary index such as `wiki/INDEX.md`, and the latest 20–30 log entries by file position.
3. Infer and preserve the actual layout (`raw/`, `wiki/`, `outputs/`, or another local convention) instead of imposing generic entity/concept directories.
4. Search for the source URL/video ID, title, and relevant concepts before creating anything.

For ingestion:

1. Capture a structured raw source with provenance and an evidence-grounded summary; transcripts are evidence, not the default saved output. Record caption/extraction source, language, coverage, mirrors or `captured_via`, and quality caveats when relevant.
2. Deduplicate before writing. If the source already exists, report its path and only enrich it when explicitly requested.
3. Update existing topic pages before creating new ones. Create a durable page only when the source is central to it or the concept recurs across sources.
4. Preserve local taxonomy/frontmatter/wikilink conventions, update actual page counts from the filesystem/list rather than guessing, and append only real changes to `log.md`.
5. Raw source bodies are immutable after ingest, but an explicitly requested maintenance pass may move or rename them without changing the body: repair inbound paths, log the move, and verify destinations and references.
6. Verify the raw note, modified topic pages, indexes, and inbound references before reporting success. Ask before an ingest that would modify 10 or more existing pages.

### Prediction-market lookup

Use market data to answer questions about forecasted probabilities, not as ground truth. Report market title, probability/price, liquidity/volume if available, and timestamp.

### Consumer hardware and product comparisons

For current hardware buying advice, gather current pricing and benchmarks from multiple sources, then synthesize around the user's actual tradeoff (performance per euro, form factor, noise, Linux/support, upgradeability, warranty). Prefer concise recommendation tables and clearly distinguish final reviews from leaks or pre-release benchmarks. For small-form-factor gaming PC comparisons, see `references/consumer-hardware-small-form-factor-gaming.md`.

### Research paper writing handoff

When moving from reconnaissance to manuscript work, create an outline with claims, experiments, baselines, figures/tables, citation gaps, and target venue constraints.

### Publication paper production

For end-to-end ML/AI paper work, treat writing as an iterative research loop: target venue constraints (NeurIPS/ICML/ICLR/ACL/AAAI/COLM), literature review, experiment design, execution/monitoring, statistical analysis, manuscript drafting, self-review, revision, and submission packaging. Maintain citation provenance, figure/table plans, ablation/baseline checklists, and reviewer-style critique before finalizing. The archived `research-paper-writing` package preserves the detailed venue templates and checklists.

## Verification

- Include source links/IDs for factual claims.
- Distinguish current market prices from real-world outcomes.
- For monitoring, show what was checked and what changed.
- For knowledge bases, confirm written note paths and distinguish attributed source claims from independently verified facts.
- During lint or maintenance, review synthesized pages and indexes—not immutable raw bodies—for obvious typos, accidental repetition, broken prose, unclear headings, or unintended language mixing. Report findings before broad edits and preserve genuine disagreements rather than silently overwriting them.

## Archived source packages

Former source-specific research skills were consolidated here. Archived packages preserve exact scripts/templates for recovery if needed.
