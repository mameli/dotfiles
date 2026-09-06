# dotfiles

A collection of dotfiles and configuration scripts for macOS, centered around zsh, vim, and developer tools.

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

## Bidirectional custom-skill synchronization

The safe synchronization engine is `scripts/skill_sync.py`; `copy_skills.sh`
remains a **one-way legacy installer** and must not be used on managed targets.

- `skills/` holds the existing shared/Codex/OpenCode catalog. A skill is installed
  only into compatible, explicitly selected targets.
- `hermes-skills/` holds selected Hermes customizations, with their category layout
  and supporting resources preserved. Hermes-specific tool instructions are not
  automatically distributed to other agents.
- `skill-sync.example.json` documents the private per-PC mapping. Copy it to
  `${XDG_CONFIG_HOME:-$HOME/.config}/agent-skills/sync.json` (mode `600`) and set
  absolute paths. `mappings[].catalog` chooses a repository skill;
  `mappings[].targets` chooses this PC's installation directories. There is no
  automatic discovery-and-publication of newly created skills.
- Reuse the runtime variables documented above. Synchronization uses its own
  private JSON settings and existing Git authentication, not `.zshrc` or a copy
  of Hermes configuration. State, backups and conflicts stay in `cache_dir`.

Install Python 3, Git and Gitleaks 8, review the engine and copy it to
`${XDG_DATA_HOME:-$HOME/.local/share}/agent-skills/skill_sync.py`. Do not symlink
that trusted copy to the automatically fetched checkout. Example manual run:

```sh
python3 "${XDG_DATA_HOME:-$HOME/.local/share}/agent-skills/skill_sync.py" \
  --config "${XDG_CONFIG_HOME:-$HOME/.config}/agent-skills/sync.json" --dry-run
# Change --dry-run to --apply only after inspecting the result.
```

The engine reconciles contents against a private successful base. Compatible
text changes can merge; conflicting versions are retained privately and block
application. Initial divergences require review. A missing local skill is not a
request to delete it on other PCs. The manual dotfiles checkout is read-only:
pending or outgoing managed changes block the job; unrelated files are untouched.
Gitleaks must pass for proposed contents and outgoing commits, but does not prove
absence of personal information or audit all pre-existing repository history.
Downloaded skill scripts are not executed as part of synchronization.

Scheduling uses one Hermes script-only job, `Custom skills sync`, expression
`0 21 * * 0` (Sunday 21:00), running trusted `scripts/skill_sync_weekly.py`.
The wrapper reads separate private `schedule.json` settings (`python`, `engine`,
`sync_config`, `state_dir`); see `skill-sync.example.json` for the sync mapping
format. Non-change runs are silent; updates and intervention-required errors
are delivered. If the PC or scheduler misses the Sunday run, the next automatic
sync is the following Sunday; run sync manually for immediate updates. See the
operations reference for setup, notifications, conflicts, deletion and
restoration.

```sh
python3 -m unittest discover -s tests -p 'test_skill_sync.py' -v
```

Full operational guidance: [sync-skills operations](skills/sync-skills/references/operations.md).

## Environment variables for custom skills

Machine-specific settings and credentials belong in the private `${XDG_CONFIG_HOME:-$HOME/.config}/agent-skills/env.zsh`, not in this repository. The public `zshrc` and the configured local `.zshrc` each contain one guarded source statement. Keep the definitions in the private file rather than duplicating exports in `.zshrc`.

For a new installation (does not overwrite an existing file):

```zsh
mkdir -p "${XDG_CONFIG_HOME:-$HOME/.config}/agent-skills"
cp -n agent-skills.env.example.zsh "${XDG_CONFIG_HOME:-$HOME/.config}/agent-skills/env.zsh"
chmod 600 "${XDG_CONFIG_HOME:-$HOME/.config}/agent-skills/env.zsh"
# Edit the local file, then load it in this shell:
source "${XDG_CONFIG_HOME:-$HOME/.config}/agent-skills/env.zsh"
```

