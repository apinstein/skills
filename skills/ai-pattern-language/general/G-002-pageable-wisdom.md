# G-002: Pageable Wisdom and Context Management

**Status:** Active
**Type:** General
**Domain:** Ecosystem
**Importance:** ***

## Context
When working with AI agents, the context window is a critical constraint. You cannot load the entire history, tacit knowledge, or codebase of a massive project into memory at once. At the same time, without memory of why decisions were made, AI agents (and human engineers) will repeat past mistakes, rewrite systems poorly, or break delicate technical tradeoffs.

## Problem
How do we preserve the deep, hard-won wisdom of a project (tradeoffs, constraints, and interconnected rules) without overwhelming an agent's context window?

## Forces
- **Context Limits:** Stuffing all knowledge into a single mega-prompt or mega-README leads to token exhaustion and diminished instruction-following capability.
- **Lost Wisdom:** Tacit knowledge is often lost in ephemeral chat logs or merged PR discussions, meaning new agents or developers lack the "Why" behind the "What".
- **Decision Scales:** Decisions happen at vastly different scales (Business strategies vs. UI component rendering), and not all scales are relevant to every task.

## Solution (The Instruction)
Treat the Pattern Language as a system of **"Pageable Wisdom"** and enforce strict context management.

1.  **Lazy Loading is Mandatory:** Never read all patterns at once. Always read the `INDEX.md` first to understand the *available* wisdom in a domain, then "page in" only the specific patterns relevant to the current task.
2.  **Contextual Decision Capture:** When an implementation decision is made that breaks from the norm or resolves a tight trade-off, you must stop and capture the "why." Prompt the human user to clarify if necessary, then store this tacit knowledge alongside the codebase as a new pattern. Never leave the "Why" trapped in ephemeral chat logs.
3.  **Link Scales Explicitly:** Use the "Related Patterns" section to link high-level wisdom (e.g., product rules) to low-level wisdom (e.g., technical implementations). This allows an agent to page-in the "Why" behind a technical constraint without loading the entire product manual.

## Consequently
By distributing wisdom across heavily indexed, modular files, the project builds a permanent, accessible memory bank. The AI can efficiently curate and load exactly the right combination of tacit knowledge needed for a specific task, maximizing both its reasoning capability and its context-window efficiency.

## Related Patterns
- **[PHILOSOPHY]**: Adheres to the framework's core meta-guidelines.
- **[G-001-architecture-diagrams.md]**: Applies the same division-of-concerns logic to documentation parsing as G-001 applies to architecture diagramming.
