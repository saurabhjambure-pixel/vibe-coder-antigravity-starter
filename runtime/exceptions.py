"""
exceptions.py — Custom exceptions for the Antigravity runtime permission system.
"""


class PermissionDeniedError(Exception):
    """Raised when a terminal command or filesystem operation is denied by policy."""

    def __init__(
        self,
        reason: str,
        command: str | None = None,
        path: str | None = None,
        matched_pattern: str | None = None,
    ) -> None:
        super().__init__(reason)
        self.reason = reason
        self.command = command
        self.path = path
        self.matched_pattern = matched_pattern


class ConfigLoadError(Exception):
    """Raised when antigravity.yaml cannot be loaded or parsed."""

    def __init__(self, path: str, detail: str) -> None:
        super().__init__(f"Failed to load config '{path}': {detail}")
        self.path = path
        self.detail = detail
