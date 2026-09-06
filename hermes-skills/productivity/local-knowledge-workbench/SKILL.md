---
name: local-knowledge-workbench
description: "Class-level workflow for local personal knowledge and exploratory workbench tools: Obsidian vault operations and stateful Jupyter/Python kernels."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [obsidian, jupyter, notes, knowledge-base, data-science, local-workflow, python]
---

# Local Knowledge Workbench

Use this umbrella when work centers on the user's local knowledge base or an iterative analysis workspace: reading/writing Obsidian notes, importing documents into a vault, enriching notes from web sources, or using a live Jupyter kernel for stateful Python exploration.

## Default workflow

1. Identify whether the task is **knowledge-base work**, **stateful exploration**, or both.
2. Resolve local paths from environment and current system state rather than assuming defaults. Validate that the vault exists: environment variables and remembered paths may be stale after a rename. If a configured path is missing, discover candidate vaults locally and report any substitution explicitly.
3. Treat the vault filesystem as the source of truth. Do not depend on a cached index or third-party search CLI unless the user explicitly requests it and its freshness has been verified.
4. Prefer safe file operations: quote paths, preserve existing note structure, and verify writes by reading back the file. Before retrying after an interruption or timeout, inspect the real destination and deduplicate by exact filename plus a stable identifier such as canonical URL, video ID, or document ID.
5. When a user names or supplies an exact note path, inspect that source note directly before answering. Do not infer its contents from backlinks, wikilinks, search snippets, or another article that cites it. If the supplied mount path is unavailable, search the resolved vault root for the exact filename and state the path substitution explicitly.
6. For iterative Python, use a live Jupyter kernel only when persistent state is valuable; otherwise use a one-shot script or terminal command.
7. Report concrete artifacts: note paths, notebook/session IDs, generated files, and verification output.

## Labeled playbooks

### Obsidian vault operations

Resolve and validate `OBSIDIAN_VAULT_PATH` first, falling back to `~/Documents/Obsidian Vault` only when unset and that directory exists. If the configured path is missing, discover the current vault rather than creating content at a stale location.

Before creating or retrying a write, inventory the destination and inspect neighboring notes for naming/frontmatter/link conventions. Search by exact filename and stable source identifier (canonical URL, video ID, document ID) and update an existing note instead of duplicating it. After an interruption, timeout, or uncertain write, inspect the destination first; never replay the write blindly. When importing PDFs or web content, keep source files and extracted Markdown together, include provenance/frontmatter where useful, and verify the destination note exists.

#### Raw-source organization

When the user explicitly asks to organize or move notes under `raw/`:

1. Inventory only the notes at the requested folder level first (for example, Markdown files directly under `raw/`), then inspect each note’s metadata, title, and summary before assigning a category.
2. Prefer an existing domain folder; create a new folder only for a stable, meaningful category rather than a one-note label.
3. An explicit move request overrides the default preservation rule for raw sources: move files without changing their source content.
4. Search the vault for path-based references to every moved note. Update active source/frontmatter links and current outputs; leave append-only logs and historical maintenance reports unchanged, then append a new move record to the log.
5. Verify that no Markdown notes remain at the targeted loose level and that every moved file and updated reference resolves at its new path.

#### Bulk-edit and link safety

- Build the exact candidate file list before a bulk replacement or deletion; do not rewrite every textual match blindly.
- Treat `.excalidraw.md`, canvas/plugin state, embedded payloads, generated indexes, and other encoded or application-managed content as special formats. A matching byte sequence is not evidence of a semantic reference; skip it unless the structure can be parsed safely.
- For renames and moves, search both plain and URL-encoded path variants where applicable. Update active wikilinks, Markdown links, and frontmatter references, while preserving append-only historical logs unless a new correction entry is needed.
- Verify the final file count, destinations, and references programmatically after a bulk operation.

### Journal entries

When the user dictates or types a personal journal entry:

1. Resolve the requested date explicitly and inspect the established daily-note folder and filename pattern before writing.
2. Edit minimally: fix grammar, punctuation, transcription artifacts, obvious repetitions, and sentence boundaries while preserving the user's tone, level of informality, events, opinions, and emotional emphasis.
3. Normalize a misspelled proper noun only when context makes the intended name clear. Never invent missing facts, summarize away details, moralize, or add headings unless the existing journal format requires them; default to natural paragraphs without headings.
4. If the target note already exists, read it first and preserve unrelated content. Treat “add/append this” as an anchored append; overwrite or replace existing journal prose only when the user explicitly asks. After writing, read back the exact target. If iCloud returns `Resource deadlock avoided` or the file appears absent immediately after a write, hydrate/retry the same path and verify before creating a duplicate elsewhere.

### Travel vault workflow

Resolve the vault through `OBSIDIAN_VAULT_PATH` using the validation rules above, then discover its existing travel folder (for example `Viaggi/` or `Travel/`); these names are examples, not required directories. For general vault work, inspect the existing trip folder, main itinerary/guide, comparisons, and `raw/` sources first. Keep captured source material separate from synthesized plans. When asked to integrate new raw material, update the relevant durable guide (itinerary, hotel/location assessment, restaurants, transport, viewpoints, local dishes, less-visited places, or booking checklist), add the appropriate wikilink to the source, and verify both the source note and the integrated destination. Use `travel-itinerary-management` when the task requires itinerary reasoning or conflict resolution.

### Stateful Jupyter exploration

Use a live Jupyter kernel for iterative analysis, DataFrame/API exploration, or notebook-like work where variables should persist across steps. Check for `uv`, JupyterLab, and an existing server before starting one. Use compact JSON output from helper scripts when possible and keep notebook/server credentials local-only.

## Verification

- For Obsidian: read back the note or list the saved file path in the vault.
- For document imports: confirm both original source and Markdown/extracted text paths.
- For Jupyter: confirm server/session discovery, execute a small expression, and include the resulting notebook/session identifier.

## Archived source packages

The former `obsidian`, `obsidian-journal`, `viaggi-obsidian`, and `jupyter-live-kernel` skills were consolidated here or into the companion `travel-itinerary-management` skill. Their full archived packages preserve detailed command examples and helper scripts for recovery.
