#!/usr/bin/env python3
"""
scaffold.py — Antigravity project scaffolder

Replaces init.sh with a structured, testable, --dry-run capable scaffolder.

Usage:
    python scaffold.py                         # scaffold in current directory
    python scaffold.py --dry-run               # preview what will be created
    python scaffold.py --name my-agent         # scaffold a new named agent
    python scaffold.py --name my-skill --type skill
    python scaffold.py --list-templates        # show available templates
    python scaffold.py --out ./my-project      # target a specific directory
    python scaffold.py --force                 # overwrite existing files

Exit codes:
    0  — success (or dry-run completed)
    1  — error (file conflict, bad args, etc.)
"""

import argparse
import os
import sys
import textwrap
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path


# ── ANSI colours ──────────────────────────────────────────────────────────────

GREEN  = "\033[92m"
BLUE   = "\033[94m"
YELLOW = "\033[93m"
RED    = "\033[91m"
DIM    = "\033[2m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

def green(s):  return f"{GREEN}{s}{RESET}"
def blue(s):   return f"{BLUE}{s}{RESET}"
def yellow(s): return f"{YELLOW}{s}{RESET}"
def red(s):    return f"{RED}{s}{RESET}"
def dim(s):    return f"{DIM}{s}{RESET}"
def bold(s):   return f"{BOLD}{s}{RESET}"


# ── File record ───────────────────────────────────────────────────────────────

@dataclass
class FileSpec:
    """A single file to be created by the scaffolder."""
    path: Path          # relative to project root
    content: str
    description: str = ""


# ── Template library ─────────────────────────────────────────────────────────

def make_skill_md(name: str, description: str = "") -> str:
    desc = description or (
        f"Use when the user wants to {name.replace('-', ' ')}. "
        f"Describe the specific scenario, action, and outcome here — "
        f"this is the semantic trigger Antigravity matches against."
    )
    return textwrap.dedent(f"""\
        ---
        name: {name}
        description: >
          {desc}
        ---

        # {name.replace('-', ' ').title()}

        ## Use this skill when
        - The user asks to [primary use case]
        - The user mentions [key phrase or concept]

        ## Do not use this skill when
        - [Scenario where another skill is more appropriate]

        ## Instructions

        1. [First step — read the relevant input file or context]
        2. [Second step — perform the core operation]
        3. [Final step — write a structured output artifact]

        ## Output Format

        Describe the expected output. If JSON, include the schema:

        ```json
        {{
          "result": "..."
        }}
        ```

        ## Guardrails

        - Never infer or hallucinate missing inputs — flag them explicitly
        - Always produce a structured artifact, never free-form prose
        - If an error occurs, write a failure artifact rather than silently stopping
    """)


def make_agent_yaml(name: str, role: str = "", skills: list[str] = None) -> str:
    role = role or f"{name.replace('-', ' ').title()} Specialist"
    skills_list = "\n".join(f"  - {s}" for s in (skills or [name.lower().replace(' ', '-')]))
    return textwrap.dedent(f"""\
        name: {name}
        role: "{role}"
        description: >
          Describe what this agent does, what it does NOT do, and when to use
          it vs. other agents. Be specific — this is read by humans and agents.

        auto_load_skills:
        {skills_list}

        # DOCUMENTATION ONLY — real permissions are set in Antigravity UI:
        # Agent Manager → Settings → Advanced → Terminal
        permissions:
          browser: false
          terminal: false
          file_system: read_only

        output_artifact: artifacts/{name.lower()}-output.json
    """)


def make_artifacts_gitkeep() -> str:
    return textwrap.dedent("""\
        # This directory holds structured JSON artifacts passed between agents.
        # It is intentionally committed so the directory exists on clone.
        # Actual artifact files should be added to .gitignore if they contain
        # generated or sensitive content.
    """)


def make_gitignore() -> str:
    return textwrap.dedent("""\
        # Antigravity artifacts — generated at runtime, not source-controlled
        artifacts/*.json

        # Python
        __pycache__/
        *.pyc
        .venv/

        # OS
        .DS_Store
        Thumbs.db
    """)