Use quoted absolute paths, including paths containing spaces. Write `"$HOME/Documents/Knowledge Vault"`, not a quoted literal `"~/Documents/Knowledge Vault"`: shells do not expand that tilde. The private file is executable shell code; source only a trusted, locally owned copy. Do not enable shell tracing or print its contents/environment.

### Variable contract

**Script** means executable code reads the variable. **Guidance** means the agent uses it when constructing a command or selecting a destination; exporting it does not configure a third-party application. Unset or empty optional variables use the stated fallback. Explicit task arguments/destinations take priority unless the row documents an existing credential-resolution order. A nonempty invalid selection must be corrected, not silently replaced with an unrelated resource.

| Variable | Purpose / affected skills | Required? Default and precedence | Non-personal example |
|---|---|---|---|
| `OBSIDIAN_VAULT_PATH` | Guidance: `local-knowledge-workbench`, `travel-itinerary-management`, saved source notes including TikTok | Required only for a default vault destination when no explicit destination/project resolves it. No machine-specific default; ask if unresolved. Explicit destination/project → variable. Does not authorize saving. | `"$HOME/Documents/Knowledge Vault"` |
| `WHISPER_MODEL_PATH` | Script: existing `whisper-audio-transcriber` in this repo, **not** the separately shipped OpenAI `whisper` skill | Optional GGML file. `--model` → this variable → directory search. A selected missing file fails; it does not fall back. | `"$HOME/.local/share/whisper/models/ggml-medium.bin"` |
| `WHISPER_MODEL_DIR` | Script: `whisper-audio-transcriber` model search | Optional; `$HOME/.local/share/whisper/models`. Used only without `--model` or `WHISPER_MODEL_PATH`; prefer `ggml-medium.bin`, otherwise first matching `ggml-*.bin`. No model found is an error before transcription output is created. | `"$HOME/Models/Speech Models"` |
| `SKILLS_CDP_URL` | Script: TikTok frame capture; guidance: TikTok, Letterboxd, Maoty | Optional; `http://127.0.0.1:9222`. Frame helper: `--cdp-url URL` → nonempty variable → generic default. Invalid URLs fail before connection. It is **not** a native Hermes browser setting or an automatic override for Maoty's external helper. | `"http://127.0.0.1:9222"` |
| `SKILLS_BROWSER_USER_DATA_DIR` | Guidance: existing dedicated Chrome profile for TikTok, Letterboxd, Maoty | Optional for attaching to an already reachable endpoint; needed when identifying/setting up the dedicated profile. No guessed personal directory. Explicit chosen profile configuration → variable; must match the existing browser. | `"$HOME/.local/share/agent-browser"` |
| `SKILLS_BROWSER_PROFILE` | Guidance: Chrome profile inside the data directory | Optional; `Default`. Explicit profile selection → variable → default. Does not switch a running browser's profile. | `"Default"` |
| `SKILLS_BROWSER_LAUNCH_AGENT` | Guidance: macOS-only recovery of an existing dedicated browser | Optional; no default label. Explicit installed label → variable. If absent, skip `launchctl` recovery rather than guessing. Does not create/install a LaunchAgent. | `"com.example.agent-browser"` |
| `SKILLS_BROWSER_LOG_DIR` | Guidance: browser diagnostics | Optional; no personal log-directory default. Explicit directory → variable; skip that log lookup if unresolved. | `"$HOME/Library/Logs/agent-browser"` |
| `RADARR_URL` | Guidance: `arr-automation` API/UI address | Optional; `http://localhost:7878`. Explicit `base_url` → variable → default. A supplied URL is validated, not silently replaced after a connection failure. | `"http://localhost:7878"` |
| `SONARR_URL` | Guidance: `arr-automation` API/UI address | Optional; `http://localhost:8989`. Explicit `base_url` → variable → default. | `"http://localhost:8989"` |
| `RADARR_API_KEY` | Secret: Radarr API access in `arr-automation` | An API key is needed for API operations. Existing resolution: environment → securely supplied key → already authenticated app context, subject to tool policy. No default. Never pass a key in a URL or print it. | `<your-private-radarr-api-key>` (placeholder only) |
| `SONARR_API_KEY` | Secret: Sonarr API access in `arr-automation` | Same resolution as Radarr; no default. | `<your-private-sonarr-api-key>` (placeholder only) |
| `RADARR_QUALITY_PROFILE` | Guidance: instance-specific Radarr profile name in `arr-automation` | Optional; no personal default. Explicit `options.qualityProfile` name/ID → variable name → valid instance default/first valid profile. A configured but absent name is an error requiring a new selection; never hardcode the instance's numeric ID. | `"Standard HD"` |
| `ARR_USER` | Secret: optional ARR UI fallback username | Optional; no default. Use only when explicitly available and the active tool permits credential entry. An existing authenticated session needs no new login. | `<your-private-ui-user>` (placeholder only) |
| `ARR_PASSWORD` | Secret: optional ARR UI fallback password | Optional; no default. Same restrictions as `ARR_USER`; `browser_exec` login walls require the user to authenticate manually. | `<your-private-ui-password>` (placeholder only) |
| `MAOTY_REPO_PATH` | Script: Maoty dataset validator; guidance: refresh checkout | Required unless an explicit existing checkout is supplied. Positional repository argument → variable; no guessed default. Absolute, relative, `~` and quoted space-containing paths are supported. Missing configuration or an unreadable/invalid dataset fails with an actionable error. | `"$HOME/Projects/album-site"` |
| `MAOTY_CRON_JOB_ID` | Guidance: select an existing Hermes Maoty job | Optional; no embedded ID. Explicit job → variable → discover the unique matching job by name; ask on ambiguity. Does not create a job or alter its prompt. | `"0123456789ab"` (illustrative ID) |
| `MAOTY_TASTE_ARTISTS_PATH` | Guidance: existing Maoty artist/taste input | Optional when repository guidance provides the input. Explicit source → variable → repository-defined source; no universal filename. **Does not reconfigure the external refresh script automatically.** | `"$MAOTY_REPO_PATH/data/taste-artists.json"` |
| `MAOTY_TASTE_NOTES_PATH` | Guidance: existing Maoty editorial taste notes | Optional when repository guidance provides them. Explicit source → variable → repository-defined notes; no universal filename. **Does not reconfigure the external refresh script automatically.** | `"$MAOTY_REPO_PATH/data/taste-notes.md"` |

