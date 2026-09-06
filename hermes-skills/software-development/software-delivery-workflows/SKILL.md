---
name: software-delivery-workflows
description: Class-level software development workflow covering planning, TDD, systematic debugging, refactoring/simplification, and multi-agent code cleanup.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [software-development, debugging, tdd, refactoring, code-cleanup, planning, testing]
---

# Software Delivery Workflows

Use this umbrella for building, fixing, testing, simplifying, and verifying software. It combines root-cause debugging, test-driven development, and disciplined refactoring into one delivery workflow.

## Default workflow

1. Understand the task and locate the relevant code/config/tests.
2. For bugs: reproduce first, identify root cause, then fix.
3. For features: write or update tests before implementation when feasible.
4. Make the smallest coherent code change.
5. Run targeted verification, then broader tests if risk justifies it.
6. Summarize changed files, real commands run, results, and remaining risks.

## Labeled playbooks

### Systematic debugging

Use a four-phase loop: reproduce, inspect evidence, form hypotheses, test the smallest hypothesis. Do not patch blindly. Capture exact error messages, environment, inputs, and regression tests.

### Test-driven development

Follow RED-GREEN-REFACTOR: add a failing test that expresses the desired behavior, implement the minimum fix, refactor while keeping tests green. If tests are impractical, explain why and create another verification artifact.

### Simplifying code

Use cleanup passes to reduce duplication, improve names, remove dead paths, tighten boundaries, and make behavior easier to test. Preserve external behavior unless the user asked for a behavior change.

### Multi-agent cleanup/review

For broad recent changes, parallelize review by concern: correctness/tests, maintainability/API, and integration/performance. Verify subagent claims before reporting success.

### Exploratory web-app QA / dogfooding

Use when the user asks to dogfood, smoke-test, or systematically QA a web application. Define scope and target URL, choose browser tooling (`agent-browser` for deterministic scripted runs or built-in browser tools for visual reasoning), explore key flows, capture screenshots/console errors/network failures, attempt minimal reproduction for each issue, and produce a structured report with severity, steps, expected/actual behavior, evidence, and suggested fix area.

## Verification discipline

- Do not stop after editing; run the relevant tests/build/lint or explain the blocker.
- Prefer focused tests first for fast feedback.
- Include real command output summaries, not invented success.
- If a tool or dependency blocks verification, try an alternative before finalizing.

## Archived source packages

Former narrow workflow skills for TDD, systematic debugging, and simplification were merged here so future agents discover one delivery entry point and branch into labeled subsections.
