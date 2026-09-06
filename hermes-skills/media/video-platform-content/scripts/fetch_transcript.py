#!/usr/bin/env python3
"""
Fetch a YouTube video transcript and output it as structured JSON.

Usage:
    python fetch_transcript.py <url_or_video_id> [--language en,tr] [--timestamps]

Output (JSON):
    {
        "video_id": "...",
        "language": "en",
        "is_generated": false,
        "segments": [{"text": "...", "start": 0.0, "duration": 2.5}, ...],
        "full_text": "complete transcript as plain text",
        "timestamped_text": "00:00 first line\n00:05 second line\n..."
    }

Install dependency:  pip install youtube-transcript-api
"""

import argparse
import json
import re
import sys
from urllib.parse import parse_qs, urlparse


def extract_video_id(url_or_id: str) -> str:
    """Extract the 11-character video ID from various YouTube URL formats."""
    if re.fullmatch(r'[a-zA-Z0-9_-]{11}', url_or_id):
        return url_or_id
    parsed = urlparse(url_or_id)
    candidate = None
    if parsed.scheme in ('http', 'https') and not parsed.username and not parsed.password:
        parts = parsed.path.split('/')
        if parsed.hostname in ('youtu.be', 'www.youtu.be') and len(parts) == 2:
            candidate = parts[1]
        elif parsed.hostname in ('youtube.com', 'www.youtube.com', 'm.youtube.com',
                                 'music.youtube.com', 'youtube-nocookie.com',
                                 'www.youtube-nocookie.com'):
            if parsed.path == '/watch':
                values = parse_qs(parsed.query, keep_blank_values=True).get('v', [])
                if len(values) == 1:
                    candidate = values[0]
            elif len(parts) == 3 and parts[1] in ('shorts', 'embed', 'live'):
                candidate = parts[2]
    if candidate is not None and re.fullmatch(r'[a-zA-Z0-9_-]{11}', candidate):
        return candidate
    raise ValueError('Expected an exact 11-character YouTube video ID or a supported YouTube URL.')


def format_timestamp(seconds: float) -> str:
    """Convert seconds to HH:MM:SS or MM:SS format."""
    total = int(seconds)
    h, remainder = divmod(total, 3600)
    m, s = divmod(remainder, 60)
    if h > 0:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


def fetch_transcript(video_id: str, languages: list = None):
    """Fetch transcript segments from YouTube.

    Returns language/provenance metadata and normalized segments.
    With no language constraint, prefer a manual track, then any generated track.
    Compatible with youtube-transcript-api v1.x.
    """
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
    except ImportError:
        print("Error: youtube-transcript-api not installed. Run: pip install youtube-transcript-api",
              file=sys.stderr)
        sys.exit(1)

    api = YouTubeTranscriptApi()
    transcripts = api.list(video_id)
    if languages:
        track = transcripts.find_transcript(languages)
    else:
        available = list(transcripts)
        if not available:
            raise ValueError('No transcript available for this video.')
        track = next((item for item in available if not item.is_generated), available[0])

    return {
        "language": track.language_code,
        "is_generated": track.is_generated,
        "segments": [
            {"text": seg.text, "start": seg.start, "duration": seg.duration}
            for seg in track.fetch()
        ],
    }


def main():
    parser = argparse.ArgumentParser(description="Fetch YouTube transcript as JSON")
    parser.add_argument("url", help="YouTube URL or video ID")
    parser.add_argument("--language", "-l", default=None,
                        help="Comma-separated language codes (e.g. en,tr). Default: auto")
    parser.add_argument("--timestamps", "-t", action="store_true",
                        help="Include timestamped text in output")
    parser.add_argument("--text-only", action="store_true",
                        help="Output plain text instead of JSON")
    args = parser.parse_args()

    try:
        video_id = extract_video_id(args.url)
        languages = [code.strip() for code in args.language.split(",")] if args.language is not None else None
        if languages is not None and not all(languages):
            raise ValueError('--language requires nonempty comma-separated language codes.')
        transcript = fetch_transcript(video_id, languages)
        segments = transcript["segments"]
    except Exception as e:
        error_msg = str(e)
        if "disabled" in error_msg.lower():
            print(json.dumps({"error": "Transcripts are disabled for this video."}))
        elif "no transcript" in error_msg.lower():
            print(json.dumps({"error": error_msg, "hint": "Retry without --language to select any available track."}))
        else:
            print(json.dumps({"error": error_msg}))
        sys.exit(1)

    full_text = " ".join(seg["text"] for seg in segments)
    timestamped = "\n".join(
        f"{format_timestamp(seg['start'])} {seg['text']}" for seg in segments
    )

    if args.text_only:
        print(timestamped if args.timestamps else full_text)
        return

    result = {
        "video_id": video_id,
        **transcript,
        "segment_count": len(segments),
        "duration": format_timestamp(segments[-1]["start"] + segments[-1]["duration"]) if segments else "0:00",
        "full_text": full_text,
    }
    if args.timestamps:
        result["timestamped_text"] = timestamped

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
