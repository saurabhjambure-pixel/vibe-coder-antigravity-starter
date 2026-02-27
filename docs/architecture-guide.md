# Architecture Guide

Antigravity is not a chat interface.

It is an orchestration platform built around modular skills, controlled agents, and structured artifacts.

If you treat it like autocomplete, your system will become unpredictable as complexity increases.

This guide explains how to design multi-agent systems that are reliable, scalable, and auditable.

---

# 1️⃣ The Four Core Primitives

Every Antigravity system is built from four primitives:

## Skills

Skills are modular capabilities.

A skill should:
- Perform exactly one responsibility
- Be deterministic
- Produce structured output
- Include validation guardrails

Good skill design:
- Narrow scope
- Clear triggers
- Strict output format
- Explicit validation steps

Bad skill design:
- Multiple responsibilities in one skill
- Vague reasoning instructions
- Free-form outputs
- No verification

---

## Agents

Agents are specialized workers that use skills.

An agent should:
- Have a narrow role
- Load only relevant skills
- Operate under restricted permissions
- Produce structured artifacts

Why restrict agents?

Unrestricted agents:
- Hallucinate tool usage
- Overreach responsibilities
- Become difficult to debug

Controlled agents:
- Are predictable
- Are testable
- Are safer

---

## Artifacts

Artifacts are structured, verifiable outputs.

Examples:
- JSON files
- Execution plans
- Validation logs
- Screenshots
- Structured reports

Artifacts create:
- Auditability
- Reproducibility
- Trust

Without artifacts, you only have reasoning.
With artifacts, you have evidence.

Always prefer structured outputs over free-form text.

---

## Orchestration

Orchestration is the coordination layer.

Complex goals should not be handled by one agent.

Instead, break work into roles:

Planner → Specialists → QA → Human review

This separation increases clarity and reliability.

---

# 2️⃣ Progressive Disclosure Model

Antigravity loads skill metadata first.

Only when a trigger matches does it load the full skill instructions.

This provides:
- Cleaner context windows
- Reduced token waste
- Improved reasoning focus
- Better determinism

Design implication:

Triggers must be:
- Specific
- Clear
- Unambiguous

If triggers are too vague:
- Skills misfire
- Or never fire

Be intentional.

---

# 3️⃣ Layered Architecture Model

Think in layers:

## Layer 1 — Capability Layer
Individual skills.

## Layer 2 — Specialization Layer
Agents assigned specific skills.

## Layer 3 — Coordination Layer
Planner agent delegates tasks.

## Layer 4 — Governance Layer
QA validation + human oversight.

If any layer is missing, reliability decreases.

---

# 4️⃣ Permission Architecture

Never give every agent:

- Full browser access
- Full terminal access
- Full filesystem access

Instead:

Planner → read_only  
Data Agent → terminal + read_only  
QA Agent → browser + read_only  
Orchestrator → minimal execution capability  

Restricting permissions:
- Improves determinism
- Reduces misuse
- Simplifies debugging

---

# 5️⃣ Deterministic Design Principles

If a system must be trusted:

- Always validate inputs
- Always validate outputs
- Always produce artifacts
- Never assume missing data
- Separate reasoning from execution

AI systems fail quietly.

Structure prevents silent failure.

---

# 6️⃣ Anti-Patterns to Avoid

## ❌ The God Agent

One massive agent with many skills and full permissions.

Results:
- Context overload
- Tool misuse
- Hard debugging
- Unpredictable behavior

---

## ❌ Skill Bloat

Large skills that attempt multiple responsibilities.

Split aggressively.

---

## ❌ Free-Form Output

Allowing reasoning without structured artifacts.

Always require structured outputs.

---

# Final Principle

Do not design for maximum intelligence.

Design for:
- Clarity
- Isolation
- Determinism
- Auditability

The strongest AI systems are not the most creative.

They are the most structured.
