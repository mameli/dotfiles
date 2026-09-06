#!/usr/bin/env python3
"""Read-only Maoty album checks; optional metadata gaps do not fail validation."""
import argparse
import collections
import json
import os
from pathlib import Path
import subprocess

VALID_LABELS = {"It's a match", "Just for you", "Maybe you'll like it"}


def inspect(data, previous):
    urls = [album.get('aoty_url') for album in data]
    duplicates = [url for url, count in collections.Counter(urls).items() if url and count > 1]
    invalid = [i for i, album in enumerate(data, 1) if album.get('taste_label') not in VALID_LABELS]
    missing_urls = [i for i, url in enumerate(urls, 1) if not url]
    batch_date = data[0].get('batch_date') if data else None
    batch_size = 0
    if batch_date:
        for album in data:
            if album.get('batch_date') != batch_date:
                break
            batch_size += 1
    previous_urls = {album.get('aoty_url') for album in previous} if previous is not None else None
    return {
        'album_count': len(data),
        'new_vs_HEAD': sum(url not in previous_urls for url in urls) if previous_urls is not None else None,
        'leading_batch_date': batch_date,
        'leading_batch_size': batch_size,
        'missing_invalid_taste_label_rows': invalid,
        'duplicate_aoty_urls': duplicates,
        'missing_aoty_url_rows': missing_urls,
        'whole_file_missing_apple_music_links': sum(not a.get('apple_music') for a in data),
        'whole_file_missing_genre_tags': sum(not a.get('genre_tags') for a in data),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('repo', nargs='?', help='Repository path (overrides MAOTY_REPO_PATH)')
    args = parser.parse_args()
    raw_repo = args.repo if args.repo is not None else os.environ.get('MAOTY_REPO_PATH')
    if not raw_repo or not raw_repo.strip():
        parser.error('Pass a repository path or set MAOTY_REPO_PATH; no repository default is assumed.')
    repo = Path(raw_repo).expanduser().resolve()
    try:
        data = json.loads((repo / 'src/data/album-list.json').read_text())
    except (OSError, ValueError):
        parser.error('Cannot read valid src/data/album-list.json; check the repository argument or MAOTY_REPO_PATH.')
    if not isinstance(data, list) or any(not isinstance(album, dict) for album in data):
        parser.error('src/data/album-list.json must be an array of album objects.')
    try:
        result = subprocess.run(['git', '-C', str(repo), 'show', 'HEAD:src/data/album-list.json'], capture_output=True, text=True)
        previous = json.loads(result.stdout) if result.returncode == 0 else None
        if not isinstance(previous, list) or any(not isinstance(album, dict) for album in previous):
            previous = None
    except (OSError, ValueError):
        previous = None
    report = inspect(data, previous)
    if previous is None:
        report['comparison_warning'] = 'HEAD dataset unavailable; new_vs_HEAD is unknown'
    print(json.dumps(report, indent=2))
    return int(bool(report['missing_invalid_taste_label_rows'] or report['duplicate_aoty_urls'] or report['missing_aoty_url_rows']))


if __name__ == '__main__':
    raise SystemExit(main())
