# G-007: Future-Proof Data Capture

**Status:** Active
**Type:** General
**Domain:** Ecosystem
**Importance:** ***

## Context
AI capabilities are advancing exponentially. The summarizations, compressions, and reasoning we consider "optimal" today will be viewed as primitive by the models of tomorrow.

## Problem
If an agent only stores the final "summary" or the end-state design decision, it permanently destroys the high-fidelity raw data and context that led to that decision. Future, more powerful AI systems will be unable to re-process the scenario to extract deeper insights because the underlying raw context is gone.

## Forces
- **Over-compression:** AI excels at summarizing, but summarization is inherently lossy.
- **Tacit Knowledge:** Deep context is often buried in raw error logs, raw usage metrics, or unparsed edge cases.
- **Future-proofing:** A project is not just a static codebase; its entire ecosystem (source code, product telemetry, user feedback, and raw interaction data) is a continuously re-processed dataset for tomorrow's AI.

## Solution (The Instruction)
Design data pipelines, logging, and knowledge capture to prioritize **Raw Data Retention**.

1.  **Capture Raw Data:** Alongside any summarized decision or state, whenever feasible, store the lower-level raw data in a structured, heavily labeled format.
2.  **Delay Lossy Transformation:** If an AI is used to process data, defer irreversible summarization to the absolute last possible step. Keep the immutable raw inputs accessible inside the system.
3.  **Future-Processable Tacit Knowledge:** When capturing decisions (as per `G-002`), explicitly include the raw forces, constraints, or error states that drove the decision, rather than just the summarized conclusion.

## Consequently
The ecosystem acts as a rich, lossless dataset. When deploying vastly superior AI models in the future, the project has retained the high-fidelity raw context required to allow the new models to uncover better optimizations or refactors, rather than hitting a ceiling governed by the compressed summaries of its predecessors.

## Related Patterns
- **[G-002-pageable-wisdom.md]**: Enhances the quality of tacit knowledge capture by demanding that the "Why" includes high-fidelity, raw constraints.
