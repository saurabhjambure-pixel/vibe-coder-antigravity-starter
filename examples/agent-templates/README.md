
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
