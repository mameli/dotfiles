---
name: kanban-workflows
description: "Use when operating Hermes Kanban workflows: orchestrating task graphs, dispatching cross-profile workers, or executing as a Kanban worker with durable handoffs."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [kanban, multi-agent, orchestration, workers, task-routing]
    related_skills: [subagent-driven-development, hermes-agent]
---

# Hermes Kanban Workflows

## Overview

This umbrella covers both sides of Hermes Kanban: the **orchestrator** that decomposes work into a persistent task graph and the **worker** that claims a card, performs work in the assigned workspace, then completes or blocks with a durable handoff.

Use Kanban when work should outlive one conversation, involve multiple profiles, require human-in-the-loop review, or benefit from a persistent audit trail. Use `delegate_task` instead for short, synchronous subtasks inside the current turn.

## When to Use

- User asks to route work through a board, dispatch persistent workers, or coordinate multiple Hermes profiles.
- A task needs crash/restart survivability, review loops, or an audit trail.
- You are spawned by the Kanban dispatcher as a worker and need deeper lifecycle/pitfall guidance.
- You need to recover stuck, crashing, or hallucinating workers.

## Orchestrator Playbook

### Step 0: Discover profiles

Do not invent assignee names. The dispatcher silently fails to spawn unknown profiles and cards remain stuck in `ready`. Use `hermes profile list` or ask the user which profiles exist. Cache the result for the session.

### Step 1: Decide whether Kanban is appropriate

Use Kanban when multiple specialists, parallel lanes, review, human intervention, or long-running persistence are needed. If it is a small one-shot reasoning task, answer directly or use `delegate_task`.

### Step 2: Sketch the graph before creating cards

Extract independent lanes, map each lane to an actual profile, and decide dependencies. Words like "also" and "finally" do not imply a dependency; link only when a child truly needs a parent's output.

### Step 3: Create parent cards first, then dependent children

Capture ids from successful `kanban_create` calls and pass them in `parents=[...]` when creating children. Avoid creating all cards as ready and linking later; the dispatcher can claim a child in the gap.

### Step 4: Report what was queued

Summarize actual profile names, task ids, dependency shape, and where the user can follow progress.

## Worker Playbook

1. **Orient first.** Call/show the task, read body, comments, previous runs, workspace kind, tenant, and acceptance criteria.
2. **Respect workspace boundaries.** Work inside `$HERMES_KANBAN_WORKSPACE`; only modify outside when the card explicitly says to.
3. **Do the work with evidence.** Run real commands/tests/checks; do not complete from intention alone.
4. **Heartbeat only when useful.** Send progress every few minutes for long jobs; avoid empty "still working" noise.
5. **Complete only when terminal.** Use structured `metadata` for changed files, tests, sources, decisions, artifacts, or created cards.
6. **Block for human input/review.** For code-changing tasks that need eyes, add a detailed comment, then `kanban_block(reason="review-required: ...")`.

## Good Handoff Shapes

Coding task metadata:

```json
{
  "changed_files": ["src/rate_limiter.py", "tests/test_rate_limiter.py"],
  "tests_run": 14,
  "tests_passed": 14,
  "decisions": ["user_id primary, IP fallback for anonymous requests"]
}
```

Research task metadata:

```json
{
  "sources_read": 12,
  "recommendation": "vLLM",
  "tradeoffs": ["higher throughput", "more memory pressure"]
}
```

Created-card rule: only list card ids captured from successful `kanban_create` returns; never invent ids from prose or copy ids another worker created.

## Recovery and Operations

- **Reclaim** stuck claimed tasks to abort a running worker and reset to `ready`.
- **Reassign** to a known-good profile when the current one lacks tools/auth/model fit.
- **Change profile model/config**, then reclaim to retry.
- Treat hallucination warnings about phantom task ids as real signals; inspect event logs before retrying.
- In tenant-aware environments, pass/propagate `HERMES_TENANT` and prefix persistent memory entries with the tenant.

## Pitfalls

- Unknown assignees silently strand work.
- Bundling independent lanes into one card destroys parallelism and creates unclear handoffs.
- Over-linking serializes work unnecessarily.
- Worker `clarify` calls time out headlessly; use comments + block instead.
- Completing code work without review can bypass human gates; block with `review-required` when appropriate.
- Re-running the same failed path on retry wastes attempts; read prior runs first.

## Verification Checklist

- [ ] Orchestrator used actual discovered profile names.
- [ ] Dependencies are explicit via `parents=[...]`, not just prose.
- [ ] Worker read current state before acting.
- [ ] Completion includes structured metadata and real evidence.
- [ ] Blocked tasks state exactly what human decision is needed.
