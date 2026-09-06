---
name: ai-music-and-audio
description: Class-level workflow for songwriting, AI music generation, audio feature analysis, MusicGen/AudioGen, and Suno-like services.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [music, audio, songwriting, suno, heartmula, audiocraft, musicgen, audiogen, spectrogram]
---

# AI Music and Audio

Use this umbrella when the task involves writing songs, generating music or sound effects, crafting Suno/HeartMuLa prompts, running local MusicGen/AudioGen, or analyzing audio features such as spectrograms, chroma, MFCCs, and mel bands.

## Default workflow

1. Clarify the target output: lyrics, style prompt, generated audio, sound effect, analysis, or iteration notes.
2. Separate craft from tooling:
   - craft lyrics/melody/structure first;
   - then choose generation backend or analysis CLI;
   - then verify the resulting file or analysis output.
3. For generation, record prompt, tags/style, duration, model/backend, seed if available, and output path/URL.
4. For analysis, use objective features to support creative decisions rather than dumping raw numbers.
5. Deliver playable media with a concise explanation of what was created or measured.

## Labeled playbooks

### Songwriting and AI music prompts

Write lyrics with clear sections, singable phrasing, rhyme discipline, and emotional progression. For AI music services, include genre, tempo, instrumentation, vocal style, structure, production references, and negative constraints.

### HeartMuLa / Suno-like generation

Prepare three artifacts: lyrics, tags/style prompt, and generation request. Keep tags concise and non-conflicting. Save outputs and report the exact media handle returned by the service.

### AudioCraft / MusicGen / AudioGen

Use local AudioCraft for controllable text-to-music or text-to-sound when Python/GPU dependencies are available. Start with small models and short durations to verify the pipeline, then scale duration/model size. Watch for CUDA OOM, sample-rate mismatches, and long first-run downloads.

### Audio feature analysis

Use spectrogram/chroma/MFCC workflows when the user asks what an audio file contains, wants visualizations, or needs feature extraction for downstream ML/music work. Summarize perceptual meaning: rhythm density, tonal center, timbral brightness, sections, silence, and artifacts.

## Verification

- Confirm the generated or analyzed file exists and is non-empty.
- For generated audio, provide the playable media path/URL.
- For analysis, include a short interpretation plus the command or script used.
- For lyrics/prompts, include structured sections and generation-ready tags.

## Archived source packages

Former tool-specific audio/music skills were folded into this class-level workflow. Their archived packages preserve detailed backend snippets if a future task needs exact legacy examples.
