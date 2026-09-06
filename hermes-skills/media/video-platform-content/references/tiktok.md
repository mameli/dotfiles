# TikTok: resolve, inspect, extract

## Dedicated browser lane

Use the existing visible Chrome profile; manual user logins persist here:

- User data: `${SKILLS_BROWSER_USER_DATA_DIR}`; profile: `${SKILLS_BROWSER_PROFILE}`
- CDP: `${SKILLS_CDP_URL}`
- LaunchAgent: `~/Library/LaunchAgents/${SKILLS_BROWSER_LAUNCH_AGENT}.plist`; label `${SKILLS_BROWSER_LAUNCH_AGENT}`
- Established settings: `browser.use_real_profile = false`, `browser.cdp_url = ${SKILLS_CDP_URL}`, `browser.cloud_provider = local`. Do not change configuration to extract a post.

Check readiness with `curl -fsS "${SKILLS_CDP_URL:-http://127.0.0.1:9222}/json/version" >/dev/null`. Diagnose the port in the selected URL, not an assumed port. Inspect logs only when `SKILLS_BROWSER_LOG_DIR` is set, using the quoted directory path. On macOS, service inspection must be guarded:

```bash
if [ -n "${SKILLS_BROWSER_LAUNCH_AGENT:-}" ]; then
  launchctl print "gui/$(id -u)/${SKILLS_BROWSER_LAUNCH_AGENT}"
else
  printf '%s\n' 'No LaunchAgent configured; ask how the existing browser is managed.' >&2
fi
```

If a restart is needed and authorized, use the same nonempty-label guard around `launchctl kickstart -k "gui/$(id -u)/${SKILLS_BROWSER_LAUNCH_AGENT}"`, then verify readiness. Do not guess a service, profile path or log directory.

Use `browser_exec` with `session="tiktok"` throughout; there is no `local=true` argument. Its Python helpers attach to the configured browser. First navigation:

```python
# Opening the TikTok post
new_tab('USER_URL')
wait_for_load()
print(page_info())
print(js('location.href'))
```

Use `goto_url(url)` for subsequent navigation, then `wait_for_load()` and refresh `page_info()`. Start every call with a plain-language comment of at most 60 characters. Python variables do not persist between calls. Pass evaluated expressions to `js`: `js('document.title')` or `js('(() => { return location.href; })()')`, never an uncalled arrow function.

At a login wall, stop and ask the user to log in manually in this dedicated Chrome window, preferably by QR, then retry after confirmation. Never request passwords, OTPs or 2FA codes. Do not interact with passkey prompts; if an overlay is non-blocking and the content remains accessible, extract only what is actually available.

## Short links, redirects and classification

Open in the browser first for viewing/analysis. If blocked, a redirect-only probe with a browser-like User-Agent can identify the target without claiming access to content:

```python
import urllib.request
from urllib.parse import parse_qs, urlparse
url = 'USER_TIKTOK_URL'
request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(request, timeout=15) as response:
        final_url = response.geturl()
        print('final_url:', final_url, 'status:', response.status)
        # parse_qs decodes the query value once; this is a target hint, not viewed content.
        print('redirect_target:', parse_qs(urlparse(final_url).query).get('redirect_url', []))
except Exception as error:
    print(type(error).__name__, str(error))
```

Classify the resolved URL: `/@username/video/<id>` is video; `/@username/photo/<id>` is photo mode/carousel; `/login?redirect_url=...` is gated even when its decoded target identifies the post. Inspect `location.href` in the browser too: HTTP redirects need not match client-side navigation. State exactly what was visible versus blocked; neither a redirect nor metadata alone proves you saw the post.

If unavailable, request a downloaded video or screen recording for video; ordered screenshots/photos for a carousel (a swiping recording is acceptable, but screenshots retain small text better).

## Photo carousels

Extract image candidates in page context:

```python
# Finding carousel image candidates
print(js('(() => { const seen = new Set(); return [...document.images].map(i => ({url:i.currentSrc || i.src, width:i.naturalWidth, height:i.naturalHeight, alt:i.alt})).filter(i => { if (!i.url || seen.has(i.url)) return false; seen.add(i.url); return true; }); })()'))
```

Keep actual post slides, typically high-resolution images such as `1440x1800` whose URLs contain `photomode-image` or `/tos-...-i-photomode-.../`. Exclude avatars (`avt`, `cropcenter:100:100`) and recommendation thumbnails. Preserve DOM order and deduplicate URLs, but verify slide order/count against the visible carousel; lazy-loaded slides may require swiping and another extraction.

An empty extraction does not prove there are no slides. Check `page_info()` and `js('location.href')`; if the wrong target is attached, inspect `cdp('Target.getTargets')`, then navigate to the exact post in the same browser session and retry. Use `cdp('Runtime.evaluate', expression='document.location.href', returnByValue=True)` when diagnosing page-context evaluation. Do not accidentally inspect another tab's data.

Direct carousel image URLs may be loaded with `vision_analyze`. Browser screenshots are different: call `capture_screenshot()` inside `browser_exec` and inspect the automatically attached image directly; never forward a browser screenshot to a separate vision tool.

For a large carousel, a temporary contact sheet can help: collect verified slide URLs first, open a separate scratch tab, build a numbered grid with DOM `createElement`/`textContent` (do not replace the source post), set the viewport with `cdp('Emulation.setDeviceMetricsOverride', width=1280, height=1600, deviceScaleFactor=1, mobile=False)`, then `capture_screenshot()`. Use smaller batches or zoom for illegible text. Restore the viewport with `cdp('Emulation.clearDeviceMetricsOverride')`. A contact sheet is an inspection aid, not evidence that every slide loaded.

