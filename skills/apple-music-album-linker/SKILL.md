---
name: apple-music-album-linker
description: Find the Apple Music album URL for a given artist name and album title by querying Apple's catalog and selecting the best match. Use when asked to look up, verify, or list Apple Music links for one or more albums, including batch lists of artist-album pairs.
---

# Apple Music Album Linker

Follow this workflow to resolve Apple Music album links accurately and consistently.

## Workflow

1. Run `scripts/find_apple_music_album.py --artist "ARTIST" --album "ALBUM"` for each requested album.
2. Use the returned `url` when the script reports `match_quality: exact`.
3. If the script reports `match_quality: likely`, verify the result by checking the artist and album names before returning it.
4. If the script exits with `No Apple Music album match found`, report that the album could not be found in the current storefront instead of guessing.
5. For batch requests, run the script once per album and return the results in the user's original order.

## Output Rules

1. Return direct Apple Music album links, not search-result pages.
2. Keep the storefront explicit when relevant; the script defaults to the US storefront.
3. If Apple labels the release differently from the user input, note the discrepancy briefly.
4. Do not invent a link for missing results.

## Script

Use `scripts/find_apple_music_album.py` as the primary path for lookups.

Examples:

```bash
python3 scripts/find_apple_music_album.py --artist "Orange Juice" --album "Rip It Up"
python3 scripts/find_apple_music_album.py --artist "Current Joys" --album "Brittle Stars" --json
```

The script prints a direct URL by default. With `--json`, it prints the normalized match details so you can inspect borderline cases.
