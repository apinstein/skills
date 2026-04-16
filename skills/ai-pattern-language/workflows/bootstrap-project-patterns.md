---
description: Bootstrap the initial project-specific pattern language by analyzing the existing codebase.
---

# Bootstrap Project AI Patterns

**Goal:** Analyze the current project source code, file structures, and existing documentation to map out the foundational project-specific patterns, using the generalized patterns as a baseline.

## Steps

1. **Read Existing Rules**
   Review `.agents/rules.md` and any existing top-level `README.md` files to understand the core directives of the project.

2. **Analyze File Structure and Tech Stack**
   Use `list_dir` or `find_by_name` to understand the main directories (e.g., `Sources/`, `Views/`, `Models/`, `Controllers/`, or web equivalents). Identify the core frameworks in use.

3. **Identify Recurring Solutions (Across Scales)**
   Look for major architectural motifs in the codebase across the 3 domains:
   - **Business Scale:** Are there obvious target audience behaviors, monetization strategies, or KPIs defined in the documentation or core app logic?
   - **Product Scale:** What are the central User Journeys? Is there a defined Design System, onboarding flow, or core UX motif?
   - **Technical Scale:** 
     - How is State Managed? (e.g., SwiftUI `@Observable`, Redux, etc.)
     - How is Data Fetched/Persisted?
     - How is Routing/Navigation handled?
     - How are Side Effects or Async Tasks managed?

4. **Scaffold the Project Structure**
   Before drafting any patterns, ensure the project destination exists. Create the following directories in the project root if they do not exist: `pattern-languages/business`, `pattern-languages/product`, and `pattern-languages/technical`.
   - Inside each of these 3 domain directories, use `.agents/skills/ai-pattern-language/resources/INDEX-template.md` to instantiate an initial `INDEX.md` file.
   - Inside the root `pattern-languages/` folder, create a simple `README.md` that instructs human engineers and AI agents to read the complete framework documentation over at `.agents/skills/ai-pattern-language/README.md`.

5. **Draft the Base Patterns**
   For each identified motif, use the template in `.agents/skills/ai-pattern-language/resources/pattern-template.md` to generate a new markdown file inside `pattern-languages/business/`, `pattern-languages/product/`, or `pattern-languages/technical/`.
   
   Name them descriptively using the correct domain prefix, e.g., `T-001-state-management.md`, `P-001-frictionless-onboarding.md`, `B-001-freemium-conversion.md`.

6. **Update Domain Indices**
   Update the `INDEX.md` files you created in Step 4. List out the newly generated patterns within each domain's index. Each entry must include a 1-sentence summary to serve as a fast-reference guide for future AI agents. Link the patterns to each other where applicable in their "Related Patterns" sections.

7. **Self-Correction & Refinement**
   Review the generated patterns. Ensure that under the "Solution" section, the instructions are written as clear, actionable directives for an AI agent to follow, rather than just passive documentation.