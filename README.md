
# 🌌 Awesome Antigravity Skills & Agent Patterns

> A structured starter reference for learning multi-agent workflows in Google Antigravity.

---

## ⚡ Try It Right Now (in Antigravity IDE)

Copy `starter-template/` into your project. Three agents appear in the panel — here’s what to say to each:

**With the Planner agent selected:**
```
Plan this: I need to analyze last month’s sales data and write a summary report.
```

**With the Data agent selected:**
```
Collect and structure the inputs from artifacts/tasks.json
```

**With the Validator agent selected:**
```
Review the output at artifacts/data.json against the tasks in artifacts/tasks.json
```

That’s the full loop. → **[Step-by-step setup guide](starter-template/GETTING-STARTED.md)** | **[All prompts & triggers](CHEATSHEET.md)**

---

## 🧠 The Idea in 30 Seconds

Most Antigravity pain comes from one source: too much responsibility in one place.

The fix:
* **Skills** = what can be done (modular, one job each)
* **Agents** = who does it (a role, not a chatbot)
* **Artifacts** = structured handoffs between agents (JSON, not vibes)

Once those are separate, experiments become predictable.

---

## 📂 What’s Inside

| Path | What it gives you |
|---|---|
| `starter-template/` | Copy-paste boilerplate — 3 agents, 3 skills, ready to fork |
| `CHEATSHEET.md` | One-page reference: all trigger phrases, agents, and prompt patterns |
| `examples/example-planner-qa/` | Full working demo: Planner → Writer → QA with real artifacts |
| `docs/architecture-guide.md` | The mental model behind all of this |
| `docs/orchestration-patterns.md` | PDCA, delegation, escalation — when to use each |
| `schema/` | JSON schemas + CLI validator for your skills/agents |
| `scaffold.py` | Interactive generator: `python scaffold.py --name my-skill --type skill` |

---

## 🚀 Get Started

**Option A — Just use the starter template (recommended for vibe coders)**

1. Copy `starter-template/` into your Antigravity project
2. Open `starter-template/GETTING-STARTED.md` — it walks you through the first 5 minutes
3. Start with the Planner agent and say `Plan this:` followed by any goal

**Option B — Run the demo locally first**

```bash
python3 examples/demo-run/run_demo.py   # generates sample artifacts
python3 -m pytest                       # runs tests
python3 schema/validate.py              # validates your skills/agents
```

Or: `make demo`, `make test`, `make validate`

**Option C — Read before you build**

Start with `docs/architecture-guide.md` for the full mental model.

---

## 🎯 Who This Is For

* PMs and builders learning to vibe code on Antigravity
* Anyone whose multi-agent setup keeps going sideways
* Teams who want auditable, structured agent outputs

Not for: production distributed systems architecture. This is intentionally a disciplined starting point.

---

## ⚠ What This Repo Is Not

* Not an official Antigravity framework
* Not a collection of prompt hacks
* Not a complete solution

It’s a structured way to think about agents while you learn.

---

## 🤝 Feedback Welcome

I’m still learning but being intentional about structure.

If you’re experimenting with multi-agent workflows, thoughtful feedback and improvements are genuinely appreciated.

---

## ⭐ Final Thought

AI systems don’t break because they aren’t smart enough.

They break because responsibilities aren’t clear.
