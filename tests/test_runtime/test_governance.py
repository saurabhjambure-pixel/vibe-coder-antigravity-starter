"""Tests for runtime/governance.py — GovernanceEngine"""

import json
import tempfile
import unittest
from pathlib import Path

from runtime.config import (
    FilesystemConfig, GovernanceConfig, PermissionsConfig,
    RuntimeConfig, RuntimeMeta, TerminalConfig,
)
from runtime.exceptions import PermissionDeniedError
from runtime.governance import GovernanceEngine


def _engine(
    allow_cmds=None,
    deny_cmds=None,
    read_write=None,
    deny_paths=None,
    mode="restricted",
    log_all=True,
) -> tuple[GovernanceEngine, Path, Path]:
    """Return (engine, log_path, repo_root) using a temp directory."""
    root = Path(tempfile.mkdtemp())
    log_path = root / ".agents" / "runtime.log"

    config = RuntimeConfig(
        runtime=RuntimeMeta(version="1.0", execution_mode=mode),
        permissions=PermissionsConfig(
            terminal=TerminalConfig(allow=allow_cmds or [], deny=deny_cmds or []),
            filesystem=FilesystemConfig(
                read_only=[],
                read_write=read_write or [],
                deny=deny_paths or [],
            ),
        ),
        governance=GovernanceConfig(
            auto_approve_safe_commands=True,
            require_human_intervention_on_deny=True,
            log_all_commands=log_all,
        ),
    )
    return GovernanceEngine(config, log_path, root), log_path, root


def _read_log(log_path: Path) -> list[dict]:
    if not log_path.exists():
        return []
    return [json.loads(line) for line in log_path.read_text().splitlines() if line.strip()]


class TestApproveTerminal(unittest.TestCase):

    def test_allowed_command_does_not_raise(self):
        engine, _, _ = _engine(allow_cmds=["git status"])
        engine.approve_terminal("git status")   # should not raise

    def test_denied_command_raises_permission_denied(self):
        engine, _, _ = _engine(deny_cmds=["sudo *"])
        with self.assertRaises(PermissionDeniedError) as ctx:
            engine.approve_terminal("sudo rm -rf /")
        self.assertIn("sudo rm -rf /", str(ctx.exception))

    def test_unlisted_command_raises_in_restricted_mode(self):
        engine, _, _ = _engine()
        with self.assertRaises(PermissionDeniedError):
            engine.approve_terminal("nmap -sV localhost")

    def test_permission_denied_error_has_command_attribute(self):
        engine, _, _ = _engine(deny_cmds=["sudo *"])
        try:
            engine.approve_terminal("sudo whoami")
        except PermissionDeniedError as e:
            self.assertEqual(e.command, "sudo whoami")
        else:
            self.fail("Expected PermissionDeniedError")


class TestApproveFilesystem(unittest.TestCase):

    def test_allowed_path_does_not_raise(self):
        engine, _, root = _engine(read_write=["./.agents/**"])
        path = root / ".agents" / "output.json"
        engine.approve_filesystem(str(path), "write")   # should not raise

    def test_denied_path_raises_permission_denied(self):
        engine, _, _ = _engine(deny_paths=["~/.ssh/**"])
        ssh_path = Path.home() / ".ssh" / "id_rsa"
        with self.assertRaises(PermissionDeniedError):
            engine.approve_filesystem(str(ssh_path), "read")

    def test_permission_denied_error_has_path_attribute(self):
        engine, _, _ = _engine(deny_paths=["~/.aws/**"])
        aws_path = Path.home() / ".aws" / "credentials"
        try:
            engine.approve_filesystem(str(aws_path), "read")
        except PermissionDeniedError as e:
            self.assertIsNotNone(e.path)
        else:
            self.fail("Expected PermissionDeniedError")


class TestLogging(unittest.TestCase):

    def test_allowed_command_is_logged(self):
        engine, log_path, _ = _engine(allow_cmds=["git status"], log_all=True)
        engine.approve_terminal("git status")
        records = _read_log(log_path)
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["decision"], "allow")
        self.assertEqual(records[0]["command"], "git status")

    def test_denied_command_is_logged_before_raise(self):
        engine, log_path, _ = _engine(deny_cmds=["sudo *"], log_all=True)
        try:
            engine.approve_terminal("sudo whoami")
        except PermissionDeniedError:
            pass
        records = _read_log(log_path)
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["decision"], "deny")

    def test_log_record_has_timestamp(self):
        engine, log_path, _ = _engine(allow_cmds=["git status"])
        engine.approve_terminal("git status")
        record = _read_log(log_path)[0]
        self.assertIn("ts", record)

    def test_log_record_is_valid_json(self):
        engine, log_path, _ = _engine(allow_cmds=["git status"])
        engine.approve_terminal("git status")
        lines = log_path.read_text().splitlines()
        for line in lines:
            json.loads(line)   # should not raise

    def test_log_skips_allowed_when_log_all_false(self):
        engine, log_path, _ = _engine(allow_cmds=["git status"], log_all=False)
        engine.approve_terminal("git status")
        records = _read_log(log_path)
        self.assertEqual(len(records), 0)

    def test_log_still_records_denials_when_log_all_false(self):
        engine, log_path, _ = _engine(deny_cmds=["sudo *"], log_all=False)
        try:
            engine.approve_terminal("sudo whoami")
        except PermissionDeniedError:
            pass
        records = _read_log(log_path)
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["decision"], "deny")

    def test_filesystem_decision_is_logged(self):
        engine, log_path, root = _engine(read_write=["./.agents/**"], log_all=True)
        path = root / ".agents" / "plan.json"
        engine.approve_filesystem(str(path), "write")
        records = _read_log(log_path)
        self.assertEqual(records[0]["type"], "filesystem")
        self.assertEqual(records[0]["operation"], "write")
        self.assertEqual(records[0]["decision"], "allow")

    def test_multiple_decisions_append_to_log(self):
        engine, log_path, root = _engine(
            allow_cmds=["git status"],
            read_write=["./.agents/**"],
            log_all=True,
        )
        engine.approve_terminal("git status")
        engine.approve_filesystem(str(root / ".agents" / "x.json"), "read")
        records = _read_log(log_path)
        self.assertEqual(len(records), 2)


if __name__ == "__main__":
    unittest.main()
