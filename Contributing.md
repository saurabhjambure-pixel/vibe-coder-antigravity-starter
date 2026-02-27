# Contributing to Awesome Antigravity Skills & Agent Architecture

Thank you for your interest in contributing.

This repository is focused on building structured, deterministic, and reliable multi-agent systems inside Google Antigravity.

We prioritize clarity, modularity, and architectural integrity over volume.

Please read this guide before submitting a pull request.

---

# 🎯 Contribution Philosophy

We are not collecting random prompts.

We are building a reference architecture library.

Every contribution must:

- Be modular
- Be deterministic
- Produce structured artifacts
- Include guardrails
- Respect separation of concerns

Low-quality, vague, or overly broad submissions will not be merged.

---

# 🧰 Contributing a Skill

To contribute a new skill:

1. Create a new directory under:

   examples/skill-templates/<skill-name>/

2. Add a `SKILL.md` file.

3. Follow this structure:

```markdown
---
name: skill-name
description: Clear, specific capability description.
triggers:
  - "explicit trigger phrase"
---

# Instructions

1. Deterministic step.
2. Deterministic step.
3. Produce structured artifact.

# Guardrails

- Validation rules
- Output format definition
- Failure handling logic
````

---

## Skill Requirements

A valid skill must:

* Do exactly one responsibility
* Use precise, unambiguous trigger phrases
* Produce structured output (JSON, logs, report, etc.)
* Include validation logic
* Avoid free-form reasoning as final output

Do not submit:

* Multi-purpose “mega skills”
* Vague or conceptual skills
* Skills without output structure
* Skills that depend on hidden assumptions

---

# 🤖 Contributing an Agent Template

To contribute an agent:

1. Add a YAML file under:

   examples/agent-templates/

2. Follow this format:

```yaml
name: Agent-Name
role: Narrow, specific role
description: Clear responsibility statement
auto_load_skills:
  - relevant-skill-name
permissions:
  browser: false
  terminal: false
  file_system: read_only
```

---

## Agent Requirements

A valid agent must:

* Have a narrow, clearly defined role
* Load minimal required skills
* Restrict permissions intentionally
* Avoid overlapping responsibilities with existing agents

Do not submit:

* “God agents” with many skills
* Fully unrestricted agents
* Agents with vague role descriptions

---

# 🏗 Contributing Documentation

Documentation improvements are welcome.

When contributing to docs:

* Improve clarity, not verbosity
* Add structure where needed
* Avoid hype language
* Keep tone technical and practical

---

# 🧪 Validation Standards

All contributions must:

* Be logically consistent
* Follow deterministic design principles
* Align with the layered architecture model
* Support artifact-first workflows

If a contribution increases ambiguity or reduces determinism, it will not be accepted.

---

# 🚀 Pull Request Process

1. Fork the repository
2. Create a feature branch
3. Commit your changes clearly
4. Submit a pull request with:

   * What problem this solves
   * Why it fits the architecture philosophy
   * Example use case

Pull requests may receive feedback before merging.

---

# ⚠ What This Repository Is Not

This is not:

* A collection of random prompt tricks
* A marketing repository
* A dumping ground for experimental ideas
* A playground for unstructured AI experiments

This is a structured architecture resource.

---

# 📐 Design Principles Reminder

Before submitting, ask:

* Does this increase clarity?
* Does this preserve modularity?
* Does this improve determinism?
* Does this strengthen validation?

If yes — contribute.

If not — refine it first.

---

# 🤝 Code of Conduct

Be respectful.
Be constructive.
Be precise.

We value thoughtful system design over volume.

---

# Final Thought

AI systems scale through structure.

Help us keep this repository focused, disciplined, and architecturally sound.
