---
name: creative-generative-production
description: "Class-level workflow for production-grade generative visual systems: ComfyUI image/video/audio pipelines, Manim educational animations, and TouchDesigner real-time/MCP visuals."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [creative, generative-ai, video, animation, comfyui, manim, touchdesigner, real-time-visuals]
---

# Creative Generative Production

Use this umbrella when the user asks for generated visuals or programmatic creative systems that require more than a single `image_generate` call: image/video/audio workflows, 3Blue1Brown-style explanatory animations, real-time TouchDesigner scenes, audio-reactive visuals, or repeatable batch rendering.

## Default workflow

1. Identify the creative output class: still image, video, educational animation, real-time installation, VJ/audio-reactive patch, or batch render.
2. Choose the engine:
   - **ComfyUI** for node-based diffusion, video/audio/3D pipelines, model/node management, and repeatable REST/WebSocket workflow execution.
   - **Manim** for explanatory/math/algorithm animations where visual pedagogy and rendered scenes matter.
   - **TouchDesigner + MCP** for live, interactive, audio-reactive, projection, GLSL, or installation-style visuals.
3. Check prerequisites before building: local GPU/VRAM vs cloud, installed binaries, server/MCP health, Python/LaTeX/ffmpeg, and target output resolution.
4. Start from the smallest runnable scene/workflow. Verify with a health check or first render before scaling.
5. Preserve reusable workflows, templates, prompts, or scene scripts as files and report exact output paths.

## Labeled playbooks

### ComfyUI workflow execution

Use ComfyUI for diffusion workflows with explicit parameter injection and dependency checks. Prefer official `comfy-cli` for install/lifecycle and REST/WebSocket API for execution. Before running a template, inspect workflow format, missing nodes/models, and controllable parameters. For cloud runs, account for authentication, redirects, concurrency limits, and resolution/VRAM ceilings.

### Manim educational animation

Use Manim when the output is an explanatory video, concept visualization, equation derivation, algorithm walkthrough, architecture diagram, or data story. Plan the narrative arc before code. Render early, inspect the output, then tune timing, opacity hierarchy, color palette, and camera framing. Geometry before algebra; pauses after key reveals are part of the explanation.

### TouchDesigner real-time visual systems

Use TouchDesigner/twozero MCP for real-time visuals. Never guess TouchDesigner parameter names: query operator parameter info first. Prefer native MCP tools over broad Python execution; if an attribute error occurs, inspect the operator before continuing. Use relative paths in callbacks, verify the MCP hub on port 40404, and respect Non-Commercial resolution caps.

## Verification

- For ComfyUI: include server/cloud health status, workflow path, dependency check result, and output media path.
- For Manim: run at least a low-quality render first; include render command and output file path.
- For TouchDesigner: call a health/error check after building and report the network/operator path created.
- For any media artifact: confirm the file exists and is viewable/analyzable before finalizing.

## Archived source packages

The former tool-specific skills (`comfyui`, `manim-video`, and `touchdesigner-mcp`) were consolidated here. Their full packages, including scripts, references, tests, and workflows, are archived recoverably for deep tool-specific restoration if needed.
