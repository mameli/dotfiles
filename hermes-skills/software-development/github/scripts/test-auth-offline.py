#!/usr/bin/env python3
"""Offline regression suite. All GitHub/network/git commands are fixture stubs.
Run: python3 <skill_dir>/scripts/test-auth-offline.py
Fixtures use the system temporary directory and are removed after each test;
the installed skill may be read-only.
"""
import os
from pathlib import Path
import runpy
import shlex
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent
PARSER = runpy.run_path(str(ROOT / 'scripts/git-credential-token.py'))
STUB = '''import json, os, pathlib, sys
name = pathlib.Path(sys.argv[0]).name
args = sys.argv[1:]
if name == 'gh':
    if os.environ.get('STUB_GH') != 'ok': sys.exit(1)
    if args == ['auth', 'status', '--hostname', 'github.com']: sys.exit(0)
    if args == ['api', '--hostname', 'github.com', 'user', '--jq', '.login']:
        print('fixture-user'); sys.exit(0)
    sys.exit(90)
if name == 'git':
    if args != ['remote', 'get-url', 'origin']: sys.exit(91)
    print(os.environ.get('STUB_REMOTE', '')); sys.exit(0)
if name == 'curl':
    expected = 'Authorization: Bearer ' + os.environ.get('EXPECTED_TOKEN', '') + '\\n'
    valid = (sys.stdin.read() == expected and '--header' in args
             and args[args.index('--header') + 1] == '@-'
             and args[-1] == 'https://api.github.com/user'
             and not any(os.environ.get('EXPECTED_TOKEN', 'NEVER') in x for x in args))
    pathlib.Path(os.environ['CURL_MARKER']).write_text('valid' if valid else 'invalid')
    if not valid or os.environ.get('STUB_CURL') == 'fail': sys.exit(22)
    print(json.dumps({'login': 'fixture-user'})); sys.exit(0)
sys.exit(92)
'''

class AuthTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='hermes-offline-auth-')
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.home = self.base / 'home'
        self.profile = self.base / 'profile'
        self.bin = self.base / 'bin'
        for directory in (self.home, self.profile, self.bin): directory.mkdir()
        for name in ('gh', 'curl', 'git'):
            path = self.bin / name
            path.write_text('#!' + sys.executable + '\n' + STUB)
            path.chmod(0o700)
        # Relocating a uv/standalone interpreter via a symlink can break its
        # stdlib discovery. Execute the original path instead.
        python = self.bin / 'python3'
        python.write_text('#!/bin/sh\nexec ' + shlex.quote(sys.executable) + ' "$@"\n')
        python.chmod(0o700)
        self.env = {'HOME': str(self.home), 'HERMES_HOME': str(self.profile),
                    'PATH': str(self.bin) + ':/usr/bin:/bin',
                    'CURL_MARKER': str(self.base / 'curl-marker'),
                    'LC_ALL': 'C', 'EXPECTED_TOKEN': 'fixture-credential'}

    def source(self, method='curl', repo='', wrapper=False):
        script = ROOT / 'scripts' / ('github-auth-gh-env.sh' if wrapper else 'gh-env.sh')
        result = subprocess.run(['/bin/bash', '-c',
            'set -euo pipefail; source "$1"; printf "RESULT=%s|%s|%s\\n" "$GH_AUTH_METHOD" "$GH_USER" "$GH_OWNER_REPO"',
            'offline-test', str(script)], env=self.env, cwd=self.base,
            capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0, 'helper failed under strict Bash')
        user = '' if method == 'none' else 'fixture-user'
        self.assertIn('RESULT=' + method + '|' + user + '|' + repo, result.stdout)
        self.assertNotIn(self.env['EXPECTED_TOKEN'], result.stdout + result.stderr)
        marker = self.base / 'curl-marker'
        if method == 'curl': self.assertEqual(marker.read_text(), 'valid')
        return result

    def test_fixture_python_stdlib(self):
        result = subprocess.run([str(self.bin / 'python3'), '-c',
            'import json, sys; print(json.dumps({"ok": True}))'],
            env=self.env, capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0)
        self.assertIn('"ok": true', result.stdout)

    def test_missing_credentials_strict_shell(self): self.source('none')
    def test_gh_preferred(self):
        self.env.update(STUB_GH='ok', GITHUB_TOKEN='fixture-credential')
        self.source('gh')
        self.assertFalse((self.base / 'curl-marker').exists())
    def test_environment_token(self):
        self.env['GITHUB_TOKEN'] = 'fixture-credential'
        self.source()
    def test_gh_token_precedence(self):
        self.env.update(GH_TOKEN='fixture-credential', GITHUB_TOKEN='other-fixture')
        self.source()
    def test_profile_quoted_equals_token(self):
        self.env['EXPECTED_TOKEN'] = 'fixture=credential'
        (self.profile / '.env').write_text('export GITHUB_TOKEN="fixture=credential" # comment\n')
        self.source()
    def test_other_profile_not_read(self):
        (self.home / '.hermes').mkdir()
        (self.home / '.hermes/.env').write_text('GITHUB_TOKEN=fixture-credential\n')
        self.source('none')
    def test_empty_env_falls_through_to_store(self):
        (self.profile / '.env').write_text('GITHUB_TOKEN=\n')
        (self.home / '.git-credentials').write_text('https://user:fixture-credential@github.com\n')
        self.source()
    def test_encoded_store_token(self):
        (self.home / '.git-credentials').write_text('https://user:fixture%2Dcredential@github.com\n')
        self.source()
    def test_failed_rest_is_not_authenticated(self):
        self.env.update(GITHUB_TOKEN='fixture-credential', STUB_CURL='fail')
        self.source('none')
    def test_header_injection_rejected(self):
        self.env['GITHUB_TOKEN'] = 'fixture-credential\nInjected: true'
        self.source('none')
        self.assertFalse((self.base / 'curl-marker').exists())
    def test_remote_formats_and_spoofs(self):
        for remote, expected in [('https://github.com/owner/repo.git', 'owner/repo'),
            ('git@github.com:owner/repo.git', 'owner/repo'),
            ('ssh://git@github.com/owner/repo', 'owner/repo'),
            ('https://github.com.evil/owner/repo.git', ''),
            ('https://evil/github.com/owner/repo.git', '')]:
            with self.subTest(remote=remote):
                self.env['STUB_REMOTE'] = remote
                self.source('none', expected)
    def test_wrapper(self):
        self.env['GITHUB_TOKEN'] = 'fixture-credential'
        self.source(wrapper=True)
    def test_trace_refused(self):
        self.env['GITHUB_TOKEN'] = 'fixture-credential'
        result = subprocess.run(['/bin/bash', '-xc', 'source "$1"', 'test',
            str(ROOT / 'scripts/gh-env.sh')], env=self.env, cwd=self.base,
            capture_output=True, text=True, timeout=10)
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn('fixture-credential', result.stdout + result.stderr)
    def test_dotenv_not_executed(self):
        (self.profile / '.env').write_text('touch SHOULD_NOT_EXIST\nGITHUB_TOKEN=fixture-credential\n')
        self.source()
        self.assertFalse((self.base / 'SHOULD_NOT_EXIST').exists())
    def test_credential_parser_security_and_unique_formats(self):
        cases = {'https://user:fixture-credential@github.com': 'fixture-credential',
            'https://fixture-credential:x-oauth-basic@github.com': 'fixture-credential',
            'https://ghp_fixture@github.com': 'ghp_fixture',
            'https://user:fixture-credential@github.com:443': 'fixture-credential',
            'https://user:fixture-credential@github.com.evil': '',
            'http://user:fixture-credential@github.com': '',
            'https://user:fixture-credential@github.com:444': '',
            'https://user:bad%0Atoken@github.com': '',
            'https://user:bad%XXtoken@github.com': '',
            'https://user@github.com': ''}
        for url, expected in cases.items():
            self.assertTrue(PARSER['_token_from_url'](url) == expected, 'credential parser regression')

if __name__ == '__main__':
    unittest.main(verbosity=2)
