#!/usr/bin/env python3
"""
validate.py — Schema validator for Antigravity skill and agent configs.

Usage:
    python schema/validate.py                   # validate everything
    python schema/validate.py --skills-only     # skills only
    python schema/validate.py --agents-only     # agents only
    python schema/validate.py --verbose         # show passing checks too

Exit codes:
    0  — all validations passed
    1  — one or more validation errors found
"""

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import jsonschema
    import yaml
except ImportError:
    print("Missing dependencies. Run:")
    print("  pip install jsonschema pyyaml")
    sys.exit(1)


# ── Paths ────────────────────────────────────────────────────────────────────

REPO_ROOT = Path(__file__).parent.parent
SCHEMA_DIR = REPO_ROOT / "schema"
SKILLS_DIR = REPO_ROOT / ".agents" / "skills"
AGENTS_DIR = REPO_ROOT / ".agents" / "agents"

SKILL_SCHEMA_PATH = SCHEMA_DIR / "skill.schema.json"
AGENT_SCHEMA_PATH = SCHEMA_DIR / "agent.schema.json"


# ── ANSI colours ─────────────────────────────────────────────────────────────

GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
BOLD   = "\033[1m"
RESET  = "\033[0m"


# ── Helpers ───────────────────────────────────────────────────────────────────

def load_schema(path: Path) -> dict:
    with open(path) as f:
        return json.load(f)


def parse_skill_frontmatter(skill_md_path: Path) -> dict | None:
    """Extract and parse the YAML frontmatter from a SKILL.md file."""
    content = skill_md_path.read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return None
    return yaml.safe_load(match.group(1))


def validate_against_schema(data: dict, schema: dict, source: str) -> list[str]:
    """Return a list of human-readable error strings (empty = valid)."""
    validator = jsonschema.Draft7Validator(schema)
    errors = []
    for error in sorted(validator.iter_errors(data), key=lambda e: list(e.path)):
        field = " → ".join(str(p) for p in error.path) or "(root)"
        errors.append(f"  Field '{field}': {error.message}")
    return errors


def result_line(ok: bool, path: str, errors: list[str], verbose: bool) -> None:
    if ok:
        if verbose:
            print(f"{GREEN}✓{RESET} {path}")
    else:
        print(f"{RED}✗{RESET} {path}")
        for e in errors:
            print(f"  {YELLOW}{e}{RESET}")


# ── Content-level checks (beyond schema) ─────────────────────────────────────

def lint_skill_content(path: Path, frontmatter: dict) -> list[str]:
    """
    Additional content checks that JSON Schema can't express:
    - description must not just repeat the name
    - SKILL.md must have an Instructions section
    - SKILL.md must have a Guardrails section
    """
    warnings = []
    content = path.read_text(encoding="utf-8")

    name = frontmatter.get("name", "")
    description = frontmatter.get("description", "")
    if name and description.lower().strip().startswith(name.lower()):
        warnings.append("  ⚠ description starts with skill name — be more specific about when/why to use it")

    if "## Instructions" not in content and "# Instructions" not in content:
        warnings.append("  ⚠ missing Instructions section — add '## Instructions' with numbered steps")

    if "## Guardrails" not in content and "# Guardrails" not in content:
        warnings.append("  ⚠ missing Guardrails section — add '## Guardrails' with explicit constraints")

    if "triggers:" in content:
        warnings.append(
            "  ℹ 'triggers:' found — this is a community convention, not the official spec. "
            "Antigravity triggers on 'description' semantically. See docs/antigravity-reference.md"
        )

    return warnings


def lint_agent_content(path: Path, data: dict) -> list[str]:
    warnings = []

    if "auto_load_skills" in data:
        # Check each referenced skill actually exists
        for skill_name in data["auto_load_skills"]:
            skill_path = SKILLS_DIR / skill_name
            if not skill_path.exists():
                warnings.append(
                    f"  ⚠ auto_load_skills references '{skill_name}' "
                    f"but .agents/skills/{skill_name}/ does not exist"
                )

    perms = data.get("permissions", {})
    if perms.get("terminal") is True and perms.get("file_system") == "read_only":
        warnings.append(
            "  ⚠ terminal=true with file_system=read_only may conflict — "
            "terminal commands often write to disk"
        )

    return warnings


# ── Validators ────────────────────────────────────────────────────────────────

def validate_skills(schema: dict, verbose: bool) -> int:
    """Return count of failures."""
    failures = 0

    skill_files = list(SKILLS_DIR.glob("*/SKILL.md")) if SKILLS_DIR.exists() else []
    if not skill_files:
        print(f"{YELLOW}No SKILL.md files found under {SKILLS_DIR}{RESET}")
        return 0

    print(f"\n{BOLD}Skills ({len(skill_files)} found){RESET}")

    for skill_path in sorted(skill_files):
        rel = skill_path.relative_to(REPO_ROOT)
        frontmatter = parse_skill_frontmatter(skill_path)

        if frontmatter is None:
            print(f"{RED}✗{RESET} {rel}  — no YAML frontmatter found (must be wrapped in --- delimiters)")
            failures += 1
            continue

        errors = validate_against_schema(frontmatter, schema, str(rel))
        warnings = lint_skill_content(skill_path, frontmatter)

        ok = len(errors) == 0
        if not ok:
            failures += 1

        result_line(ok, str(rel), errors, verbose)

        for w in warnings:
            print(f"  {YELLOW}{w}{RESET}")

    return failures


def validate_agents(schema: dict, verbose: bool) -> int:
    """Return count of failures."""
    failures = 0

    agent_files = list(AGENTS_DIR.glob("*.yaml")) if AGENTS_DIR.exists() else []
    if not agent_files:
        print(f"{YELLOW}No agent .yaml files found under {AGENTS_DIR}{RESET}")
        return 0

    print(f"\n{BOLD}Agents ({len(agent_files)} found){RESET}")

    for agent_path in sorted(agent_files):
        rel = agent_path.relative_to(REPO_ROOT)

        try:
            with open(agent_path) as f:
                data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(f"{RED}✗{RESET} {rel}  — YAML parse error: {e}")
            failures += 1
            continue

        if not isinstance(data, dict):
            print(f"{RED}✗{RESET} {rel}  — file must be a YAML mapping (got {type(data).__name__})")
            failures += 1
            continue

        errors = validate_against_schema(data, schema, str(rel))
        warnings = lint_agent_content(agent_path, data)

        ok = len(errors) == 0
        if not ok:
            failures += 1

        result_line(ok, str(rel), errors, verbose)

        for w in warnings:
            print(f"  {YELLOW}{w}{RESET}")

    return failures


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Validate Antigravity skill and agent configs")
    parser.add_argument("--skills-only", action="store_true")
    parser.add_argument("--agents-only", action="store_true")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show passing checks")
    args = parser.parse_args()

    skill_schema = load_schema(SKILL_SCHEMA_PATH)
    agent_schema = load_schema(AGENT_SCHEMA_PATH)

    total_failures = 0

    if not args.agents_only:
        total_failures += validate_skills(skill_schema, args.verbose)

    if not args.skills_only:
        total_failures += validate_agents(agent_schema, args.verbose)

    print()
    if total_failures == 0:
        print(f"{GREEN}{BOLD}✓ All validations passed{RESET}")
    else:
        print(f"{RED}{BOLD}✗ {total_failures} validation error(s) found{RESET}")
        sys.exit(1)


if __name__ == "__main__":
    main()
