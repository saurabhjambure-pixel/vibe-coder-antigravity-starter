#!/usr/bin/env bash
# .git/hooks/pre-commit
#
# Runs schema validation before every commit.
# Blocks commits that introduce invalid SKILL.md or agent.yaml files.
#
# Installation (run once from repo root):
#   cp schema/pre-commit-hook.sh .git/hooks/pre-commit
#   chmod +x .git/hooks/pre-commit
#
# To skip in an emergency:
#   git commit --no-verify

set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
VALIDATE="$REPO_ROOT/schema/validate.py"

# Only run if skill or agent files changed in this commit
CHANGED=$(git diff --cached --name-only)

SKILL_CHANGED=$(echo "$CHANGED" | grep -E '\.agents/skills/.+/SKILL\.md' || true)
AGENT_CHANGED=$(echo "$CHANGED" | grep -E '\.agents/agents/.+\.yaml' || true)

if [ -z "$SKILL_CHANGED" ] && [ -z "$AGENT_CHANGED" ]; then
  exit 0
fi

echo "🔍 Antigravity schema validation..."

# Ensure dependencies are available
if ! python3 -c "import jsonschema, yaml" 2>/dev/null; then
  echo "⚠ Missing dependencies — run: pip install jsonschema pyyaml"
  echo "⚠ Skipping validation (install dependencies to enable)"
  exit 0
fi

if python3 "$VALIDATE"; then
  echo "✅ Schema validation passed"
  exit 0
else
  echo ""
  echo "❌ Schema validation failed — commit blocked."
  echo "   Fix the errors above, then re-run: git commit"
  echo "   To skip (not recommended): git commit --no-verify"
  exit 1
fi
