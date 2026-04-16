---
description: Acts as a stringent editorial reviewer for a single pattern, checking structural compliance, conciseness, visual aids, and cross-link validity.
---

# Review Pattern (The Editor)

**Goal:** Act as a critical, high-standards "Editor-in-Chief" for a single pattern file. Ensure the pattern strictly adheres to the pedagogical constraints, is free of bloat, and provides genuine invariant value.

## Context
Writing a pattern is easy; writing a *good* pattern that resolves a powerful conflict concisely is very hard. As the ecosystem scales, patterns can become bloated, lose their instructional edge, or break links. This workflow enforces the "Quality is Free" standard on individual micro-patterns.

## Analysis Steps

1. **Target the Pattern**
   - The user must specify the path to a single pattern file (e.g., `G-005-tool-driven-correctness.md` or a project's `product/P-001-button.md`). Read the file.

2. **Template Compliance Checks**
   - *Check:* Does it contain all explicit sections defined in `pattern-template.md` (Context, Problem, Forces, Solution, Consequently, Related Patterns)?
   - *Check:* Is the Problem section extremely constrained (1-3 sentences maximum)?
   - *Check:* Is the Solution section strictly stated as a direct **instruction/mandate** rather than passive advice?

3. **Conciseness & Power Checks**
   - *Check:* Is the language concise and powerful? Flag paragraphs that ramble.
   - *Check (The Hallucination Test):* Is this actually a structural invariant (a real pattern), or is it just generic trite advice (e.g., "write clean code")? It must resolve a specific tension.
   - *Check (Force Tension):* Do the elements listed under "Forces" genuinely conflict with each other? Without conflicting forces, there is no need for a pattern.

4. **Visual Aids & Pedagogy**
   - *Check:* If the pattern discusses complex object relationships, state changes, or UI flow, does it contain a Mermaid diagram or LikeC4 layout? 
   - *Action:* If a drawing would drastically clarify the text, explicitly flag it and suggest adding one.

5. **Cross-Link & Ecosystem Validity**
   - *Check:* Use `list_dir` or `find` to verify that every `[Pattern Name](file_path)` cross-link actually points to a file that exists on disk.
   - *Check:* Review the "Related Patterns" section. Are there other obvious patterns in the ecosystem that this pattern *should* link to but misses? 

6. **Index Placement**
   - *Check:* Read the appropriate `INDEX.md` where this pattern is listed. Is it placed in the correct logical category? Does its visual position accurately reflect its underlying pedagogical Scale?

## Output
Generate a Markdown editorial review grading the pattern on these axes, explicitly listing what must be fixed before the pattern is considered "Production Grade." Do not modify the file until the user reviews the edit suggestions.
