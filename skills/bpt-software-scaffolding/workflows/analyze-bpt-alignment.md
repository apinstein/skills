---
description: Analyzes the boundaries and inter-links between the Business, Product, and Technical pattern languages of a specific software project.
---

# Analyze BPT Alignment (Business, Product, Technical)

**Goal:** Provide a high-level architectural review to ensure the Business, Product, and Technical (BPT) pattern languages are properly respecting their boundaries, and that cross-domain linking correctly follows the "Product is the center of gravity" philosophy.

## Context
In a software company ecosystem, the pattern language is explicitly bifurcated into Business, Product, and Technical domains. These domains are deeply interlocking, but their relationships must be strictly hierarchical (e.g. Product translates Business goals into actionable Technical requirements).

Because this Triad approach is highly opinionated, it is isolated here in the `bpt-software-scaffolding` skill. However, the physical mechanics of creating, ordering, and maintaining the three independent directories is entirely delegated to the `pattern-language-engine` skill. If a Technical pattern dictates a Product flow without a compelling architectural mandate, or a Product pattern operates completely divorced from the Business goals, the design is misaligned.

## Analysis Steps

1. **Read all Project Indices**
   - Read `pattern-languages/business/INDEX.md`
   - Read `pattern-languages/product/INDEX.md`
   - Read `pattern-languages/technical/INDEX.md`

2. **Evaluate Domain Boundary Respect**
   - *Technical Bleed:* Check the Technical index. Are any technical patterns improperly dictating User Experience (UX) rules that belong in the Product index? 
   - *Business Isolation:* Check the Product index. Are the Product flows completely isolated from the Business monetization/KPI patterns?

3. **Evaluate Hierarchical Dependency Links**
   - *Gravity Check:* Technical decisions exist to serve the Product. Therefore, Technical patterns should explicitly cross-link *upward* to the Product patterns they serve. Product patterns should primarily cross-link *upward* to Business patterns. 
   - *Action:* Look for orphaned domains. Do we have 20 Technical patterns and only 1 Product pattern? This implies the Technical architecture has lost its "Why."

4. **Generate Alignment Proposal**
   - Do not automatically modify the files. 
   - Generate a Markdown report detailing the health of the BPT triad. Highlight specific patterns that bleed across domains, suggest where missing cross-domain lateral links are needed, and point out if the ecosystem is over-indexing on Technical patterns while starving the Product/Business rules.

5. **Execution (Delegated to the Engine)**
   - Once the user approves the structural changes recommended by the BPT Alignment Proposal, you must **not** perform mass renames or re-indexing manually.
   - You must leverage the generic `.agents/skills/pattern-language-engine/workflows/analyze-pattern-organization.md` workflow on each of the affected domains *individually* to safely execute the physical re-alignments. The BPT skill tells you *what* should change, but the Engine skill dictates *how* it safely changes.
