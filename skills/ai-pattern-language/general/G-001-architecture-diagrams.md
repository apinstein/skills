# G-001: Architecture Diagrams (LikeC4 vs Mermaid)

**Status:** Active
**Type:** General
**Domain:** Ecosystem
**Importance:** ***

## Context
As software ecosystems scale across multi-platform repositories (e.g., native apps, cloud backends, AI services), static code analysis alone is insufficient for understanding the entire ecosystem. AI agents must use diagram-as-code tools to model systems and comprehend structural boundaries compared to localized logic.

## Problem
Different diagram-as-code tools excel at diametrically opposed things. Using Mermaid for static architecture results in complex, unmaintainable "spaghetti" diagrams that AI struggles to safely modify. Conversely, using C4 to model sequential logic flowcharts or state machines is structurally impossible and semantic malpractice.

## Forces
- We need absolute high-level structural clarity (Containers, Components, Dependencies).
- We also need zero-ambiguity low-level algorithmic clarity (if/then flowcharts, state machines).
- Striving to keep all architecture in a single "omni-tool" breaks the semantics of both.

## Solution (The Instruction)
As an Agent, you must bifurcate your diagramming concerns based on the nature of the request:

1. **Use LikeC4 (`.c4`) for Static Architecture and Dependency Boundaries.**
   - Model the ecosystem using strict C4 hierarchy (`Person`, `System`, `ExternalSystem`, `Container`, `Component`).
   - Define purposeful `views` to zoom into specific boundaries without cluttering the visualization.
2. **Use Mermaid (`.md`) for Dynamic Logic, Flowcharts, and Sequence Diagrams.**
   - Use Mermaid exclusively for step-by-step algorithms, conditional branches, loops, and state machines.
3. **Cross-Link Between Them.**
   - In LikeC4 components that house complex internal algorithms, use the `link ../<file>.md` property to natively deep-link out to the Markdown document containing the granular Mermaid flowchart.

*Example:*
```likec4
calibration = component 'Calibration & Tracking Engine' {
  description 'Manages world anchors and space transformations.'
  link ../README-docs.md
}
```

## Consequently
Universally across all repositories, the macro-architecture remains structurally sound and zoomable (C4), while complex algorithmic logic is delegated to the proper tool (Mermaid), creating a tightly integrated but philosophically delineated documentation suite.

## Related Patterns
- **PHILOSOPHY**: This enforces structural purity, allowing the Model's context window to clearly index components without choking on Mermaid node sprawl.
