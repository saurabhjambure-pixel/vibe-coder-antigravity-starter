---
name: content-writer
description: Write concise content for each planned task using provided inputs and produce the specified artifact.
version: 0.1.0
---

Deliver the required content for the current task, using provided data and tone, and save it to the expected artifact path.
Keep outputs tight and acceptance-criteria focused so QA can validate easily.

## Use this skill when
- A plan step calls for drafting or rewriting content.
- Inputs (data, outline, tone) are available from previous artifacts or the prompt.

## Do not use this skill when
- Research or data gathering is required first.
- The request is purely evaluative (use QA skill instead).

## Instructions
1. Read the task definition, acceptance criteria, and any upstream artifacts.
2. Draft content that satisfies criteria; respect tone/format instructions.
3. Write the deliverable to the specified file under `artifacts/` or `.agents/`.
4. Include a brief self-check summary (bullets) noting how criteria were met.

## Guardrails
- Do not fabricate data; use only provided inputs.
- Keep style aligned to user specs; avoid generic filler.
- If blocking info is missing, request it instead of guessing.
