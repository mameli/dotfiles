"""Offline CLI portability tests; only temporary fixture repositories are read."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).with_name('validate_album_data.py')


class PortabilityTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='maoty portability ')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.repo = self.root / 'repo with spaces'
        self.data = self.repo / 'src/data/album-list.json'
        self.data.parent.mkdir(parents=True)
        self.data.write_text('[]')
        self.env = {k: v for k, v in os.environ.items() if k != 'MAOTY_REPO_PATH'}

    def run_cli(self, *args, value=None):
        env = self.env.copy()
        if value is not None:
            env['MAOTY_REPO_PATH'] = value
        return subprocess.run([sys.executable, '-B', str(SCRIPT), *args], env=env,
                              cwd=self.root, capture_output=True, text=True)

    def test_missing_and_empty(self):
        for value in (None, '', ' '):
            result = self.run_cli(value=value)
            self.assertEqual(result.returncode, 2)
            self.assertIn('MAOTY_REPO_PATH', result.stderr)
            self.assertNotIn('Traceback', result.stderr)

    def test_environment_absolute_spaces(self):
        result = self.run_cli(value=str(self.repo))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['album_count'], 0)

    def test_explicit_overrides_bad_environment(self):
        result = self.run_cli(str(self.repo), value=str(self.root / 'missing'))
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_relative_spaces(self):
        self.assertEqual(self.run_cli('repo with spaces').returncode, 0)

    def test_explicit_empty_does_not_fall_back(self):
        self.assertEqual(self.run_cli('', value=str(self.repo)).returncode, 2)

    def test_missing_and_invalid_dataset(self):
        for content in ('not json', '{}', '[1]'):
            self.data.write_text(content)
            result = self.run_cli(str(self.repo))
            self.assertEqual(result.returncode, 2)
            self.assertNotIn('Traceback', result.stderr)
        self.data.unlink()
        self.assertEqual(self.run_cli(str(self.repo)).returncode, 2)


if __name__ == '__main__':
    unittest.main()
