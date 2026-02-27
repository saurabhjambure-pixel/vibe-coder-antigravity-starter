
# Agent Templates

Agents should be narrow, controlled, and deterministic.

---

## Planner Agent

```yaml
name: Planner-Agent
role: Systems Planner
description: Breaks goals into structured atomic tasks.
auto_load_skills: []
permissions:
  browser: false
  terminal: false
  file_system: read_only

name: DataAnalyst-Agent
role: Structured Data Processor
description: Validates and structures datasets.
auto_load_skills:
  - financial-data-parser
  - logic-sanity-check
permissions:
  browser: false
  terminal: true
  file_system: read_only

name: DataAnalyst-Agent
role: Structured Data Processor
description: Validates and structures datasets.
auto_load_skills:
  - financial-data-parser
  - logic-sanity-check
permissions:
  browser: false
  terminal: true
  file_system: read_only

name: QA-Agent
role: Quality Assurance Engineer
description: Validates outputs before approval.
auto_load_skills:
  - regression-test-runner
  - artifact-verifier
permissions:
  browser: true
  terminal: true
  file_system: read_only

