# G-008: Tool Specification Schema

**Status:** Draft
**Type:** General
**Domain:** Ecosystem
**Importance:** **

## Context
When an AI requires new capabilities, we build strongly constrained wrapper tools to prevent it from relying on open-ended destruction (as mandated by G-004). 

## Problem
If these bespoke tools are built ad-hoc, with ambiguous input expectations or sprawling scopes, the AI will use them incorrectly, waste context tokens guessing syntax, or induce the very silent failures the tool was meant to prevent.

## Forces
- **Ambiguity vs Rigidity:** An AI reading a loosely defined tool description will hallucinate the arguments.
- **Scope Creep:** A tool built to "check git status" often slowly morphs into "check git status and pull and rebase", becoming a destructive omni-tool.

## Solution (The Instruction)
When building a new constrained tool for the ecosystem, it must adhere to a strict specification schema:

1.  **Single Responsibility:** The tool must do exactly one thing. If it alters state, it cannot also cleanly report complex state. 
2.  **Explicit Typed Interfaces:** Arguments must be explicitly documented. Avoid open-ended natural language string arguments if a rigid enum or specific file path will suffice.
3.  **Non-Destructive Defaults:** By default, tools should read or verify. If a tool writes, it must require explicit validation flags or perform algorithmic safety checks.

## Consequently
By forcing a strict definition schema, the AI can effortlessly discover, understand, and rigidly apply the tool without expending inference cycles determining *how* the tool is intended to function.

## Related Patterns
- **[G-004-strongly-constrained-tools.md]**: This pattern explicitly fulfills the mandate set by G-004 by defining *how* to build the constrained wrapper tools.
