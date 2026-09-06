#!/usr/bin/env python3
"""Trusted weekly Hermes entry point: run the sync engine once per tick.

No LLM, no shell initialization. The scheduler itself provides the weekly
cadence; this wrapper only locates the trusted engine and private config.
"""
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


def tick(settings, *, runner=subprocess.run):
    c = json.loads(Path(settings).read_text())
    if set(c) != {"python", "engine", "sync_config", "state_dir"}:
        raise ValueError("unsupported schedule settings")
    for key in ("python", "engine", "sync_config"):
        p = Path(c[key])
        if not p.is_absolute() or any(a.is_symlink() for a in (p, *p.parents)):
            raise ValueError("schedule paths must be absolute and not symlinked")
    result = runner([c["python"], c["engine"], "--config", c["sync_config"], "--apply"],
                    capture_output=True, text=True, timeout=900)
    # The trusted engine emits sanitized diagnostics only. Never print settings.
    output = result.stdout.strip()
    if output:
        print(output)
    if result.returncode:
        print(result.stderr.strip() or "skill-sync blocked: inspect private state")
    return result.returncode


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
        print("skill-sync blocked: invalid or inaccessible private schedule configuration")
        return 1


if __name__ == "__main__":
    sys.exit(main())
