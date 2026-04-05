# 🗺 Antigravity Vibe Coder Cheatsheet

One-page reference. Everything you need to work with this repo in Antigravity IDE.

---

## 🤖 The Three Agents (starter-template)

| Agent | Role | Say this to activate |
|---|---|---|
| **Planner** | Breaks your goal into ordered tasks | `Plan this: <your goal>` |
| **Data** | Gathers, structures, or synthesizes inputs | `Collect and structure inputs for <topic>` |
| **Validator** | Checks outputs against acceptance criteria | `Review <artifact> against <criteria or plan>` |

> Switch agents in the Antigravity side panel. Each agent only loads the skills it needs.

---

## 🛠 Skills & Their Trigger Phrases

### `task-planner` (loaded by Planner)

| Say this | What happens |
|---|---|
| `Plan this: <goal>` | Breaks goal into 3–7 tasks with owners + artifacts |
| `Create a task plan for <goal>` | Same; more explicit phrasing |
| `What steps do we need to <goal>?` | Same trigger, conversational phrasing |

**Output:** `artifacts/tasks.json`

---

### `data-agent` (loaded by Data)

| Say this | What happens |
|---|---|
| `Collect inputs for the tasks in artifacts/tasks.json` | Gathers structured data needed for each task |
| `Structure the data from <source>` | Normalizes raw input into a clean artifact |
| `Synthesize information about <topic>` | Researches and structures content |

**Output:** `artifacts/data.json`

---

### `qa-reviewer` (loaded by Validator)

| Say this | What happens |
|---|---|
| `Review artifacts/data.json against artifacts/tasks.json` | Full pass/fail audit per acceptance criterion |
| `Validate the output at <path>` | Checks structure, completeness, schema compliance |
| `Run sanity check on <artifact>` | Quick logical consistency check |

**Output:** A pass/fail report with blocking issues listed

---

## 🔄 The Standard Loop

```
1. Planner  → "Plan this: <goal>"           → artifacts/tasks.json
2. Data     → "Collect inputs from tasks"   → artifacts/data.json
3. Validator → "Review data against tasks"  → QA report
```

Repeat from step 1 if QA fails. The Planner refines the plan.

---

## 💡 Prompt Patterns That Work Well

| Goal | What to say |
|---|---|
| Kick off any project | `Plan this: <describe your goal in 1-2 sentences>` |
| Get structured data | `Collect and structure inputs for task <id> from artifacts/tasks.json` |
| Validate a file | `Review artifacts/<file> against the acceptance criteria in artifacts/tasks.json` |
| Debug a failed task | `Why did task <id> fail? What's the minimal fix?` |
| Add a new skill | `python scaffold.py --name <skill-name> --type skill` (in terminal) |
| See your agents | Look in `.agents/agents/` — one YAML per agent |
| See your skills | Look in `.agents/skills/<name>/SKILL.md` |

---

## 📁 Key Files

```
starter-template/
├── .agents/
│   ├── agents/
│   │   ├── Planner.yaml      ← role + skills + permissions for Planner
│   │   ├── Data.yaml         ← role + skills + permissions for Data agent
│   │   └── Validator.yaml    ← role + skills + permissions for QA
│   └── skills/
│       ├── task-planner/SKILL.md      ← what Planner does + guardrails
│       ├── data-agent/SKILL.md        ← what Data agent does + guardrails
│       └── qa-reviewer/SKILL.md       ← what Validator does + guardrails
artifacts/                    ← structured outputs land here
```

---

## ✅ Does / ❌ Doesn't

| ✅ This repo helps you | ❌ This repo won't |
|---|---|
| Structure agents with clear roles | Replace official Antigravity docs |
| Write skills that trigger reliably | Work as a production framework |
| Build auditable handoffs between agents | Handle deployment or hosting |
| Avoid the "god agent" trap | Auto-configure your IDE |

---

## 🆘 Troubleshooting

**Skill isn't triggering?**
→ Check the `description` field in `SKILL.md` — it must clearly describe what the skill does. Antigravity uses semantic matching, not keywords.

**Agents doing too much?**
→ Check permissions in `agents/*.yaml` — restrict terminal/browser/filesystem to what's actually needed.

**Outputs are just free-form text?**
→ Add explicit output format instructions to the skill's `## Instructions` section.

**Not sure which agent to use?**
→ Use the [Skill Selection Decision Aid](docs/architecture-guide.md#skill-selection-decision-aid) in the architecture guide.

---

> Full walkthrough → [GETTING-STARTED.md](starter-template/GETTING-STARTED.md)  
> Deep dive → [docs/architecture-guide.md](docs/architecture-guide.md)
