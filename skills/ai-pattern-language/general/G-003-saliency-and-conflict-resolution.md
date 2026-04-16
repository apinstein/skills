# G-003: Saliency and Conflict Resolution

**Status:** Active
**Type:** General
**Domain:** Ecosystem
**Importance:** ***

## Context
When working on large-scale software, there are thousands of rules, constraints, and best practices. Often, these rules conflict with each other (e.g., "Keep the database normalized for consistency" vs. "Denormalize data for read performance"). 

## Problem
If you give an AI agent (or a human engineer) a flat, unstructured list of 1,000 rules, it becomes nearly impossible to decide which rule to prioritize when facing a conflict. A massive wall of text diminishes the **saliency** (prominence and relevance) of the correct solution.

## Forces
- **Rule Sprawl:** As a project matures, the number of "best practices" and directives grows exponentially.
- **Context-Dependency:** Most rules are only "correct" in a specific context. A flat list treats all rules as universally applicable.
- **Agent Paralysis:** An AI given too many competing constraints will either hallucinate a compromised middle-ground or arbitrarily ignore important rules.

## Solution (The Instruction)
Avoid flat "rules.md" lists. Ensure all architectural, product, and business guidelines are structured as Patterns.

1.  **Map Solutions to Context:** A pattern must clearly define the *Context* and the competing *Forces* that make a specific solution correct. By tightly coupling the answer to the situation, you improve the **saliency** of the solution for the AI.
2.  **Context-Driven Navigation:** When deciding between competing approaches, the AI should use the pattern indices to find the context that best matches the current problem. 
3.  **Hierarchy of Importance:** Use confidence rankings (`*` vs `***`) and cross-referencing to establish which patterns override others. (e.g., A High-Confidence Product pattern generally overrules a Medium-Confidence Technical constraint, as defined by `PHILOSOPHY.md`).

## Consequently
Instead of navigating a chaotic list of 1,000 equal-weight rules, the AI navigates a structured graph of problems and solutions. This drastically improves the AI's ability to select the correct approach from a massive set of possible solutions, preventing paralysis and ensuring edge cases are handled correctly based on historical precedent.

## Related Patterns
- **[PHILOSOPHY]**: Provides the ultimate tie-breaker (Product > Technology) for conflict resolution.
- **[G-002-pageable-wisdom.md]**: Saliency relies on the context-management principles defined in G-002, ensuring that only the relevant rules are paged into memory at any given time.
