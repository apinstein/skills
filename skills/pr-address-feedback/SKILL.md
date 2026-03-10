---
name: pr-address-feedback
description: Read all review feedback on a GitHub PR (with Reviewable.io) and systematically address each Reviewable thread.
---

# PR Address Feedback Skill

Systematically read and address Reviewable review comments on the current branch's PR using the co-located `scripts/reviewable` helper.

## Prerequisites
- `gh` CLI must be installed and authenticated (the script will check and fail gracefully if not)
- Current branch must have an open PR (the script auto-detects the PR via `gh pr view` on the current branch)

## Resolve Script Path

Determine `REVIEWABLE` as the path to the co-located script relative to this SKILL.md file:
```
REVIEWABLE=<directory containing this SKILL.md>/scripts/reviewable
```

All commands below use `REVIEWABLE` to stay portable regardless of skill directory name.

## Step 1 — List Open Threads

```bash
$REVIEWABLE list
```

This outputs threads with status "Action Required". If no threads need attention, stop here unless the user specifically asks to review closed threads.

## Step 2 — Analyze Feedback

For each open thread:
- Read the snippets provided in the list output.
- If more context is needed, view the full conversation:
  ```bash
  $REVIEWABLE thread <THREAD_ID>
  ```
- Determine the required action (code change, question answer, suggestion).

## Step 3 — Address Each Thread

For each open thread:

1. **Code changes** — Make the requested change to the codebase.
2. **Reply** — Use the helper script to reply:
   ```bash
   $REVIEWABLE reply <THREAD_ID> "<YOUR_MESSAGE>"
   ```
   The message should explain what you did or answer the question.
   **Do not** include `[AI]` prefix or signature — the script handles that automatically.

## Step 4 — Verify

```bash
$REVIEWABLE list
```

Confirm all threads are now addressed (no output).

## Step 5 — Commit & Push

After all code changes are made:
- Commit with a message like `fix(review): address PR #<NUMBER> feedback`
- Push

## Step 6 — Final Report

Summarize for the user: which threads were addressed, what code changes were made, and commit/push status.

## Notes
- The co-located `scripts/reviewable` is a thin `gh` CLI wrapper that limits which `gh` subcommands can be issued. This makes it safe to auto-run (`SafeToAutoRun: true`), since the script's attack surface is constrained to read-only queries and posting issue comments — unlike whitelisting raw `gh` which could be destructive (e.g. `gh repo delete`).
- The script handles thread grouping (Reviewable-specific), status tracking (AI vs human last reply), and reply formatting (prefix + signature).
- If you encounter an error with the script, check if `gh` is authenticated (`gh auth status`) and the PR is open.
