---
description: Bootstrap the initial project-specific pattern language by analyzing the existing codebase.
---

# Bootstrap Project AI Patterns

**Goal:** We do not build "one" project-specific pattern language. We explicitly bootstrap **three complementary, standalone pattern languages** (Business, Product, and Technical) for the target software project. Each domain is managed as its own completely independent ecosystem (with its own `INDEX.md` and scale hierarchies), but they communicate via strict cross-domain external references (governed by `.agents/skills/bpt-software-scaffolding/workflows/analyze-bpt-alignment.md`).

## Steps

0. **Guard** This workflow is only to be run once per project. If the pattern language already exists, this task should abort.

1. **Gather Project Context**
   Read all documentation to deeply understand the project from a unified Business, Product, and Technical lens. This includes reviewing `.agents/rules.md`, top-level `README.md` files, analyzing the physical file structure and tech stack (e.g. Models/Views/Controllers), and referencing any external tools like linked mission docs, issue trackers (e.g. Linear), or design files.

2. **Identify Recurring Solutions (Across Domains)**
   Based on the context from Step 1, look for major architectural motifs in the codebase across the 3 domains:
   - **Business Scale:** Are there obvious target audience behaviors, monetization strategies, or KPIs defined in the documentation or core app logic?
   - **Product Scale:** What are the central User Journeys? Is there a defined Design System, onboarding flow, or core UX motif?
   - **Technical Scale:** 
     - How is State Managed? (e.g., SwiftUI `@Observable`, Redux, etc.)
     - How is Data Fetched/Persisted?
     - How is Routing/Navigation handled?
     - How are Side Effects or Async Tasks managed?

3. **Scaffold the Project Structure**
   Create the following directories in the project root if they do not exist: `pattern-languages/business`, `pattern-languages/product`, and `pattern-languages/technical`.
   - Inside each of these 3 domain directories, use `.agents/skills/pattern-language-engine/resources/INDEX-template.md` to instantiate an initial `INDEX.md` file.
   - Inside the root `pattern-languages/` folder, create a simple `README.md` that instructs human engineers and AI agents to read the complete framework documentation over at `.agents/skills/pattern-language-engine/README.md`.

4. **Draft the Base Patterns (Seeding the Namespace)**
   For each of the three newly created standalone pattern languages, use `.agents/skills/pattern-language-engine/resources/pattern-template.md` to generate the foundational files.

   While each of the three pattern languages is independent, they should be cross-linked where applicable. This initial seeding is a unique opporuntity to identify and segregate project patterns into these complementary domains. For example, a technical pattern might reference a product pattern that it enables, or a business pattern might reference a product pattern that it incentivizes.
   
5. **Update Domain Indices**
   Update the `INDEX.md` files you created in Step 3. List out the newly generated patterns within each domain's index. Each entry must include a 1-sentence summary to serve as a fast-reference guide for future AI agents. Link the patterns to each other where applicable in their "Related Patterns" sections.
