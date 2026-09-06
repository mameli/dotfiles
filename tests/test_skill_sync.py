"""Isolated integration tests: only temporary local bare remotes/installations.
Run: python3 -m unittest discover -s tests -p 'test_skill_sync.py' -v
The small scanner double tests orchestration/failure handling; real gitleaks
integration is included when gitleaks is installed (otherwise explicitly skipped).
"""
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "skill_sync.py"
spec = importlib.util.spec_from_file_location("skill_sync", SCRIPT)
assert spec is not None and spec.loader is not None
engine = importlib.util.module_from_spec(spec)
spec.loader.exec_module(engine)
TEXT = "title\none\ntwo\nthree\nfour\nfive\nsix\nseven\neight\nnine\nend\n"


def command(*args, cwd=None):
    p = subprocess.run([str(x) for x in args], cwd=cwd, capture_output=True)
    if p.returncode:
        raise AssertionError((args, p.returncode, p.stderr.decode()))
    return p.stdout.decode().strip()


class SyncTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="skill-sync-test-")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()
        self.remote = self.root / "remote.git"
        self.author = self.root / "author"
        self.workspace = self.root / "workspace"
        self.a, self.b = self.root / "hermes" / "demo", self.root / "codex" / "demo"
        self.cache = self.root / "cache"
        command("git", "init", "--bare", self.remote)
        command("git", "init", "-b", "main", self.author)
        self.g("config", "user.name", "Test")
        self.g("config", "user.email", "test@localhost")
        self.write(self.author / "skills/demo/SKILL.md", TEXT)
        self.write(self.author / "unrelated.txt", "leave me alone\n")
        self.g("add", "--", "skills/demo/SKILL.md", "unrelated.txt")
        self.g("commit", "-m", "initial")
        self.g("remote", "add", "origin", str(self.remote))
        self.g("push", "-u", "origin", "main")
        command("git", "symbolic-ref", "HEAD", "refs/heads/main", cwd=self.remote)
        command("git", "clone", self.remote, self.workspace)
        for t in (self.a, self.b):
            self.write(t / "SKILL.md", TEXT)
        self.scanner = self.root / "scanner"
        self.log = self.root / "scans.log"
        self.write(self.scanner, '#!' + sys.executable + '\nimport pathlib,sys\np=pathlib.Path(__file__).parent\nwith (p/"scans.log").open("a") as f: f.write(" ".join(sys.argv[1:])+"\\n")\nif (p/"fail-scanner").exists(): sys.exit(1)\npathlib.Path(sys.argv[sys.argv.index("--report-path")+1]).write_text("[]")\n')
        self.scanner.chmod(0o700)
        self.config = self.root / "config.json"
        self.cfg = {"version": 1, "remote": str(self.remote), "branch": "main", "workspace": str(self.workspace), "cache_dir": str(self.cache), "scanner": str(self.scanner), "mappings": [{"catalog": "skills/demo", "targets": [str(self.a), str(self.b)]}]}
        self.save_config()

    def save_config(self):
        self.write(self.config, json.dumps(self.cfg))
        self.config.chmod(0o600)

    @staticmethod
    def write(path, content):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content if isinstance(content, bytes) else content.encode())

    def g(self, *args):
        return command("git", *args, cwd=self.author)

    def invoke(self, apply=True, ok=True):
        p = subprocess.run([sys.executable, str(SCRIPT), "--config", str(self.config), "--apply" if apply else "--dry-run"], capture_output=True, text=True)
        self.assertEqual(p.returncode, 0 if ok else 1, p.stdout + p.stderr)
        return p

    def tip(self):
        return command("git", "rev-parse", "refs/heads/main", cwd=self.remote)

    def published(self, path="skills/demo/SKILL.md"):
        return command("git", "show", "refs/heads/main:" + path, cwd=self.remote) + "\n"

    def publish(self, content, path="skills/demo/SKILL.md"):
        self.g("pull", "--ff-only")
        if content is None:
            self.g("rm", "--", path)
        else:
            self.write(self.author / path, content)
            self.g("add", "--", path)
        self.g("commit", "-m", "remote edit")
        self.g("push", "origin", "main")

    def test_initial_idempotent_and_scan_both_modes(self):
        self.invoke()
        p = self.invoke()
        self.assertEqual(p.stdout, "")
        calls = self.log.read_text().splitlines()
        self.assertEqual(len(calls), 4)
        self.assertTrue(calls[0].startswith("dir "))
        self.assertTrue(calls[1].startswith("git "))
        for line in calls:
            self.assertIn("--redact", line)
            self.assertIn("--config", line)
            self.assertIn("--ignore-gitleaks-allow", line)
            self.assertIn("--gitleaks-ignore-path", line)

    def test_local_to_remote_and_two_installations_unrelated_untouched(self):
        self.invoke()
        self.write(self.workspace / "unrelated.txt", "uncommitted unrelated\n")
        self.write(self.a / ".env", "DO_NOT_COPY=local\n")
        self.write(self.a / "cache/junk.md", "cache\n")
        self.write(self.a / "SKILL.md", TEXT.replace("title", "local title"))
        old_workspace = (self.workspace / "skills/demo/SKILL.md").read_bytes()
        self.invoke()
        self.assertEqual(self.published(), (self.a / "SKILL.md").read_text())
        self.assertEqual((self.b / "SKILL.md").read_bytes(), (self.a / "SKILL.md").read_bytes())
        self.assertEqual((self.workspace / "skills/demo/SKILL.md").read_bytes(), old_workspace)
        self.assertEqual((self.workspace / "unrelated.txt").read_text(), "uncommitted unrelated\n")
        self.assertEqual(self.published("unrelated.txt"), "leave me alone\n")
        self.assertFalse((self.cache / "clone/skills/demo/.env").exists())
        self.assertTrue((self.a / ".env").exists())

    def test_remote_to_local(self):
        self.invoke()
        self.publish(TEXT.replace("title", "remote title"))
        self.invoke()
        self.assertEqual((self.a / "SKILL.md").read_text(), self.published())
        self.assertEqual((self.b / "SKILL.md").read_text(), self.published())

    def test_disjoint_three_way_three_sources(self):
        self.invoke()
        self.publish(TEXT.replace("title", "remote title"))
        self.write(self.a / "SKILL.md", TEXT.replace("four", "local four"))
        self.write(self.b / "SKILL.md", TEXT.replace("end", "other end"))
        self.invoke()
        expected = TEXT.replace("title", "remote title").replace("four", "local four").replace("end", "other end")
        self.assertEqual(self.published(), expected)
        self.assertEqual((self.a / "SKILL.md").read_text(), expected)
        self.assertEqual((self.b / "SKILL.md").read_text(), expected)

    def test_conflict_blocks_every_installation_preserves_versions(self):
        self.invoke()
        state = (self.cache / "state.json").read_bytes()
        self.publish(TEXT.replace("title", "remote"))
        self.write(self.a / "SKILL.md", TEXT.replace("title", "local"))
        self.write(self.b / "extra.md", "independent addition\n")
        tip = self.tip()
        self.invoke(ok=False)
        self.assertEqual(self.tip(), tip)
        self.assertEqual((self.b / "SKILL.md").read_text(), TEXT)
        self.assertFalse((self.a / "extra.md").exists())
        self.assertEqual((self.cache / "state.json").read_bytes(), state)
        conflicts = list((self.cache / "conflicts").glob("*.json"))
        self.assertEqual(len(conflicts), 1)
        conflict = json.loads(conflicts[0].read_text())[0]
        self.assertEqual({item["path"] for item in conflict["targets"]}, {str(self.a), str(self.b)})
        self.assertIn("remote", conflict)
        self.assertEqual(conflicts[0].stat().st_mode & 0o077, 0)

    def test_delete_modify_blocks_and_plain_delete_propagates(self):
        self.write(self.a / "extra.md", "base\n")
        self.invoke()
        (self.a / "extra.md").unlink()
        self.write(self.b / "extra.md", "modified\n")
        self.invoke(ok=False)
        self.assertEqual((self.b / "extra.md").read_text(), "modified\n")
        self.write(self.b / "extra.md", "base\n")
        self.invoke()
        self.assertFalse((self.b / "extra.md").exists())
        self.assertFalse((self.cache / "clone/skills/demo/extra.md").exists())

    def test_first_absent_installation_is_install_later_absence_blocks(self):
        shutil.rmtree(self.b)
        self.invoke()
        self.assertEqual((self.b / "SKILL.md").read_text(), TEXT)
        shutil.rmtree(self.b)
        self.invoke(ok=False)
        self.assertFalse(self.b.exists())

    def test_new_target_absence_not_deletion(self):
        self.write(self.a / "extra.md", "present\n")
        self.invoke()
        third = self.root / "opencode/demo"
        self.cfg["mappings"][0]["targets"].append(str(third))
        self.save_config()
        self.invoke()
        self.assertEqual((third / "extra.md").read_text(), "present\n")
        self.assertEqual((third / "SKILL.md").read_text(), TEXT)

    def test_disable_target_does_not_delete_shared_skill(self):
        self.invoke()
        self.cfg["mappings"][0]["targets"].remove(str(self.b))
        self.save_config()
        shutil.rmtree(self.b)
        self.invoke()
        self.assertEqual(self.published(), TEXT)
        self.assertFalse(self.b.exists())
        self.cfg["mappings"][0]["targets"].append(str(self.b))
        self.save_config()
        self.invoke()
        self.assertEqual((self.b / "SKILL.md").read_text(), TEXT)

    def test_disable_mapping_does_not_delete_catalog(self):
        other = self.root / "hermes/other"
        self.write(other / "SKILL.md", "other skill\n")
        self.cfg["mappings"].append({"catalog": "skills/other", "targets": [str(other)]})
        self.save_config()
        self.invoke()
        self.cfg["mappings"].pop()
        self.save_config()
        shutil.rmtree(other)
        self.invoke()
        self.assertEqual(self.published("skills/other/SKILL.md"), "other skill\n")
        self.assertFalse(other.exists())

    def test_dry_run_no_state_installation_or_public_changes(self):
        shutil.rmtree(self.b)
        self.write(self.a / "new.md", "new\n")
        tip = self.tip()
        self.invoke(apply=False)
        self.assertEqual(self.tip(), tip)
        self.assertFalse(self.b.exists())
        for name in ("state.json", "pending.json", "backups", "conflicts"):
            self.assertFalse((self.cache / name).exists())
        self.assertFalse((self.workspace / "skills/demo/new.md").exists())

    def test_missing_or_failing_scanner_fails_closed(self):
        self.write(self.a / "new.md", "new\n")
        tip = self.tip()
        self.write(self.root / "fail-scanner", "yes")
        self.invoke(ok=False)
        self.assertEqual(self.tip(), tip)
        self.assertFalse((self.b / "new.md").exists())
        self.scanner.unlink()
        self.invoke(ok=False)
        self.assertFalse((self.cache / "state.json").exists())

    def test_push_rejected_preserves_edits_and_blocks_retry(self):
        self.invoke()
        state = (self.cache / "state.json").read_bytes()
        self.write(self.a / "SKILL.md", TEXT + "local edit\n")
        hook = self.remote / "hooks/pre-receive"
        self.write(hook, "#!/bin/sh\nexit 1\n")
        hook.chmod(0o700)
        tip = self.tip()
        self.invoke(ok=False)
        self.assertEqual(self.tip(), tip)
        self.assertEqual((self.a / "SKILL.md").read_text(), TEXT + "local edit\n")
        self.assertEqual((self.b / "SKILL.md").read_text(), TEXT)
        self.assertTrue((self.cache / "pending.json").exists())
        self.assertEqual((self.cache / "state.json").read_bytes(), state)
        self.assertIn("interrupted transaction", self.invoke(ok=False).stderr)

    def test_interrupted_deployment_keeps_base_and_journal(self):
        self.invoke()
        old = (self.cache / "state.json").read_bytes()
        self.publish(TEXT + "remote edit\n")
        original_put = engine.put
        def interrupted(path, content, mode=None):
            if path == self.b / "SKILL.md":
                raise OSError("simulated interruption")
            return original_put(path, content, mode)
        with mock.patch.object(engine, "put", side_effect=interrupted):
            with self.assertRaises(OSError):
                engine.sync(engine.config_load(self.config), True)
        self.assertEqual((self.cache / "state.json").read_bytes(), old)
        self.assertTrue((self.cache / "pending.json").exists())
        self.assertIn("interrupted transaction", self.invoke(ok=False).stderr)
        self.assertEqual((self.b / "SKILL.md").read_text(), TEXT)

    def test_concurrent_edit_after_scan_not_overwritten(self):
        self.invoke()
        self.publish(TEXT + "remote\n")
        original_scanner = engine.scanner
        def racing(*args):
            original_scanner(*args)
            self.write(self.a / "SKILL.md", "user concurrent edit\n")
        with mock.patch.object(engine, "scanner", side_effect=racing):
            with self.assertRaisesRegex(engine.Blocked, "changed during planning"):
                engine.sync(engine.config_load(self.config), True)
        self.assertEqual((self.a / "SKILL.md").read_text(), "user concurrent edit\n")
        self.assertEqual((self.b / "SKILL.md").read_text(), TEXT)

    def test_dirty_managed_and_outgoing_managed_checkout_block(self):
        self.write(self.workspace / "skills/demo/SKILL.md", "dirty\n")
        self.assertIn("dirty managed", self.invoke(ok=False).stderr)
        command("git", "-c", "user.name=Test", "-c", "user.email=test@localhost", "commit", "-am", "outgoing", cwd=self.workspace)
        self.assertIn("outgoing commits", self.invoke(ok=False).stderr)

    def test_binary_conflict_and_symlink_block(self):
        self.write(self.a / "data.txt", b"a\0base")
        self.invoke()
        self.write(self.a / "data.txt", b"a\0ours")
        self.write(self.b / "data.txt", b"a\0theirs")
        self.invoke(ok=False)
        self.assertEqual((self.b / "data.txt").read_bytes(), b"a\0theirs")
        (self.a / "link.md").symlink_to(self.root / "outside")
        self.assertIn("symlink", self.invoke(ok=False).stderr)

    def test_executable_script_mode_preserved(self):
        self.write(self.a / "run.sh", "#!/bin/sh\nprintf 'ok\\n'\n")
        (self.a / "run.sh").chmod(0o755)
        self.invoke()
        self.assertTrue((self.b / "run.sh").stat().st_mode & 0o111)
        self.assertTrue((self.cache / "clone/skills/demo/run.sh").stat().st_mode & 0o111)
        self.assertEqual(self.invoke().stdout, "")

    def test_real_gitleaks_rejects_secret_even_allow_comment_and_env(self):
        scanner = shutil.which("gitleaks") or ("/opt/homebrew/bin/gitleaks" if Path("/opt/homebrew/bin/gitleaks").exists() else None)
        if not scanner:
            self.skipTest("real gitleaks not installed")
        self.cfg["scanner"] = str(Path(scanner).resolve())
        self.save_config()
        self.invoke()  # real scanner accepts safe tree and empty outgoing range
        token = "ghp_" + "aB3dE6gH9jK2mN5pQ8sT1vW4yZ7cF0iL3oR6"
        self.write(self.a / "leak.md", "github_token = " + token + " # gitleaks:allow\n")
        tip = self.tip()
        bypass = self.root / "bypass.toml"
        self.write(bypass, '[allowlist]\npaths=[".*"]\n')
        with mock.patch.dict(os.environ, {"GITLEAKS_CONFIG": str(bypass)}):
            result = self.invoke(ok=False)
        self.assertNotIn(token, result.stderr)
        self.assertEqual(self.tip(), tip)
        self.assertFalse((self.b / "leak.md").exists())
        self.assertFalse((self.cache / "pending.json").exists())

    def test_remote_scanner_policy_override_blocks(self):
        self.publish('[allowlist]\npaths=[".*"]\n', "skills/demo/.gitleaks.toml")
        self.assertIn("disallowed remote managed file", self.invoke(ok=False).stderr)
        self.assertFalse((self.cache / "state.json").exists())

    def test_lock_blocks_parallel_run(self):
        import fcntl
        self.cache.mkdir(mode=0o700)
        with (self.cache / "lock").open("a+b") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            self.assertIn("holds the lock", self.invoke(ok=False).stderr)


if __name__ == "__main__":
    unittest.main()