def make_readme(project_name: str) -> str:
    return textwrap.dedent(f"""\
        # {project_name}

        > Scaffolded with [vibe-coder-antigravity-starter](https://github.com/saurabhjambure-pixel/vibe-coder-antigravity-starter)

        ## Structure

        ```
        .agent/
          agents/    ← Agent configs (.yaml)
          skills/    ← Skill definitions (SKILL.md)
        artifacts/   ← Runtime JSON handoffs between agents
        schema/      ← Validation schemas and tooling
        ```

        ## Getting Started

        1. Edit the skill descriptions in `.agent/skills/*/SKILL.md`
        2. Configure agents in `.agent/agents/*.yaml`
        3. Open this folder in [Google Antigravity](https://antigravity.google)
        4. Prompt the Planner agent with your goal

        ## Validation

        ```bash
        pip install jsonschema pyyaml
        python schema/validate.py
        ```

        See `schema/README.md` for full validation docs.
    """)


# ── Template sets ─────────────────────────────────────────────────────────────

TEMPLATES = {
    "full": "Complete Planner → Worker → QA multi-agent scaffold (recommended for new projects)",
    "minimal": "Bare minimum: one skill + one agent",
    "skill": "A single new skill (use with --name)",
    "agent": "A single new agent (use with --name)",
}


def full_scaffold(root: Path, project_name: str) -> list[FileSpec]:
    """The complete Planner → Worker → QA scaffold."""
    return [
        FileSpec(
            path=root / ".agent" / "skills" / "task-planner" / "SKILL.md",
            content=make_skill_md(
                "task-planner",
                "Use when the user wants to decompose a high-level goal into an "
                "ordered list of atomic subtasks assigned to specialist agents. "
                "Produces a structured tasks.json artifact."
            ),
            description="Planner skill",
        ),
        FileSpec(
            path=root / ".agent" / "skills" / "logic-sanity-check" / "SKILL.md",
            content=make_skill_md(
                "logic-sanity-check",
                "Use when the user wants to validate completed task outputs against "
                "their original acceptance criteria, producing a structured pass/fail "
                "QA report artifact."
            ),
            description="QA validation skill",
        ),
        FileSpec(
            path=root / ".agent" / "agents" / "Planner.yaml",
            content=make_agent_yaml("Planner", "Project Orchestrator", ["task-planner"]),
            description="Planner agent",
        ),
        FileSpec(
            path=root / ".agent" / "agents" / "QA-Validator.yaml",
            content=make_agent_yaml("QA-Validator", "Quality Assurance Lead", ["logic-sanity-check"]),
            description="QA agent",
        ),
        FileSpec(
            path=root / "artifacts" / ".gitkeep",
            content=make_artifacts_gitkeep(),
            description="artifacts/ directory marker",
        ),
        FileSpec(
            path=root / ".gitignore",
            content=make_gitignore(),
            description=".gitignore",
        ),
        FileSpec(
            path=root / "README.md",
            content=make_readme(project_name),
            description="Project README",
        ),
    ]


def minimal_scaffold(root: Path, project_name: str) -> list[FileSpec]:
    """One skill, one agent — bare minimum to get started."""
    return [
        FileSpec(
            path=root / ".agent" / "skills" / "my-skill" / "SKILL.md",
            content=make_skill_md("my-skill"),
            description="Starter skill",
        ),
        FileSpec(
            path=root / ".agent" / "agents" / "My-Agent.yaml",
            content=make_agent_yaml("My-Agent", "Specialist", ["my-skill"]),
            description="Starter agent",
        ),
        FileSpec(
            path=root / "artifacts" / ".gitkeep",
            content=make_artifacts_gitkeep(),
            description="artifacts/ directory",
        ),
        FileSpec(
            path=root / ".gitignore",
            content=make_gitignore(),
            description=".gitignore",
        ),
    ]


def single_skill_scaffold(root: Path, name: str) -> list[FileSpec]:
    slug = name.lower().replace(" ", "-")
    return [
        FileSpec(
            path=root / ".agent" / "skills" / slug / "SKILL.md",
            content=make_skill_md(slug),
            description=f"Skill: {slug}",
        ),
    ]


def single_agent_scaffold(root: Path, name: str) -> list[FileSpec]:
    pascal = name.replace("-", " ").title().replace(" ", "-")
    return [
        FileSpec(
            path=root / ".agent" / "agents" / f"{pascal}.yaml",
            content=make_agent_yaml(pascal),
            description=f"Agent: {pascal}",
        ),
    ]


# ── Dry-run renderer ──────────────────────────────────────────────────────────

