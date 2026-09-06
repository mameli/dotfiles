---
name: maoty-maintenance
description: "Refresh Maoty albums or troubleshoot its weekly AOTY job."
version: 2.1.0
---

# Maoty maintenance

Repository: `${MAOTY_REPO_PATH}`. Read its `AGENT.md` for collection, enrichment, ordering and editorial rules when running or changing the refresh.

- **Run a refresh:** [refresh workflow](references/refresh-workflow.md).
- **Browser/authentication trouble:** [direct CDP](references/direct-cdp.md). Maoty uses `scripts/aoty_cdp.py`, never Playwright or playwright-cli.
- **Labels and final counts:** [reporting and labeling](references/weekly-refresh-reporting-and-labeling.md).
- **Read-only dataset checks:** run this skill's `scripts/validate_album_data.py [REPO]`; an explicit path overrides `MAOTY_REPO_PATH`.

The refresh is cumulative. Preserve existing albums and labels; assign labels editorially, not from scores. Missing Apple Music links or genre tags are reportable gaps, not reasons to abort.

Reuse existing Last.fm/mixtape inputs. Stage only intentional refresh changes; a regenerated tag-browse file is not automatically part of the album update. `bun run albums` mutates dates/ranks even off Friday: do not run it merely to test browser connectivity.

The scheduled job is `Maoty Friday Album Refresh` (`${MAOTY_CRON_JOB_ID}`). Use Hermes cron tools for job inspection or changes; do not hand-edit job storage. A manual rerun is a real refresh with the job's commit/push behavior, not a read-only health check.

## Local environment

Read the relevant exported variables; if unavailable, source `${XDG_CONFIG_HOME:-$HOME/.config}/agent-skills/env.zsh` into the command environment. Never print credential values. In prose and configuration examples, `${VAR}` denotes a value to resolve; do not write literal placeholders into application settings.

Browser workflow values use explicit task settings > nonempty environment > generic defaults: `SKILLS_CDP_URL` defaults to `http://127.0.0.1:9222`, `SKILLS_BROWSER_PROFILE` to `Default`. `SKILLS_BROWSER_USER_DATA_DIR` identifies the existing profile root; if needed but unset, ask rather than invent a path. Optional `SKILLS_BROWSER_LAUNCH_AGENT` and `SKILLS_BROWSER_LOG_DIR` select the macOS service and diagnostic logs; unset means skip those operations. These describe an existing browser and are not consumers in the external Maoty helper. They do not provision Chrome or reconfigure Hermes. Verify configuration and external constants match before use.

For repository selection, an explicit path overrides `MAOTY_REPO_PATH`; if both are absent, ask (the validator exits with usage guidance). An explicit scheduled-job selection overrides `MAOTY_CRON_JOB_ID`; if unset, identify the existing job by name with cron tools. For taste-source inspection, explicit paths override `MAOTY_TASTE_ARTISTS_PATH` / `MAOTY_TASTE_NOTES_PATH`, then repository instructions; if unresolved, ask. These are workflow inputs, not automatic overrides of external scripts. Read the [external compatibility limits](references/direct-cdp.md#external-compatibility-limits) before a refresh.
