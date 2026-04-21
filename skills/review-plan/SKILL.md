---
name: review-plan
description: Guidelines and checklist for reviewing implementation plans consistently.
---

# Review Plan Skill

When reviewing an implementation plan for a project, follow these checklist items systematically. Your goal is to provide a comprehensive, rigorous review comparing the plan to the project's goals, standards, and required components.

## 1. Goal and Product Alignment
- [ ] **Business/Product Goals**: Does the plan directly address the core objectives described by the user?
- [ ] **Cross-Reference Product Documentation**: Does the plan align with existing business mission, vision, and strategy, product roadmaps, requirements documents, or user stories without conflicting with established business rules or product visions?
- [ ] **Scope Creep**: Are the proposed changes localized to the objective, or are there unnecessary tangents?

## 2. Technical Standards and Constraints
- [ ] **Coding Conventions**: Does the technical design follow our documented coding conventions?
- [ ] **Pattern Languages**: Does the plan adhere to the pattern languages established in the project (where applicable)?
- [ ] **Cross-Reference Project Documentation**: Does the plan directly conflict with or reinvent patterns established in the project's documentation at all levels (architecture docs, case studies, KIs)? All historical nuances and boundaries must be accounted for.
- [ ] **Documentation Updates**: Does the plan explicitly document the changes required for system documentation, code comments, or user-facing guides? Often missing, ensure it is highlighted if absent!

## 3. Canonical Plan Completeness
Verify that the implementation plan contains the expected core components. A proper plan should follow this canonical structure:
- [ ] **Goal Description / Context**: What the work is and why we are doing it.
- [ ] **User Review Required**: Does the plan explicitly document breaking changes or significant design choices that the user must approve, using markdown alerts (`> [!IMPORTANT]`)?
- [ ] **Plan Visualizations**: Does the plan include appropriate diagrams (e.g. Mermaid sequence diagrams, state transitions, class diagrams) to clarify complex workflows or structural changes for the plan review?
- [ ] **Proposed Changes**: The specific code changes, grouped by components or files.
- [ ] **Documentation Changes**: What documentation (architecture docs in c4/mermaid/*.md, etc.) updates should be made to keep the system documentation in sync with the changes.
- [ ] **Verification Plan**: Must include both automated and manual tests. The plan should indicate that the user is NOT asked to perform manual verification until the entire plan is complete and all automated tests are passing. (Exceptions are permitted if the AI specifically needs the user to test a tricky component early, but this is never a substitute for diligently developing automated tests and getting them passing).

## 4. Development Methodology
- [ ] **Spec-Driven Development (TDD)**: Reinforce that development must follow spec-driven development using a strict Red-Green cycle. Point out anywhere in the verification plan that lacks automated tests for the feature.
- [ ] **Implementation Instructions**: Does the plan explicitly instruct the executing AI or engineer to query and reference the project's coding standards and related documentation files during implementation?

## 5. The "Two Hard Problems" in CS
Address naming and caching explicitly, as they are historically the source of the most challenging bugs and technical debt:
- [ ] **Naming Things**: Are the proposed names for new components, files, functions, variables, and API endpoints clear, consistent with existing conventions, and accurately descriptive of their purpose? If the plan introduces new concepts, are the names chosen carefully to avoid ambiguity?
- [ ] **Cache Invalidation**: Does the plan introduce or interact with any caching layers? If so, are the cache invalidation strategies, TTLs, and cache coherence mechanisms explicitly planned out and documented?

## 6. Red-Teaming the Plan
Aggressively review the plan for robustness by checking the following:
- [ ] **Internal Consistency**: Is the plan logically sound and internally consistent from end-to-end?
- [ ] **Comprehensiveness (No Glossing Over)**: Does the plan skip or gloss over foreseeable details that will become blockers during implementation? While some minor things must be figured out at runtime, all foreseeable architectural specifics or known edge-cases must be clarified in the text.
- [ ] **Cross-Referencing**: Where details depend on other components, are they properly cross-referenced against the rest of the plan or existing system documentation?
- [ ] **Anticipation of Failure Modes** Reading the plan, can you anticipate any failures in execution we will have due to lack of planning?

## 7. Output and Action
Present your review as a structured response identifying any missing pieces or areas of misalignment based on this checklist. **Most importantly, DO NOT just ask the user if they want to update the plan.** After summarizing the audit, proactively patch the `implementation_plan.md` file (or relevant plan document) to fix all the methodological gaps and discrepancies you identified.
