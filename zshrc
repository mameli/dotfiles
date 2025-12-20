# =============================================================================
# ZSH CONFIGURATION FILE
# =============================================================================

# Path to Oh My Zsh installation
export ZSH="$HOME/.oh-my-zsh"

# Theme configuration
ZSH_THEME="robbyrussell"

# Plugins to load
# Standard plugins can be found in $ZSH/plugins/
plugins=(git docker docker-compose)

# Oh My Zsh settings
ZSH_AUTOSUGGEST_HIGHLIGHT_STYLE="fg=#00ccff,bg=grey,bold"

# Initialize Oh My Zsh
source $ZSH/oh-my-zsh.sh

# ---------------------
# PATH CONFIGURATION
# ---------------------
# Ensure /usr/local/bin is in PATH
PATH="/usr/local/bin:$PATH"

# user bin
export PATH="$HOME/bin:$PATH"

# ---------------------
# ZSH EXTENSIONS
# ---------------------
# Zsh autosuggestions
source $(brew --prefix)/share/zsh-autosuggestions/zsh-autosuggestions.zsh

# Zsh syntax highlighting
source $(brew --prefix)/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh

# Zoxide navigation
eval "$(zoxide init zsh)"

# Atuin shell history
eval "$(atuin init zsh)"

# ---------------------
# PYTHON/UV CONFIGURATION
# ---------------------
# Source uv environment
source $HOME/.local/bin/env

# ---------------------
# ENVIRONMENT VARIABLES
# ---------------------
# Current folder variable
export CURRENT_FOLDER=$(basename "$PWD")

# VSCode suggestion
export VSCODE_SUGGEST=1

export EDITOR="code --wait"

# ---------------------
# ALIASES
# ---------------------

# Shell reload aliases
alias reload_shell="source $HOME/.zshrc"

# Configuration file aliases
alias zsh_config="code ~/.zshrc"
alias aws_config="code ~/.aws/credentials"

# Development aliases
alias notebook_edit="uv run marimo edit"

# Activate python env
alias activate_venv="source .venv/bin/activate"

# ---------------------
# CUSTOM FUNCTIONS
# ---------------------
# Terraform force unlock function
tf_force_unlock() {
  echo "Force unlocking Terraform state with ID: $1"
  terraform force-unlock -force "$1"
}

# Git last commits function
git_last_commits() {
  local n=${1:-5}
  echo "Last $n commit:"
  git log -n "$n" --pretty=format:"%h %ad %s" --date=short
}

# Git configuration functions
git_config_work() {
  echo "Setting Git configuration for work..."
  git config user.name "filippo-mameli"
  git config user.email "filippo.mameli@agilelab.it"
  echo "✅ Work Git config set:"
  echo "   Name:  filippo-mameli"
  echo "   Email: filippo.mameli@agilelab.it"
}

git_config_personal() {
  echo "Setting Git configuration for personal projects..."
  git config user.name "mameli"
  git config user.email "mameli93@gmail.com"
  echo "✅ Personal Git config set:"
  echo "   Name:  mameli"
  echo "   Email: mameli93@gmail.com"
}
