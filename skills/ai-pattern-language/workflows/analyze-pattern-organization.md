---
description: Analyzes the organization of the pattern language indices to ensure logical grouping by Scale, Domain, and Complementary relationships.
---

# Analyze Pattern Organization

**Goal:** Provide an introspective, recursive self-improvement pass over the current Pattern Language ecosystem to ensure patterns are organized correctly according to formal Pattern Language pedagogy.

## Context
A pattern language is only as useful as its index. If patterns are grouped arbitrarily, an AI or human engineer will fail to find the right context. Christopher Alexander's pedagogy dictates that patterns should be ordered structurally, forming a cohesive graph from the macroscopic to the microscopic.

## Analysis Steps

1. **Target the Index**
   - The user must specify the path to a pattern language folder (e.g., `.agents/skills/ai-pattern-language/general/` or a project's `pattern-languages/technical/`) or the direct path to the `INDEX.md` itself.
   - If a folder is provided, explicitly read the `INDEX.md` inside that folder.

2. **Evaluate Groupings by Scale (Macroscopic to Microscopic)**
   - *Alexander's Pedagogy:* Patterns must be ordered from the largest architectural structures down to the smallest implementation details.
   - *Action:* Review the order of patterns within each index. Does a microscopic implementation detail (e.g., "Button Padding") appear before a macroscopic structural rule (e.g., "Global Design System")? Suggest a reordering so that "reading down" the index logically zooms in on the scale.

3. **Evaluate Groupings by Domain/Context**
   - *Alexander's Pedagogy:* Patterns that solve similar morphological problems should be grouped into clusters (sub-sections).
   - *Action:* Identify flat lists of more than 5-7 patterns. Suggest categorical subheadings to group them logically (e.g., in Technical, creating sub-groups for "State Management", "Data Persistence", "UI Rendering").

4. **Evaluate Morphological/Complementary Links**
   - *Alexander's Pedagogy:* "Each pattern implies a smaller pattern which completes it." No pattern exists in isolation. 
   - *Action:* Look at the 1-sentence summaries in the indices. Are there patterns that seem orphaned or redundant? Are there macroscopic patterns that lack any resolving microscopic patterns? Suggest new patterns that need to be written to bridge the gaps, or suggest merging redundant ones.

5. **Generate Reorganization Proposal**
   - Do not automatically modify the files without user consent. 
   - Generate a Markdown report for the user detailing the structural health of the pattern language, highlighting misaligned scales, missing complementary links, or suggested new sub-categories. 
   - Explicitly ask the user for approval before proceeding to Phase 2.

## Phase 2: The Executioner
Once the user approves the Phase 1 structural reorganization, you must mechanically execute the changes to preserve the Semantic ID namespace.

1. **Calculate Semantic Blocks**
   - Read the newly approved index order. Map it to the standard Semantic Scale Blocks (e.g. `1-19` for Macro, `20-39` for Meso, `40-59` for Micro). We always leave a little space at the end for new patterns to fill in, unless we think the pattern language is nearly complete, in which case we keep numbers strictly sequential and do not leave space at the end of categories.
   - Determine the new chronological mathematical IDs for each file.

2. **The Infallible Rename Sweep**
   To prevent catastrophic namespace collisions (e.g., if the new ID for pattern A was the old ID for pattern B), you must execute renaming in a strict three-step buffer process:
   - **Step 2a:** Draft the new desired numbering explicitly into the `INDEX.md` alongside the current number so the mapping is formally captured. (e.g., Update the list item from `- [G-002: Pageable Wisdom]` to `- [G-020 (was G-002): Pageable Wisdom]`).
   - **Step 2b (Buffer):** Physically rename all existing pattern files to `.tmp`. Do not do this via ad-hoc terminal manipulation; it wastes tokens and risks scale error. Run the provided strongly constrained script tool: `bash path/to/ai-pattern-language/scripts/buffer-namespace.sh [path/to/folder]`. This clears the local `G-###.md` namespace perfectly.
   - **Step 2c (Resolve):** Do not manually execute the renames. Instead, explicitly run the execution tool: `bash path/to/ai-pattern-language/scripts/resolve-namespace.sh [path/to/folder]`. This script will programmatically extract every `[NEW (was OLD)]` mapping from the `INDEX.md`, formally validate that there are no duplicates and that every mapping has a matching `.tmp` file, and execute all renames flawlessly in milliseconds without AI risk.

3. **Link Healing**
   - Run a workspace-wide string replacement sweep to find any broken markdown links pointing to the old IDs (e.g. `[G-002`) and replace them with the new IDs (`[G-020`). 
   - Clean up the `INDEX.md` to remove any mapping drafts and ensure every link perfectly points to the newly re-indexed files.
