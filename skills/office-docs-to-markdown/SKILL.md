---
name: office-docs-to-markdown
description: Convert local office and document files into Markdown, excluding PDFs. Use when the user asks to convert DOCX, PPTX, XLSX, HTML, CSV, JSON, XML, EPUB, or similar local files into Markdown.
---

# Office Docs To Markdown

Use this skill to convert a local file into reusable Markdown in any workspace.

Default behavior:

- Use the office-document converter runtime provided by this skill.
- Do not use this skill for PDF input. Route PDF conversion to `pdf-to-markdown`.
- Write the final Markdown next to the source file unless the user provides a destination.
- Keep the converted body as close as possible to raw output.
- Add a metadata block at the top, but avoid rewriting the document into a separate summary structure unless the user explicitly asks for that.

## Workflow

1. Verify the source file exists and is a local path.
2. Infer the file type from the extension and fail clearly if the file is obviously unsupported or is a PDF.
3. Run `bash scripts/run_document_to_markdown.sh "<source-path>"` from this skill directory to get the raw conversion.
4. Inspect the raw Markdown before writing anything. If the conversion fails, is empty, or is clearly unusable, stop and report the failure.
5. Build the final Markdown by prepending a metadata block when source metadata is available, then keep the converter output body substantially intact.
6. Apply only minimal cleanup when needed for readability:
   - normalize an obviously bad title derived from the filename if better metadata is unavailable
   - remove accidental leading or trailing empty noise
   - keep page breaks, lists, headings, and extracted wording unless the user asks for a rewrite
   - add a short note only when a conversion caveat is important enough that the raw body would otherwise be misleading
7. Default the output path to a sibling Markdown file with the same basename as the source file.
8. If that sibling Markdown file already exists, write to a deterministic non-destructive fallback path by appending `.converted` before `.md`.
9. If the user provides an output file or folder, honor it instead of the default sibling path.
10. Do not write a partial output file when conversion fails.

## Output Rules

- Keep the final output generic. Do not assume any Obsidian, wiki, or vault layout.
- If metadata such as title, author, or source is unavailable, omit it or derive a sensible fallback from the filename.
- Preserve the converter's headings, lists, ordering, spacing, and wording as much as possible.
- Do not compress, summarize, or reorganize the document by default.
- The default result should look like raw converter output with metadata prepended, not like a separate editorial summary.
- When the user explicitly asks for a summary or cleaned rewrite, that is a different mode and should be treated as an override.

## Command

```bash
bash scripts/run_document_to_markdown.sh "/absolute/path/to/source.docx"
```

Optional output override for raw dumps:

```bash
bash scripts/run_document_to_markdown.sh "/absolute/path/to/source.docx" --output "/absolute/path/to/output.md"
```

## Notes

- The helper script bootstraps its own isolated environment and does not assume a global converter install.
- Prefer `uv` if available; otherwise use `python3 -m venv`.
- The bundled runtime installs and pins its dependencies automatically.
- Keep v1 narrow: do not add alternate converters or manual fallback extraction logic.
