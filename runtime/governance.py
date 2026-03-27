"""
governance.py — GovernanceEngine: orchestrates permission checks and audit logging.

The engine is the single public surface for callers.  Instantiate once, then
call approve_terminal() / approve_filesystem() before every guarded operation.
A return without exception means the operation is permitted.

Log format: JSON Lines (.jsonl), one record per line, written to .agents/runtime.log.
The _log() method writes directly to disk, bypassing FilesystemGuard, to avoid
infinite recursion when the engine logs its own decisions.

Usage:
    from runtime.governance import GovernanceEngine
    from runtime.config import load_config
    from pathlib import Path

    config = load_config()
    engine = GovernanceEngine(
        config,
        log_path=Path(".agents/runtime.log"),
        repo_root=Path("."),
    )

    engine.approve_terminal("git status")                          # OK
    engine.approve_terminal("sudo rm -rf /")                      # raises PermissionDeniedError
    engine.approve_filesystem("./docs/notes.md", "write")         # OK
    engine.approve_filesystem("~/.aws/credentials", "read")       # raises PermissionDeniedError
"""

import json
from datetime import datetime, timezone
from pathlib import Path

from runtime.config import RuntimeConfig
from runtime.exceptions import PermissionDeniedError
from runtime.filesystem import FilesystemGuard
from runtime.terminal import TerminalGuard


# ── ANSI colours (matches project convention) ─────────────────────────────────

GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
RESET  = "\033[0m"


class GovernanceEngine:
    """
    Orchestrates terminal and filesystem permission checks.
    Logs every decision and raises PermissionDeniedError on denial.
    """

    def __init__(
        self,
        config: RuntimeConfig,
        log_path: Path,
        repo_root: Path,
    ) -> None:
        self._config = config
        self._log_path = log_path
        self._terminal_guard = TerminalGuard(
            config.permissions.terminal,
            execution_mode=config.runtime.execution_mode,
        )
        self._fs_guard = FilesystemGuard(config.permissions.filesystem, repo_root)

    # ── Public API ────────────────────────────────────────────────────────────

    def approve_terminal(self, command: str) -> None:
        """
        Allow or deny a shell command.

        Returns None if allowed.
        Raises PermissionDeniedError if denied (and logs the decision first).
        """
        result = self._terminal_guard.check(command)

        if self._config.governance.log_all_commands or not result.allowed:
            self._log({
                "type": "terminal",
                "command": command,
                "decision": "allow" if result.allowed else "deny",
                "matched_rule": result.matched_rule,
                "matched_pattern": result.matched_pattern,
                "execution_mode": self._config.runtime.execution_mode,
            })

        if not result.allowed:
            raise PermissionDeniedError(
                reason=self._terminal_deny_message(command, result.matched_pattern),
                command=command,
                matched_pattern=result.matched_pattern,
            )

    def approve_filesystem(self, path: str | Path, operation: str) -> None:
        """
        Allow or deny a filesystem read or write.

        Returns None if allowed.
        Raises PermissionDeniedError if denied (and logs the decision first).
        """
        result = self._fs_guard.check(path, operation)
        path_str = str(path)

        if self._config.governance.log_all_commands or not result.allowed:
            self._log({
                "type": "filesystem",
                "path": path_str,
                "operation": operation,
                "decision": "allow" if result.allowed else "deny",
                "matched_rule": result.matched_rule,
                "matched_pattern": result.matched_pattern,
                "execution_mode": self._config.runtime.execution_mode,
            })

        if not result.allowed:
            raise PermissionDeniedError(
                reason=self._fs_deny_message(path_str, operation, result.matched_pattern),
                path=path_str,
                matched_pattern=result.matched_pattern,
            )

    # ── Internals ─────────────────────────────────────────────────────────────

    def _log(self, record: dict) -> None:
        """Append one JSON Lines record to the log file (bypasses FilesystemGuard)."""
        record["ts"] = datetime.now(timezone.utc).isoformat()
        self._log_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self._log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")

    @staticmethod
    def _terminal_deny_message(command: str, pattern: str | None) -> str:
        if pattern:
            return (
                f"Command '{command}' matched deny pattern '{pattern}'. "
                f"Human review required. "
                f"To allow it, add it to permissions.terminal.allow in antigravity.yaml "
                f"and ensure it does not match any deny pattern."
            )
        return (
            f"Command '{command}' is not on the allow list and execution_mode is 'restricted'. "
            f"Add it to permissions.terminal.allow in antigravity.yaml to permit it."
        )

    @staticmethod
    def _fs_deny_message(path: str, operation: str, pattern: str | None) -> str:
        if pattern:
            return (
                f"Path '{path}' ({operation}) matched deny pattern '{pattern}'. "
                f"Human review required. "
                f"Remove the deny pattern or exclude this path in antigravity.yaml."
            )
        return (
            f"Path '{path}' is not in any permitted filesystem zone for '{operation}'. "
            f"Add it to permissions.filesystem.read_write (or read_only for reads) "
            f"in antigravity.yaml."
        )
