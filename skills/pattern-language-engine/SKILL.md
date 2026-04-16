---
name: pattern-language-engine
description: Manage a hierarchical Pattern Language for documenting abstract wisdom.
---

# Pattern Language Engine Skill

This skill imbues an AI agent with the algorithmic ability to manage, enforce, and recursively self-improve an arbitrary repository directory using a hierarchical Pattern Language ecosystem.

## Core Mechanisms

1. **Lazy Loading Context**: The ecosystem uses `INDEX.md` files in directory domain folders. Before executing an architectural change, the AI must locate and read the relevant local `INDEX.md` to inherit context without blowing its token limit.
2. **Writing Patterns**: When instructed to document a new best practice, do not write unstructured notes. Generate a new rigidly-formatted pattern using `.agents/skills/pattern-language-engine/resources/pattern-template.md`.
   - **Numbering & Naming (Semantic Blocks)**: It enforces strict Semantic Namespace Blocks based on categories across increasingly small levels of scale. By leaving numeric space between different categories, this mitigates the need to re-organize the entire pattern language each time a new pattern is added or re-arranged:
     - `001-019`: Category 1 (e.g., overarching rules).
     - `020-039`: Category 2 (e.g., system integration).
     - `040-059`: Category 3 (e.g., implementation details).
     - ... additional categories
     The filename must start with this ID (e.g. `T-042-my-rule.md`).
3. **Index Maintenance**: Whenever you write or modify a pattern, you **MUST** update its corresponding domain `INDEX.md` and include a 1-sentence summary definition. If none exists, scaffold one via `.agents/skills/pattern-language-engine/resources/INDEX-template.md`. 
4. **Bootstrapping**: If a strictly opinionated BPT (Business/Product/Technical) format is requested for app software scaffolding, use the **bpt-software-scaffolding** skill instead.

## Structural Workflows

As pattern networks grow organically, they become structurally messy. This engine provides two executable commands for recursive self-improvement on any tracked directory:

1. **Internal Organization:** Analyze a pattern language folder, ensure patterns are ordered correctly by category, and physically execute ID re-mapping safely using `.tmp` buffers to guarantee zero namespace collisions.
   `/analyze-patterns [path/to/folder, if it's not obvious which to target]`

2. **Editorial Review:** Acts as an Editor-In-Chief to enforce strict format compliance, narrative conciseness, and lateral link-validity on a specific pattern file.
   `/review-pattern [pattern ID or path/to/pattern.md]`

## Use

The pattern language managed by this engine is a standalone work. It should be useful to both human readers and AI's. For AI's, it acts as a hierarchical memory and principles engine. Pattern Languages are very helpful for AI's to navigate decision-making in real-world environments with competiting concenrs. Pattern Languages are more salient than flat rules lists, as they are specifically designed to help navigate trade-offs inherent in large problem spaces.
