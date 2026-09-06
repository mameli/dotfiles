import importlib.util
from datetime import datetime
import contextlib
import io
import json
from pathlib import Path
import tempfile
import types
import unittest
from zoneinfo import ZoneInfo

spec = importlib.util.spec_from_file_location("schedule", Path(__file__).resolve().parents[1] / "scripts/skill_sync_schedule.py")
assert spec is not None and spec.loader is not None
schedule = importlib.util.module_from_spec(spec)
spec.loader.exec_module(schedule)


class ScheduleTests(unittest.TestCase):
    def test_dst_and_weekly_window(self):
        for stamp in ["2026-10-25T20:00:00+00:00", "2027-03-28T19:00:00+00:00"]:
            now = datetime.fromisoformat(stamp)
            self.assertTrue(schedule.due(now, None))
            self.assertFalse(schedule.due(now, now.astimezone(ZoneInfo("Europe/Rome")).date().isoformat()))
        for stamp in ["2026-10-25T19:00:00+00:00", "2026-10-25T21:00:00+00:00", "2026-10-26T20:00:00+00:00", "2027-03-28T20:00:00+00:00"]:
            self.assertFalse(schedule.due(datetime.fromisoformat(stamp), None))

    def test_non_due_no_settings_needed(self):
        self.assertEqual(schedule.tick(Path("/nonexistent"), now=datetime.fromisoformat("2026-10-26T20:00:00+00:00")), 0)

    def test_success_silent_and_deduped(self):
        self.exercise(0)

    def test_failure_not_marked_success(self):
        self.exercise(1)

    def exercise(self, status):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d).resolve()
            cfg = root / "settings.json"
            cfg.write_text(json.dumps({"python": str(root / "python"), "engine": str(root / "engine"), "sync_config": str(root / "sync.json"), "state_dir": str(root / "state")}))
            cfg.chmod(0o600)
            calls = []
            def run(args, **kwargs):
                calls.append(args)
                return types.SimpleNamespace(returncode=status, stdout="", stderr="blocked diagnostic" if status else "")
            now = datetime.fromisoformat("2026-10-25T20:00:00+00:00")
            stream = io.StringIO()
            with contextlib.redirect_stdout(stream):
                self.assertEqual(schedule.tick(cfg, now=now, runner=run), status)
                self.assertEqual(schedule.tick(cfg, now=now, runner=run), status)
            self.assertEqual(len(calls), 2 if status else 1)
            self.assertEqual((root / "state/schedule.json").exists(), not status)
            if not status:
                self.assertEqual(stream.getvalue(), "")
            else:
                self.assertIn("blocked diagnostic", stream.getvalue())
            self.assertEqual(calls[0][-1], "--apply")


if __name__ == "__main__":
    unittest.main()
