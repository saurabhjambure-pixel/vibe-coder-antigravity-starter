# Skill Templates

Each skill must:

- Have clear YAML frontmatter
- Include explicit trigger phrases
- Be deterministic
- Produce structured artifacts

---

## Basic Template

```markdown
---
name: example-skill
description: Clear and specific capability description.
triggers:
  - "explicit trigger phrase"
---

# Instructions

1. Perform deterministic action.
2. Validate output.
3. Produce structured artifact.

# Guardrails

- Do not assume missing values.
- Always validate before output.
