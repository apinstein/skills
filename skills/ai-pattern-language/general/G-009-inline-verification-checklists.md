# G-009: Inline Verification Checklists

**Status:** Draft
**Type:** General
**Domain:** Ecosystem
**Importance:** **

## Context
During adversarial verification loops (mandated by G-006), the AI explicitly acts as a reviewer to catch its own mistakes.

## Problem
If an agent acts as a reviewer but is only given a generic "check for errors" prompt, it will suffer from the same confirmation bias as the generator, leading to superficial verification and "looks good to me" approvals over broken code.

## Forces
- **Confirmation Bias:** An AI naturally wants to approve code that looks syntactically similar to the prompt it just executed.
- **Context Loss:** Reviewing a massive codebase diff leads to dropped context on specific, tiny architectural constraints.

## Solution (The Instruction)
Adversarial verification passes must be executed against explicit, concrete **Inline Verification Checklists**.

1.  **Materialize the Checklist:** Do not hold the standards purely in prompt context. Generate an explicit markdown checklist (e.g., inside `task.md`, the AI's scratchpad, or the verification artifact).
2.  **Explicit Standard Verification:** Each item on the checklist must test a specific structural, business, or product constraint (e.g., "Are the unit tests decoupled?", "Did the PR address the UX rule P-001?").
3.  **Mandatory Fails:** A task cannot proceed until every checkbox passes. If a check fails, the task immediately halts and reverts to execution mode to structurally enforce quality.

## Consequently
Verification shifts from an arbitrary, subjective "vibe check" into an objective structural audit. This completely short-circuits confirmation bias by forcing the AI to manually validate granular constraints individually before proceeding.

## Related Patterns
- **[G-006-adversarial-verification.md]**: This pattern is the microscopic execution detail required to fulfill the macroscopic strategy defined by G-006.
