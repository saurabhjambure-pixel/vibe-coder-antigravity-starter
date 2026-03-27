---
name: task-planner
description: Plan a user goal into ordered, atomic subtasks with owners and expected artifacts.
version: 0.1.0
---

Draft a short, dependency-aware task plan for the user's goal and assign each task to the right specialist agent.
Ensure the plan yields concrete artifacts the downstream agents can validate.

## Use this skill when
- The user provides a goal that needs to be broken into actionable steps.
- Multiple agents or roles should collaborate in sequence.

## Do not use this skill when
- The request is a single, simple action with no dependencies.
- The user already supplied a complete task list with owners.

## Instructions
1. Clarify the end goal and acceptance criteria; ask only if blocking.
2. Produce 3-7 ordered tasks with clear owners (Planner/Data/QA) and required artifacts per task.
3. Mark dependencies explicitly so agents run in the correct order.
4. Keep wording concise and execution-ready.

## Guardrails
- Prefer fewer, atomic tasks over verbose lists.
- Avoid assigning tasks to unspecified agents; stick to available roles.
- Always specify expected artifact filenames under `.agents/` or `artifacts/`.
