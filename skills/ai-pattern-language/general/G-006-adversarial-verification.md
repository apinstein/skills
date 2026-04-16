# G-006: Adversarial Verification Loops

**Status:** Active
**Type:** General
**Domain:** Ecosystem
**Importance:** ***

## Context
AI agents frequently suffer from "premature finish" syndrome—declaring a complex task complete after solving the "happy path," while ignoring edge cases, integration failures, or broken tests.

## Problem
How do we ensure robust quality control and standard adherence when the primary generation agent is biased toward believing its own output is flawless?

## Forces
- **Confirmation Bias:** The generating model inherently believes its generated solution is optimal.
- **Context Exhaustion:** By the end of a generation phase, the agent's context window is cluttered, making clear-headed review difficult.
- **Silent Degradation:** If "mostly working" code is merged, system quality silently degrades over time (lowering the "Quality is Free" standard).

## Solution (The Instruction)
Implement **Adversarial Multi-Step Verification Loops** and **Inline Standard Checking**.

1.  **Separate Verification:** Do not rely solely on the generating step to verify its own work. Orchestrate workflows where tasks are explicitly divided: Phase 1 generates, Phase 2 (an adversarial prompt or literal distinct agent role) actively attempts to find flaws, missing test coverage, or compliance failures.
2.  **Inline Standard Checking:** During the verification loop, the AI must explicitly log a checklist against the project's standard guidelines (e.g., "Did I log this decision? Did I preserve the interface? Are the unit tests decoupled?").
3.  **Halt on Failure:** If the verification loop fails, the process must immediately revert to execution mode. A task is not "complete" until the verification loop has passed cleanly.

## Consequently
This structurally offsets AI overconfidence. It guarantees that high standards of correctness and maintainability (e.g., test coverage, DRY) act as a rigid gate before the AI successfully completes the iteration. 

## Related Patterns
- **[G-005-tool-driven-correctness.md]**: Automated tooling serves as the objective foundation for the verification loop.
