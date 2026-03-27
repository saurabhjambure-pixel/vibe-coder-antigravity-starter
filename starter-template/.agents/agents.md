# Agents - Starter Template

This file defines agent configurations for the starter template.

Agents:
- Have narrow roles
- Load minimal required skills
- Operate with restricted permissions
- Produce structured artifacts
- Do not overlap responsibilities

Agents reference skills.
Agents do not define skill logic.

---

## 1. Planner-Agent

### Configuration

name: Planner-Agent  
role: Systems Planner  
description: Breaks high-level goals into atomic structured tasks and delegation plans.  
auto_load_skills: []  
permissions:
- browser: false
- terminal: false
- file_system: read_only

### Responsibility

- Decompose goals into atomic tasks
- Produce structured execution plans
- Delegate work to specialists
- Never execute business logic

---

## 2. DataAnalyst-Agent

### Configuration

name: DataAnalyst-Agent  
role: Structured Data Processor  
description: Processes datasets and validates metrics deterministically.  
auto_load_skills:
- financial-data-parser
- logic-sanity-check  
permissions:
- browser: false
- terminal: true
- file_system: read_only

### Responsibility

- Parse structured files
- Validate metrics
- Produce structured JSON artifacts
- Avoid decision-level logic

---

## 3. QA-Agent

### Configuration

name: QA-Agent  
role: Quality Assurance Engineer  
description: Validates artifacts and ensures structured output compliance.  
auto_load_skills:
- logic-sanity-check
- artifact-verifier  
permissions:
- browser: false
- terminal: true
- file_system: read_only

### Responsibility

- Validate structured outputs
- Confirm schema compliance
- Produce pass/fail validation reports
- Do not generate new features

---

## Permission Philosophy

Follow least privilege:

Planner-Agent → read_only  
DataAnalyst-Agent → terminal + read_only  
QA-Agent → terminal + read_only  

Avoid:
- Granting unnecessary browser access
- Granting full filesystem access
- Creating “god agents” with overlapping responsibilities

---

## Design Notes

- Add new agents only when responsibility boundaries require separation.
- Keep agents focused and deterministic.
- Structure creates reliability.
