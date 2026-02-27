#!/bin/bash
# init.sh - Scaffolds the Antigravity Agent directory structure

echo "🚀 Initializing Antigravity Agent Architecture..."

# Create core directories
mkdir -p .agent/skills/logic-sanity-check
mkdir -p .agent/agents

# Create a sample Agent persona
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

# Create a sample Skill
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
echo "Next step: Add your custom logic to the generated templates."
