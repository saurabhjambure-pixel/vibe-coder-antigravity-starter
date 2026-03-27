---
name: task-planner
description: Break a user goal into ordered, atomic tasks with owners and required artifacts.
version: 0.1.0
---

Produce a short task plan that sequences work for the Planner → Content-Writer → QA-Validator pipeline.
Each task must have an owner, dependency notes, and an expected artifact name.

## Use this skill when
- A new goal needs decomposition into clear, assignable steps.
- You must coordinate multiple agents to avoid overlap.

## Do not use this skill when
- The user already supplied a concrete task list.
- Only a single, simple action is requested.

## Instructions
1. Capture the goal and acceptance criteria; ask clarifications only if blocking.
2. Propose 3–6 tasks, each with owner, dependency, and artifact path under `artifacts/` or `.agents/`.
3. Keep language concise and execution-ready; avoid narrative prose.
4. Emit JSON and a short bullet list if the host expects artifacts; otherwise plain bullets are fine.

## Guardrails
- Avoid creating tasks for unavailable agents.
- Do not invent acceptance criteria; restate provided ones.
- Ensure ordering respects dependencies.
