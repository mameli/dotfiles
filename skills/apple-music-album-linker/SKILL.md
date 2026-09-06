---
name: apple-music-album-linker
description: Find direct Apple Music album links from artist and album names, including batch lookups.
---

# Apple Music album links

Run `python3 scripts/find_apple_music_album.py --artist "ARTIST" --album "ALBUM" --json` from this skill directory. The helper defaults to the US storefront.

Use exact matches directly; inspect artist, album and edition for likely matches. Report missing matches instead of guessing. Return direct album URLs in the requested order, noting material title, edition or storefront differences.
