# Antigravity Documentation Reference

This page maps every convention used in this repo to its official source, and notes where community patterns diverge from the spec.

---

## Official Sources

| Resource | URL | What it covers |
|---|---|---|
| Download & install | [antigravity.google/download](https://antigravity.google/download) | macOS, Windows, Linux installers |
| Official docs home | [antigravity.google/docs/home](https://antigravity.google/docs/home) | Full reference |
| Skills reference | [antigravity.google/docs/skills](https://antigravity.google/docs/skills) | SKILL.md spec, scopes, patterns |
| Getting Started codelab | [codelabs.developers.google.com/getting-started-google-antigravity](https://codelabs.developers.google.com/getting-started-google-antigravity) | Installation, Agent Manager, permissions |
| Authoring Skills codelab | [codelabs.developers.google.com/getting-started-with-antigravity-skills](https://codelabs.developers.google.com/getting-started-with-antigravity-skills) | SKILL.md format, directory structure, patterns |
| Google Developers Blog announcement | [developers.googleblog.com/build-with-google-antigravity](https://developers.googleblog.com/build-with-google-antigravity-our-new-agentic-development-platform/) | Platform overview, architecture |

---

## Key Concepts Defined by Official Docs

### What Antigravity Is

Antigravity is an agentic development platform that combines a familiar AI-powered coding experience with a new agent-first interface, allowing you to deploy agents that autonomously plan, execute, and verify complex tasks across your editor, terminal, and browser.

### What Skills Are

Skills are an open standard for extending agent capabilities. A skill is a folder containing a SKILL.md file with instructions that the agent can follow when working on specific tasks.

Skills are **on-demand** — unlike a System Prompt which is always loaded, a Skill is only loaded into the agent's context when the agent determines it is relevant to the user's current request.

### How Skill Triggering Works

Antigravity achieves automatic skill selection through Semantic Triggering, where the agent compares the user's natural language input against the description field in the SKILL.md metadata. You don't invoke skills by name — the agent matches them from your description.

### Skill Scopes

Skills can be defined at two scopes: Workspace Scope, located in `<workspace-root>/.agent/skills/`, available only within the specific project; and Global Scope, located in `~/.gemini/antigravity/skills/`, available across all projects on the user's machine.

### Permission System

Giving an AI agent access to your terminal and browser is a double-edged sword. Antigravity addresses this through a granular permission system revolving around Terminal Command Auto Execution policies, Allow Lists, and Deny Lists.

---

## Official SKILL.md Format

Based on the official Skills codelab and documentation, the canonical format is:

```markdown
---
name: my-skill-name
description: One sentence describing when the agent should use this skill. This is the semantic trigger — write it as a phrase a user might naturally say.
---

# Skill Title

## Use this skill when
- ...

## Do not use this skill when
- ...

## Instructions
1. Step one
2. Step two

## Guardrails
- Never do X
- Always do Y
```

### Frontmatter Fields

| Field | Required | Notes |
|---|---|---|
| `name` | ✅ Yes | Unique identifier, kebab-case |
| `description` | ✅ Yes | The semantic trigger — the most important field |

> **Note:** Some tutorials show a `triggers:` list field in frontmatter. This is a community pattern, not part of the official spec. The official mechanism relies entirely on the `description` field for semantic matching. Use `description` as your primary trigger signal.

---

## Official Skill Directory Structure

```
.agent/skills/
└── my-skill/
    ├── SKILL.md          # Required — definition and instructions
    ├── scripts/          # Optional — Python, Bash, or Node scripts
    │   └── run.py
    ├── resources/        # Optional — templates, reference docs
    └── examples/         # Optional — few-shot examples for the agent
```

The design is intentionally simple, relying on widely understood formats like Markdown and YAML, lowering the barrier to entry for developers wishing to extend the IDE's capabilities.

---

## Convention Map: This Repo vs. Official Spec

| Convention used in this repo | Official status | Notes |
|---|---|---|
| `.agent/skills/<name>/SKILL.md` | ✅ Canonical | Matches workspace scope path exactly |
| `.agent/agents/<name>.yaml` | ⚠️ Community pattern | Official docs don't define a standard agent.yaml spec — this is an emerging convention common in the community but not yet in official docs |
| `triggers:` list in SKILL.md frontmatter | ⚠️ Community extension | Not in the official spec. Description alone drives triggering. Kept here for clarity but may not be parsed by the engine |
| `auto_load_skills:` in agent.yaml | ⚠️ Community pattern | Not documented officially. In practice, skills load semantically — this field serves as human-readable intent documentation |
| `permissions:` block in agent.yaml | ⚠️ Community pattern | Real permissions are set in Antigravity's Settings UI (Agent Manager → Settings → Advanced), not via file |
| `artifacts/` directory for structured JSON handoffs | ✅ Aligned with platform | Antigravity natively produces Artifacts; using a local `artifacts/` folder for inter-agent handoffs is architecturally sound |

---

## Setting Permissions Correctly

Unlike the `permissions:` block in `agent.yaml` (which is human documentation, not machine-enforced), real Antigravity permissions are configured in the UI:

1. Open **Agent Manager**
2. Go to **Settings → Advanced Settings → Terminal**
3. Set your **Terminal Command Auto Execution** policy:
   - `Always Proceed` — agent runs commands without asking
   - `Request Review` — agent asks before every command
4. Configure **Allow List** and **Deny List** for specific commands

The Allow List is used primarily with the Off policy and represents a positive security model, meaning everything is forbidden unless expressly permitted.

---

## Further Reading

- [Google Cloud Community: Building Custom Skills — 5 Practical Examples](https://medium.com/google-cloud/tutorial-getting-started-with-antigravity-skills-864041811e0d)
- [learnwithcheer.com: How to Install and Create Agent Skills](https://learnwithcheer.com/blog/agents-skills-in-antigravity)
- [rmyndharis/antigravity-skills](https://github.com/rmyndharis/antigravity-skills) — community collection of 300+ production skills
- [Wikipedia: Google Antigravity](https://en.wikipedia.org/wiki/Google_Antigravity) — platform background and model support
