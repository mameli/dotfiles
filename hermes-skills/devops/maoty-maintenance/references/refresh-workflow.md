# Maoty album refresh

Work in `${MAOTY_REPO_PATH}`; `AGENT.md` owns source selection, metadata fields, cumulative ordering and taste-label rules.

## Run and review

1. Inspect repository status so pre-existing changes are not reverted or committed accidentally.
2. Run `bun run albums` only for an intended refresh. It invokes the direct-CDP helper and closes its run-owned tab.
3. Review `src/data/album-list.json`. Preserve existing labels; assign each genuinely new album one of `It's a match`, `Just for you`, or `Maybe you'll like it` using the existing mixtape taste context. Do not compute labels from scores.
4. Run this skill's read-only validator, then `bun run build`. Load `references/weekly-refresh-reporting-and-labeling.md` for count interpretation and label calibration.
5. When the requested refresh includes publication and the build passes, commit intentional changes and push. A normal scheduled refresh stages only `src/data/album-list.json`, unless other changes were explicitly requested. No data changes means no commit.

The default validator invocation from this skill's directory is:

```bash
python3 -B scripts/validate_album_data.py
# Or override MAOTY_REPO_PATH, including an absolute path containing spaces:
python3 -B scripts/validate_album_data.py "/path/to/Maoty checkout"
```

The positional repository path is optional and wins over `MAOTY_REPO_PATH`. There is no guessed checkout default. Relative paths resolve from the current working directory; absolute paths, `~`, and quoted paths containing spaces are supported. Missing configuration or unreadable/invalid album JSON exits with actionable usage guidance. An unavailable Git HEAD is a comparison warning, not a validation failure.

Offline regression: `python3 -B scripts/test_validate_album_data.py -v` from this skill directory. Keep these tests on temporary fixtures rather than running the real refresh to test portability.

## Data and publication boundaries

- Apple Music links are optional. If AOTY has no link and the permitted fallback raises a runtime error or finds no match, keep `apple_music` null/missing and count the gap. Do not invent a link, discard the album, or block build/commit/push solely for that gap.
- Genre tags are optional too: keep `genre_tags: []` and report the absence.
- Reuse `${MAOTY_TASTE_ARTISTS_PATH}` and `${MAOTY_TASTE_NOTES_PATH}`; do not refresh the Last.fm export without a request.
- Check the [external compatibility limits](direct-cdp.md#external-compatibility-limits): the external builder uses fixed taste paths, not these variables. The refresh may regenerate its actual `TAG_BROWSE_PATH`. Leave that output uncommitted for an ordinary album update rather than reverting possible user changes.
- Existing albums may move into the current top batch. Distinguish top-batch membership from genuinely new URLs versus HEAD.
- Preserve the album JSON formatting (`indent=2`, `ensure_ascii=True`, trailing newline). For manual multi-album edits, target records by stable URL or artist/album keys, not repeated `taste_label: null` text.
- An off-Friday `bun run albums` can mutate `batch_date`, rank and review counts without adding albums. For an explicitly requested refresh test, snapshot the data first and restore only that test's changes; never commit test churn.
- If push fails with a temporary DNS/network error, retry once. If still failing, use `ssh -T git@github.com` to distinguish authentication from connectivity and report the actual blocker. Do not include unrelated edits just to make the tree clean.

## Scheduled job and report

Job: `Maoty Friday Album Refresh`, ID `${MAOTY_CRON_JOB_ID}`. Inspect/update it with Hermes cron tools. Immediate reruns are asynchronous; inspect the resulting run output rather than treating scheduling as completion. Output lives under `~/.hermes/cron/output/${MAOTY_CRON_JOB_ID}/`.

Report script counts for Must Hear, qualified New Releases, Apple fallback lookups and optional metadata gaps. Separately report the top/current-batch size, genuinely new albums versus HEAD, invalid/missing labels, duplicates, build, commit and push outcomes. State whether metadata-gap counts are for the refreshed batch or the entire dataset. Report blockers other than optional metadata explicitly.
