---
name: platform-cli-integrations
description: "Class-level workflow for external platform CLIs and lightweight APIs: email, X/Twitter, Yuanbao messaging, Tenor GIFs, and Philips Hue/OpenHue control."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [cli, api, integrations, email, social-media, messaging, tenor, hue, smart-home]
---

# Platform CLI Integrations

Use this umbrella when a task is best handled through a dedicated external platform CLI or small HTTP API rather than a first-class Hermes tool: email via Himalaya, X/Twitter via `xurl`, Yuanbao group/DM operations, Tenor GIF search/download, or Philips Hue control via OpenHue.

## Default workflow

1. Identify the platform and action: read/send/search, post/reply/DM, mention, GIF lookup/download, or device/scene control.
2. Check prerequisites without exposing secrets: installed command, required env vars, auth status, bridge/API reachability, and user/account scope.
3. Use the platform's safest narrow command first. Avoid verbose modes or commands that print tokens.
4. For side effects (send/post/DM/device control), verify the target and content before executing when ambiguity would matter.
5. Report the exact action taken plus platform IDs, URLs, output paths, or state verification where available.

## Labeled playbooks

### Email via Himalaya

Use Himalaya for IMAP/SMTP email from the terminal. Verify `himalaya --version`, discover accounts/folders, and respect config-path differences on macOS/XDG. For composition, use message/MML files and avoid printing credentials.

### X/Twitter via xurl

Use official `xurl` for X API v2 operations: posting, replying, search, timelines, likes, bookmarks, media upload, DMs, and raw endpoint access. Never read or print `~/.xurl`; verify only with `xurl auth status`. Do not use verbose mode or inline credential flags.

### Yuanbao groups and DMs

For Yuanbao group mentions, query members first to get the exact nickname, then include `@nickname` in the final response text; the gateway converts it into a real mention. For private messages, use the Yuanbao DM tool with the target name and message, then report result status.

### Tenor GIF search/download

Use Tenor API with `TENOR_API_KEY`, `curl`, and `jq` for reaction GIFs or downloadable visual media. Prefer `tinygif`/`mp4` for chat previews and full `gif` for saved artifacts. Preserve title, URL, preview URL, and dimensions when returning choices.

### OpenHue smart-light control

Use OpenHue for Philips Hue rooms, zones, scenes, and lights. Confirm the bridge is reachable and paired; list rooms/lights/scenes before acting if names are uncertain. For side effects, summarize the targeted room/light and desired on/off/brightness/color/scene.

## Verification

- For reads/searches: include returned IDs/URLs/snippets and timestamps when relevant.
- For sends/posts/DMs: include platform response IDs/status without exposing tokens.
- For downloads: verify the media file exists.
- For device control: read/list resulting state when the CLI supports it.

## Archived source packages

Former narrow platform-specific skills (`himalaya`, `xurl`, `yuanbao`, `gif-search`, and `openhue`) were consolidated here. Their full packages are archived recoverably with original command examples and references.
