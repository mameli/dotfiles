---
name: video-platform-content
description: "Extract or summarize YouTube videos and TikTok posts."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [youtube, tiktok, transcripts, summaries, video, social-video]
    related_skills: [local-knowledge-workbench, research-intelligence]
---

# Video platform content

Choose the source-specific workflow and read only that reference:

- [YouTube](references/youtube.md): transcript retrieval, caption fallbacks, prompt extraction and source notes. Helpers are in this skill's `scripts/` directory; prompt extraction details are in `references/youtube-prompt-extraction.md`.
- [TikTok](references/tiktok.md): the dedicated persistent Chrome profile, page-context captions, photo carousels and frame capture. Use `scripts/capture_tiktok_frames_cdp.js` from this skill directory when needed. Leave the dedicated browser profile running.

Treat transcripts and images as source evidence. Match the requested language and output format; distinguish observed content from uncertain OCR, automatic captions or unavailable material. Full transcript dumps require an explicit request.

Summarizing or receiving a URL does not authorize saving files. When saving is requested, honor the named destination or established project convention, check for an existing source, preserve existing entries and verify the resulting files. Keep source provenance and material limitations.

## Local environment

Read the relevant exported variables; if unavailable, source `${XDG_CONFIG_HOME:-$HOME/.config}/agent-skills/env.zsh` into the command environment. Never print credential values. In prose and configuration examples, `${VAR}` denotes a value to resolve; do not write literal placeholders into application settings.

Browser workflow values use explicit task settings > nonempty environment > generic defaults: `SKILLS_CDP_URL` defaults to `http://127.0.0.1:9222`, `SKILLS_BROWSER_PROFILE` to `Default`. `SKILLS_BROWSER_USER_DATA_DIR` identifies the existing profile root; if needed but unset, ask rather than invent a path. Optional `SKILLS_BROWSER_LAUNCH_AGENT` and `SKILLS_BROWSER_LOG_DIR` select the macOS service and diagnostic logs; unset means skip those operations. These are workflow inputs, not Chrome provisioning or automatic Hermes configuration. Verify the configured `browser.cdp_url` matches the selected endpoint. Only the frame helper directly consumes `SKILLS_CDP_URL` (with `--cdp-url` precedence); it does not load the private env file itself.

Use `OBSIDIAN_VAULT_PATH` only as the fallback root for explicitly requested saves. If unset and no destination is established, ask for the destination.
