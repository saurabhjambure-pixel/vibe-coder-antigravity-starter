---
name: logic-sanity-check
description: Audit outputs against acceptance criteria and logical consistency, producing a pass/fail QA report.
version: 0.1.0
---

Evaluate completed artifacts for correctness, completeness, and adherence to the task plan, then emit a clear verdict with fixes.
Keep the review terse and evidence-based so the team can act quickly.

## Use this skill when
- A task deliverable needs validation before handoff.
- The user asks whether the output meets criteria or has logical gaps.

## Do not use this skill when
- The work is unfinished or lacks criteria to check against.
- The request is for new content creation.

## Instructions
1. Load the deliverable and acceptance criteria from artifacts or the prompt.
2. Check for factual accuracy, completeness, and alignment to requirements.
3. Produce a QA report with pass/fail, issues found, and minimal fixes.
4. Save the report to the expected artifact path (e.g., `artifacts/qa-report.json`).

## Guardrails
- Do not rewrite the content; focus on evaluation.
- Flag missing inputs rather than guessing.
- Keep severity levels simple: `blocker`, `minor`, `note`.
