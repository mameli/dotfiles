---
name: sync-skills
description: "Use when syncing custom skills across PCs and agents."
---

# Sync skills

Manage the selected custom skills for Hermes, Codex and OpenCode with the
trusted local sync script, not a blind copy or an LLM rewrite.

## Run

Private settings: `${XDG_CONFIG_HOME:-$HOME/.config}/agent-skills/sync.json`.
Trusted script: `${XDG_DATA_HOME:-$HOME/.local/share}/agent-skills/skill_sync.py`.

```sh
python3 "${XDG_DATA_HOME:-$HOME/.local/share}/agent-skills/skill_sync.py" \
  --config "${XDG_CONFIG_HOME:-$HOME/.config}/agent-skills/sync.json" --dry-run
# After inspecting the dry-run, use --apply instead of --dry-run.
```

The JSON lists the repository, private cache directory and explicit catalog-to-
installation mappings. Each PC chooses its own targets. Keep populated settings,
state, conflict snapshots and backups outside Git. Reuse the existing private
`agent-skills/env.zsh` for skill runtime variables; the sync engine does not source it.

## Safety

- Do not run `copy_skills.sh` against a managed installation: it is one-way and
  can overwrite local changes without reconciliation.
- Never resolve a conflict by deleting state or choosing the newest timestamp.
- A dirty/manual outgoing change in a managed dotfiles path blocks the run;
  inspect and commit/publish or deliberately move that work before retrying.
- Never remove a local skill to request a shared deletion. Remove a target from
  private selection to stop managing it. Catalog removals require explicit review.
- Do not execute remote scripts during synchronization. To update the trusted
  engine, review its diff, run isolated tests, then deliberately replace the local copy.
- Scanner failures block publication. Report paths/categories, never values.

For setup, conflicts, recovery and the weekly Hermes script-only job, read
`references/operations.md`. Use native Hermes cron tooling to inspect/update the
existing job by name; never create a duplicate or edit its storage directly.
