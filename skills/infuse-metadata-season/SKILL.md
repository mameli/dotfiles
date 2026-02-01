---
name: infuse-metadata-season
description: Normalize TV/anime season folders and filenames so Infuse can discover metadata. Use when a user says wants file/folder renames for Infuse or other media managers.
---

# Infuse Metadata Season

## Overview

Standardize a single show/season’s folder structure and episode filenames so Infuse can identify the series, season, and episode numbers reliably.

## Workflow

### 1) Gather required inputs

Ask for the minimum needed to rename safely:

- Series title (exact canonical title)
- Season number (and optional season name if it’s a split cour)
- Current folder path and a directory listing
- Episode ordering source (user-confirmed or file order)
- Preferred naming pattern if they already use one

If the user provides a message like “this is season 2 of X,” still request the folder path and current filenames before renaming.

### 2) Choose a consistent structure

Default structure (adjust if the user already has a house style):

```
Show Name (Year)/
  Season 02/
    Show Name - S02E01.ext
```

Notes:
- Include year only if the user wants disambiguation.
- Use zero-padded season/episode numbers (S02E01).
- Keep episode titles out unless the user requests them.

### 3) Build the rename map

Create a before/after mapping so the user can confirm:

- Folder rename(s)
- Each episode filename rename

If episode numbers are unclear, pause and ask for the correct ordering rather than guessing.

### 4) Apply changes

Use safe renames only after user confirmation of the mapping.

### 5) Validate

Re-list the directory to confirm the final structure and that all files follow a single pattern.

## Quick prompts to reuse

- “Please paste the current folder path and filenames so I can build a rename map.”
- “What is the canonical title and season number you want Infuse to match?”
- “Should I include the year in the show folder name, or omit it?”
- “Do you want episode titles in filenames, or just SxxExx?”
