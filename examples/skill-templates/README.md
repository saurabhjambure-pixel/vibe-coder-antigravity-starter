# Skill Templates

Skills are modular capabilities.

A skill teaches an agent how to perform one repeatable task reliably.

Good skills improve determinism.
Bad skills increase ambiguity.

This document defines how to design skills that are production-safe, modular, and verifiable.

---

# 🧠 Skill Design Principles

Before creating a skill, ask:

1. Does this skill perform exactly one responsibility?
2. Is the output structured and verifiable?
3. Are the triggers precise and unambiguous?
4. Does it include validation guardrails?

If not, the skill is too broad.

---

# 📦 Standard SKILL.md Structure

Every skill must contain:

- YAML frontmatter
- Clear trigger phrases
- Deterministic instructions
- Explicit guardrails
- Structured output expectations

---

## Base Template

```markdown
---
name: skill-name
description: Clear, specific capability description.
triggers:
  - "explicit trigger phrase"
  - "secondary explicit phrase"
---

# Instructions

1. Perform deterministic action.
2. Validate input.
3. Execute logic.
4. Produce structured artifact.

# Guardrails

- Do not assume missing values.
- Validate schema before output.
- Fail explicitly on invalid input.

# Output Format

Provide output in structured JSON format:
{
  "status": "success | failure",
  "data": {},
  "validation_summary": {}
}
````

---

# 🎯 Trigger Design Guidelines

Triggers control progressive disclosure.

They must be:

* Explicit
* Context-aware
* Narrow in meaning

Good example:

* "parse financial data"
* "validate API schema"
* "run regression tests"

Bad example:

* "analyze"
* "check data"
* "fix issue"

If triggers are vague:

* Skills misfire
* Or fail to activate

Be intentional.

---

# 🧩 Skill Categories & Reference Templates

Below are recommended categories and patterns.

---

# 1️⃣ Data Processing Skills

Used for structured data extraction and transformation.

### Example: financial-data-parser

Responsibility:

* Extract CSV/XLSX
* Sanitize rows
* Validate schema
* Output JSON

Output:

* Structured dataset
* Validation report

Never:

* Guess missing values
* Perform business decisions

---

# 2️⃣ Validation & Guardrail Skills

Used to prevent silent failure.

### Example: logic-sanity-check

Responsibility:

* Validate computed metrics
* Check bounds
* Detect anomalies

Output:

* Pass/Fail status
* Structured error explanation

These skills increase trust.

---

# 3️⃣ Retrieval Skills (RAG)

Used for controlled information retrieval.

### Example: rag-knowledge-retrieval

Responsibility:

* Query vector database
* Rank top-K results
* Return structured references

Output:

* Ranked document list
* Relevance score
* Source metadata

Never:

* Summarize unless explicitly required
* Modify retrieved content

---

# 4️⃣ Testing Skills

Used by QA agents.

### Example: regression-test-runner

Responsibility:

* Execute test suite
* Collect failures
* Produce structured test log

Output:

* Test results JSON
* Error breakdown

Testing skills should not modify system state.

---

# 5️⃣ Automation Skills

Used for UI and system verification.

### Example: browser-ui-verifier

Responsibility:

* Navigate UI flow
* Capture screenshots
* Verify state

Output:

* Screenshot artifacts
* Navigation log
* Pass/Fail summary

Automation skills must be step-by-step deterministic.

---

# 🔒 Guardrail Design Rules

Every skill should include:

* Input validation
* Output schema definition
* Explicit failure conditions
* No silent fallback logic

Avoid:

* Implicit assumptions
* Auto-correction without logging
* Hidden state changes

---

# 🚫 Anti-Patterns

## ❌ Mega Skills

One skill doing:

* Parsing
* Decision logic
* Reporting
* Validation

Split responsibilities aggressively.

---

## ❌ Vague Output

Returning only reasoning text.

Always require structured artifacts.

---

## ❌ Overlapping Responsibilities

Two skills performing similar logic.

This creates:

* Confusion
* Trigger collisions
* Debugging difficulty

---

# 🧪 Deterministic Skill Checklist

Before submitting a skill, confirm:

* It has clear YAML frontmatter
* Triggers are explicit
* Instructions are step-by-step
* Output format is defined
* Validation rules exist
* Scope is narrow

If any item fails, refine before submission.

---

# 📐 Mental Model

Skills are not prompts.

Skills are modular execution units.

The goal is not creativity.

The goal is reliability and clarity.

When skills are well-designed:

* Agents become predictable
* Orchestration becomes clean
* Systems scale safely
