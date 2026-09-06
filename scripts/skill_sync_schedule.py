#!/usr/bin/env python3
"""Trusted hourly Hermes entry point; run sync only Sunday 21:xx Europe/Rome.

No LLM, no shell initialization, no catch-up outside the Sunday window.
The engine and this entry point are deployed locally after explicit review.
"""
import argparse
from datetime import datetime
import fcntl
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from zoneinfo import ZoneInfo


def due(now, last_success):
    local = now.astimezone(ZoneInfo("Europe/Rome"))
    return local.weekday() == 6 and local.hour == 21 and last_success != local.date().isoformat()


def private_json(path):
    if path.is_symlink() or not path.is_file() or path.stat().st_mode & 0o077:
        raise ValueError("schedule settings/state must be private regular files (0600)")
    return json.loads(path.read_text())


def write_state(path, value):
    fd, tmp = tempfile.mkstemp(prefix=".schedule-", dir=path.parent)
    try:
        with os.fdopen(fd, "w") as handle:
            json.dump(value, handle)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def tick(settings, *, now=None, runner=subprocess.run):
    now = now or datetime.now(ZoneInfo("Europe/Rome"))
    # A non-due tick needs neither private credentials nor filesystem writes.
    if not due(now, None):
        return 0
    c = private_json(settings)
    if set(c) != {"python", "engine", "sync_config", "state_dir"}:
        raise ValueError("unsupported schedule settings")
    for key, value in c.items():
        p = Path(value)
        if not p.is_absolute() or any(a.is_symlink() for a in (p, *p.parents)):
            raise ValueError("schedule paths must be absolute and not symlinked")
    state_dir = Path(c["state_dir"])
    state_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
    if state_dir.stat().st_mode & 0o077:
        raise ValueError("schedule state directory must be private (0700)")
    lock_path = state_dir / "schedule.lock"
    if lock_path.is_symlink():
        raise ValueError("schedule lock must not be a symlink")
    with lock_path.open("a+b") as lock:
        os.chmod(lock_path, 0o600)
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            print("skill-sync: another scheduled run is active; skipped")
            return 1
        ledger = state_dir / "schedule.json"
        last = private_json(ledger).get("last_success") if ledger.exists() else None
        if not due(now, last):
            return 0
        result = runner([c["python"], c["engine"], "--config", c["sync_config"], "--apply"],
                        capture_output=True, text=True, timeout=900)
        # The trusted engine emits sanitized diagnostics only. Never print settings.
        output = result.stdout.strip()
        if output:
            print(output)
        if result.returncode:
            print(result.stderr.strip() or "skill-sync blocked: inspect private state")
            return result.returncode
        write_state(ledger, {"last_success": now.astimezone(ZoneInfo("Europe/Rome")).date().isoformat()})
        return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    default = Path(os.environ.get("XDG_CONFIG_HOME", str(Path.home() / ".config"))) / "agent-skills/schedule.json"
    parser.add_argument("--config", type=Path, default=default)
    args = parser.parse_args(argv)
    os.umask(0o077)
    try:
        return tick(args.config)
    except subprocess.TimeoutExpired:
        print("skill-sync blocked: scheduled execution timed out; inspect transaction state before retrying")
        return 1
    except (OSError, ValueError, KeyError, TypeError):
        print("skill-sync blocked: invalid or inaccessible private schedule configuration/state")
        return 1


if __name__ == "__main__":
    sys.exit(main())
