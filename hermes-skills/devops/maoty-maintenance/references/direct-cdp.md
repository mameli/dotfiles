# Maoty browser: direct CDP

The repository's `scripts/aoty_cdp.py` owns the browser connection; the refresh script imports it directly. Do not use Playwright, playwright-cli, a named browser session, or a second profile for AOTY. The former `.playwright/cli.config.json` was removed; do not recreate it.

- Endpoint: `${SKILLS_CDP_URL}`.
- Dedicated Chrome user-data-dir: `${SKILLS_BROWSER_USER_DATA_DIR}`.
- LaunchAgent: `${SKILLS_BROWSER_LAUNCH_AGENT}`.
- Python dependency: `websocket-client` in the interpreter running the refresh. Check import before installing anything.

The helper checks `/json/version`, kickstarts the LaunchAgent if unavailable, creates a run-owned tab using `PUT /json/new`, attaches with `Target.attachToTarget`, and evaluates with `Runtime.evaluate`. Its context manager closes only that tab. Leave Chrome, its profile, and unrelated tabs intact.

For a read-only connectivity check, call `ensure_cdp_ready(kickstart=False)` from the helper only after verifying its hardcoded endpoint matches the selected endpoint. If unavailable, inspect the endpoint before restarting. Only when an interruption is authorized and `SKILLS_BROWSER_LAUNCH_AGENT` is nonempty, use:

```bash
if [ -n "${SKILLS_BROWSER_LAUNCH_AGENT:-}" ]; then
  launchctl kickstart -k "gui/$(id -u)/${SKILLS_BROWSER_LAUNCH_AGENT}"
else
  printf '%s\n' 'No LaunchAgent configured; ask how the browser is managed.' >&2
fi
```

This can interrupt the dedicated browser. Do not infer a service label.

## External compatibility limits

Read-only inspection of the external repository found concrete portability blockers:

- `scripts/aoty_cdp.py` assigns literal `CDP_HTTP` and `LAUNCHAGENT_LABEL` constants. It does not read `SKILLS_CDP_URL` or `SKILLS_BROWSER_LAUNCH_AGENT`. `AotyCdp.__enter__()` calls readiness with kickstart enabled, so even a navigation check can restart that hardcoded service if unavailable.
- `scripts/build_album_data.py` assigns `MIXTAPE_PATH` and `TAG_BROWSE_PATH` to fixed, account-specific filenames under the repository's `output/`. It does not read `MAOTY_TASTE_ARTISTS_PATH` or `MAOTY_TASTE_NOTES_PATH`; the notes output can therefore differ from the selected workflow path.
- Its Apple Music helper candidates include a fixed legacy skill location under the user's home; moving this installed skill does not relocate that dependency.

Personal labels and filenames are intentionally omitted. Before running a refresh, inspect these constants locally and compare them with the resolved workflow values. If they differ, stop and request a separately authorized external-repository change; exporting variables does not fix the mismatch. This skill does not modify the external repository, browser configuration, service or scheduled-job payload. Existing cron payloads may also need a separately authorized review.

Do not use `with AotyCdp()` as a side-effect-free readiness test: its context entry can restart the configured service, even after a successful earlier readiness check. Keep read-only checks to `ensure_cdp_ready(kickstart=False)` after verifying the external constants. A live navigation check requires separately authorized tab creation and possible service interruption until the external helper supports an explicit no-restart context.

`AotyCdp.evaluate` accepts both arrow functions and expressions. Chrome rejects WebSocket connections with an Origin header in this setup; the helper uses `suppress_origin=True`.

The AOTY login and Cloudflare clearance persist in the dedicated profile. If blocked, wait and retry once in the same session; if authentication is required, ask the user to log in manually in that Chrome window. Never infer page content from a failed extraction.
