---
name: fix-bugs
description: Systematic bug-fixing workflow for reported defects, regressions, failing behavior, flaky tests, crashes, visual/UI bugs, platform-specific failures, log-reported errors, and production-like failures. Use when Codex is asked to investigate, debug, fix, or verify a bug and should reproduce the issue with ecosystem-appropriate tools, identify the cause, add or prove regression coverage, implement a targeted fix, run tests, and re-verify using the original reproduction path.
---

# Fix Bugs

Use this workflow to prevent premature code edits. Treat reproduction and verification as first-class deliverables, not optional setup and cleanup.

## Core Rule

Do not start by editing product code. First understand the report, reproduce the bug or create equivalent failing evidence, then diagnose the code path. Only implement after there is a concrete failure signal and a plan.

If reproducing the bug is blocked by missing access, unavailable hardware, external credentials, or unclear requirements, state the blocker and use the closest defensible evidence path. Do not pretend the bug was reproduced.

## Ecosystem-Native Debugging

Before choosing a reproduction or diagnostic method, identify the debugging tools and evidence surfaces that fit the project's platform, framework, and runtime. Do not default to "check logs" as a generic step.

Examples include browser DevTools, Playwright traces, console/network panels, accessibility snapshots, Xcode simulators, device logs, Instruments, crash reports, Android logcat, test runner snapshots, database query traces, framework-specific devtools, server metrics, distributed traces, structured application logs, or project-local smoke scripts. Use the tools that provide the clearest signal for the reported failure.

## Workflow

1. Understand the bug report.
   - Restate the expected behavior, actual behavior, affected environment, and user-visible impact.
   - Inspect attached screenshots, logs, stack traces, issue links, failing tests, or reproduction steps before theorizing.
   - Identify the platform, runtime, framework, and project-local tooling likely to produce the best debugging evidence.
   - Ask a concise clarifying question only when the report is contradictory, missing a required artifact, or has materially different possible meanings. Otherwise proceed.

2. Reproduce or prove the bug.
   - Select reproduction tools based on the ecosystem and bug type, then explain why that evidence path is appropriate.
   - For UI bugs, use the app, browser, simulator, screenshots, accessibility tree, console output, network traces, visual snapshots, or framework-specific devtools as appropriate.
   - For programmatic bugs, run the failing command or add a focused failing test that captures the reported behavior.
   - For crashes or runtime failures, capture the most diagnostic platform artifact: stack trace, crash report, device or process log, trace span, failing input, and command or interaction that triggers it.
   - Record the exact reproduction command, route, state, fixture, or interaction sequence.

3. Localize the cause.
   - Trace the failing behavior through the owning code path before editing.
   - Read the nearby tests, fixtures, docs, recent diffs, and existing helpers for the affected area.
   - Decide whether the cause is a narrow missing edge case, a broken contract between components, stale state, timing/concurrency, data migration, environment/configuration, or a deeper architectural mismatch.
   - Prefer project-local patterns and existing abstractions over inventing new ones.

4. Plan the fix.
   - State the smallest change that should fix the reproduced failure and why that code path owns the behavior.
   - Include the regression guard: a new failing test, an existing test made red, a fixture/assertion update, or an explicit explanation for why automated coverage is not practical.
   - Identify any risk areas, including compatibility, migrations, cache invalidation, concurrency, accessibility, performance, or user-facing behavior.

5. Make the regression test red.
   - Add or adjust the focused test before changing product code whenever practical.
   - Run the focused test and confirm it fails for the expected reason.
   - If a red test cannot be run first, preserve equivalent evidence such as a failing UI smoke, snapshot, log assertion, or reproduction transcript, and explain the gap.

6. Implement the fix.
   - Keep the change scoped to the diagnosed cause.
   - Avoid opportunistic refactors, unrelated formatting churn, or broad rewrites unless the diagnosis shows they are necessary.
   - Add comments only where they clarify non-obvious behavior, invariants, or edge cases.

7. Verify with tests.
   - Re-run the focused regression test and confirm it passes.
   - Run the relevant broader suite, smoke test, build, lint, typecheck, or platform-specific verification needed for the touched area.
   - If a test is unavailable, skipped, flaky, or blocked, report that precisely.

8. Re-verify with the original reproduction path.
   - Repeat the same UI flow, command, fixture, log inspection, screenshot comparison, or failing scenario used to prove the bug.
   - Confirm that the original symptom is gone, not merely that the new unit test passes.
   - Check for adjacent regressions along the path that failed.

## Output

When finishing, report:

- The reproduction evidence used before the fix.
- The ecosystem-specific debugging tools or artifacts used, if relevant.
- The root cause, with file/function references when useful.
- The fix summary.
- The regression coverage added or confirmed.
- The exact verification commands or manual/UI checks run after the fix.
- Any residual risk or blocked verification.
