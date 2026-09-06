import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import types
import unittest

spec = importlib.util.spec_from_file_location("weekly", Path(__file__).resolve().parents[1] / "scripts/skill_sync_weekly.py")
assert spec is not None and spec.loader is not None
weekly = importlib.util.module_from_spec(spec)
spec.loader.exec_module(weekly)


class WeeklyTests(unittest.TestCase):
    def exercise(self, status):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d).resolve()
            cfg = root / "settings.json"
            cfg.write_text(json.dumps({"python": str(root / "python"), "engine": str(root / "engine"), "sync_config": str(root / "sync.json"), "state_dir": str(root / "state")}))
            cfg.chmod(0o600)
            calls = []
            def run(args, **kwargs):
                calls.append(args)
                return types.SimpleNamespace(returncode=status, stdout="" if not status else "synced: 1 catalog file change(s)",
                                             stderr="" if not status else "blocked diagnostic")
            stream = io.StringIO()
            with contextlib.redirect_stdout(stream):
                self.assertEqual(weekly.tick(cfg, runner=run), status)
            self.assertEqual(calls[0][-1], "--apply")
            if status:
                self.assertIn("blocked diagnostic", stream.getvalue())
            else:
                self.assertEqual(stream.getvalue(), "")

    def test_success_silent(self):
        self.exercise(0)

    def test_failure_reported(self):
        self.exercise(1)

    def test_bad_settings_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            cfg = Path(d) / "settings.json"
            cfg.write_text(json.dumps({"python": "relative", "engine": "/e", "sync_config": "/s", "state_dir": "/d"}))
            with self.assertRaises(ValueError):
                weekly.tick(cfg)


if __name__ == "__main__":
    unittest.main()
