---
name: code-review
description: Guidelines and checklist for performing rigorous AI-based code reviews emphasizing test coverage, naming, DRY principles, and standards alignment.
---

# Code Review Skill

When performing a code review, follow this checklist to ensure high quality, maintainable code. Your review should be rigorous, catching both macro architectural missteps and micro implementation flaws.

## 1. Project-Specific Standards
- [ ] **Coding Standards**: Does the code strictly adhere to the project's specifically documented coding standards? (Reference project-local documentation first).

## 2. General Code Quality
- [ ] **Idiomatic Implementation**: Is the code written using APIs, patterns, and architectural semantics that are idiomatic to the specific host environment being modified? Especially in monorepos, explicitly verify that you are evaluating the code within its correct context (e.g., Apple ecosystem paradigms for Swift, TS/React paradigms for the web) rather than applying generalized defaults.
- [ ] **Naming Conventions**: Are the names for variables, functions, and classes clear, descriptive, and accurately reflective of their intent, while remaining consistent with the overall naming patterns of the project and its ecosystem? (Think hard about this—bad naming is technical debt).
- [ ] **Inline Documentation**: Are non-trivial implementations properly documented with inline comments or docstrings? Documentation should explain the *why* and the intent behind complex logic to a "future version of yourself" in a way that makes the function immediately easy to grok.
- [ ] **Readability & Complexity**: Is the logic overly "clever" or unnecessarily complex? Ensure the code is simplified or factored cleanly so that future developers can easily comprehend it.
- [ ] **The Boy Scout Rule (No Lazy Defers)**: Did the coder leave trivial "will fix later" or "TODO" notes out of laziness? AI coders have the capacity to apply trivial improvements instantly; code must be left better than it was found. (Note: Carefully distinguish this from initiating massive, spiraling refactors, which violates the Scope Creep rule).

## 3. Test Coverage
- [ ] **Verification & Test Matrix**: Is there robust automated test coverage for all newly created or modified code? Assert that tests form a proper "test matrix" covering materially different input ranges (to trigger distinct behaviors) as well as pathological cases where explicit guards and edge-case handling are required.

## 4. DRY Principle (Don't Repeat Yourself)
- [ ] **Reinventing the Wheel**: Does the code duplicate functionality that already exists elsewhere in the codebase? (Crucial: identify if existing utilities, helpers, or pattern language classes should have been used instead).

## 5. Architecture and Logic
- [ ] **Error Handling**: Are all reasonable failure modes and edge cases anticipated and handled gracefully?
- [ ] **Scope Creep**: Are the code changes strictly constrained to the stated goals? Call out any unprovoked refactoring or unrelated changes.
- [ ] **Data Migrations**: If changes involve schema updates or data transformations, assess the rollout risk. Are migrations safe, reversible, and designed to run without locking core tables or causing downtime?
- [ ] **Performance**: Are there any obvious performance bottlenecks (e.g., N+1 queries, unnecessary loop iterations, or large object allocations)?
- [ ] **Security**: Does the code introduce any vulnerabilities? Look specifically for missing authentication/authorization guards on new routes, unsanitized inputs susceptible to injection, or accidental exposure of secrets/PII.
- [ ] **Observability**: Does the code emit appropriate logs or metrics for production debugging without exposing sensitive data?
- [ ] **Backward Compatibility**: If this alters APIs, database schemas, or exported modules, is it backward compatible? Ensure that any breaking changes are explicitly highlighted and that downstream consequences are handled.
- [ ] **Concurrency & Thread Safety**: Is the code thread-safe? Ensure that no race conditions or deadlocks are introduced, particularly in asynchronous operations.
- [ ] **Coupling & Domain Boundaries**: Does the change inappropriately couple two separate domains or modules (e.g., UI code leaking into the database layer)? Ensure strict modular boundaries are respected.

## 6. Output and Action
Present your findings as a structured code review. If applicable, provide the exact diffs or replacement blocks required to resolve the issues you found, or proactively patch the code based on the established workflow.
