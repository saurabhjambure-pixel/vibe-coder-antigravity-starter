# Example: Planner → Worker → QA Loop

This is a complete, working end-to-end example of the Antigravity orchestration pattern.

**Goal:** Write a 3-section product overview for a B2B SaaS invoicing tool.

---

## What This Example Demonstrates

- A **Planner agent** decomposing a goal into 3 ordered, atomic subtasks
- A **Content-Writer agent** executing each task with self-validation
- A **QA-Validator agent** auditing outputs against acceptance criteria
- Structured JSON artifacts flowing between each stage
- The `depends_on` chain enforcing task ordering without manual coordination

---

## Directory Structure

```
example-planner-qa/
├── .agent/
│   ├── agents/
│   │   ├── Planner.yaml           ← Orchestrator: breaks goals into tasks
│   │   ├── Content-Writer.yaml    ← Worker: executes writing tasks
│   │   └── QA-Validator.yaml      ← Auditor: validates outputs
│   └── skills/
│       ├── task-planner/
│       │   └── SKILL.md           ← Loaded by Planner on trigger
│       ├── content-writer/
│       │   └── SKILL.md           ← Loaded by Content-Writer on trigger
│       └── logic-sanity-check/
│           └── SKILL.md           ← Loaded by QA-Validator on trigger
└── artifacts/
    ├── tasks.json                 ← Stage 1 output: Planner's task plan
    ├── output.json                ← Stage 2 output: Worker's completed results
    └── qa-report.json             ← Stage 3 output: QA audit with pass/fail
```

---

## How to Run It

### Stage 1 — Planner

Open Antigravity with the **Planner** agent active.

Send this prompt:
```
Plan this: Write a 3-section product overview for a B2B SaaS invoicing tool targeting freelancers.
```

The `task-planner` skill triggers. The Planner produces `artifacts/tasks.json` with 3 tasks, ordered by dependency.

**Expected output:** `artifacts/tasks.json` ✅

---

### Stage 2 — Content-Writer

Switch to the **Content-Writer** agent.

Send this prompt:
```
Execute tasks assigned to me from artifacts/tasks.json
```

The `content-writer` skill triggers. The agent reads `tasks.json`, respects the `depends_on` order, produces content for each task, self-validates against acceptance criteria, and writes `artifacts/output.json`.

**Expected output:** `artifacts/output.json` ✅

---

### Stage 3 — QA-Validator

Switch to the **QA-Validator** agent.

Send this prompt:
```
Run sanity check on artifacts/output.json against artifacts/tasks.json
```

The `logic-sanity-check` skill triggers. The QA agent evaluates each output against its acceptance criteria, assigns pass/fail verdicts per criterion, and writes `artifacts/qa-report.json`.

**Expected output:** `artifacts/qa-report.json` ✅

---

## Reading the Artifacts

### `tasks.json` — The Plan
Each task has an `id`, `assigned_to`, `depends_on` chain, and explicit `acceptance_criteria`. This is the contract between the Planner and every other agent.

### `output.json` — The Work
Each result includes the actual content plus a `self_check` block where the Worker declares which criteria it believes it met. This is the Worker's claim — not ground truth.

### `qa-report.json` — The Audit
The QA agent evaluates the Worker's claims independently. Criteria are verified one by one. `human_review_required` is always `true` — the QA agent flags, but a human decides.

---

## Key Design Decisions

| Decision | Reason |
|---|---|
| Agents read/write structured JSON, not free text | Enables deterministic handoffs and machine-readable auditing |
| `depends_on` is declared in the plan, not hardcoded | Planner controls sequencing without agents needing to know each other |
| Worker includes `self_check` | Makes the Worker's assumptions explicit and easier for QA to evaluate |
| QA always sets `human_review_required: true` | The loop is advisory. Humans remain the final decision-maker |
| Agent permissions are `read_only` for QA | QA can never corrupt outputs, even accidentally |

---

## What to Try Next

- Change the goal and rerun Stage 1 to see the Planner adapt the task list
- Deliberately introduce a flaw in `output.json` and rerun Stage 3 to see a `"fail"` verdict
- Add a fourth task to `tasks.json` assigned to a new specialist agent
- Extend `logic-sanity-check` with a word-count verification step using a terminal call
