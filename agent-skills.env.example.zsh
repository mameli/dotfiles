# Copy to ~/.config/agent-skills/env.zsh (or $XDG_CONFIG_HOME/agent-skills/env.zsh).
# Set only variables used by your skills. Keep actual secrets in the local file.

# Obsidian: absolute vault directory, needed only for default save destinations.
# export OBSIDIAN_VAULT_PATH="$HOME/Documents/MyVault"

# Whisper: --model overrides WHISPER_MODEL_PATH; otherwise search WHISPER_MODEL_DIR.
# export WHISPER_MODEL_DIR="$HOME/.local/share/whisper/models"
# export WHISPER_MODEL_PATH="$WHISPER_MODEL_DIR/ggml-medium.bin"

# Browser workflows: point to an existing dedicated browser; this does not launch it.
export SKILLS_CDP_URL="http://127.0.0.1:9222"
# export SKILLS_BROWSER_USER_DATA_DIR="$HOME/.local/share/agent-browser"
export SKILLS_BROWSER_PROFILE="Default"
# macOS only: label of your already-installed browser LaunchAgent.
# export SKILLS_BROWSER_LAUNCH_AGENT="com.example.agent-browser"
# export SKILLS_BROWSER_LOG_DIR="$HOME/Library/Logs/agent-browser"

# Radarr/Sonarr: omit URLs for localhost defaults; API keys stay private.
# export RADARR_URL="http://localhost:7878"
# export SONARR_URL="http://localhost:8989"
# export RADARR_API_KEY=""
# Optional instance-specific profile name; explicit task options take precedence.
# export RADARR_QUALITY_PROFILE="Standard HD"
# export SONARR_API_KEY=""
# Optional UI fallback credentials:
# export ARR_USER=""
# export ARR_PASSWORD=""

# Maoty-specific workflow; unnecessary for other skills.
# export MAOTY_REPO_PATH="$HOME/Projects/maoty"
# export MAOTY_CRON_JOB_ID=""
# export MAOTY_TASTE_ARTISTS_PATH="$MAOTY_REPO_PATH/output/taste-artists.json"
# export MAOTY_TASTE_NOTES_PATH="$MAOTY_REPO_PATH/output/taste-notes.md"
