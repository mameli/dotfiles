---
name: youtube-to-obsidian-raw
description: Extract a YouTube video into a structured Markdown source note in an Obsidian vault `_Wiki/raw` folder using `yt-dlp`. Use when the user wants the video content captured as structured source material, not as a raw transcript dump and not as a direct wiki note.
---

# YouTube To Obsidian

Use this skill to turn a YouTube video into a structured source note inside `_Wiki/raw`. Do not default to saving a transcript dump, and do not create a note directly in `_Wiki/wiki`.

## Workflow

1. Confirm `yt-dlp` is available.
2. Create a temp directory and run `bash scripts/youtube_to_obsidian_bundle.sh "<youtube-url>" "<temp-dir>"`.
3. Read `manifest.json` and `transcript.txt` from that temp directory.
4. Inspect the vault structure and confirm `_Wiki/raw` exists.
5. Write one structured Markdown source note into `_Wiki/raw`, using the transcript as working material rather than as note content.
6. Do not create or update files in `_Wiki/wiki` unless the user explicitly asks for a wiki promotion step.
7. Only write a raw transcript file if the user explicitly asks for archival raw content.

## Output Rules

- Default to a structured raw note in `_Wiki/raw`.
- Do not put the transcript into the raw note.
- Do not add transcript links or transcript file references to the raw note unless the user explicitly asks for that.
- Preserve the source URL, channel, and publication date in the raw note.
- Include the video description when it adds context.
- Prefer subtitles in this order: Italian, English, then the first available language.
- Prefer manual subtitles over automatic captions when both exist.
- If no subtitles are available, still create the structured raw note from metadata and description.
- Match the destination note to the vault's existing raw/source conventions.
- The default structure should be a source-style note with:
  - opening summary
  - source section
  - main ideas
  - core argument or takeaways
  - useful concepts / links
  - limits and caveats
- The note should aim to preserve the substance of the full video in structured form, but without embedding the transcript itself.

## Command

```bash
tmp_dir="$(mktemp -d)"
bash ./scripts/youtube_to_obsidian_bundle.sh "https://youtu.be/VIDEO_ID" "$tmp_dir"
```

## Notes

- Use `bash scripts/youtube_to_obsidian_raw.sh` only when the user explicitly asks to preserve the raw transcript/source file.
- The bundle script is the default extraction path because it avoids cluttering the vault with intermediate transcript dumps.
- Auto-generated subtitles can be noisy or end abruptly. Treat them as evidence for structuring the raw note, not as note content to preserve.
