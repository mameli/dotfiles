---
name: playwright-cli
description: Automate browser interactions with Playwright CLI for web testing, forms, screenshots, or extraction.
---

# Playwright CLI

Use this workflow when CLI browser automation fits the task and the user's chosen browser environment. Run `playwright-cli` through the shell, or `npx playwright-cli` if the binary is unavailable.

Open the target with `playwright-cli open "URL"`. Inspect the returned snapshot and use its element references for `click`, `fill` and other actions. Refresh the snapshot when references become stale. Verify the requested result and close sessions created for this task when finished.

Read only the reference needed:

- [Command syntax and examples](references/commands.md) for navigation, input, screenshots and tabs.
- [Sessions](references/session-management.md) for persistent profiles or multiple sessions.
- [Storage state](references/storage-state.md) for cookies and local storage.
- [Request mocking](references/request-mocking.md) for network interception.
- [Running code](references/running-code.md) for Playwright code execution.
- [Test generation](references/test-generation.md) when asked to generate tests.
- [Tracing](references/tracing.md) or [video](references/video-recording.md) for those diagnostic artifacts.

Keep actions within the requested task and existing authorization. Scope cleanup to the task's session; avoid commands that close unrelated browsers or delete unrelated profiles.
