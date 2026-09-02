#!/usr/bin/env python3
"""Validate the extension's dependency and execution boundaries."""

from __future__ import annotations

import json
import re
import stat
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "cmux-extension.json"
PACKAGE_PATH = ROOT / "package.json"
LOCK_PATH = ROOT / "package-lock.json"
INSTALLER_PATH = ROOT / "scripts" / "install-dependencies.sh"
RUNNER_PATH = ROOT / "scripts" / "run-ccusage.sh"
NETWORK_GUARD_PATH = ROOT / "scripts" / "deny-network.cjs"

CCUSAGE_VERSION = "17.2.1"
CCUSAGE_TARBALL = (
    "https://registry.npmjs.org/ccusage/-/ccusage-17.2.1.tgz"
)
CCUSAGE_INTEGRITY = (
    "sha512-++F9rwk7EHsNyuCfs0D2vHyT/G0kaS3GVHhyh4BJ+dVKm0W4a/"
    "Mkld9lXGesgQzMnI6uE0V5RgmB/2Jf8zR7yg=="
)

MUTABLE_NPM_REF = re.compile(
    r"(?:@(?:latest|next|beta|canary|dev|nightly)|(?:^|:)\s*[~^<>=*])"
)


def read_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as stream:
        return json.load(stream)


def command_tokens(value: object) -> list[str]:
    """Return every string in command/build arrays in a manifest value."""
    if isinstance(value, list):
        return [token for item in value for token in command_tokens(item)]
    if isinstance(value, dict):
        return [token for item in value.values() for token in command_tokens(item)]
    return [value] if isinstance(value, str) else []


class ManifestTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = read_json(MANIFEST_PATH)
        cls.package = read_json(PACKAGE_PATH)
        cls.lock = read_json(LOCK_PATH)

    def test_commands_use_local_pinned_runner(self) -> None:
        panes = {pane["id"]: pane for pane in self.manifest["panes"]}
        self.assertEqual(
            panes["live"]["command"],
            ["./scripts/run-ccusage.sh", "blocks", "--live", "--offline"],
        )
        self.assertEqual(
            panes["daily"]["command"],
            ["./scripts/run-ccusage.sh", "daily", "--offline"],
        )
        self.assertEqual(
            self.manifest["build"],
            [{"command": ["./scripts/install-dependencies.sh"]}],
        )

    def test_manifest_has_no_mutable_npm_reference(self) -> None:
        tokens = command_tokens(self.manifest)
        self.assertNotIn("npx", tokens)
        for token in tokens:
            self.assertFalse(
                MUTABLE_NPM_REF.search(token),
                f"mutable npm reference in manifest command: {token}",
            )

    def test_lockfile_pins_expected_tarball_and_integrity(self) -> None:
        root = self.lock["packages"][""]
        package = self.lock["packages"][f"node_modules/ccusage"]
        self.assertEqual(self.lock["lockfileVersion"], 3)
        self.assertEqual(root["dependencies"]["ccusage"], CCUSAGE_VERSION)
        self.assertEqual(package["version"], CCUSAGE_VERSION)
        self.assertEqual(package["resolved"], CCUSAGE_TARBALL)
        self.assertEqual(package["integrity"], CCUSAGE_INTEGRITY)

    def test_installation_and_runtime_scripts_are_hardened(self) -> None:
        installer = INSTALLER_PATH.read_text(encoding="utf-8")
        runner = RUNNER_PATH.read_text(encoding="utf-8")
        guard = NETWORK_GUARD_PATH.read_text(encoding="utf-8")
        for option in (
            "npm ci",
            "--ignore-scripts",
            "--no-audit",
            "--no-fund",
            "--omit=dev",
            "env -i",
        ):
            self.assertIn(option, installer)
        self.assertIn("env -i", runner)
        self.assertIn("--require", runner)
        self.assertIn("node_modules/ccusage/dist/index.js", runner)
        self.assertIn("globalThis.fetch", guard)
        for path in (INSTALLER_PATH, RUNNER_PATH):
            self.assertTrue(
                path.stat().st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH),
                f"{path} must be executable",
            )


if __name__ == "__main__":
    unittest.main()
