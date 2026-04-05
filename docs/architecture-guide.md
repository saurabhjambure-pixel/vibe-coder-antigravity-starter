# Architecture Guide

> **In a hurry?** Jump to the [30-Second Mental Model](#-30-second-mental-model) below, then come back for the details.

Antigravity is not a chat interface.

It is an orchestration platform built around modular skills, controlled agents, and structured artifacts.

If you treat it like autocomplete, your system will become unpredictable as complexity increases.

This guide explains how to design multi-agent systems that are reliable, scalable, and auditable.

---

## ⚡ 30-Second Mental Model

If you read nothing else, read this:

| Concept | Think of it as | One-line rule |
|---|---|---|
| **Skill** | A function | Does exactly one thing; never two |
| **Agent** | A role / job title | Loads only the skills it needs for its job |
| **Artifact** | A structured handoff | JSON output that the next agent reads, not free text |
| **Orchestration** | The pipeline | Planner → Specialists → QA; each stage reads the previous artifact |

**The loop:**
```
1. Planner gets a goal → writes artifacts/tasks.json
2. Specialist reads tasks.json → does the work → writes artifacts/output.json
3. QA reads output.json vs tasks.json → writes pass/fail verdict
4. If failed → back to step 1 with refined goal
```

**The one anti-pattern to avoid:**  
One agent that does all of the above. That's a "god agent" — it works until it doesn't, and when it breaks, you can't tell why.

→ Ready for details? Read on. Want to just build? Start with [starter-template/GETTING-STARTED.md](../starter-template/GETTING-STARTED.md).

---

---

# 1️⃣ The Four Core Primitives

Every Antigravity system is built from four primitives:

## Skills

Skills = **Capabilities** (what can be done).

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

Agents = **Personas/Responsibilities** (who does it).

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

### Artifact Standards

A high-quality artifact is:
- **Status-tagged**: `[DRAFT]`, `[IN-REVIEW]`, or `[APPROVED]` in the header.
- **Structured**: JSON/YAML/CSV/Markdown with clear sections and schema notes.
- **Traceable**: Lists source inputs and assumptions; includes timestamps.
- **Actionable**: States next action or acceptance state; avoids vague prose.
- **Validatable**: Contains check results or schema that downstream agents/QA can verify.

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

# Skill Selection Decision Aid

| If input / need | Pick this Skill | Produces |
| --- | --- | --- |
| Raw CSV/JSON needs cleaning or shaping | Data-Cleaner | `artifacts/cleaned-data.json` |
| Broad, unstructured goal | Task-Planner | `artifacts/tasks.json` |
| Write content from given data/outline | Content-Writer | `artifacts/output.md` |
| Validate output against acceptance criteria | Logic-Sanity-Check (Validator) | `artifacts/qa-report.json` |
| Missing clarity on requirements | Planner clarification loop | Updated `artifacts/tasks.json` |

Rule of thumb: choose the most specific skill that yields a structured artifact the next agent can consume; if none match, escalate to Planner.

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

## Runtime Sandbox (new)

If you want the repo’s examples to actually enforce the above boundaries, load `antigravity.yaml` with the lightweight Python runtime in `runtime/`. It:
- Parses `execution_mode`, terminal allow/deny, filesystem allow/deny, and governance flags.
- Exposes helpers for command gating and path checks.
- Ships with pytest coverage in `tests/test_runtime` so you can extend rules safely.

Opt-in/out:
- **Use it** when you want reproducible guardrails for demos or teaching.
- **Skip it** if you’re only reading patterns—nothing else depends on it.

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

## 🏗 Architecture Overview

```mermaid
flowchart TD

    User[User / High-Level Goal]

    subgraph Orchestration Layer
        Planner[Planner-Agent]
        Orchestrator[Orchestrator-Agent]
    end

    subgraph Specialization Layer
        DataAgent[DataAnalyst-Agent]
        QAAgent[QA-Agent]
    end

    subgraph Capability Layer
        Skill1[financial-data-parser]
        Skill2[logic-sanity-check]
        Skill3[artifact-verifier]
    end

    subgraph Governance Layer
        Human[Human Review]
    end

    User --> Planner
    Planner --> Orchestrator
    Orchestrator --> DataAgent
    Orchestrator --> QAAgent

    DataAgent --> Skill1
    DataAgent --> Skill2
    QAAgent --> Skill2
    QAAgent --> Skill3

    DataAgent --> QAAgent
    QAAgent --> Human
