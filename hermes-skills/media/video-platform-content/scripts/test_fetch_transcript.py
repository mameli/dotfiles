"""Offline regression fixtures; no YouTube or browser connections."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('fetch_transcript', Path(__file__).with_name('fetch_transcript.py'))
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)
VIDEO_ID = 'aB0_-123456'

class Track:
    def __init__(self, language, generated=False, segments=None):
        self.language_code = language
        self.is_generated = generated
        self.segments = segments if segments is not None else [SimpleNamespace(text='Fixture caption', start=1.5, duration=2.0)]
    def fetch(self):
        return self.segments

class TranscriptTests(unittest.TestCase):
    def test_valid_ids(self):
        for value in [VIDEO_ID, f'https://youtube.com/watch?v={VIDEO_ID}&t=5', f'https://youtu.be/{VIDEO_ID}?si=test', f'https://www.youtube.com/shorts/{VIDEO_ID}', f'https://m.youtube.com/live/{VIDEO_ID}', f'https://www.youtube-nocookie.com/embed/{VIDEO_ID}']:
            with self.subTest(value=value):
                self.assertEqual(helper.extract_video_id(value), VIDEO_ID)

    def test_rejects_malformed_ids_and_hosts(self):
        for value in [VIDEO_ID+'x', f'https://youtube.com/watch?v={VIDEO_ID}x', f'https://youtu.be/{VIDEO_ID}x', f'https://evil.example/watch?v={VIDEO_ID}', f'https://youtube.com.evil.example/watch?v={VIDEO_ID}', f'https://youtube.com/watch?v={VIDEO_ID}&v={VIDEO_ID}', f'https://youtube.com/shorts/{VIDEO_ID}/extra', 'short', 'https://youtube.com/watch?v=!!!!!!!!!!!']:
            with self.subTest(value=value), self.assertRaises(ValueError):
                helper.extract_video_id(value)

    def run_cli(self, tracks, *args):
        class Tracks(list):
            def find_transcript(self, languages):
                for language in languages:
                    matches = [track for track in self if track.language_code == language]
                    if matches:
                        return sorted(matches, key=lambda track: track.is_generated)[0]
                raise RuntimeError('No transcript found for requested languages')
        api = SimpleNamespace(list=lambda video_id: Tracks(tracks))
        module = SimpleNamespace(YouTubeTranscriptApi=lambda: api)
        output = io.StringIO()
        with patch.dict(sys.modules, {'youtube_transcript_api': module}), patch.object(sys, 'argv', ['fetch_transcript.py', VIDEO_ID, *args]), contextlib.redirect_stdout(output):
            helper.main()
        return output.getvalue()

    def test_unconstrained_prefers_available_manual_non_english(self):
        result = json.loads(self.run_cli([Track('en', True), Track('it')], '--timestamps'))
        self.assertEqual(result['language'], 'it')
        self.assertFalse(result['is_generated'])
        self.assertEqual(result['segments'], [{'text': 'Fixture caption', 'start': 1.5, 'duration': 2.0}])
        self.assertEqual(result['segment_count'], 1)
        self.assertEqual(result['timestamped_text'], '0:01 Fixture caption')

    def test_generated_only_and_empty_segments(self):
        result = json.loads(self.run_cli([Track('ja', True, [])]))
        self.assertEqual(result['language'], 'ja')
        self.assertTrue(result['is_generated'])
        self.assertEqual(result['segments'], [])
        self.assertEqual(result['duration'], '0:00')
        self.assertNotIn('timestamped_text', result)

    def test_explicit_language_order(self):
        result = json.loads(self.run_cli([Track('en'), Track('it')], '--language', 'it,en'))
        self.assertEqual(result['language'], 'it')

    def test_text_modes(self):
        self.assertEqual(self.run_cli([Track('it')], '--text-only'), 'Fixture caption\n')
        self.assertEqual(self.run_cli([Track('it')], '--text-only', '--timestamps'), '0:01 Fixture caption\n')

    def test_unavailable_language_does_not_silently_fallback(self):
        with self.assertRaises(SystemExit) as error:
            self.run_cli([Track('it')], '--language', 'fr')
        self.assertEqual(error.exception.code, 1)

    def test_invalid_cli_input_fails_before_api_access(self):
        for arguments in [[VIDEO_ID + 'x'], [VIDEO_ID, '--language', 'en,'], [VIDEO_ID, '--language', '']]:
            output = io.StringIO()
            with self.subTest(arguments=arguments), patch.object(sys, 'argv', ['fetch_transcript.py', *arguments]), patch.object(helper, 'fetch_transcript') as fetch, contextlib.redirect_stdout(output):
                with self.assertRaises(SystemExit) as error:
                    helper.main()
                self.assertEqual(error.exception.code, 1)
                fetch.assert_not_called()
                self.assertIn('error', json.loads(output.getvalue()))

    def test_no_tracks(self):
        with self.assertRaises(SystemExit) as error:
            self.run_cli([])
        self.assertEqual(error.exception.code, 1)

if __name__ == '__main__':
    unittest.main()
