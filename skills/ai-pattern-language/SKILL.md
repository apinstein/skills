---
name: ai-pattern-language
description: Instructs the AI to operate using the Christopher Alexander "Pattern Language" ecosystem, managing architecture context and rules recursively.
---

# AI Pattern Language Skill

This skill imbues an AI agent with the ability to manage, enforce, and recursively self-improve using a Pattern Language ecosystem (inspired by Christopher Alexander).

## Core Mechanisms
1. **Lazy Loading Context**: The ecosystem uses `INDEX.md` files in each domain folder (`pattern-languages/business`, `product`, `technical`, and `.agents/skills/ai-pattern-language/general`). Before executing an architectural change, the AI should locate and read the relevant `INDEX.md` to get the context without blowing its token limit.
2. **Writing Patterns**: When instructed to document a new best practice or when resolving a dead end, do not write raw unstructured notes. You must generate a new pattern using `.agents/skills/ai-pattern-language/resources/pattern-template.md`.
   - **Numbering & Naming**: New patterns must be systematically numbered via an ID (e.g. `P-001`, `B-042`). You **must** ensure the pattern's filename strictly starts with this exact ID as a checksum (e.g. `T-014-database-scaling.md`). 
3. **Index Maintenance**: Whenever you write or modify a pattern, you **MUST** update its corresponding domain `INDEX.md` and include a 1-sentence summary. If the `INDEX.md` doesn't exist, generate one using `.agents/skills/ai-pattern-language/resources/INDEX-template.md`. Check the `INDEX.md` to determine the next available ID before creating a new pattern.
4. **Bootstrapping**: If a project doesn't have any patterns yet, you can run `.agents/skills/ai-pattern-language/workflows/bootstrap-project-patterns.md` to scaffold them.

## Directory Structure
- **This Skill Directory** (`.agents/skills/ai-pattern-language`): Houses the universal, heavily opinionated "General framework" (`general/PHILOSOPHY.md`, `G-001...`), alongside the templates and workflows. This directory is meant to be portable (e.g., as a git submodule) across multiple repos.
- **The Project Directory** (`pattern-languages/`): Houses the patterns specific to *this* project, safely separated from the skill logic.
