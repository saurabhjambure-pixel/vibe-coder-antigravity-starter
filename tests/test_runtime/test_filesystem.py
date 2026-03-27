"""Tests for runtime/filesystem.py — FilesystemGuard"""

import tempfile
import unittest
from pathlib import Path

from runtime.config import FilesystemConfig
from runtime.filesystem import FilesystemGuard


def _guard(
    read_only=None,
    read_write=None,
    deny=None,
    repo_root: Path | None = None,
) -> FilesystemGuard:
    if repo_root is None:
        repo_root = Path(tempfile.mkdtemp())
    return FilesystemGuard(
        FilesystemConfig(
            read_only=read_only or [],
            read_write=read_write or [],
            deny=deny or [],
        ),
        repo_root=repo_root,
    )


class TestReadOnlyAccess(unittest.TestCase):

    def test_read_allowed_from_read_only(self):
        g = _guard(read_only=["/etc/hosts"])
        r = g.check("/etc/hosts", "read")
        self.assertTrue(r.allowed)

    def test_write_denied_from_read_only(self):
        g = _guard(read_only=["/etc/hosts"])
        r = g.check("/etc/hosts", "write")
        self.assertFalse(r.allowed)


class TestReadWriteAccess(unittest.TestCase):

    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        self.guard = _guard(read_write=["./.agents/**"], repo_root=self.root)

    def test_read_allowed_from_read_write(self):
        path = self.root / ".agents" / "plan.json"
        r = self.guard.check(str(path), "read")
        self.assertTrue(r.allowed)

    def test_write_allowed_from_read_write(self):
        path = self.root / ".agents" / "plan.json"
        r = self.guard.check(str(path), "write")
        self.assertTrue(r.allowed)

    def test_read_write_relative_path(self):
        r = self.guard.check("./.agents/output.json", "write")
        self.assertTrue(r.allowed)


class TestDenyPatterns(unittest.TestCase):

    def test_ssh_key_read_denied(self):
        g = _guard(deny=["~/.ssh/**"])
        ssh_path = Path.home() / ".ssh" / "id_rsa"
        r = g.check(str(ssh_path), "read")
        self.assertFalse(r.allowed)
        self.assertEqual(r.matched_rule, "deny")

    def test_aws_credentials_denied(self):
        g = _guard(deny=["~/.aws/**"])
        aws_path = Path.home() / ".aws" / "credentials"
        r = g.check(str(aws_path), "read")
        self.assertFalse(r.allowed)

    def test_env_file_denied_anywhere(self):
        g = _guard(deny=["**/.env"], read_write=["./**"])
        root = Path(tempfile.mkdtemp())
        env_path = root / "src" / "app" / ".env"
        r = g.check(str(env_path), "read")
        self.assertFalse(r.allowed)
        self.assertEqual(r.matched_rule, "deny")

    def test_deny_wins_over_read_write(self):
        g = _guard(read_write=["~/.ssh/**"], deny=["~/.ssh/**"])
        ssh_path = Path.home() / ".ssh" / "id_rsa"
        r = g.check(str(ssh_path), "write")
        self.assertFalse(r.allowed)
        self.assertEqual(r.matched_rule, "deny")


class TestPathTraversalBlocked(unittest.TestCase):

    def test_traversal_into_ssh_is_blocked(self):
        root = Path(tempfile.mkdtemp())
        g = _guard(deny=["~/.ssh/**"], read_write=["./docs/**"], repo_root=root)
        # Attempt to sneak past docs/ using traversal
        traversal = str(root / "docs" / ".." / ".." / ".ssh" / "config")
        r = g.check(traversal, "read")
        self.assertFalse(r.allowed)

    def test_relative_traversal_normalised(self):
        root = Path(tempfile.mkdtemp())
        g = _guard(deny=["~/.ssh/**"], repo_root=root)
        # Use a relative path with ..
        ssh_via_relative = "./../../.ssh/id_rsa"
        r = g.check(ssh_via_relative, "read")
        # After resolve this should be outside all read_write zones → default deny
        self.assertFalse(r.allowed)


class TestDefaultDeny(unittest.TestCase):

    def test_unmatched_path_is_denied(self):
        g = _guard(read_only=["/etc/hosts"])
        r = g.check("/var/log/system.log", "read")
        self.assertFalse(r.allowed)
        self.assertEqual(r.matched_rule, "default_deny")


class TestAntigravityYamlConfig(unittest.TestCase):
    """End-to-end against the actual antigravity.yaml filesystem config."""

    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        self.guard = FilesystemGuard(
            FilesystemConfig(
                read_only=["/etc/hosts"],
                read_write=["./.agents/**", "./docs/**", "./examples/**"],
                deny=["~/.ssh/**", "~/.aws/**", "**/.env"],
            ),
            repo_root=self.root,
        )

    def test_etc_hosts_readable(self):
        self.assertTrue(self.guard.check("/etc/hosts", "read").allowed)

    def test_etc_hosts_not_writable(self):
        self.assertFalse(self.guard.check("/etc/hosts", "write").allowed)

    def test_agents_dir_writable(self):
        path = self.root / ".agents" / "runtime.log"
        self.assertTrue(self.guard.check(str(path), "write").allowed)

    def test_docs_dir_writable(self):
        path = self.root / "docs" / "guide.md"
        self.assertTrue(self.guard.check(str(path), "write").allowed)

    def test_examples_dir_readable(self):
        path = self.root / "examples" / "template.md"
        self.assertTrue(self.guard.check(str(path), "read").allowed)

    def test_ssh_key_blocked(self):
        path = Path.home() / ".ssh" / "id_rsa"
        self.assertFalse(self.guard.check(str(path), "read").allowed)

    def test_aws_creds_blocked(self):
        path = Path.home() / ".aws" / "credentials"
        self.assertFalse(self.guard.check(str(path), "read").allowed)

    def test_env_file_blocked(self):
        path = self.root / "docs" / ".env"
        self.assertFalse(self.guard.check(str(path), "read").allowed)


if __name__ == "__main__":
    unittest.main()
