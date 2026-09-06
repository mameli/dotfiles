---
name: baoyu-visual-content
description: "Use when generating Baoyu-style educational visual content: article illustrations, knowledge comics, or structured infographics with image_generate and reproducible prompt files."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [baoyu, visual-content, image-generation, infographic, comic, article-illustration]
    related_skills: [ascii-media, pixel-art, powerpoint]
---

# Baoyu Visual Content

## Overview

This umbrella consolidates the Baoyu visual-generation workflows. They share the same operating model: analyze source content, choose a visual form, write reproducible prompt files, generate images with Hermes `image_generate`, download returned URLs to deterministic local paths, and report the artifacts created.

Use this as the entry point for three deliverable classes:

| Deliverable | Former narrow workflow | Best for |
|---|---|---|
| **Article illustrations** | `baoyu-article-illustrator` | Adding multiple concept visuals to an existing article at chosen positions |
| **Knowledge comics** | `baoyu-comic` | Educational/biography/tutorial narratives with panels, characters, pages |
| **Infographics** | `baoyu-infographic` | Single high-density visual summaries, maps, matrices, timelines, dashboards |

## When to Use

- User says: "illustrate this article", "add images", "为文章配图".
- User asks for a knowledge comic, educational comic, biography comic, tutorial comic, Logicomix-style output, or "知识漫画".
- User asks for an infographic, visual summary, information graphic, "信息图", "可视化", or high-density information poster.

## Shared Workflow

1. **Intake and safety**
   - Accept pasted text, file paths, URLs, and optional reference image paths.
   - Strip secrets/API keys/tokens before writing source-derived files.
   - If reference images are supplied, use `vision_analyze` to extract style/palette/composition traits in text; `image_generate` is prompt-only and cannot consume reference images directly.

2. **Analyze content**
   - Identify topic, purpose, audience, source language, user language, data/argument structure, and visual opportunities.
   - Write `analysis.md` in the output directory before prompt generation.

3. **Choose deliverable and options**
   - Article illustrations: type × style × palette; density can be minimal/balanced/per-section/rich.
   - Knowledge comics: art style × tone × layout × aspect; decide review gates and recurring character needs.
   - Infographics: layout × style × aspect; choose from the content structure and user keywords.

4. **Create reproducibility records before generation**
   - Every image must have a saved prompt markdown file before calling `image_generate`.
   - Prompts include YAML/frontmatter or structured sections recording selected options, labels, source data, and reference-image traits.

5. **Generate and download**
   - Call `image_generate(prompt=..., aspect_ratio=landscape|portrait|square)`.
   - Map custom ratios to the nearest enum; do not claim backend/model selection.
   - Download returned image URLs via `curl -fsSL "<url>" -o "<absolute-output-path>"` and verify non-empty files.

6. **Finalize**
   - Article illustrations: insert markdown image links after target paragraphs.
   - Comics: report storyboard/prompts/pages/character sheet locations.
   - Infographics: report layout/style/aspect/language and output path.

## Deliverable-Specific Sections

### Article Illustrations

Output layout usually follows:

```
{article-dir}/imgs/
├── outline.md
├── prompts/NN-{type}-{slug}.md
└── NN-{type}-{slug}.png
```

Default types: `infographic`, `scene`, `flowchart`, `comparison`, `framework`, `timeline`. Select positions where an image clarifies an argument, visualizes a framework, preserves concrete data, or breaks up a dense section. Do not illustrate metaphors literally; visualize the underlying concept.

### Knowledge Comics

Output layout usually follows:

```
comic/{topic-slug}/
├── source-{slug}.md
├── analysis.md
├── storyboard.md
├── characters/characters.md
├── characters/characters.png
├── prompts/NN-{cover|page}-{slug}.md
└── NN-{cover|page}-{slug}.png
```

Use text descriptions from `characters/characters.md` inside every page prompt. The optional PNG character sheet is a human review/regeneration artifact, not an input to `image_generate`. Ask confirmation for style/focus/audience/review gates when not already specified.

### Infographics

Output layout usually follows:

```
infographic/{topic-slug}/
├── source-{slug}.md
├── analysis.md
├── structured-content.md
├── prompts/infographic.md
└── infographic.png
```

Choose a layout based on structure: timeline/process → `linear-progression`; comparison → `binary-comparison`/`comparison-matrix`; metrics → `dashboard`; overview → `bento-grid`; categories → `tree-branching`/`periodic-table`; cycles → `circular-flow`; high-density guides → `dense-modules`.

## Hard Pitfalls

- **Prompt files first.** Never generate an image before writing the exact prompt file.
- **Absolute download paths.** Avoid `curl -o relative.png`; persistent shell CWD can drift between tool calls.
- **Data integrity.** Statistics and labels copied from the source must stay exact.
- **Reference images are textual traits only.** Use `vision_analyze`; do not pretend the image model receives the image.
- **One clarify question at a time.** Skip already-specified options; do not ask a long questionnaire when a reasonable default is obvious.
- **Backup before regenerating.** Rename existing prompt/image files with `-backup-YYYYMMDD-HHMMSS` before overwriting.

## Verification Checklist

- [ ] Source/analysis and all prompt files are saved.
- [ ] Every generated image URL was downloaded to an absolute path and verified non-empty.
- [ ] Output language follows user/source-language rules.
- [ ] Source data, labels, and quotes remain faithful.
- [ ] Final report names files created and any skipped/failed generations.