Standard integration variables are not alternate names for the settings above:

| Variable | Purpose / affected component | Requirement, default and precedence | Generic example |
|---|---|---|---|
| `XDG_CONFIG_HOME` | Both zsh source blocks locate the private file | Optional; `$HOME/.config`. Set it **before** sourcing; do not set it inside the file as a relocation mechanism. | `"$HOME/.config"` |
| `HERMES_HOME` | Hermes profile location and profile-aware helpers such as GitHub auth | Optional; normally `$HOME/.hermes` for the default profile. Preserve the value chosen by Hermes' profile launcher; do not duplicate it in the private file unless intentionally launching that profile. | `"$HOME/.hermes"` |
| `GH_TOKEN`, `GITHUB_TOKEN` | Existing `github` helper, not new skill settings | Optional if `gh auth status` works. Authenticated `gh` is preferred; fallback token precedence is `GH_TOKEN` → `GITHUB_TOKEN` → selected `$HERMES_HOME/.env` → Git credential helper. No default token. Use existing credential management instead of creating duplicate copies. | `<your-private-github-token>` (placeholder only) |

### Hermes, GUI processes and scheduled jobs

Interactive `.zshrc` is not a universal environment loader. For CLI Hermes, load the private file in the shell **before** launching the backend. To execute a command without any interactive-shell initialization:

```zsh
/bin/zsh -f -c '
  file="${XDG_CONFIG_HOME:-$HOME/.config}/agent-skills/env.zsh"
  [[ -r "$file" ]] || { print -u2 "Private agent-skills environment is missing"; exit 1; }
  source "$file" || exit
  exec "$@"
' agent-skills hermes
```

