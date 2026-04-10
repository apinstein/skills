---
name: pr-address-feedback
description: ALWAYS use this skill to access, address, reply to, or resolve GitHub PR review comments or Reviewable.io threads. Do NOT use raw `gh pr comment`, `gh api`, or any other gh subcommand directly — use the co-located `reviewable` script instead.
---

# PR Address Feedback Skill

Systematically read and address Reviewable review comments on the current branch's PR using the co-located `scripts/reviewable` helper.

> [!IMPORTANT]
> **Always** use the `reviewable` script for all PR comment operations. Never use `gh pr comment`, `gh api`, or similar raw commands — they bypass thread tracking, AI signature injection, and the Reviewable thread model.

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

This prints all threads with status "Action Required", including the **full conversation history** for each thread inline. If there are no open threads, stop here.

> [!NOTE]
> PRs can have **dozens of threads**. Thread IDs are long opaque strings. Track them carefully — it is easy to accidentally post the same reply to multiple threads or mix up which reply belongs where.

For each thread, determine the required action (code change, question answer, suggestion).

Use `$REVIEWABLE thread <THREAD_ID>` only if you need to re-read a specific thread independently.

## Step 2 — Address Each Thread

For each open thread:

1. **Code changes** — Make the requested change to the codebase (if needed).
2. **Reply** — Pipe a heredoc directly into the script to avoid shell-escaping issues with backticks, quotes, and special characters:
   ```bash
   $REVIEWABLE reply <THREAD_ID> - << 'REPLY'
   <YOUR_MESSAGE>
   REPLY
   ```
   The message should explain what you did or answer the question.
   **Do not** include `[AI]` prefix or signature — the script handles that automatically.

> [!CAUTION]
> Double-check the Thread ID **before each `reply` call**. Posting the wrong reply to the wrong thread cannot be undone.

## Step 3 — Verify

```bash
$REVIEWABLE list
```

Confirm all threads are now addressed (no output).

## Step 4 — Commit & Push

After all code changes are made:
- Commit with a message like `fix(review): address PR #<NUMBER> feedback`
- Push

## Step 5 — Final Report

Summarize for the user: which threads were addressed, what code changes were made, and commit/push status.

## Notes
- The co-located `scripts/reviewable` is a thin `gh` CLI wrapper that limits which `gh` subcommands can be issued. This makes it safe to auto-run (`SafeToAutoRun: true`), since the script's attack surface is constrained to read-only queries and posting issue comments — unlike whitelisting raw `gh` which could be destructive (e.g. `gh repo delete`).
- The script handles thread grouping (Reviewable-specific), status tracking (AI vs human last reply), and reply formatting (prefix + signature).
- If you encounter an error with the script, check if `gh` is authenticated (`gh auth status`) and the PR is open.
