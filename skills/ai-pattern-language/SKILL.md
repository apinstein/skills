---
name: ai-pattern-language
description: Instructs the AI to operate using the Christopher Alexander "Pattern Language" ecosystem, managing architecture context and rules recursively.
---

# AI Pattern Language Skill

This skill imbues an AI agent with the ability to manage, enforce, and recursively self-improve using a Pattern Language ecosystem (inspired by Christopher Alexander).

## Core Mechanisms
1. **Lazy Loading Context**: The ecosystem uses `INDEX.md` files in each domain folder (`pattern-languages/business`, `product`, `technical`, and `.agents/skills/ai-pattern-language/general`). Before executing an architectural change, the AI should locate and read the relevant `INDEX.md` to get the context without blowing its token limit.
2. **Writing Patterns**: When instructed to document a new best practice or when resolving a dead end, do not write raw unstructured notes. You must generate a new pattern using `.agents/skills/ai-pattern-language/resources/pattern-template.md`.
   - **Numbering & Naming (Semantic Blocks)**: New patterns must be numbered using the Semantic Scale Blocks. Macro-scale patterns (overarching philosophy) sit in `001-019`. Meso-scale (system coordination) in `020-039`. Micro-scale (implementation details) in `040-059`. When minting a new pattern, identify its scale and select the next available integer *within that specific block*. You **must** ensure the filename strictly starts with this ID (e.g. `T-042-sql-indices.md`).
3. **Index Maintenance**: Whenever you write or modify a pattern, you **MUST** update its corresponding domain `INDEX.md` and include a 1-sentence summary. If the `INDEX.md` doesn't exist, generate one using `.agents/skills/ai-pattern-language/resources/INDEX-template.md`. Check the `INDEX.md` to determine the next available ID before creating a new pattern.
4. **Bootstrapping**: If a project doesn't have any patterns yet, you can run `.agents/skills/ai-pattern-language/workflows/bpt/bootstrap-project-patterns.md` to scaffold them.

## Directory Structure (The Meta vs The Project)
- **The General Skill Directory** (`.agents/skills/ai-pattern-language`): This is the "meta" language. It houses the universal, heavily opinionated patterns (`general/PHILOSOPHY.md`, `G-001...`) that instruct the AI on *how to leverage AI to build software*. This directory contains the guidelines for the execution of work itself, and is portable (e.g., as a git submodule) across multiple repos.
- **The Project Directory** (`pattern-languages/`): This is the "domain" language. It houses the patterns specific to the codebase of *this* project, defining *what* software is being built. This logic is safely separated from the skill framework.
