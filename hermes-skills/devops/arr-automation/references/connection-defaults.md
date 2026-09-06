# ARR inputs, connection and defaults

Inputs:
- `arr_target` (required): `radarr` | `sonarr`
- `base_url` (optional): full app URL
- `identifier` (required): Radarr `{ tmdbId }` preferred, or `{ imdbId }` / `{ query }`; Sonarr `{ tvdbId }` preferred, or `{ imdbId }` / `{ query }`
- `options` (optional): `monitored` (bool), `search` (bool), `qualityProfile` (name or id), `rootFolder` (path)

Resolve `base_url`: explicit input → `RADARR_URL` / `SONARR_URL` → localhost default (`http://localhost:7878` for Radarr; `http://localhost:8989` for Sonarr). Do not assume machine-specific hosts.

Resolve credentials in order:
1. `RADARR_API_KEY` / `SONARR_API_KEY` from the current process environment. If absent, ask the user to provide them through their existing credential configuration; do not source an interactive shell profile as a credential-loading mechanism.
2. API key already supplied by the user.
3. API key available in an authenticated app context (`window.Radarr?.apiKey` / `window.Sonarr?.apiKey`), kept in process memory rather than printed.
4. UI credentials explicitly available as `ARR_USER` / `ARR_PASSWORD`, if the active tool's login policy permits their use. With `browser_exec`, stop at a login wall and ask the user to authenticate; never guess credentials.

Never print, log or return credentials, including browser evaluations that would expose API keys. Check only whether a variable is set and, if needed, its length. Do not display secret-bearing shell-profile or environment-file lines.

Defaults unless explicitly overridden:
- `monitored = true`
- `search = true` (an add can therefore trigger downloads; disclose this when presenting resolved options)
- Radarr quality profile: explicit `options.qualityProfile` (name or id) → nonempty `RADARR_QUALITY_PROFILE` (exact profile name) → valid instance default → first valid profile returned by `/api/v3/qualityprofile`. Resolve the selected name/id against the live profile list before writing; if an explicit option or configured name is absent, stop and report the mismatch rather than silently substituting a different quality. Never hardcode a numeric ID. `RADARR_QUALITY_PROFILE` is an optional non-secret setting; unset/empty means use instance discovery.
- Sonarr quality profile: instance default unless specified, otherwise first valid profile.
- Root: query `/api/v3/rootfolder`; prefer a valid instance default, otherwise an accessible returned root. Never hardcode a previously observed NAS path or blindly use an inaccessible first entry.

For parameters from previous browser workflows, see [legacy parameters](legacy-parameters.md).
