---
name: apple-automation
description: "Class-level macOS Apple app automation: Notes, Reminders, Messages/iMessage/SMS, Find My, and background desktop UI control."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [apple, macos, notes, reminders, imessage, findmy, computer-use, automation]
---

# Apple Automation on macOS

Use this umbrella whenever the user asks Hermes to interact with Apple ecosystem apps or the macOS desktop: Notes, Reminders, Messages/iMessage/SMS, Find My, or GUI-only workflows. Prefer purpose-built CLIs when available; fall back to UI automation only when there is no supported API.

## Global prerequisites and safety

- Host must be macOS with the relevant Apple app signed in/configured.
- Expect Privacy permissions: Automation, Full Disk Access, Screen Recording, Contacts/Reminders/Notes as applicable.
- Never type passwords, API keys, credit cards, 2FA codes, or other secrets into macOS UI.
- Never click permission, payment, login, or destructive confirmation dialogs without explicit user approval.
- For messaging, always confirm recipient identity and exact message before sending unless the user has unambiguously specified both in the same turn.
- Use dedicated Hermes tools for Telegram/Discord/Slack/etc.; this umbrella is for Apple-native apps.

## Notes.app via `memo`

Trigger: create, search, edit, move, export, or organize Apple Notes for cross-device access.

Prerequisites:

```bash
brew tap antoniorodr/memo && brew install antoniorodr/memo/memo
```

Operational rules:

- Use Apple Notes only when the user asks for Notes.app/iCloud Notes. For Obsidian vault work, load/use the Obsidian skill instead.
- Prefer structured note titles and folders when the user provides a project/topic.
- Avoid editing notes with attachments/images unless the CLI supports the operation; warn when rich content may be lost.

## Reminders.app via `remindctl`

Trigger: personal reminders/to-dos that should sync to iPhone/iPad.

Prerequisites:

```bash
brew install steipete/tap/remindctl
remindctl status || remindctl authorize
```

Operational rules:

- Distinguish Apple Reminders from Hermes cron alerts. If the user wants an agent to notify later, use the cronjob tool; if they want it in Reminders.app, use `remindctl`.
- `--due` sets the task due time; pass `--alarm` explicitly for early nudges or guaranteed notification timing.
- Date formats usually accepted: `today`, `tomorrow`, `YYYY-MM-DD`, `YYYY-MM-DD HH:mm`, ISO 8601.

## Messages.app / iMessage / SMS via `imsg`

Trigger: send/read/check iMessage or SMS from the user's macOS Messages.app.

Prerequisites:

```bash
brew install steipete/tap/imsg
```

Permissions: Messages.app signed in, Full Disk Access for terminal, Automation permission when prompted.

Operational rules:

- Identify the chat/recipient first, then confirm before sending if there is any ambiguity.
- `--service imessage` forces blue-bubble iMessage, `--service sms` forces SMS, `--service auto` lets Messages decide.
- Do not bulk/mass message without explicit confirmation.

## Find My via UI automation

Trigger: “where is my phone/keys/bag/cat?”, AirTag/device location checks, or monitoring item movement.

Prerequisites:

- Find My app configured with iCloud and devices/items.
- Screen Recording permission for screenshots.
- Optional: `peekaboo` or the macOS computer-use driver for annotated UI capture.

Rules and limitations:

- Find My has no public CLI/API; use AppleScript/screenshots/UI automation.
- AirTag locations update opportunistically and may require the item detail page to remain open.
- Location accuracy depends on the Find My network; report timestamps/uncertainty.

## Background macOS computer use

Trigger: GUI-only workflows where no CLI/API exists.

Canonical loop:

1. Capture the app/window and inspect accessibility labels.
2. Click/type/keypress only using visible, intended targets.
3. Re-capture after each meaningful action.
4. Stop at login, permission, payment, or secret prompts and ask the user.

Text input patterns:

- Use regular typing for text fields.
- Use key shortcuts for app actions: `cmd+s`, `cmd+t`, `cmd+w`, `cmd+shift+g`, `return`, `escape`, `tab`, arrows.

Failure modes:

- Missing computer-use driver or permissions: enable/install the relevant Hermes computer-use support and grant macOS Screen Recording/Accessibility permissions.
- UI labels drift across macOS versions; rely on fresh screenshots/accessibility trees, not stale coordinates.
