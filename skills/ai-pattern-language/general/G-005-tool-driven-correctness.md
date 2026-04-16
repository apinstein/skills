# G-005: Tool-Driven Correctness

**Status:** Active
**Type:** General
**Domain:** Ecosystem
**Importance:** ***

## Context
AI agents possess powerful heuristic reasoning, but they notoriously struggle with absolute syntactic, structural, and semantic correctness at scale.

## Problem
Relying on an AI to purely "reason" about the correctness of a complex codebase leads to compounded errors, hallucinated variables, and structural mismatches.

## Forces
- **Stochastic Reasoning:** AI text generation is probabilistic, not deterministic.
- **Scale:** In a large repository, predicting all side-effects or formatting constraints through reasoning alone is impossible.
- **The "Looks Good" Trap:** AI output often looks superficially correct but structurally fails or violates strict standards.

## Solution (The Instruction)
Offload absolute truth to **Hard Harnessed Tools** with explicit, strict boundaries (e.g., compilers, type checkers, or specialized validators).

1.  **Objective Ground Truth:** The rigid tool is the only acceptable source of truth for validity. This fundamentally shifts the AI away from wasting massive context tokens trying to subjectively reason about complex state, replacing it with an objective, binary feedback loop.
2.  **High Saliency Feedback:** Because the rigid tool's boundary is strict, the feedback errors are highly salient—they act as explicit, non-debatable instructions that perfectly guide stochastic correction.
3.  **Iterative Verification:** Whenever modifying systems, the AI must immediately run the associated verification tool. Tool errors are not roadblocks; they are the required map.
4.  **Enforce Structural Transformation (e.g., Boundary ML / BAML):** Use specialized framework tools that convert stochastic "AI looseness" directly into strict, typed function wrappers or objects. This acts as an architectural boundary, casting unpredictable text generation into rigid, deterministic data structures that the rest of the system can rely upon securely.

## Consequently
The AI is relieved of the burden of maintaining perfect structural correctness in its own memory. It instead acts as the creative orchestrator, with the rigid tooling acting as the structural integrity test. Quality remains high, preventing technical debt from minor hallucinations.

## Related Patterns
- **[G-004-strongly-constrained-tools.md]**: Building custom verification scripts or linting commands acts as the foundation for this pattern.
- **[G-006-adversarial-verification.md]**: Automated tooling serves as the first objective baseline of an adversarial verification loop.
