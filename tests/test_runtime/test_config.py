"""Tests for runtime/config.py — load_config()"""

import tempfile
import unittest
from pathlib import Path

from runtime.config import load_config, RuntimeConfig
from runtime.exceptions import ConfigLoadError

MINIMAL_YAML = """\
runtime:
  version: "1.0"
  execution_mode: "restricted"

permissions:
  terminal:
    allow: ["git status"]
    deny: ["sudo *"]
  filesystem:
    read_only: ["/etc/hosts"]
    read_write: ["./.agents/**"]
    deny: ["~/.ssh/**"]

governance:
  auto_approve_safe_commands: true
  require_human_intervention_on_deny: true
  log_all_commands: false
"""


class TestLoadConfig(unittest.TestCase):

    def _write(self, content: str) -> Path:
        tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False)
        tmp.write(content)
        tmp.flush()
        return Path(tmp.name)

    def test_valid_config_returns_runtime_config(self):
        path = self._write(MINIMAL_YAML)
        config = load_config(path)
        self.assertIsInstance(config, RuntimeConfig)
        self.assertEqual(config.runtime.version, "1.0")
        self.assertEqual(config.runtime.execution_mode, "restricted")

    def test_terminal_allow_and_deny_loaded(self):
        path = self._write(MINIMAL_YAML)
        config = load_config(path)
        self.assertIn("git status", config.permissions.terminal.allow)
        self.assertIn("sudo *", config.permissions.terminal.deny)

    def test_filesystem_lists_loaded(self):
        path = self._write(MINIMAL_YAML)
        config = load_config(path)
        self.assertIn("/etc/hosts", config.permissions.filesystem.read_only)
        self.assertIn("./.agents/**", config.permissions.filesystem.read_write)
        self.assertIn("~/.ssh/**", config.permissions.filesystem.deny)

    def test_governance_flags_loaded(self):
        path = self._write(MINIMAL_YAML)
        config = load_config(path)
        self.assertTrue(config.governance.auto_approve_safe_commands)
        self.assertTrue(config.governance.require_human_intervention_on_deny)
        self.assertFalse(config.governance.log_all_commands)

    def test_missing_file_raises_config_load_error(self):
        with self.assertRaises(ConfigLoadError) as ctx:
            load_config(Path("/nonexistent/antigravity.yaml"))
        self.assertIn("file not found", str(ctx.exception))

    def test_invalid_yaml_raises_config_load_error(self):
        path = self._write("runtime: [\nbad: yaml: here")
        with self.assertRaises(ConfigLoadError) as ctx:
            load_config(path)
        self.assertIn("YAML parse error", str(ctx.exception))

    def test_missing_required_key_raises_config_load_error(self):
        path = self._write("runtime:\n  version: '1.0'\n  execution_mode: restricted\n")
        with self.assertRaises(ConfigLoadError) as ctx:
            load_config(path)
        self.assertIn("permissions", str(ctx.exception))

    def test_non_mapping_raises_config_load_error(self):
        path = self._write("- item1\n- item2\n")
        with self.assertRaises(ConfigLoadError) as ctx:
            load_config(path)
        self.assertIn("mapping", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
