---
name: document-processing
description: "Convert PDF and Office documents to Markdown or text."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [documents, pdf, markdown, ocr, office, conversion, extraction]
---

# Document conversion

Run helpers from this skill directory:

- PDF to Markdown: `bash scripts/run_pdf_to_markdown.sh "input.pdf"`.
- Non-PDF office/document to Markdown: `bash scripts/run_document_to_markdown.sh "input.docx"`.

The helpers bootstrap separate runtimes in `.runtime/office` and `.runtime/pdf`; the PDF converter requires a working Java runtime. Both support `--output`. Check the destination first because an explicit output may overwrite it. Honor the user's destination; otherwise choose a sibling `.md`, using an unused `.converted.md` or numbered name if necessary.

Preserve extracted structure and wording unless a rewrite is requested. Add source metadata or extraction caveats only when useful. Inspect the output for completeness before delivery.

If PDF conversion fails, use `python3 scripts/extract_pymupdf.py "input.pdf"` for text extraction (`--metadata` returns metadata only). For scanned or complex content, consult the `ocr-and-documents` skill and use `scripts/extract_marker.py` when appropriate. Use a working isolated environment for missing dependencies. Label flattened tables, missing figures and partial extraction honestly.

PDF creation, forms, splitting, merging and editing belong to `pdf`; Word authoring to `docx`; spreadsheet editing to `xlsx`. This skill handles conversion, not those editing workflows.
