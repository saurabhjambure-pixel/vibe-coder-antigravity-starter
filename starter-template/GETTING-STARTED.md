# Getting Started with the Starter Template

This guide gets you from zero to a working Planner → Data → Validator loop in Antigravity IDE.

**Time to first result: ~5 minutes.**

---

## Step 1 — Copy the template into your project

Copy the entire `starter-template/` folder into your Antigravity project. The key part is the `.agents/` directory — Antigravity reads it automatically.

Your project should look like this afterward:

```
your-project/
├── .agents/
│   ├── agents/
│   │   ├── Planner.yaml
│   │   ├── Data.yaml
│   │   └── Validator.yaml
│   └── skills/
│       ├── task-planner/SKILL.md
│       ├── data-agent/SKILL.md
│       └── qa-reviewer/SKILL.md
└── artifacts/          ← outputs land here (created automatically)
```

> The `artifacts/` folder will be created by agents when they write outputs. You don't need to create it.

---

## Step 2 — Open Antigravity, select the Planner agent

In the Antigravity IDE side panel, you should see three agents: **Planner**, **Data**, and **Validator**.

Select **Planner**.

---

## Step 3 — Give the Planner a goal

Type something like:

```
Plan this: I need to research competitors in the project management tool space and write a comparison summary.
```

The `task-planner` skill triggers. The Planner will break your goal into 3–7 ordered tasks, assign each to an agent, and write `artifacts/tasks.json`.

Open `artifacts/tasks.json` to see the plan before moving on.

---

## Step 4 — Switch to the Data agent, run the tasks

Select the **Data** agent in the panel.

Send:
```
Collect and structure the inputs for the tasks assigned to me in artifacts/tasks.json
```

The `data-agent` skill triggers. The Data agent reads the plan, works through its assigned tasks, and writes `artifacts/data.json`.

---

## Step 5 — Switch to the Validator, run QA

Select the **Validator** agent.

Send:
```
Review artifacts/data.json against the acceptance criteria in artifacts/tasks.json
```

The `qa-reviewer` skill triggers. The Validator checks every output against its acceptance criteria and tells you what passed, what failed, and what needs fixing.

---

## What you just built

```
Your goal
   ↓ (Planner)
artifacts/tasks.json    ← ordered task plan with owners
   ↓ (Data)
artifacts/data.json     ← structured work product
   ↓ (Validator)
QA report               ← pass/fail per criterion
```

Each agent only does its job. Outputs are structured so the next agent can read them without guessing.

---

## Next steps

**Customize for your use case:**
- Edit `.agents/agents/Planner.yaml` to change what the Planner focuses on
- Edit `.agents/skills/task-planner/SKILL.md` to change how tasks are structured
- Add a new skill: `python scaffold.py --name my-skill --type skill` from the repo root

**Try variations:**
- Give the Planner a completely different goal and rerun the loop
- Ask the Validator to fail something intentionally: edit `artifacts/data.json`, remove a field, and re-run the Validator
- Add a fourth task directly in `artifacts/tasks.json` and see if the Data agent picks it up

**Go deeper:**
- [`CHEATSHEET.md`](../CHEATSHEET.md) — all trigger phrases and prompt patterns
- [`docs/architecture-guide.md`](../docs/architecture-guide.md) — the full mental model
- [`examples/example-planner-qa/`](../examples/example-planner-qa/README.md) — a more complex end-to-end demo

---

## Common issues

**"The agent ignored my prompt"**
Rephrase using the trigger language from the SKILL.md file. Antigravity matches semantically — the closer your prompt matches the skill's `description`, the more reliably it triggers.

**"The output was free-form text, not JSON"**
The skill instructions specify the output format. If you've customized a skill and removed the output format section, add it back. Structured output requires explicit instructions.

**"I don't see the agents in the panel"**
Make sure `.agents/` is at the root of your Antigravity project, not inside a subfolder. The path should be `<project-root>/.agents/agents/*.yaml`.

**"I want to start over"**
Delete the `artifacts/` folder and re-run from Step 3. The agents will regenerate all outputs from scratch.
