---
name: vtt-transcript-reader
description: Use when a user provides or references a local .vtt/WebVTT transcript and wants it cleaned, rewritten, summarized, or converted into article-style study prose with optional Q&A.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [vtt, transcripts, webvtt, study-notes, article]
    related_skills: [youtube-content, pdf-to-markdown, obsidian]
---

# VTT Transcript Reader

## Overview

Use this skill to read a local `.vtt` / WebVTT transcript, validate that it parsed cleanly, and turn the cue text into readable prose. The bundled parser strips WebVTT timing lines, cue identifiers, tags, and HTML entities while preserving cue order.

The default output is a well-structured study article: continuous prose, clear headings, concept-level subtitles, and a `Questions and Answers` chapter only when explicit questions appear in the source material.

## When to Use

Use this skill when the user:

- uploads a `.vtt` file and asks to “trascrivere”, “ripulire”, “riassumere”, “convertire”, “studiare”, or “fare una nota”
- provides a local path to a `.vtt` transcript
- wants timestamp-free prose from captions/subtitles
- wants structured article-style notes from meeting, lesson, webinar, interview, or YouTube subtitle exports
- asks whether parsing was complete or whether any cues were lost

Do not use this skill for:

- live audio/video transcription from media files — use a speech-to-text/Whisper workflow instead
- direct YouTube URL transcript fetching — use `youtube-content` first, then this skill only if you already have a `.vtt` file
- PDF/document extraction — use the relevant document skill first

## Workflow

1. **Validate the input**
   - The input path must exist and point to a local file.
   - The file should end with `.vtt`.
   - If the user uploaded the document through a chat gateway, use the saved local path from the attachment metadata.

2. **Run parser stats first**

   ```bash
   python3 SKILL_DIR/scripts/parse_vtt.py "/absolute/path/to/file.vtt" --stats-only
   ```

3. **Check completeness**
   - Verify `cue_count == consumed_count`.
   - Report parsing loss explicitly before rewriting if they differ.
   - Note `empty_cues` if it is non-zero, but do not treat empty cues as a failure by itself.

4. **Extract clean text**

   ```bash
   python3 SKILL_DIR/scripts/parse_vtt.py "/absolute/path/to/file.vtt" --format text
   ```

   For structured inspection, use JSON or JSONL:

   ```bash
   python3 SKILL_DIR/scripts/parse_vtt.py "/absolute/path/to/file.vtt" --format json
   python3 SKILL_DIR/scripts/parse_vtt.py "/absolute/path/to/file.vtt" --format jsonl
   ```

5. **Transform according to the request**
   - If the user asks for plain cleanup, return cleaned text.
   - If the user asks for a summary, produce the requested summary style.
   - If the user asks for notes/study material and gives no other format, default to the article format below.
   - Do not write files unless the user explicitly asks.

6. **Chunk long transcripts**
   - If clean text is too large for a single response, split into overlapping chunks.
   - Summarize or rewrite each chunk first, then merge into one coherent final output.
   - Preserve the original order of concepts.

## Default Article Output

When the user asks for a readable transformation without specifying a detailed format, produce chat-only article prose.

Rules:

- Keep the output language aligned with the source transcript unless requested otherwise.
- Write complete paragraphs, not bullet lists, unless the user specifically asks for bullets.
- Use Markdown headings for structure:
  - `##` for major sections
  - `###` for concept-level subtitles
- Preserve actual explanations and argument flow; do not collapse everything into a very short summary unless requested.
- Do not output speaker labels.
- Do not output timestamps.
- Do not output raw transcript/cue blocks.
- Do not use meeting/transcript framing phrases such as “the discussion starts”, “in the conversation”, “during the meeting”, or “the transcript explains”.
- Mark missing facts as `Not specified in source material` instead of inventing them.

Suggested structure:

```markdown
## <Concise descriptive title>

### <First concept subtitle>

<Full prose explanation.>

### <Second concept subtitle>

<Full prose explanation.>

## Questions and Answers

Question: <Question from the source material.>

Answer: <Answer in full prose.>

## Closing

<Short closing paragraph with follow-ups or next steps, only when present in the source.>
```

Only include `Questions and Answers` when explicit questions appear in the source content. Omit the chapter entirely when there are no questions.

Only include `Closing` when the source contains genuine conclusions, follow-ups, decisions, or next steps. Otherwise omit it.

## Command Reference

```bash
# Stats for completeness checks
python3 SKILL_DIR/scripts/parse_vtt.py "/absolute/path/to/file.vtt" --stats-only

# Text only: cleaned cue text, one line per non-empty cue
python3 SKILL_DIR/scripts/parse_vtt.py "/absolute/path/to/file.vtt" --format text

# Full structured JSON
python3 SKILL_DIR/scripts/parse_vtt.py "/absolute/path/to/file.vtt" --format json

# One JSON object per cue
python3 SKILL_DIR/scripts/parse_vtt.py "/absolute/path/to/file.vtt" --format jsonl
```

Replace `SKILL_DIR` with the path reported by `skill_view(name='vtt-transcript-reader')`.

## Common Pitfalls

1. **Skipping the stats check.** Always run `--stats-only` before rewriting so parsing problems are caught early.

2. **Treating cue count as word count.** `cue_count` counts WebVTT cues, not lines, paragraphs, or sentences.

3. **Outputting timestamps by habit.** The default transformation is timestamp-free prose. Include timestamps only if the user asks.

4. **Adding speaker labels not present in the source.** Do not infer speakers unless the cue text itself reliably contains them.

5. **Inventing missing context.** If the transcript references slides, gestures, screens, or missing attachments that are not in the text, say `Not specified in source material`.

6. **Over-summarizing study prose.** When the requested output is article-style notes, preserve explanations and conceptual flow instead of reducing the material to a few bullets.

## Verification Checklist

- [ ] Input path exists and ends with `.vtt`
- [ ] Parser stats were run before content extraction
- [ ] `cue_count == consumed_count` or parsing loss was reported
- [ ] Clean text is non-empty
- [ ] Output format matches the user’s request
- [ ] Default article output has headings and coherent prose
- [ ] No timestamps, cue blocks, or speaker labels appear unless requested
- [ ] Missing facts are not invented
