## YouTube Workflow

Default philosophy: use transcripts as evidence, not as a verbatim dump. Unless the user explicitly asks for a full transcript, produce structured notes/summaries with timestamps and provenance.

Persistence is opt-in: a bare YouTube URL, a request to summarize/analyze, or activity inside a YouTube Telegram topic does not authorize creating or modifying files. Save only when the user explicitly asks to save/add/archive/store the content or explicitly names a destination to update.

### Fetch transcript

A helper script is available at `scripts/fetch_transcript.py`:

```bash
python3 SKILL_DIR/scripts/fetch_transcript.py "https://youtube.com/watch?v=VIDEO_ID"
python3 SKILL_DIR/scripts/fetch_transcript.py "URL" --text-only --timestamps
python3 SKILL_DIR/scripts/fetch_transcript.py "URL" --language it,en
```

If the helper dependency is missing, install `youtube-transcript-api` and retry. Without `--language`, the helper selects an available manual track, otherwise an automatic track; it does not force English. Explicit language codes are tried in order; if no match is found, retry without a language constraint. JSON includes actual `language`, `is_generated`, timed `segments`, `segment_count`, `duration` and `full_text`; `--timestamps` adds `timestamped_text`. IDs must be exactly 11 valid characters; malformed IDs are rejected, never truncated.

Offline helper regressions: `PYTHONDONTWRITEBYTECODE=1 python3 SKILL_DIR/scripts/test_fetch_transcript.py`.

### Transform formats

Supported outputs: concise summary, timestamped chapters, chapter summaries, structured source note, X/Twitter thread, blog post, quotes with timestamps, prompt/system-prompt extraction, or full transcript only on explicit request.

For a bare YouTube link with no instruction, default to a concise summary in the user's language and keep it in chat; do not persist it. For structured notes, adapt sections to the domain and destination—for example travel implications and places to verify, cooking techniques and safety notes, or gameplay advice—and omit empty boilerplate sections.

For save/archive requests, default to a structured source note with frontmatter (`source`, `video_id`, `channel`, `duration`, `transcript_language`, `transcript_source`, `saved`) and sections such as Summary/Riassunto, Source/Fonte, Chapters/Capitoli, chapter synthesis, main ideas, takeaways, useful quotes, caveats, and quality flags. Treat vague requests to save the video's “content” as a request for this structured summary, not a transcript dump. For a batch, create and verify one structured summary note per video; when the user requests separate chat messages, deliver one self-contained result per video rather than merging the batch.

### Prompt / system-prompt extraction

When the user asks for prompts, system prompts, or instructions from a video, produce the requested summary plus the prompt material. Do not rely only on transcript paraphrase when the video references a public tool/package: check upstream artifacts where practical (GitHub, npm package tarballs, README, bundled `SKILL.md`, command files, instruction builders). Clearly label whether each prompt is directly quoted from the transcript, reconstructed from the video, or taken from an authoritative source file. See `references/youtube-prompt-extraction.md` for the workflow and npm-package probe pattern.

### Fallbacks

If `youtube-transcript-api` fails but captions appear available, inspect `yt-dlp --dump-json --skip-download URL` for `subtitles` and `automatic_captions`. Prefer `json3` timedtext URLs, fetch them directly with a browser User-Agent, and parse `events[].segs[].utf8` with `events[].tStartMs` timestamps. Do not stop at `yt-dlp --write-auto-subs` HTTP 429; metadata often still contains usable signed caption URLs.


## Save/Destination Policy

Enter this save workflow only after explicit save intent. Follow the user's named destination or an unambiguous established project convention; do not infer permission to write merely because a vault, project, or Telegram topic is active. Do not assume all YouTube content belongs in `_Wiki/raw/youtube/`. When updating an index or combined note, read the existing list and end section first, preserve prior entries, update counts from the actual list, and verify after patching.

### Wiki ingest: dedupe and governance first

When a user says only “add/save this” and the established destination is a maintained local wiki:

1. Resolve the canonical YouTube URL and `video_id` from metadata.
2. Before creating a raw note, search the wiki for the exact `video_id`, canonical URL, and distinctive title. A previously ingested source may have a different filename or title.
3. If the video already exists, do **not** create a duplicate or rewrite its raw note. Tell the user it is already saved and give the existing path; only enrich it if they explicitly request an update.
4. Read the wiki's local agent/governance file before any write. Follow its raw/wiki/index/log conventions, update existing topic pages before creating new ones, and record only actual file changes in the operation log.
5. For a new video, create a structured source note (not a transcript dump), then update only the relevant durable topics and indexes. Re-read the created source and verify inbound references before reporting success.

