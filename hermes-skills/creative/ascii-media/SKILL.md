---
name: ascii-media
description: "Use when creating terminal/text-art media: static ASCII banners, decorative text blocks, image-to-ASCII conversions, or animated ASCII video/GIF/MP4 visualizers."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [ascii, text-art, video, animation, terminal-art, creative]
    related_skills: [excalidraw, manim-video, pixel-art]
---

# ASCII Media

## Overview

This umbrella covers ASCII/text-art output across static and animated forms. Use one decision tree instead of separate skills for banners, cowsay/boxes, image-to-ASCII, pre-made ASCII art, generative ASCII animation, audio-reactive visualizers, and video-to-ASCII conversion.

## When to Use

- User asks for ASCII art, text art, terminal art, Unicode box/block drawings, banners, cowsay, decorative borders, QR/weather ASCII, or image-to-ASCII.
- User asks for ASCII video, animated terminal-style MP4/GIF, audio-reactive ASCII visualizers, lyrics/text overlays, or retro text animation.
- User wants a creative text-art artifact and did not specify a different medium.

## Decision Tree

1. **Static text banner** → use `pyfiglet` locally; fall back to `https://asciified.thelicato.io/api/v2/ascii` when no install is desired.
2. **Speech/thought bubble** → use `cowsay`/`cowthink` and pick a character (`tux`, `dragon`, `stegosaurus`, etc.).
3. **Decorative framed text** → use `boxes`; optionally pipe figlet output into it.
4. **Image to ASCII** → use `ascii-image-converter` for color/Braille/URL support; `jp2a` is a lightweight JPEG-only fallback.
5. **Pre-made subject art** → fetch `https://ascii.co.uk/art/<subject>` and extract `<pre>` blocks; preserve artist signatures.
6. **Animated/video output** → build a self-contained Python + NumPy/Pillow/ffmpeg pipeline: input/analyze → scene function → tonemap → shader → encode.
7. **Audio-reactive output** → extract FFT/bands/beats, drive scene parameters per frame, and mux original or generated audio via ffmpeg.

## Static ASCII Recipes

```bash
python3 -m pyfiglet "HERMES" -f slant
python3 -m pyfiglet --list_fonts
curl -s "https://asciified.thelicato.io/api/v2/ascii?text=Hello&font=Slant"
echo "Hello" | boxes -d stone
cowsay -f dragon "Rawr!"
curl -s "qrenco.de/https://example.com"
```

Image conversion:

```bash
ascii-image-converter image.png -C -d 80,40
ascii-image-converter image.png -b --save-txt out
jp2a --width=80 --colors image.jpg
```

## Animated ASCII Pipeline

Use a single project script and render test frames before full encoding.

```
INPUT → ANALYZE → SCENE_FN → TONEMAP → SHADE → ENCODE
```

Recommended stack: Python 3.10+, NumPy, Pillow, SciPy for audio, ffmpeg CLI, optional OpenCV. Default output targets: MP4 (H.264), GIF (lower resolution), or PNG sequence.

### Creative Standard

Before coding, articulate: mood, visual story, color world, character texture, and the one thing making this project unique. Avoid flat black backgrounds and one-effect videos. Compose multiple grids/layers, vary scenes over time, and include at least one deliberate transition or visual moment the user did not explicitly ask for.

### Core Implementation Notes

- Use adaptive `tonemap()` instead of linear brightness multipliers; ASCII-on-black is otherwise too dark.
- For macOS Pillow, prefer `font.getmetrics()` for cell height; `textbbox()` can underreport.
- Do not pipe long-running ffmpeg `stderr` into memory; redirect to a log file to avoid deadlocks.
- Validate Unicode palettes in the target font; some glyphs render blank.
- For segmented videos, render clips separately, then concatenate/mux so failed sections can be re-rendered.

## Verification Checklist

- [ ] Static art respects monospace width and line length constraints.
- [ ] For generated/converted images, dimensions and contrast are readable in the target chat/terminal.
- [ ] For videos, render key test frames first and inspect brightness/coherence before full encode.
- [ ] Verify output file exists, is non-empty, and opens with `ffprobe`/`ffmpeg -i` or equivalent.
- [ ] Preserve source attribution/signatures for fetched pre-made ASCII art.
