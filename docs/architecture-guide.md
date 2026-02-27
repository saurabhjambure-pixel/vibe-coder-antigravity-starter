# Architecture Guide

Antigravity is an orchestration platform built around modular capabilities and controlled agents.

This guide explains how to design systems that scale without becoming unstable.

---

# 1️⃣ The Four Core Primitives

## Skills

Modular, isolated capabilities.

A skill should:
- Do one thing only
- Be deterministic
- Produce structured output
- Include validation guardrails

Bad design:
- Multi-purpose skills
- Vague reasoning instructions
- No structured output

---

## Agents

Specialized personas with limited permissions.

Agents should:
- Have narrow roles
- Load minimal skills
- Avoid overlapping responsibilities
- Operate within restricted tool access

Unrestricted agents become unpredictable.

---

## Artifacts

Structured, verifiable outputs.

Examples:
- JSON
- Logs
- Execution plans
- Screenshots
- Validation reports

Artifacts create auditability and trust.

---

## Orchestration

Complex tasks should not be handled by one agent.

Use structured delegation:

Planner → Specialists → QA → Human

---

# 2️⃣ Progressive Disclosure

Antigravity loads skill metadata first.

Only when a trigger matches does it load full instructions.

This:
- Preserves context window
- Reduces token waste
- Improves reasoning focus

Triggers must be precise and unambiguous.

---

# 3️⃣ Layered Architecture Model

Layer 1 — Skills  
Layer 2 — Agents  
Layer 3 — Orchestration  
Layer 4 — Governance (QA + Human)

Each layer must exist.

---

# 4️⃣ Deterministic Design Principles

- Validate inputs
- Validate outputs
- Always produce artifacts
- Separate reasoning from execution
- Restrict permissions aggressively

---

# 5️⃣ Anti-Patterns

## The God Agent
One agent with many skills and full permissions.

Results:
- Context overload
- Tool misuse
- Debugging difficulty

## Skill Bloat
Large skills handling multiple responsibilities.

Split aggressively.

---

# 6️⃣ When Multi-Agent Design Makes Sense

Use it when:
- Tasks involve multiple domains
- Validation is critical
- Tools must be used
- Auditability is required

Avoid it for trivial tasks.

---

# Final Principle

Design for clarity and reliability, not cleverness.
