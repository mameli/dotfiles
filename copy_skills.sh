#!/bin/bash

# Copy skills from this repo to a user-specified destination.
# Usage: ./copy_skills.sh /path/to/destination
# Examples:
#   ./copy_skills.sh ~/.codex
#   ./copy_skills.sh ~/.codex/skills
#   ./copy_skills.sh ~/.config/opencode
#   ./copy_skills.sh ~/.config/opencode/skills
#   ./copy_skills.sh ~/.claude
#   ./copy_skills.sh ~/.claude/skills

set -euo pipefail

SOURCE_DIR="./skills"
DEST_INPUT="${1:-}"

if [[ -z "$DEST_INPUT" ]]; then
  echo "Usage: $0 /path/to/destination"
  exit 1
fi

if [[ ! -d "$SOURCE_DIR" ]]; then
  echo "Source directory not found: $SOURCE_DIR"
  exit 1
fi

normalize_dest() {
  local input="${1%/}"
  if [[ -n "${CODEX_HOME:-}" && "$input" == "$CODEX_HOME" ]]; then
    echo "$input/skills"
    return
  fi
  case "$input" in
    */.opencode/skill|*/.config/opencode/skill)
      # Accept historical OpenCode path and normalize to /skills.
      echo "${input%/skill}/skills"
      ;;
    */skills|*/skill)
      echo "$input"
      ;;
    */.codex)
      echo "$input/skills"
      ;;
    */.opencode|*/.config/opencode)
      echo "$input/skills"
      ;;
    */.claude)
      echo "$input/skills"
      ;;
    *)
      echo "$input"
      ;;
  esac
}

DEST_DIR="$(normalize_dest "$DEST_INPUT")"

mkdir -p "$DEST_DIR"

# Preserve structure; update only when content differs.
rsync -a --checksum "$SOURCE_DIR"/ "$DEST_DIR"/

echo "Copied skills from $SOURCE_DIR to $DEST_DIR"
