# Consolidated tool notes

## ComfyUI
- Use `comfy-cli` for install/lifecycle and REST/WebSocket API for execution.
- Check GPU/VRAM and decide local vs cloud before setup.
- Inspect workflow JSON for controllable params and missing nodes/models before running.
- For official templates, convert editor format to API format carefully; Reroute nodes and dotted dynamic-input keys are common pitfalls.

## Manim
- Use for educational/math/algorithm animations.
- Start with narrative arc and the intended aha moment before coding.
- Verify with a low-quality render, then tune timing, opacity layering, palette, and camera framing.
- Requires Python, Manim CE, LaTeX, and ffmpeg.

## TouchDesigner/twozero MCP
- Query operator hints/parameter info before setting parameters; do not trust guessed names.
- Prefer native MCP tools over broad `td_execute_python`.
- Use relative paths in callbacks and verify hub health on `127.0.0.1:40404`.
- Non-Commercial TouchDesigner has resolution caps.

Full original packages were archived unchanged so support files remain recoverable.