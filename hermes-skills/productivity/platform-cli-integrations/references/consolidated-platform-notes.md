# Consolidated platform notes

## Himalaya email
- Verify install and account config with non-secret status/list commands.
- macOS may store config under `~/Library/Application Support/himalaya/` rather than `~/.config/himalaya/`.
- Use message files/MML for attachments and composed email.

## xurl for X/Twitter
- Official X API CLI for posts, replies, search, timelines, bookmarks, media, DMs, and raw v2 endpoints.
- Never read/print `~/.xurl`; use only `xurl auth status` to verify auth.
- Avoid `--verbose` and inline secret flags.

## Yuanbao
- Final assistant text is the group message. Query members to get the exact nickname before using `@nickname`.
- Use the DM tool for private messages and report status.

## Tenor GIF search
- Requires `TENOR_API_KEY`, `curl`, and `jq`.
- Use `tinygif`/`mp4` for previews and full `gif` for saved artifacts.

## OpenHue
- Pair with Hue Bridge first and list resources before controlling uncertain names.
- Verify resulting room/light/scene state when possible.

Full original packages were archived unchanged so exact commands and references remain recoverable.