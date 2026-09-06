---
name: external-coding-agents
description: "Delegate coding work to Codex, Claude Code or OpenCode."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [coding-agents, claude-code, codex, opencode, kanban, delegation, worktrees]
    related_skills: [hermes-agent, github, subagent-driven-development]
---

# External Coding Agents

Use this umbrella when Hermes should delegate implementation, refactoring, review, migration, or batch issue work to a separate coding agent CLI while Hermes remains responsible for scope, verification, reconciliation, and user-facing truth.

## Core orchestration rules

1. Check prerequisites before launching: CLI installed, auth configured, repo/workdir exists, git status understood.
2. Prefer an isolated git branch or worktree for non-trivial edits and parallel lanes.
3. Give the external agent explicit scope, acceptance criteria, forbidden actions, allowed files, and required output.
4. Hermes must verify results with `git diff`, tests/lint, and read-back of changed files. Never trust self-reported success.
5. Do not expose secrets or let external agents mutate credential stores, messaging platforms, production order entry, or unrelated repo areas.
6. Long-running bounded tasks should run as tracked background processes with completion notification; long-lived TUIs need PTY/tmux monitoring.

## Claude Code lane

Trigger: user explicitly asks for Claude Code, or a strong external implementation/review agent is useful and Claude Code is available.

Prerequisites:

```bash
npm install -g @anthropic-ai/claude-code
claude auth status || claude auth login --console
claude doctor
claude --version
```

Preferred non-interactive mode:

```python
terminal(command="claude -p 'Add error handling to all API calls in src/' --allowedTools 'Read,Edit' --max-turns 10", workdir="/path/to/project", timeout=120)
```

Interactive mode:

- Use tmux/PTY for multi-turn work, slash commands, or trust/permission dialogs.
- Handle workspace-trust and permission dialogs deliberately; capture panes before sending follow-ups.

## Codex CLI lane

Trigger: user explicitly asks for Codex, a git-repo coding task fits Codex CLI, or a Kanban implementation lane needs an isolated Codex run.

Prerequisites:

```bash
npm install -g @openai/codex
codex --version
```

Rules:

- Codex generally expects a git repository.
- Use `pty=true` for interactive Codex CLI invocations.
- For one-shot work: `codex exec 'task...'` from the repo/worktree.
- For parallel issue fixing, create separate worktrees, monitor each process, then reconcile and PR from Hermes.

## OpenCode lane

Trigger: user explicitly asks for OpenCode, or OpenCode is the configured external agent for implementation/review.

Prerequisites:

```bash
which -a opencode
opencode --version
opencode auth list
```

Install options include `npm i -g opencode-ai@latest` or `brew install anomalyco/tap/opencode`.

Patterns:

```python
terminal(command="opencode run 'Add retry logic to API calls and update tests'", workdir="/path/to/project", timeout=300)
terminal(command="opencode", workdir="/path/to/project", background=True, pty=True)
```

Use `opencode session list` and resume flags for ongoing sessions. Resolve binary-path conflicts explicitly if multiple `opencode` binaries exist.

## Kanban implementation lane

Use when a Hermes Kanban worker wants an external coding lane but Hermes owns lifecycle, reconciliation, testing, and handoff.

Required pattern:

1. Create an isolated worktree/branch named for the task.
2. Run capability/auth checks for the selected agent.
3. Prompt from `templates/pmb-codex-lane-prompt.md` or an equivalent task-specific prompt.
4. State that Hermes owns board status and must verify after the lane exits.
5. Run tests and inspect diffs before accepting or handoff.

For safety-critical trading/live-sim work, explicitly forbid live order entry, market orders, fake fills/PnL/order states, weakened risk gates, secrets access, and unrelated hot-path changes.

## Verification checklist

- `git status --short` shows only expected files.
- `git diff --stat` and targeted file reads match the requested scope.
- Tests/lints relevant to touched areas actually ran; record real output.
- Generated commits/PRs, if any, use the user/project's conventions.
- Final user summary separates what the external agent claimed from what Hermes verified.
