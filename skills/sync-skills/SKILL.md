---
name: sync-skills
description: Sync skill folders from the current workspace `skills/` directory into Codex, OpenCode, or Claude skill folders. Use when a user asks to sync/copy/update skills into codex, opencode, or claude.
---

# Sync Skills

Use this skill to copy skills from the current repository into the requested target platform.

## Workflow

1. Confirm the current workspace contains a `skills/` folder.
2. Detect the target from the prompt and run:

```bash
# If target is codex
bash ./copy_skills.sh ~/.codex

# If target is opencode
bash ./copy_skills.sh ~/.config/opencode

# If target is claude
bash ./copy_skills.sh ~/.claude
```

3. Verify the sync completed:

```bash
ls -la ~/.codex/skills
ls -la ~/.config/opencode/skills
ls -la ~/.claude/skills
```

Only verify the directory for the selected target.

## Notes

- `copy_skills.sh` normalizes destinations:
  - `~/.codex` -> `~/.codex/skills`
  - `~/.config/opencode` or `~/.opencode` -> `.../skills`
  - `~/.claude` -> `~/.claude/skills`
- The copy uses `rsync --checksum`, so unchanged files are not recopied unnecessarily.
- If no target is provided, ask the user whether to sync to codex, opencode, or claude.
- If the script is run outside the repository root, run it with the full path, for example:

```bash
bash /path/to/dotfiles/copy_skills.sh ~/.codex
```
