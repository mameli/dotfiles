---
name: whisper-audio-transcriber
description: Use when you need to transcribe a local audio file with whisper-cpp. The skill creates a timestamped folder next to the source audio, copies the original file there, converts it to a Whisper-friendly WAV, and writes a plain-text transcript. Default language is Italian; optionally force English.
---

# Whisper Audio Transcriber

Use this skill for one-off local transcriptions with `whisper-cli` and `ffmpeg`.

Default language is Italian. Use English only when the source audio is clearly in English.

## Workflow

1. Confirm the input audio path.
2. Run `scripts/transcribe_audio.sh` with the audio path.
3. By default, do not pass a language flag, so the script uses Italian.
4. If the user says the audio is in English, pass `--language en`.
5. Return the output folder path and the transcript path.

## Command

Italian by default:

```bash
/Users/mameli/.codex/skills/whisper-audio-transcriber/scripts/transcribe_audio.sh /absolute/path/to/file.m4a
```

Force English:

```bash
/Users/mameli/.codex/skills/whisper-audio-transcriber/scripts/transcribe_audio.sh --language en /absolute/path/to/file.m4a
```

Optional model override:

```bash
/Users/mameli/.codex/skills/whisper-audio-transcriber/scripts/transcribe_audio.sh --model /Users/mameli/Ai_models/ggml-medium.bin /absolute/path/to/file.m4a
```

## Output Layout

The script creates a folder next to the source file with this naming pattern:

```text
YYYY-MM-DD_HH-MM_file-name/
```

Inside it, write:

- the original audio file
- `*_whisper.wav` converted to `mono`, `16 kHz`, `pcm_s16le`
- `*_transcript.txt` as plain text

## Requirements

- `ffmpeg`
- `whisper-cli`
- a local GGML model, defaulting to `/Users/mameli/Ai_models/ggml-medium.bin` when present

If the default model is missing, pass `--model`.

## Notes

- Keep the transcript as plain text only. Do not request subtitle output unless the user asks.
- If the input audio is already WAV, still place all generated files inside the timestamped folder.
- If language is not specified by the user, use Italian.
