# 🌌 Awesome Antigravity Skills & Agent Architecture

> For new vibe coders who want to move from prompting AI to engineering structured multi-agent systems in Google Antigravity.

Antigravity is not a chat interface.
It is an orchestration platform built around modular skills and controlled agents.

If you treat it like autocomplete, your system will eventually collapse under complexity.

This repository teaches you how to design:

* Modular **Skills**
* Specialized **Agents**
* Multi-agent orchestration workflows
* Deterministic validation loops
* Safe permission models

---

## ✨ What This Repo Provides

* Production-ready skill templates
* Agent configuration patterns
* Architecture design principles
* Orchestration workflows (PDCA model)
* A forkable starter template

This is built for developers who want structure, auditability, and reliability — not chaos prompting.

---

## 🧠 Core Philosophy

Instead of writing bigger prompts:

* **Skills define capability**
* **Agents define responsibility**
* **Orchestration defines reliability**

AI systems should be structured, auditable, and deterministic.

---

## 🛠️ The Mechanics at a Glance

Antigravity orchestration relies on two simple, deterministic file structures: **Skills** and **Agents**.

### 1. The Skill Template (`SKILL.md`)
Skills live in `.agent/skills/`. The YAML frontmatter acts as the API endpoint for the LLM, ensuring it only loads the full instructions when a trigger is hit.

```markdown
---
name: financial-data-parser
description: Extracts, sanitizes, and structures financial spreadsheets into clean JSON.
triggers:
  - "parse financial data"
  - "analyze runway"
  - "read spreadsheet"
---

# Instructions
1. Locate the target `.csv` or `.xlsx` file in the workspace.
2. Run the included Python script in `/scripts/sanitize.py` to strip empty rows.
3. Validate the extracted data against the schema in `/assets/schema.json`.
4. Generate a verifiable Artifact containing the final JSON.

# Guardrails
Never infer missing financial data. If a cell is empty, flag it in the validation artifact.

```

### 2. The Agent Template (`agent.yaml`)

Agents live in `.agent/agents/`. You define their role, lock in their skills, and tightly restrict their system permissions.

```yaml
name: Founder-Metrics-Analyst
role: "Senior Financial Analyst"
description: "Specializes in parsing SaaS metrics, calculating runway, and building data artifacts."
auto_load_skills:
  - financial-data-parser
  - confidence-scorer
permissions:
  browser: false
  terminal: true
  file_system: read_only

```

---

## 📂 Repository Structure

```text
awesome-antigravity-skills/
│
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── docs/
│   ├── architecture-guide.md
│   └── orchestration-patterns.md
│
├── examples/
│   ├── skill-templates/
│   └── agent-templates/
│
└── starter-template/
    └── .agent/
        ├── skills/
        └── agents/

```

---

## 🚀 Getting Started

### Quick Start (Frictionless Scaffold)

Run this script in your project root to instantly scaffold the Antigravity architecture and generate your first QA agent and validation skill:

```bash
mkdir -p .agent/skills/logic-sanity-check .agent/agents

cat <<EOF > .agent/agents/QA-Validator.yaml
name: QA-Validator
role: "Quality Assurance Lead"
description: "Verifies the outputs of other agents before human review."
auto_load_skills:
  - logic-sanity-check
permissions:
  browser: true
  terminal: false
  file_system: read_only
EOF

cat <<EOF > .agent/skills/logic-sanity-check/SKILL.md
---
name: logic-sanity-check
description: Verifies calculations and data integrity before final output.
triggers:
  - "run sanity check"
  - "validate output"
---

# Instructions
1. Review the generated Artifact.
2. Recalculate any mathematical formulas independently.
3. Output a Pass/Fail status with a list of any discrepancies.
EOF

echo "✅ Architecture scaffolded successfully in .agent/"

```

### Next Steps

1. Read `docs/architecture-guide.md`
2. Review `docs/orchestration-patterns.md`
3. Explore `examples/skill-templates/`
4. Explore `examples/agent-templates/`
5. Fork `starter-template/`
6. Build your first Planner → QA loop

Start small. Add structure before adding intelligence.

---

## 🧰 Included Skill Categories

### Data & Validation

* financial-data-parser
* logic-sanity-check
* anomaly-detector
* api-schema-validator
* **confidence-scorer** *(Ensures citations and validation scores)*

### Retrieval & Context

* rag-knowledge-retrieval
* prompt-compression-engine

### Testing & Governance

* regression-test-runner
* artifact-verifier
* feature-flag-tester

### Automation & Infrastructure

* browser-ui-verifier
* dependency-auditor
* performance-profiler
* migration-risk-analyzer
* decision-explainer

All skills are designed to:

* Be modular
* Use clear trigger phrases
* Produce structured artifacts
* Enforce guardrails

---

## 🔄 Recommended Orchestration Pattern (PDCA)

**Plan**
Planner agent breaks high-level goals into atomic tasks.

**Do**
Specialist agents execute tasks independently.

**Check**
QA agent validates outputs using structured validation skills.

**Act**
Human reviews artifacts before merge or deployment.

This loop prevents silent failure and builds system trust.

---

## ⚠ Common Mistakes to Avoid

* Creating one mega-agent with full permissions
* Writing vague skill triggers
* Allowing free-form output without artifacts
* Mixing multiple responsibilities inside one skill
* Skipping validation loops

AI systems fail quietly. Structure prevents silent failure.

---

## 🧭 Who This Is For

* Developers exploring Antigravity
* AI engineers designing orchestration systems
* Builders creating logic-heavy assistants
* Teams that need auditability and guardrails

If you just want better autocomplete, this isn’t for you.

If you want architecture-level control, welcome.

---

## 🤝 Contributing

Contributions are welcome.

To add a skill:

1. Create a new directory under `examples/skill-templates/`
2. Add a structured `SKILL.md`
3. Keep scope narrow and deterministic
4. Include guardrails and structured outputs

To add an agent:

* Define a narrow role
* Restrict permissions
* Avoid overlap with existing agents

See `CONTRIBUTING.md` for details.

---

## 📜 License

MIT License.

---

## ⭐ Final Thought

AI engineering is shifting from:

> “How do I prompt better?”

to:

> “How do I design systems that don’t break?”

Skills give capability.
Agents give specialization.
Orchestration gives reliability.

If this repository helps you, consider starring ⭐ and contributing back.

```
