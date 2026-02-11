---
name: markdown-to-pdf-export
description: Convert Markdown files to PDF with Pandoc using consistent XeLaTeX settings (margin 1.2cm, font size 10pt, line stretch 0.95). Use when a user asks to export or render `.md` content as `.pdf`, especially for interview notes, reports, or technical documents that need compact formatting.
---

# Markdown to PDF Export

Use this skill to generate a PDF from a Markdown file with a fixed formatting profile.

## Workflow
1. Confirm `pandoc` and `xelatex` are available before converting.
2. Run `scripts/markdown_to_pdf.sh <input.md> [output.pdf]`.
3. If `output.pdf` is omitted, write next to the input file with the same basename.

## Command Profile
The script applies this conversion profile:
- `--pdf-engine=xelatex`
- `-V geometry:margin=1.2cm`
- `-V fontsize=10pt`
- `-V linestretch=0.95`

## Troubleshooting
- If `pandoc: command not found`, install Pandoc.
- If PDF generation fails with a LaTeX error, install a TeX distribution that includes `xelatex`.
- If the input path contains spaces, keep the path quoted.
