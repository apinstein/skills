# G-004: Strongly Constrained Tools

**Status:** Active
**Type:** General
**Domain:** Ecosystem
**Importance:** ***

## Context
AI agents are prone to hallucination, silent failures, and getting lost when given overly broad capability sets or highly destructive raw tools (e.g., raw bash commands across a sensitive domain).

## Problem
How do we counteract an AI's tendency to fail silently or misuse general tools when operating inside complex or sensitive architectural boundaries?

## Forces
- **Agent Omnipotence:** General-purpose AI models will attempt to solve anything with raw bash scripting, often destructively.
- **Silent Failures:** Broad tools mask specific failures.
- **Cognitive Load:** An AI wastes context tokens reasoning about complex tool arguments instead of the problem itself.

## Solution (The Instruction)
Build and utilize **Strongly Constrained, Specific Tools** (non-destructive convenience wrappers).

1.  **Narrow Scope over General Knowledge:** Prioritize using tools that wrap a single, specific capability with hard boundaries (e.g., using a dedicated `read_test_results` tool over a raw `cat` command in bash).
2.  **Constrained Tool Definition Standard:** When building custom tools or scripts for agents, define them with a consistent template: explicit inputs, explicit non-destructive outputs, and strict limits on scope.
3.  **Enforce Salience:** Narrow tools force the agent to remain focused on the explicit boundaries of the task, reducing tangential hallucinations.

## Consequently
The AI's operational arena becomes a set of safe, deterministic guardrails. The agent spends its intelligence on *orchestrating* the problem rather than trying to perfectly craft an unwieldy, potentially destructive mega-command.

## Related Patterns
- **[G-005-tool-driven-correctness.md]**: Relies on specific objective tooling rather than raw AI reasoning.
