---
name: pdf-to-markdown
description: Convert local PDF files into Markdown. Use when the user asks to convert a PDF into Markdown.
---

# PDF To Markdown

Use this skill to convert a local PDF file into reusable Markdown in any workspace.

Default behavior:

- Use the PDF converter runtime provided by this skill.
- Accept only PDF input files.
- Write the final Markdown next to the source file unless the user provides a destination.
- Keep the generated Markdown as close as possible to the raw conversion.

## Workflow

1. Verify the source file exists, is local, and has a `.pdf` extension.
2. Run `bash scripts/run_pdf_to_markdown.sh "<source-path>"` from this skill directory.
3. Inspect conversion output before writing anything. If conversion fails, is empty, or is clearly unusable, stop and report failure.
4. Default output path to a sibling Markdown file with the same basename as the source PDF.
5. If that sibling Markdown file already exists, write to a deterministic non-destructive fallback path by appending `.converted` before `.md`.
6. If the user provides an output file or folder, honor it instead of the default sibling path.
7. Do not write a partial output file when conversion fails.

## Output Rules

- Keep output generic and portable; do not assume Obsidian-specific structure.
- Preserve headings, lists, ordering, and wording from conversion output as much as possible.
- Do not summarize or rewrite by default.

## Command

```bash
bash scripts/run_pdf_to_markdown.sh "/absolute/path/to/source.pdf"
```

Optional output override:

```bash
bash scripts/run_pdf_to_markdown.sh "/absolute/path/to/source.pdf" --output "/absolute/path/to/output.md"
```

## Notes

- The helper script bootstraps an isolated Python environment and does not assume a global converter install.
- Java must be available on the system path for the converter runtime.
