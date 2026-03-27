"""
filesystem.py — FilesystemGuard: path-based access control.

Paths are resolved to absolute canonical form before any comparison,
which prevents directory-traversal tricks such as:
    ./docs/../../.ssh/config  →  /Users/you/.ssh/config  (hits deny list)

Permission matrix:
    deny patterns     →  always blocked (read or write)
    read_write paths  →  readable and writable
    read_only paths   →  readable but NOT writable
    default           →  deny (execution_mode == "restricted")

Deny is evaluated first, giving it unconditional precedence.
"""

import re
from pathlib import Path

from runtime.config import FilesystemConfig
from runtime.terminal import MatchResult   # reuse the same dataclass


class FilesystemGuard:
    """Stateless path checker.  Thread-safe."""

    def __init__(self, config: FilesystemConfig, repo_root: Path) -> None:
        self._config = config
        self._repo_root = repo_root.resolve()

    # ── Public API ────────────────────────────────────────────────────────────

    def check(self, path: str | Path, operation: str) -> MatchResult:
        """
        Return a MatchResult for accessing *path* with *operation* ("read" or "write").

        The resolved absolute path is matched against deny → read_write → read_only
        (read_only is skipped for write operations).
        """
        resolved = self._resolve(path)

        # 1. Deny patterns win
        for pattern in self._config.deny:
            if self._match_pattern(resolved, pattern):
                return MatchResult(allowed=False, matched_rule="deny", matched_pattern=pattern)

        # 2. read_write allows both reads and writes
        for pattern in self._config.read_write:
            if self._match_pattern(resolved, pattern):
                return MatchResult(allowed=True, matched_rule="read_write", matched_pattern=pattern)

        # 3. read_only allows reads only
        if operation == "read":
            for pattern in self._config.read_only:
                if self._match_pattern(resolved, pattern):
                    return MatchResult(allowed=True, matched_rule="read_only", matched_pattern=pattern)

        return MatchResult(allowed=False, matched_rule="default_deny", matched_pattern=None)

    # ── Internals ─────────────────────────────────────────────────────────────

    def _resolve(self, path: str | Path) -> Path:
        """Expand ~, anchor relative paths to repo_root, then canonicalise."""
        p = Path(path).expanduser()
        if not p.is_absolute():
            p = self._repo_root / p
        # resolve() follows symlinks and removes .. components
        # strict=False so it works even when the path doesn't exist yet
        return p.resolve()

    def _match_pattern(self, resolved: Path, pattern: str) -> bool:
        """
        Return True if resolved (absolute Path) matches pattern.

        Pattern forms:
          /etc/hosts           →  exact absolute path (compared after symlink resolution)
          ~/.ssh/**            →  home-relative glob
          ./.agents/**         →  repo-relative glob, anchored to repo_root
          **/.env              →  filesystem-wide: any path ending in /.env

        Anchoring rule: patterns starting with "**" are NOT anchored to repo_root;
        they match anywhere on the filesystem.  All other relative patterns are
        anchored to repo_root.
        """
        pat_path = Path(pattern).expanduser()
        if not pat_path.is_absolute() and not pattern.startswith("**"):
            pat_path = self._repo_root / pat_path

        resolved_str = str(resolved)
        pattern_str = str(pat_path)

        # Tier 1: no wildcards — resolve both paths to handle symlinks (e.g.
        #   /etc → /private/etc on macOS) before comparing.
        if "*" not in pattern_str:
            try:
                return resolved == pat_path.resolve()
            except Exception:
                return resolved_str == pattern_str

        # Tier 2: pathlib.Path.match() — natively supports ** and single *
        try:
            if resolved.match(pattern_str):
                return True
        except Exception:
            pass

        # Tier 3: regex — convert ** → .* and * → [^/]* for explicit anchoring
        escaped = re.escape(pattern_str)
        regex = escaped.replace(r"\*\*", ".*").replace(r"\*", "[^/]*")
        return bool(re.fullmatch(regex, resolved_str))