For all-slide/all-entry requests, append each batch to JSON/CSV in the browser workspace, then read back and dedupe/count/sort in Python. Verify the collected count against the post/request before claiming completeness. Separate cover/title slides from actual list entries.

Summarize in the user's language (Italian when appropriate). Include visible text, relevant names/objects and takeaways. Preserve uncertain proper nouns as seen; mark unclear ratings, prices, review counts, addresses and model names `da verificare`. Distinguish `estratto dal TikTok` from `verificato esternamente`. Verify truncated or consequential resource names from authoritative/independent sources when practical; never silently normalize uncertain OCR.

## Videos: metadata, captions, frames

Read caption, author and visible text with `page_info()` and `js('document.body.innerText')`; filter large outputs. For accessibility details, use `cdp('Accessibility.getFullAXTree')['nodes']`, filtering role/name/backendDOMNodeId in Python before printing. Inspect visual details with `capture_screenshot()` directly.

Extract page-context metadata before attempting unauthenticated downloads:

```python
# Reading TikTok metadata and caption tracks
print(js("""(() => {
  const item = window.__$UNIVERSAL_DATA$__?.__DEFAULT_SCOPE__?.['webapp.video-detail']?.itemInfo?.itemStruct;
  return {
    author: item?.author?.uniqueId, nickname: item?.author?.nickname,
    desc: item?.desc, stickers: item?.stickersOnItem?.flatMap(s => s.stickerText || []),
    music: item?.music && {title:item.music.title, authorName:item.music.authorName},
    stats: item?.stats,
    subtitles: item?.video?.subtitleInfos || item?.video?.claInfo?.captionInfos || item?.claInfo?.captionInfos || []
  };
})()"""))
```

Select a returned caption track matching the requested language when available; record actual language and automatic/manual provenance. Fetch its exact observed URL in page context so session access is retained:

```python
# Fetching the observed caption track
import json
track_url = 'OBSERVED_SUBTITLE_URL'
expression = 'fetch(' + json.dumps(track_url) + ').then(r => { if (!r.ok) throw new Error(String(r.status)); return r.text(); })'
print(cdp('Runtime.evaluate', expression=expression, awaitPromise=True, returnByValue=True))
```

Check CDP errors/`exceptionDetails` rather than treating an unsuccessful fetch as empty captions. Parse WebVTT cues, omitting headers, timestamps and cue numbers for plain text while retaining timing for citations. Summarize/translate in the user's language. Captions can mishear proper nouns, slang, music or noisy speech; combine them with description, stickers and on-screen evidence.

For recommendation/list videos, verify names and arrondissements on key frames. Seek and pause with a called `js` expression, wait for the observed `seeked`/ready state, then `capture_screenshot()` and inspect directly. Alternatively, `scripts/capture_tiktok_frames_cdp.js` saves JPEGs drawn from the video element through canvas via the persistent CDP websocket:

```bash
node "SKILL_DIR/scripts/capture_tiktok_frames_cdp.js" "VIDEO_ID" "OUTPUT_DIR" 2.0=cover 64.0=place
# Explicit endpoint overrides the environment:
node "SKILL_DIR/scripts/capture_tiktok_frames_cdp.js" --cdp-url "http://127.0.0.1:9222" "VIDEO_ID" "OUTPUT_DIR" 2.0=cover
```

Offline portability regression (no browser/network): `node "SKILL_DIR/scripts/test_capture_tiktok_frames_cdp.js"`. Validate all CLI inputs before network access or creating output directories; keep argument parsing importable so endpoint precedence can be tested with stubbed fetch.

These canvas video-frame files (not browser screenshots) may be read with `vision_analyze`; the helper avoids giant base64 tool output. Requires Node.js 22+ with global `fetch`/`WebSocket` and the exact post already loaded at the selected endpoint. The helper consumes `--cdp-url URL` > nonempty `SKILLS_CDP_URL` > `http://127.0.0.1:9222`; it rejects non-HTTP(S) URLs, embedded credentials, whitespace, query strings and fragments before any network or output-directory operation. Quote explicit output directories containing spaces. The helper does not launch Chrome or consume profile/service/log settings. Prefer on-screen OCR for proper names and VTT for spoken commentary. Do not imply silent frame captures include audio.

If page extraction fails, optionally inspect `yt-dlp` subtitle availability and request an available language, or use `--cookies-from-browser` only within the authorized browser profile. Prefer page-context extraction; TikTok often blocks unauthenticated CLI requests. If playback/content remains unavailable, ask for a downloaded video, recording or key screenshots; label missing captions and visual coverage plainly.

## Saving and leaving sessions intact

Save only on explicit request. Include original URL, author, caption, retrieval date, concise summary and per-slide notes for carousels. Use the named destination or established project/trip convention; for an existing project, its `raw/` source folder plus the relevant durable note is preferred over a generic TikTok folder. Only when no better context exists and `OBSIDIAN_VAULT_PATH` is nonempty, the fallback is `${OBSIDIAN_VAULT_PATH}/_Wiki/raw/tiktok/`; otherwise ask for a destination (never default to `/_Wiki`). Suggested name: `TikTok - <author> - <short caption or topic>.md`.

Keep creator claims separate from verified facts, dedupe existing sources, preserve prior entries, and verify saved files. Leave the dedicated Chrome running; do not close it, delete its profile or log out unless explicitly asked.
