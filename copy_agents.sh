#!/bin/bash

# Copy agents from local dotfiles repo to opencode config, only if not present

SOURCE_DIR="./agent"
DEST_DIR="$HOME/.config/opencode/agent"

# Ensure destination directory exists
mkdir -p "$DEST_DIR"

for file in "$SOURCE_DIR"/*; do
    if [[ -f "$file" ]]; then
        basename=$(basename "$file")
        if [[ ! -e "$DEST_DIR/$basename" ]] || ! cmp -s "$file" "$DEST_DIR/$basename"; then
            cp "$file" "$DEST_DIR/"
            echo "Copied $basename to $DEST_DIR"
        else
            echo "$basename already exists with same content, skipping"
        fi
    fi
done

echo "Copy operation completed."