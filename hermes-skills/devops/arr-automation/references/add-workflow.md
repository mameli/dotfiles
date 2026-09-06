# ARR API-first add and verification

Read [connection/defaults](connection-defaults.md) first. Use UI only when API prerequisites are unavailable or blocked.

## API flow

1. Confirm reachability (`GET /` or login page), resolve the API key and validate it with `GET /api/v3/system/status`. Always send the `X-Api-Key` header; an authenticated UI session alone does not authorize API calls.
2. Query `GET /api/v3/qualityprofile` and `GET /api/v3/rootfolder`. Resolve explicit options and the profile/root precedence in connection/defaults; do not replace the Radarr named-profile preference with the first result.
3. Resolve the intended work and check duplicates:
   - For referential requests such as “il seguito” or “quello del 2013”, use topic/session context first. Ask before writing if more than one interpretation remains plausible.
   - Radarr lookup: `GET /api/v3/movie/lookup?term=<query>`, `GET /api/v3/movie/lookup/tmdb?tmdbId=<id>`, or `GET /api/v3/movie/lookup/imdb?imdbId=<id>`.
   - Sonarr lookup: `GET /api/v3/series/lookup?term=<query-or-id>`; use `tvdb:<id>` or `imdb:<id>` if the instance supports those forms.
   - Prefer an exact supplied external-ID match; otherwise require compatible normalized title and year/context. Never select the first lookup result merely because it exists. Ask if multiple works remain plausible.
   - Before POST, fetch `GET /api/v3/movie` or `GET /api/v3/series` and compare canonical TMDb/TVDb/IMDb identifiers. If already present, do not add a duplicate; report its current monitored/profile/path state.
4. Build explicit add payloads:
   - Radarr `POST /api/v3/movie`: in practice provide `tmdbId`, `title`, `year`, `qualityProfileId`, `rootFolderPath`, `path`, `monitored`. `path` must be absolute under `rootFolderPath` (e.g. `<rootFolderPath>/<Movie Folder>`), not just a folder name. Recommended `minimumAvailability: "released"`; set `addOptions: { searchForMovie: <bool> }` explicitly.
   - Sonarr `POST /api/v3/series`: in practice provide `tvdbId` (or looked-up ids/title fields), `title`, `qualityProfileId`, `rootFolderPath`, `monitored`; set `addOptions: { searchForMissingEpisodes: <bool> }` explicitly. Apply extra lifecycle preferences such as season monitoring only when requested.
5. Submit (typically HTTP 201), then re-fetch list/detail from `/api/v3/movie` or `/api/v3/series`. Match the exact canonical ID and confirm title/year, monitored state, qualityProfileId mapped to profile name and path/root. A successful POST alone is not verification.

On HTTP 400/409, re-fetch by canonical external ID before classifying: an existing entity is not an add failure, but is not newly created either.

## UI fallback

Use `browser_exec` Python helpers. Start the first navigation with `new_tab(base_url)`, then `wait_for_load()` and `page_info()`. Use `goto_url(url)` for later navigation. After navigation/modal transitions, refresh page state rather than reusing stale element references. Start each call with a plain-language comment of at most 60 characters. At a login wall, stop and ask the user to authenticate.

Read fields via `js('document.body.innerText')` or a called expression such as `js('(() => { return document.title; })()')`; inspect/filter `cdp('Accessibility.getFullAXTree')['nodes']` when needed. Use `fill_input(selector, text)` for observed inputs and `click_at_xy(x, y)` for verified coordinates. `capture_screenshot()` attaches the image for direct inspection; do not send browser screenshots to a separate vision tool.

Add flow: click `Add New` → enter query (press Enter if needed for results) → open the exact matching card → confirm profile/root/monitor/search in the modal → click `Add Movie` or `Add Series`. Verify via API when possible, otherwise re-open the exact entity in UI and record only fields actually observed.

## Result contract

Return concise confirmed fields, not a process replay:
- `arr_target`, `base_url`
- `method`: `api-first` | `ui-fallback`
- `added`: true only if the requested entity is verified present after the operation
- `createdNow`: true only if this operation created it
- `alreadyExists`: true if present before the operation
- canonical `tmdbId` or `tvdbId`, `title`, `year` when available
- `monitored`, `qualityProfileName`, `path`
- `searchTriggered`: true only if this request actually initiated a search, not merely because search was the default

Include resolved overrides/defaults and any non-fatal caveats or unverified fields. Do not mark a write successful when read-back fails.
