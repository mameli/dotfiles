# dotfiles

A collection of dotfiles and configuration scripts for macOS, focused on zsh, vim, and developer tools.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/dotfiles.git
   cd dotfiles
   ```

2. Run the Homebrew installation script to install required tools:
   ```bash
   ./brew.sh
   ```

3. Copy configuration files (e.g., zshrc) to your home directory or source them as needed.

4. Copy OpenCode agents to the config directory:
   ```bash
   ./copy_agents.sh
   ```

5. Copy Codex/OpenCode/Claude Code skills to your desired config directory:
   ```bash
   ./copy_skills.sh ~/.codex/skills
   ./copy_skills.sh ~/.config/opencode/skills
   ```
   Notes:
   - Codex skills live under `~/.codex/skills` (or `.codex/skills` in a repo).
   - OpenCode skills live under `~/.config/opencode/skills` (or `.opencode/skills` in a repo).
   - Claude Code skills live under `~/.claude/skills` (or `.claude/skills` in a repo).
   - The script accepts either the root folder (e.g. `~/.codex`) or the final skills path.

6. For Ghostty terminal configuration, copy `config_ghostty.txt` to your Ghostty config location.

## Configurations Included

- **zshrc**: Zsh configuration with Oh My Zsh, plugins (git, docker, docker-compose), autosuggestions, syntax highlighting, Zoxide, Atuin, and custom aliases/functions.
- **brew.sh**: Script to install essential Homebrew packages like Git, Python, OpenCode, Atuin, Zoxide, etc.
- **copy_agents.sh**: Script to copy OpenCode custom agents to the config directory.
- **copy_skills.sh**: Script to copy Codex/OpenCode/Claude Code skills to a chosen destination.
- **config_ghostty.txt**: Configuration for Ghostty terminal emulator.

## Requirements

- macOS
- Homebrew
