# Agent Templates

Agents are not prompts.

Agents are controlled execution units with:

- A narrow role
- Defined skill access
- Restricted permissions
- Structured output expectations

Good agent design increases reliability.
Bad agent design creates chaos.

This document provides reference templates and design rules.

---

# 🧠 Agent Design Principles

Before creating an agent, ask:

1. What single responsibility does this agent own?
2. What skills does it actually need?
3. What permissions are absolutely necessary?
4. What artifact should it produce?

If you cannot answer these clearly, the agent is too broad.

---

# 1️⃣ Planner Agent

The Planner does not execute logic.

It decomposes goals into atomic tasks.

## Use When

- Goal is complex
- Multiple domains are involved
- Validation loop is required

## Template

```yaml
name: Planner-Agent
role: Systems Planner
description: Breaks high-level goals into atomic, structured tasks.
auto_load_skills: []
permissions:
  browser: false
  terminal: false
  file_system: read_only
````

## Output Expectation

* Structured execution plan (JSON)
* Delegation map
* Task breakdown artifact

Never allow the Planner to execute business logic.

---

# 2️⃣ Data Analyst Agent

Processes structured datasets.

## Use When

* CSV / XLSX parsing
* Metric calculations
* Structured validation

## Template

```yaml
name: DataAnalyst-Agent
role: Structured Data Processor
description: Validates and structures datasets using deterministic skills.
auto_load_skills:
  - financial-data-parser
  - logic-sanity-check
permissions:
  browser: false
  terminal: true
  file_system: read_only
```

## Output Expectation

* Structured JSON
* Validation log
* Schema verification artifact

---

# 3️⃣ QA Agent

The QA agent is intentionally skeptical.

Its job is to challenge outputs.

## Use When

* Validation is critical
* Safety matters
* Deployment risk exists

## Template

```yaml
name: QA-Agent
role: Quality Assurance Engineer
description: Validates outputs using structured validation and testing skills.
auto_load_skills:
  - regression-test-runner
  - artifact-verifier
permissions:
  browser: true
  terminal: true
  file_system: read_only
```

## Output Expectation

* Validation report
* Pass/Fail result
* Error summary artifact

QA should never generate new features.

It only validates.

---

# 4️⃣ Browser Automation Agent

Handles UI verification and interaction.

## Use When

* UI needs verification
* Flow validation required
* Screenshot capture needed

## Template

```yaml
name: BrowserAutomation-Agent
role: UI Verification Specialist
description: Navigates UI flows and verifies state via browser automation skills.
auto_load_skills:
  - browser-ui-verifier
permissions:
  browser: true
  terminal: false
  file_system: read_only
```

## Output Expectation

* Screenshots
* Navigation logs
* Verification summary

---

# 5️⃣ Orchestrator Agent

Coordinates agents but avoids deep execution.

## Use When

* Multi-agent coordination required
* Aggregating artifacts
* Generating synthesis reports

## Template

```yaml
name: Orchestrator-Agent
role: Multi-Agent Coordinator
description: Delegates tasks and compiles final structured reports.
auto_load_skills: []
permissions:
  browser: false
  terminal: false
  file_system: read_only
```

## Output Expectation

* Consolidated report
* Agent output references
* Summary artifact

---

# 🚫 Anti-Patterns

## The God Agent

An agent with:

* 10+ skills
* Full permissions
* Vague role
* Mixed responsibilities

This reduces determinism and increases hallucination risk.

---

## Overlapping Agents

Two agents performing the same responsibility.

This creates:

* Role confusion
* Delegation ambiguity
* Debugging complexity

---

## Permission Sprawl

Giving all agents:

* Browser access
* Terminal access
* Full filesystem access

Restrict aggressively.

---

# 📐 Agent Permission Strategy

Follow least privilege:

Planner → read_only
Data Agent → terminal + read_only
QA Agent → browser + terminal + read_only
Orchestrator → read_only

Never grant permissions “just in case.”

---

# 🧩 Choosing the Right Agent Pattern

Use multi-agent systems when:

* Task spans domains
* Validation loop required
* External tools are involved
* Auditability matters

Use single-agent execution when:

* Task is simple
* No tool interaction
* No validation layer needed

Avoid unnecessary complexity.

---

# Final Principle

Agents are not about intelligence.

They are about responsibility boundaries.

Clear responsibility boundaries create reliable systems.
