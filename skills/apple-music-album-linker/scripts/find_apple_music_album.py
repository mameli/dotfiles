#!/usr/bin/env python3
"""Find the best Apple Music album URL for an artist and album title."""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
import urllib.parse
import urllib.request


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.casefold()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return " ".join(text.split())


def build_url(artist: str, album: str, country: str, limit: int) -> str:
    query = urllib.parse.urlencode(
        {
            "term": f"{artist} {album}",
            "entity": "album",
            "country": country,
            "limit": limit,
        }
    )
    return f"https://itunes.apple.com/search?{query}"


def fetch_results(url: str) -> list[dict]:
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request) as response:
        payload = json.load(response)
    return payload.get("results", [])


def score_result(result: dict, artist_norm: str, album_norm: str) -> tuple[int, str]:
    result_artist = normalize(result.get("artistName", ""))
    result_album = normalize(result.get("collectionName", ""))

    score = 0

    if result_artist == artist_norm:
        score += 100
    elif artist_norm and artist_norm in result_artist:
        score += 60

    if result_album == album_norm:
        score += 100
    elif album_norm and album_norm in result_album:
        score += 60
    elif result_album and result_album in album_norm:
        score += 30

    if result.get("collectionType") == "Album":
        score += 10

    quality = "exact" if score >= 210 else "likely" if score >= 130 else "weak"
    return score, quality


def clean_url(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    return urllib.parse.urlunparse(parsed._replace(query=""))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Find the best Apple Music album URL for an artist and album title."
    )
    parser.add_argument("--artist", required=True, help="Artist or band name")
    parser.add_argument("--album", required=True, help="Album title")
    parser.add_argument("--country", default="us", help="Apple storefront country code")
    parser.add_argument("--limit", type=int, default=25, help="Maximum results to inspect")
    parser.add_argument("--json", action="store_true", help="Print structured JSON output")
    args = parser.parse_args()

    artist_norm = normalize(args.artist)
    album_norm = normalize(args.album)
    url = build_url(args.artist, args.album, args.country, args.limit)
    results = fetch_results(url)

    ranked: list[tuple[int, str, dict]] = []
    for result in results:
        score, quality = score_result(result, artist_norm, album_norm)
        ranked.append((score, quality, result))

    ranked.sort(
        key=lambda item: (
            item[0],
            item[2].get("artistName", ""),
            item[2].get("collectionName", ""),
        ),
        reverse=True,
    )

    if not ranked or ranked[0][1] == "weak":
        print("No Apple Music album match found", file=sys.stderr)
        return 1

    score, quality, match = ranked[0]
    output = {
        "artist": match.get("artistName"),
        "album": match.get("collectionName"),
        "url": clean_url(match.get("collectionViewUrl", "")),
        "country": args.country.lower(),
        "match_quality": quality,
        "score": score,
    }

    if args.json:
        json.dump(output, sys.stdout, ensure_ascii=True, indent=2)
        sys.stdout.write("\n")
    else:
        print(output["url"])

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
