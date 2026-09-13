#!/usr/bin/env bash

set -euo pipefail

brew update
brew upgrade

formulae=(
  agent-browser
  atuin
  eza
  ffmpeg
  gh
  git
  gitleaks
  grep
  herdr
  himalaya
  iperf3
  llama.cpp
  mole
  neovim
  opencode
  openssh
  oven-sh/bun/bun
  python@3.14
  uv
  yt-dlp
  zoxide
  zsh
  zsh-autosuggestions
  zsh-syntax-highlighting
)

casks=(
  agentsview
  betterdisplay
  bitwarden
  blip
  chatgpt
  codex
  codexbar
  dbeaver-community
  ghostty
  google-chrome
  hermes-desktop
  obsidian
  paseo
  telegram
  transmission
  unsloth
  visual-studio-code
  vorssaint
  zen
)

brew install "${formulae[@]}"
brew install --cask "${casks[@]}"

brew cleanup
