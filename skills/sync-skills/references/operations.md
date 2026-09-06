# Skill synchronization operations

## Install on another PC

1. Inspect the selected skills before trusting their instructions. Install Python 3,
   Git and Gitleaks 8 (`brew install gitleaks` on macOS). Configure Git/SSH credentials
   using the existing credential manager; never put credentials in the remote URL.
2. Review `scripts/skill_sync.py` and `tests/test_skill_sync.py`, then run:
   `python3 -m unittest discover -s tests -p 'test_skill_sync.py' -v`.
3. Copy the reviewed script to
   `${XDG_DATA_HOME:-$HOME/.local/share}/agent-skills/skill_sync.py`.
   It is a trusted local deployment, not a symlink to an automatically updated checkout.
4. Copy `skill-sync.example.json` to
   `${XDG_CONFIG_HOME:-$HOME/.config}/agent-skills/sync.json`, without overwriting
   existing settings. Use mode `600` and private parent/cache directories (`700`).
5. Set absolute `workspace`, `cache_dir`, `scanner`, remote and branch. Choose
   `mappings`: each `catalog` is a repository-relative skill directory, and
   `targets` contains the full installation directories for this PC. Do not map
   the same destination twice or overlap roots. Omit agents/skills not wanted.
6. Run `--dry-run`, resolve initial differences, then `--apply`. A dry-run may
   fetch/create private inspection data but must not publish or change installations
   or the successful base. Divergent first versions have no trustworthy ancestor:
   they require a decision, not a timestamp-based winner.
7. Only after a successful apply and an unchanged repeat, configure the job.

Existing runtime settings remain in private `agent-skills/env.zsh`; see the
README variable contract. They are not synchronization settings, and sync does
not need to source the file or `.zshrc`.

## Catalog and selection

- `skills/`: existing shared/other-agent skill catalog. Select only compatible
  consumers; a shared entry need not be installed into every agent.
- `hermes-skills/`: Hermes-specific customized skills, preserving category
  directories, instructions, helper assets, licenses and attribution. Do not
  indiscriminately install these into Codex/OpenCode: Hermes tool names differ.
- The private mappings are the exact write boundary. New local directories are
  **not** auto-published. Add a mapping only after ownership, portability,
  licensing, resources and secrets have been reviewed.
- Unchanged vendor packages, archives, external symlinks, runtimes, credentials,
  cookies, caches, logs and personal outputs are not part of the export.

When adding another installation to an existing mapping, inspect its contents
first. An absent initial installation is populated; a divergent existing copy
must be reconciled. Disabling an installation means removing that target from
private configuration, not deleting the shared catalog.

## Conflicts and interrupted operations

Stop the scheduled job while resolving a conflict. Keep all snapshots and the
successful base. Inspect the reported private conflict/backup paths; compare
base, each local installation and the remote. Compose the intended result
manually, preserve unrelated edits and run another dry-run before applying.
Do not put `.local`/`.remote` conflict copies inside active skill discovery.

Missing whole skills are treated conservatively, not as cross-PC delete requests.
File deletions within a managed skill require a known base; delete-versus-edit
conflicts stop the run. To retire a skill, remove its mappings on affected PCs
and explicitly review the catalog deletion. Stale PCs must be reconfigured before
resuming; do not infer retirement from an absent directory.

If an interrupted transaction is reported, preserve the transaction journal and
backup first. Inspect which remote commit actually exists and which installation
files were written. Never delete the journal merely to bypass the guard. Restore
only the affected files from a chosen backup after comparing current changes;
retain an additional copy of any changes made since the interruption. Rebuild
state only from verified matching contents. If uncertain, leave the job paused.

The manual dotfiles checkout is read-only to the scheduled engine. Pending
managed changes or outgoing managed commits block synchronization. Publish or
otherwise preserve that work intentionally, then retry. Changes to unrelated
dotfiles are neither staged nor overwritten.

## Scheduling and notifications

Use one Hermes native job named `Custom skills sync`, expression `0 21 * * 0`,
`no_agent: true`, running a trusted local copy of `scripts/skill_sync_weekly.py`.
Its private settings default to `agent-skills/schedule.json` under XDG_CONFIG_HOME
(`python`, `engine`, `sync_config`, `state_dir`). The wrapper runs the engine
with `--apply` once per tick: empty stdout stays silent, updates and
intervention-required errors are delivered. Note: installed native weekly
scheduling failed an autumn DST check in testing (22:00 instead of 21:00); the
run still happens weekly on Sunday, just possibly an hour off after a DST change.
Hermes currently uses profile/environment timezone rather than a per-job timezone
field. Check other jobs before changing profile settings.

The wrapper supplies explicit executable/config paths without interactive shell
initialization. Empty stdout means no delivery; updates and intervention-required
errors produce a concise notification. Native run history lives under the active
Hermes profile's `cron/output/<job-id>/`. Private synchronization data lives
under `cache_dir` from `sync.json`.

The PC must be awake and a Hermes scheduler must be running for the Sunday run.
If that run is missed, the next automatic sync is the following Sunday. Use the
manual command for immediate updates. No OS wake job is installed. Recheck native
scheduling after Hermes upgrades.

## Limits

Gitleaks catches recognizable credentials, not every private hostname, account,
path or piece of personal prose. First export review is separate from scanning;
scanner success is not proof that the entire pre-existing dotfiles history is
secret-free. The engine scans proposed managed contents and outgoing commits,
not arbitrary private files, and does not rewrite instructions to sanitize them.

Compatible textual merges are syntactic, not a proof of semantic correctness.
Remote helper code is copied as data, not executed by sync. It can be executed
later when a user invokes the skill: only share skills from trusted collaborators.
