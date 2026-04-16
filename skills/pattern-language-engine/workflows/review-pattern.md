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
   - *Check:* Does it start with a title containing the appropriate Confidence Tag (`**`, `*`, or no asterisk)?
   - *Check:* Does it contain an archetypal picture or placeholder?
   - *Check:* Are the `⋇ ⋇ ⋇` markers used around the problem and solution blocks?
   - *Check:* Is the essence of the problem 1-2 sentences maximum?
   - *Check:* Is the Solution section strictly stated as a direct **instruction** rather than passive advice?
   - *Check:* Is there a solution diagram present?

3. **Invariant & Context Checks**
   - *Check (Confidence Validation):* If the pattern is marked with `**` (high confidence), does it truly summarize a property common to all possible ways of solving the problem (an inescapable invariant)? Or is it just a single solution among many (should have low confidence)?
   - *Check (Context Sensitive):* Does the pattern properly establish its context by linking UP to larger patterns and DOWN to smaller patterns using the final paragraph?

4. **Visual Aids & Pedagogy**
   - *Check:* Verify that the archetypal picture and the labeled solution diagram are genuinely useful and clarify the pattern effectively according to Alexander's pedagogical constraints.

5. **Cross-Link & Ecosystem Validity**
   - *Check:* Use `list_dir` or `find` to verify that every `[Pattern Name](file_path)` cross-link actually points to a file that exists on disk.
   - *Check:* Review the "Related Patterns" section. Are there other obvious patterns in the ecosystem that this pattern *should* link to but misses? 

6. **Index Placement**
   - *Check:* Read the appropriate `INDEX.md` where this pattern is listed. Is it placed in the correct logical category? Does its visual position accurately reflect its underlying pedagogical Scale?

## Output
Generate a Markdown editorial review grading the pattern on these axes, explicitly listing what must be fixed before the pattern is considered "Production Grade." Do not modify the file until the user reviews the edit suggestions.