def render_dry_run(files: list[FileSpec], root: Path) -> None:
    print(f"\n{bold('Dry run — no files will be written')}\n")
    print(f"  Root: {blue(str(root))}\n")

    for spec in files:
        rel = spec.path.relative_to(root) if spec.path.is_absolute() else spec.path
        exists = spec.path.exists()
        status = yellow("[overwrite]") if exists else green("[create]  ")
        label  = dim(f"  # {spec.description}") if spec.description else ""
        print(f"  {status}  {rel}{label}")

    print(f"\n  {len(files)} file(s) would be written.\n")

    # Show first file's content as a preview
    if files:
        first = files[0]
        rel = first.path.relative_to(root) if first.path.is_absolute() else first.path
        print(f"{bold('Preview:')} {rel}\n")
        print(dim("  " + "\n  ".join(first.content.split("\n")[:20])))
        if first.content.count("\n") > 20:
            print(dim(f"  ... ({first.content.count(chr(10)) - 20} more lines)"))
        print()


# ── Writer ────────────────────────────────────────────────────────────────────

def write_files(files: list[FileSpec], root: Path, force: bool) -> int:
    written = 0
    skipped = 0
    errors  = 0

    for spec in files:
        rel = spec.path.relative_to(root) if spec.path.is_absolute() else spec.path

        if spec.path.exists() and not force:
            print(f"  {yellow('~')} {rel}  {dim('(exists — use --force to overwrite)')}")
            skipped += 1
            continue

        try:
            spec.path.parent.mkdir(parents=True, exist_ok=True)
            spec.path.write_text(spec.content, encoding="utf-8")
            print(f"  {green('✓')} {rel}")
            written += 1
        except OSError as e:
            print(f"  {red('✗')} {rel}  — {e}")
            errors += 1

    return errors


# ── Entry point ───────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scaffold an Antigravity skill/agent project",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            Examples:
              python scaffold.py --dry-run
              python scaffold.py --template minimal
              python scaffold.py --name data-cleaner --type skill
              python scaffold.py --name Summariser --type agent
              python scaffold.py --out ./my-project --template full
        """),
    )
    parser.add_argument(
        "--dry-run", "-n",
        action="store_true",
        help="Preview what would be created without writing any files",
    )
    parser.add_argument(
        "--template", "-t",
        choices=list(TEMPLATES.keys()),
        default="full",
        help="Which scaffold template to use (default: full)",
    )
    parser.add_argument(
        "--name",
        help="Name for a single skill or agent (used with --type skill/agent)",
    )
    parser.add_argument(
        "--type",
        choices=["skill", "agent"],
        help="What to scaffold when using --name",
    )
    parser.add_argument(
        "--out",
        default=".",
        help="Target directory (default: current directory)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing files",
    )
    parser.add_argument(
        "--list-templates",
        action="store_true",
        help="List available templates and exit",
    )

    args = parser.parse_args()

    # ── List templates ────────────────────────────────────────────────────────
    if args.list_templates:
        print(f"\n{bold('Available templates:')}\n")
        for name, desc in TEMPLATES.items():
            print(f"  {blue(name):30s}  {desc}")
        print()
        return

    root = Path(args.out).resolve()
    project_name = root.name if root.name != "." else "my-antigravity-project"

    # ── Resolve file list ─────────────────────────────────────────────────────
    if args.name and args.type:
        if args.type == "skill":
            files = single_skill_scaffold(root, args.name)
        else:
            files = single_agent_scaffold(root, args.name)
    elif args.template == "full":
        files = full_scaffold(root, project_name)
    elif args.template == "minimal":
        files = minimal_scaffold(root, project_name)
    elif args.template == "skill":
        if not args.name:
            parser.error("--template skill requires --name")
        files = single_skill_scaffold(root, args.name)
    elif args.template == "agent":
        if not args.name:
            parser.error("--template agent requires --name")
        files = single_agent_scaffold(root, args.name)
    else:
        files = full_scaffold(root, project_name)

    # ── Dry run or write ──────────────────────────────────────────────────────
    if args.dry_run:
        render_dry_run(files, root)
        return

    template_label = f"{args.type} '{args.name}'" if (args.name and args.type) else args.template
    print(f"\n{bold('Scaffolding')} {blue(template_label)} → {blue(str(root))}\n")

    errors = write_files(files, root, args.force)

    print()
    if errors == 0:
        written_count = sum(1 for f in files if f.path.exists())
        print(f"{green('✓')} Done. {written_count} file(s) written.")
        print(f"\n{dim('Next steps:')}")
        print(f"  1. Edit skill descriptions in {blue('.agent/skills/*/SKILL.md')}")
        print(f"  2. Open {blue(str(root))} in Google Antigravity")
        print(f"  3. Run {blue('python schema/validate.py')} to check your configs")
        print()
    else:
        print(f"{red('✗')} Completed with {errors} error(s).")
        sys.exit(1)


if __name__ == "__main__":
    main()
