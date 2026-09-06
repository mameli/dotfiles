# Consolidated workbench notes

## Obsidian
- Resolve `OBSIDIAN_VAULT_PATH` first; quote vault paths because they often contain spaces.
- Read an existing note before modifying it and verify writes by reading back.
- For PDF imports, download with `curl -L`, save the original PDF in the vault, extract text (for example with `pypdf`), and create a Markdown note with provenance and wikilinks.
- For web enrichment, preserve the note's existing structure and append to the most relevant section.

## Jupyter live kernel
- Use only when persistent Python state is valuable; otherwise prefer one-shot scripts.
- Check for `uv`, JupyterLab, and an existing server before starting one.
- Use compact JSON output from helper scripts to save context.
- Keep local notebook servers unauthenticated only on localhost/headless trusted environments.

Full original packages were archived unchanged so detailed examples remain recoverable.