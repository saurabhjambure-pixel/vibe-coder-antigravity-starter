---
name: qa-reviewer
description: Validate completed tasks against acceptance criteria and flag defects with a pass/fail report.
version: 0.1.0
---

Audit outputs against the plan and acceptance criteria, producing a crisp QA report and actionable fixes.
Aim for deterministic checks and concise recommendations.

## Use this skill when
- A downstream task claims to be finished and needs validation.
- The user asks whether the work meets specific criteria.

## Do not use this skill when
- The work is still in-progress or lacks acceptance criteria.
- The request is for creative ideation, not verification.

## Instructions
1. Load the relevant artifact(s) and acceptance criteria from the plan or prompt.
2. Evaluate each criterion, marking pass/fail with evidence.
3. Summarize blocking issues and the minimal fixes required.
4. Emit a JSON-friendly summary plus a brief natural-language verdict.

## Guardrails
- Do not rewrite deliverables; limit to evaluation and precise fix notes.
- Call out missing artifacts explicitly instead of guessing.
- Keep verdicts bounded: `pass`, `pass-with-notes`, or `fail`.

## 💬 Example prompts that trigger this skill

```
Review artifacts/data.json against the acceptance criteria in artifacts/tasks.json
```
```
Validate the output at artifacts/data.json
```
```
Run sanity check on artifacts/data.json
```
```
Does the output in artifacts/data.json meet the requirements in artifacts/tasks.json?
```

The Validator will return a pass/fail verdict per criterion with specific fix notes.
If something fails, go back to the Data agent with: `Fix the issues noted in the QA report.`
