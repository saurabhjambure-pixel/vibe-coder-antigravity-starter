# Orchestration Patterns

Multi-agent systems require structured coordination.

Without orchestration patterns, complexity turns into chaos.

This document outlines practical patterns for reliable agent workflows.

---

# 1️⃣ The PDCA Model (Recommended)

PDCA stands for:

Plan → Do → Check → Act

It creates a reliability loop for multi-agent systems.

---

## Plan

Planner Agent:
- Breaks high-level goals into atomic tasks
- Produces structured execution plan artifact
- Does not execute logic-heavy tasks

Output:
- Task breakdown JSON
- Delegation map

---

## Do

Specialist Agents:
- Execute only domain-specific responsibilities
- Use relevant skills
- Produce structured artifacts

Examples:
- Data agent processes metrics
- Retrieval agent fetches documents
- UI agent generates interface
- API agent writes endpoints

Each agent works independently.

---

## Check

QA Agent:
- Validates outputs using testing skills
- Runs schema validation
- Executes regression tests
- Produces structured validation report

If validation fails:
- Task is reassigned
- Specialist corrects output
- QA revalidates

Repeat until artifact passes checks.

---

## Act

Human:
- Reviews artifacts
- Confirms reliability
- Approves merge or deployment

Human oversight remains critical.

---

# 2️⃣ Delegation Pattern

Do not allow planners to execute.

Planner:
- Defines tasks
- Assigns responsibilities
- Does not implement logic

Specialists:
- Execute isolated work

QA:
- Verifies and challenges

This separation improves clarity and reduces context overload.

---

# 3️⃣ Artifact-First Workflow

Never allow agents to output only reasoning.

Require:
- Structured JSON
- Logs
- Execution plans
- Screenshots (for UI validation)
- Validation reports

Artifacts reduce ambiguity and make debugging easier.

---

# 4️⃣ Parallel Execution Pattern

Independent tasks can be delegated simultaneously to different agents.

Benefits:
- Faster iteration
- Reduced context congestion
- Clear role boundaries

Use parallelism when tasks are logically independent.

---

# 5️⃣ Escalation Pattern

If validation repeatedly fails:

1. Planner revisits task definition.
2. Adjust scope or constraints.
3. Reassign to specialist.
4. QA revalidates.

Avoid infinite correction loops without planner intervention.

---

# 6️⃣ When to Keep It Simple

Multi-agent orchestration is powerful but not always necessary.

Use a single agent when:
- Task is simple
- No external tools are involved
- No validation loop is required
- Determinism is not critical

Do not over-engineer.

---

# 7️⃣ Reviewer-Worker Loop (Validator Pattern)

**Planner → Worker → Validator** ensures outputs are actionable and safe before marking tasks complete.

- Planner creates an ordered task list with owners and expected artifacts.
- Worker (Data or Specialist) executes a task and writes the artifact.
- Validator reviews the artifact against acceptance criteria and common failure modes (missing error handling, vague tasks, absent artifacts, untested edges).
- If Validator fails the artifact, it sends concise fix notes back to the Worker; loop continues until pass.
- If requirements are ambiguous, Validator escalates to Planner for clarification instead of guessing.

Benefits:
- Prevents “God Agent” behavior by isolating review from execution.
- Catches structural issues early (unclear tasks, missing outputs, weak validation).
- Produces a QA report artifact, improving auditability and trust.

---

# Skill Selection Decision Tree

Use this quick mapping to choose the right skill:

| If input / need | Use this skill | Expected artifact |
| --- | --- | --- |
| Raw CSV / JSON needs cleaning or shaping | Data-Cleaner | `artifacts/cleaned-data.json` or `.csv` |
| User goal is broad and unstructured | Task-Planner | `artifacts/tasks.json` |
| Content needs to be drafted from supplied data/outline | Content-Writer | `artifacts/output.md` |
| Completed output needs validation against criteria | Logic-Sanity-Check (Validator) | `artifacts/qa-report.json` |
| Ambiguous requirements or missing data | Planner clarification loop (re-plan) | Updated `artifacts/tasks.json` |
| Terminal permission/governance checks | Runtime Governance helper | `.agents/runtime.log` |

Guideline: Prefer the most specific skill that produces a structured artifact the next agent can consume. If none match, escalate to Planner to refine the ask.

Schemas for validation:
- `schema/artifacts/tasks.schema.json`
- `schema/artifacts/output.schema.json`
- `schema/artifacts/qa-report.schema.json`

---

# Closing Thought

Orchestration is about structure, not complexity.

The goal is not to create more agents.

The goal is to create clearer responsibility boundaries and reliable validation loops.

When done correctly, multi-agent systems become predictable, testable, and scalable.
