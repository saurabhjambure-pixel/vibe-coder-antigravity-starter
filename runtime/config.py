"""
config.py — Loads and parses antigravity.yaml into typed dataclasses.

Usage:
    from runtime.config import load_config
    from pathlib import Path

    config = load_config(Path("antigravity.yaml"))
    print(config.runtime.execution_mode)   # "restricted"
    print(config.permissions.terminal.allow)
"""

import os
import sys
from dataclasses import dataclass, field
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Missing dependency. Run:  pip install pyyaml")
    sys.exit(1)

from runtime.exceptions import ConfigLoadError


# ── Dataclasses ───────────────────────────────────────────────────────────────

@dataclass
class RuntimeMeta:
    version: str
    execution_mode: str  # "restricted" | "open"


@dataclass
class TerminalConfig:
    allow: list[str] = field(default_factory=list)
    deny: list[str] = field(default_factory=list)


@dataclass
class FilesystemConfig:
    read_only: list[str] = field(default_factory=list)
    read_write: list[str] = field(default_factory=list)
    deny: list[str] = field(default_factory=list)


@dataclass
class GovernanceConfig:
    auto_approve_safe_commands: bool = True
    require_human_intervention_on_deny: bool = True
    log_all_commands: bool = True


@dataclass
class PermissionsConfig:
    terminal: TerminalConfig = field(default_factory=TerminalConfig)
    filesystem: FilesystemConfig = field(default_factory=FilesystemConfig)


@dataclass
class RuntimeConfig:
    runtime: RuntimeMeta
    permissions: PermissionsConfig
    governance: GovernanceConfig


# ── Loader ────────────────────────────────────────────────────────────────────

def load_config(config_path: Path | None = None) -> RuntimeConfig:
    """
    Load antigravity.yaml from:
      1. Explicit path argument
      2. ANTIGRAVITY_CONFIG environment variable
      3. Repo root (relative to this file's parent.parent)

    Raises ConfigLoadError on missing file, parse error, or missing required keys.
    """
    if config_path is None:
        env_path = os.environ.get("ANTIGRAVITY_CONFIG")
        if env_path:
            config_path = Path(env_path)
        else:
            config_path = Path(__file__).parent.parent / "antigravity.yaml"

    path_str = str(config_path)

    if not config_path.exists():
        raise ConfigLoadError(path_str, "file not found")

    try:
        raw = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    except yaml.YAMLError as e:
        raise ConfigLoadError(path_str, f"YAML parse error: {e}")

    if not isinstance(raw, dict):
        raise ConfigLoadError(path_str, "top-level value must be a YAML mapping")

    for key in ("runtime", "permissions", "governance"):
        if key not in raw:
            raise ConfigLoadError(path_str, f"missing required top-level key: '{key}'")

    # ── runtime ───────────────────────────────────────────────────────────────
    rt = raw["runtime"]
    runtime_meta = RuntimeMeta(
        version=str(rt.get("version", "1.0")),
        execution_mode=str(rt.get("execution_mode", "restricted")),
    )

    # ── permissions ───────────────────────────────────────────────────────────
    perms = raw["permissions"]

    term_raw = perms.get("terminal", {}) or {}
    terminal = TerminalConfig(
        allow=list(term_raw.get("allow", []) or []),
        deny=list(term_raw.get("deny", []) or []),
    )

    fs_raw = perms.get("filesystem", {}) or {}
    filesystem = FilesystemConfig(
        read_only=list(fs_raw.get("read_only", []) or []),
        read_write=list(fs_raw.get("read_write", []) or []),
        deny=list(fs_raw.get("deny", []) or []),
    )

    permissions = PermissionsConfig(terminal=terminal, filesystem=filesystem)

    # ── governance ────────────────────────────────────────────────────────────
    gov = raw["governance"]
    governance = GovernanceConfig(
        auto_approve_safe_commands=bool(gov.get("auto_approve_safe_commands", True)),
        require_human_intervention_on_deny=bool(gov.get("require_human_intervention_on_deny", True)),
        log_all_commands=bool(gov.get("log_all_commands", True)),
    )

    return RuntimeConfig(
        runtime=runtime_meta,
        permissions=permissions,
        governance=governance,
    )
