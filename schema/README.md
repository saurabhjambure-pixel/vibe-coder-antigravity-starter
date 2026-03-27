# schema/

Validation schemas and tooling for Antigravity skill and agent configs.

---

## Files

| File | Purpose |
|---|---|
| `skill.schema.json` | JSON Schema (Draft 7) for SKILL.md frontmatter |
| `agent.schema.json` | JSON Schema (Draft 7) for agent.yaml files |
| `validate.py` | CLI validator — runs both schemas against all files |
| `pre-commit-hook.sh` | Git hook — blocks commits with invalid configs |
| `ci-validate.yml` | GitHub Actions workflow — runs on every PR |

---

## Quick Start

**Install dependencies (once):**
```bash
pip install jsonschema pyyaml
```

**Validate everything:**
```bash
python schema/validate.py
```

**Validate with passing results shown:**
```bash
python schema/validate.py --verbose
```

**Validate skills only or agents only:**
```bash
python schema/validate.py --skills-only
python schema/validate.py --agents-only
```

**Install the pre-commit hook (run once from repo root):**
```bash
cp schema/pre-commit-hook.sh .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

**Set up CI (copy the workflow file):**
```bash
mkdir -p .github/workflows
cp schema/ci-validate.yml .github/workflows/validate.yml
```

---

## What Gets Validated

### SKILL.md frontmatter

| Field | Required | Rule |
|---|---|---|
| `name` | ✅ | kebab-case, 3–60 chars |
| `description` | ✅ | 40–500 chars — this is the semantic trigger |
| `triggers` | optional | community convention only, 1–10 items |
| `version` | optional | semver format (e.g. `1.0.0`) |
| `author` | optional | string, max 80 chars |
| `tags` | optional | array of kebab-case strings |

**Content-level checks (beyond schema):**
- Must have an `## Instructions` section
- Must have a `## Guardrails` section
- Description must not simply repeat the skill name
- Warns if `triggers:` is present (community extension, not official spec)

### agent.yaml

| Field | Required | Rule |
|---|---|---|
| `name` | ✅ | PascalCase or kebab-case, must match filename |
| `role` | ✅ | 5–100 chars |
| `description` | ✅ | 30–1000 chars |
| `auto_load_skills` | optional | array of existing skill names |
| `permissions` | optional | `browser`, `terminal` (bool), `file_system` (enum) |
| `input_artifact` | optional | relative path string |
| `output_artifact` | optional | relative path string |

**Content-level checks:**
- Warns if `auto_load_skills` references a skill that doesn't exist on disk
- Warns if `terminal: true` is combined with `file_system: read_only`

---

## Example Output

```
Skills (3 found)
✓ .agents/skills/logic-sanity-check/SKILL.md
✓ .agents/skills/task-planner/SKILL.md
✗ .agents/skills/content-writer/SKILL.md
  Field 'description': 'Write content' is too short (minimum 40 characters)
  ⚠ missing Guardrails section

Agents (3 found)
✓ .agents/agents/Planner.yaml
✓ .agents/agents/QA-Validator.yaml
✓ .agents/agents/Content-Writer.yaml
  ⚠ auto_load_skills references 'anomaly-detector' but .agents/skills/anomaly-detector/ does not exist

✗ 1 validation error(s) found
```

---

## Schema Spec Basis

Schemas are grounded in the official Antigravity documentation:
- Skills format: [antigravity.google/docs/skills](https://antigravity.google/docs/skills)
- Skills codelab: [codelabs.developers.google.com/getting-started-with-antigravity-skills](https://codelabs.developers.google.com/getting-started-with-antigravity-skills)

See `docs/antigravity-reference.md` for a full map of which conventions are official vs. community patterns.