For a scheduled **command**, keep the same wrapper and replace `hermes` with the executable and separately quoted arguments. For example, a read-only check can end with `agent-skills python3 "/path/to/skill/scripts/validate_album_data.py" "/path/to/album checkout"`. The wrapper preserves argument boundaries and never reads all of `.zshrc`. For a per-command environment override, assign it **after** sourcing the private file; otherwise an unconditional export in that file can replace it.

For Hermes agent jobs, either start the actual scheduler/backend with this environment or source the dedicated file inside the relevant terminal command. A setting in an interactive terminal does not automatically reach a browser worker, a remote/container terminal, or a previously running GUI/backend. Mount/copy the private configuration privately to the execution host where necessary; do not assume a host path exists remotely. Verify only variable presence and necessary path access there, never dump values. Restart the responsible process deliberately after changes; this preparation does not restart it.

For `launchd`, a plist's `EnvironmentVariables` dictionary does not expand `$HOME` or other shell expressions. Use an explicitly configured local wrapper/`ProgramArguments` or literal private values outside Git. No LaunchAgent, live cron job or service was changed by this preparation.

### External configuration boundaries

- `SKILLS_CDP_URL` is consumed by the TikTok frame script. Hermes `browser_exec` separately uses Hermes' configured browser endpoint; setting this variable alone does not change `browser.cdp_url`. Reconcile those settings explicitly before browser work using the supported Hermes configuration interface.
- Browser profile, LaunchAgent and log variables are agent guidance, not Chrome configuration APIs. They neither launch a profile nor change an existing browser's arguments.
- Read-only inspection confirmed that Maoty's external `aoty_cdp.py` uses fixed endpoint/LaunchAgent constants and may automatically restart its service on context entry; the external refresh script uses account-specific taste-source filenames and a legacy helper location. They do not consume these new settings. Exporting `SKILLS_*` or `MAOTY_TASTE_*` therefore **does not make that checkout portable**. The installed skill documents the mismatch and requires a separate, authorized compatibility change before running on a different setup. No external repository, browser configuration, scheduled-job payload or service was changed.
- OpenAI's bundled `whisper` skill does not consume the GGML model variables: those belong to the existing whisper-cpp wrapper in this repository.
- Keeping the Whisper wrapper does not install or retain a model. Its example settings are optional; an installation without a model should leave them unset until a model is explicitly supplied.

### Scope and publication status

Do not copy all of `~/.hermes/skills` into Git. It mixes original/local skills, locally customized bundled skills, optional third-party packages and external symlinks. Use the installed bundled manifest plus the bundled/optional source trees to identify upstream copies; an untracked name does not establish authorship, and divergence from the current upstream tree does not alone prove a personal customization. Preserve licenses/attribution and exclude `.archive`, runtime environments, browser state, caches and sync metadata. External symlink targets require a separate inclusion decision.

The targeted installed-skill portability pass is complete: the fixed Letterboxd account was removed, Maoty's validator consumes its repository variable, and the TikTok helper supports a validated explicit/environment/default endpoint. The broader inventory distinguishes upstream/optional packages from local or third-party candidates; generic documentation examples are not machine dependencies. External Maoty compatibility limits remain explicit, not silently worked around. This work **has not imported Hermes skills, staged files, committed or pushed**. The existing copy script is not a reviewed export manifest; do not use it to publish the entire installed tree blindly.

Environment-loading, Whisper-wrapper, GitHub-auth, document-conversion, YouTube, Maoty-validator and TikTok-endpoint checks use isolated local fixtures; they do not validate real speech recognition, perform live browser captures or contact services. Changed scripts also receive syntax checks. The targeted source scan excludes unchanged upstream material and distinguishes existing nonsecret Git identity metadata from new skill settings; it is not a sanitization of every pre-existing dotfile. The `.gitignore` rules guard common private configuration/generated paths, but do not remove already tracked files. This preparation is **not a complete secrets scan or a Git-history audit**. Before publication, separately review all export candidates, staged content, third-party assets and repository history; never publish the populated `env.zsh`, credentials, cookies or browser/session state.
