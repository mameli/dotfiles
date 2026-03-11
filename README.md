# dotfiles

A collection of dotfiles and configuration scripts for macOS, focused on zsh, vim, and developer tools.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/dotfiles.git
   cd dotfiles
   ```

2. Install Homebrew if it is not already available:
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

3. Run the Homebrew installation script to install required tools, including zsh and the Cascadia Code font used by the Ghostty config:
   ```bash
   ./brew.sh
   ```

4. Install Oh My Zsh:
   ```bash
   sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
   ```

5. Copy configuration files (e.g., zshrc) to your home directory or source them as needed.

6. Copy OpenCode agents to the config directory:
   ```bash
   ./copy_agents.sh
   ```

7. Copy Codex/OpenCode/Claude Code skills to your desired config directory:
   ```bash
   ./copy_skills.sh ~/.codex/skills
   ./copy_skills.sh ~/.config/opencode/skills
   ```
   Notes:
   - Codex skills live under `~/.codex/skills` (or `.codex/skills` in a repo).
   - OpenCode skills live under `~/.config/opencode/skills` (or `.opencode/skills` in a repo).
   - Claude Code skills live under `~/.claude/skills` (or `.claude/skills` in a repo).
   - The script accepts either the root folder (e.g. `~/.codex`) or the final skills path.

8. For Ghostty terminal configuration, copy `config_ghostty.txt` to your Ghostty config location.

9. List the available Ghostty themes with:
    ```bash
    ghostty +list-themes
    ```

## Configurations Included

- **zshrc**: Zsh configuration with Oh My Zsh, plugins (git, docker, docker-compose), autosuggestions, syntax highlighting, Zoxide, Atuin, and custom aliases/functions.
- **brew.sh**: Script to install essential Homebrew packages and casks like Git, Python, Bun, zsh, Ghostty, Cascadia Code, Bitwarden, Maccy, and more.
- **copy_agents.sh**: Script to copy OpenCode custom agents to the config directory.
- **copy_skills.sh**: Script to copy Codex/OpenCode/Claude Code skills to a chosen destination.
- **config_ghostty.txt**: Configuration for Ghostty terminal emulator.

## Requirements

- macOS
- Homebrew
