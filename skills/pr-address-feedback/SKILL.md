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

This outputs threads with status "Action Required". If no threads need attention, stop here unless the user specifically asks to review closed threads.

## Step 2 — Analyze Feedback

> [!NOTE]
> PRs can have **dozens of threads**. Thread IDs are long opaque strings. Track them carefully — it is easy to accidentally post the same reply to multiple threads or mix up which reply belongs where.

For each open thread:
- Read the snippets provided in the list output.
- If more context is needed, view the full conversation:
  ```bash
  $REVIEWABLE thread <THREAD_ID>
  ```
- Determine the required action (code change, question answer, suggestion).

## Step 2b — Build a Reply Plan

Before posting **any** replies, write out an explicit plan mapping each thread to its intended reply. This is your source of truth when posting — do not rely on memory.

| Thread ID | Summary | Planned Reply |
|-----------|---------|---------------|
| `<ID1>` | what the reviewer asked | your reply |
| `<ID2>` | ... | ... |

Make any required **code changes first**, then post replies in order from the plan, checking off each row as you go.

## Step 3 — Address Each Thread

Work through the reply plan row by row:

1. **Code changes** — Make the requested change to the codebase (if not already done).
2. **Reply** — Pipe a heredoc directly into the script to avoid all shell-escaping issues with backticks, quotes, and special characters:
   ```bash
   $REVIEWABLE reply <THREAD_ID> - << 'REPLY'
   <YOUR_MESSAGE>
   REPLY
   ```
   The message should explain what you did or answer the question.
   **Do not** include `[AI]` prefix or signature — the script handles that automatically.

> [!CAUTION]
> Double-check the Thread ID against your reply plan **before each `reply` call**. Posting the wrong reply to the wrong thread cannot be undone.

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
