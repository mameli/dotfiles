# Weekly refresh reporting and taste-labeling notes

These notes capture recurring details observed during a successful Maoty Friday refresh and are meant to supplement `SKILL.md`, not replace `AGENT.md`.

## Reading refresh stats

`bun run albums` prints a JSON line like:

```json
{"refresh_stats": {"must_hear_scraped": 5, "new_releases_qualified": 3, "apple_fallback_lookups": 0, "missing_apple_music_links": 0}}
```

Use these script stats for:

- Must Hear scraped count
- New Releases qualified count
- Apple Music fallback lookup count during this run
- Missing Apple Music links produced by the current run

Then independently validate the resulting `src/data/album-list.json` for whole-file integrity:

- missing/invalid `taste_label`
- duplicate `aoty_url`
- whole-file missing Apple Music count
- top current-batch size

The whole-file missing Apple Music count may include older albums as well as newly refreshed albums. Report it as “missing Apple Music links after fallback” if the prompt asks for a final site-wide count, but do not treat it as a blocker.

## Counting inserted/top-batch albums

To report “albums inserted at the top,” count the contiguous leading entries whose `batch_date` matches the current refresh date. This includes both newly added albums and previously known albums that were updated/moved into the new Friday batch. Separately, `new_vs_HEAD` counts truly new albums by comparing `aoty_url` against `git show HEAD:src/data/album-list.json`.

## Labeling examples from the 2026-06-05 run

Use these as calibration examples for future editorial labels:

- Vince Staples — *Cry Baby* (`Political Hip Hop`, `Rap Rock`, `West Coast Hip Hop`): `It's a match` because hip-hop/rap are core taste lanes.
- Death Cab for Cutie — *I Built You A Tower* (`Indie Rock`, `Indie Pop`, `Post-Punk Revival`): `It's a match` because indie rock/indie pop directly match the profile.
- SLIFT — *Fantasia* (`Psychedelic Rock`, `Space Rock`, `Heavy Psych`): `Maybe you'll like it` because psychedelic rock is present but peripheral and the album leans exploratory/heavy.
- Kim Petras — *Detour* (`Electropop`, `Electronic Dance Music`, `Hyperpop`): `Just for you` because electronic/pop/electropop overlap is real, but the dance/hyperpop angle is less central.
- Boards of Canada — *Inferno* (`Downtempo`, `IDM`, `Ambient`): `Just for you` because downtempo/ambient/electronic are meaningful taste signals, though less direct than indie/hip-hop/R&B.

## Labeling examples from the 2026-06-12 run

Use these as additional calibration examples for future editorial labels:

- Olivia Rodrigo — *you seem pretty sad for a girl so in love* (`Pop Rock`, `Singer-Songwriter`, `New Wave`): `It's a match` because pop rock plus singer-songwriter sits directly in the recurring pop/indie/singer-songwriter taste lane.
- Navy Blue — *Sir Render* (`Drumless`, `Abstract Hip Hop`, `Conscious Hip Hop`): `It's a match` because abstract/conscious hip-hop is a clear match for the hip-hop/rap core taste lane even when the AOTY row has only a user/low-review Must Hear score.

## Generated tag browse output

`bun run albums` may rewrite the external builder's actual `TAG_BROWSE_PATH` even when the Last.fm export was not intentionally refreshed. It does not consume `MAOTY_TASTE_NOTES_PATH`; verify the mapping as described in [external compatibility limits](direct-cdp.md#external-compatibility-limits). Leave that file uncommitted unless the user explicitly requested a Last.fm/tag-export refresh.
