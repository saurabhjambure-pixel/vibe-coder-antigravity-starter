"""
terminal.py — TerminalGuard: pattern-based allow/deny checking for shell commands.

The guard is a pure, side-effect-free checker.  GovernanceEngine decides what to
do with the result (log, raise, etc.).

Matching tiers (most to least specific, applied in order):
  1. Exact string match
  2. Prefix match  — "git log --oneline" matches "git log --oneline -5"
  3. fnmatch       — handles wildcards like "sudo *" and "kill -9 *"
  4. Regex          — converts "**" → ".*" for patterns like "cat **/*.md"

Deny patterns are always evaluated before allow patterns.  If nothing matches,
execution_mode determines the default: "restricted" → deny, anything else → allow.
"""

import fnmatch
import re
from dataclasses import dataclass

from runtime.config import TerminalConfig


# ── Types ─────────────────────────────────────────────────────────────────────

@dataclass
class MatchResult:
    allowed: bool
    matched_rule: str          # "allow" | "deny" | "default_deny" | "default_allow"
    matched_pattern: str | None


# ── Guard ─────────────────────────────────────────────────────────────────────

class TerminalGuard:
    """Stateless command checker.  Thread-safe."""

    def __init__(self, config: TerminalConfig, execution_mode: str = "restricted") -> None:
        self._config = config
        self._execution_mode = execution_mode

    # ── Public API ────────────────────────────────────────────────────────────

    def check(self, command: str) -> MatchResult:
        """Return a MatchResult for the given command string."""
        cmd = self._normalize(command)

        # 1. Deny patterns win — checked first
        for pattern in self._config.deny:
            if self._match_pattern(cmd, pattern):
                return MatchResult(allowed=False, matched_rule="deny", matched_pattern=pattern)

        # 2. Allow patterns
        for pattern in self._config.allow:
            if self._match_pattern(cmd, pattern):
                return MatchResult(allowed=True, matched_rule="allow", matched_pattern=pattern)

        # 3. Default based on execution mode
        if self._execution_mode == "restricted":
            return MatchResult(allowed=False, matched_rule="default_deny", matched_pattern=None)
        return MatchResult(allowed=True, matched_rule="default_allow", matched_pattern=None)

    # ── Internals ─────────────────────────────────────────────────────────────

    @staticmethod
    def _normalize(command: str) -> str:
        """Strip edges and collapse internal whitespace."""
        return " ".join(command.split())

    @staticmethod
    def _match_pattern(command: str, pattern: str) -> bool:
        """
        Return True if command matches pattern using the four-tier strategy.

        Tier 1 — exact:   "git status" == "git status"
        Tier 2 — prefix:  "git log --oneline -5" starts with "git log --oneline "
        Tier 3 — fnmatch: "sudo apt install curl" matches "sudo *"
        Tier 4 — regex:   "cat docs/guide.md" matches "cat **/*.md"
        """
        pat = " ".join(pattern.split())   # normalise the pattern too

        # Tier 1: exact
        if command == pat:
            return True

        # Tier 2: prefix (pattern is a prefix of the command with a space boundary)
        if command.startswith(pat + " "):
            return True

        # Tier 3: fnmatch (handles *, ?, [...] — treats | as literal)
        if fnmatch.fnmatch(command, pat):
            return True

        # Tier 4: double-star regex conversion ("cat **/*.md" → r"cat (?:.*/)?[^ ]*\.md")
        if "**" in pat:
            # Split on "**", escape each segment, then rejoin.
            # The join uses (?:.*/)? so that ** can match ZERO path components,
            # allowing "cat **/*.md" to match both "cat README.md" (no directory)
            # and "cat docs/guide.md" (with a directory prefix).
            parts = pat.split("**")
            escaped_parts = [re.escape(p).replace(r"\*", r"[^ ]*") for p in parts]
            regex = r"(?:.*/?)?".join(escaped_parts)
            # Simplify (?:.*/?)?/ → (?:.*/)? to avoid requiring a literal slash
            # when ** immediately precedes a / in the pattern.
            regex = regex.replace(r"(?:.*/?)?/", r"(?:.*/)?")
            if re.fullmatch(regex, command):
                return True

        return False
