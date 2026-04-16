# Pattern Language Engine

This repository provides an algorithmic engine that allows AI agents to organize and maintain large, scale-free knowledge hierarchies based on [Christopher Alexander's](https://en.wikipedia.org/wiki/Christopher_Alexander) "[Pattern Language](https://en.wikipedia.org/wiki/Pattern_language)".


## Why a Pattern Language for AI?

AI agents are effectively unbounded intelligences operating across vast spaces of decision-making. Christopher Alexander's structural concept is a perfect fit for guiding AIs because it provides:

- **Context Window Efficiency (Lazy Loading):** Patterns are highly modular and cross-linkable. An AI can read a high-level master `INDEX.md` to grasp options, and dynamically traverse only specific markdown files required for its immediate task without blowing its token limit.
- **Continuous Scale:** The language seamlessly maps relationships from high-level abstractions down to tiny implementation details. when
- **Principled Trade-offs** Pattern Languages are excellent at guiding decisions with large trade-off boundaries, which is a great fit for AI's. The context and structure of the individual patterns that are apropos for a decision provide incredibly useful guidance for AI's to make better decisions and trade-offs.

## The Agnostic Setup

This skill is strictly "content agnostic". It does not dictate *what* you document (e.g., Code architecture vs. Botanical concepts), but rather *how* you document it so that AIs can traverse it flawlessly.

