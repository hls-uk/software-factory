#!/usr/bin/env python3
"""Contract tests for the embedded Beads toolchain checker."""

from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
ROOT = SKILL.parents[1]
CHECKER = SKILL / "scripts" / "check-toolchain.py"
MANIFEST = SKILL / "references" / "toolchain.json"


class ToolchainTests(unittest.TestCase):
    def run_checker(
        self,
        version: str,
        schema: int = 1,
        *,
        candidate: bool = False,
        manifest: dict[str, object] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            binary = root / "bd"
            binary.write_text(
                "#!/bin/sh\n"
                f"printf '%s\\n' '{{\"version\":\"{version}\","
                f"\"schema_version\":{schema}}}'\n",
                encoding="utf-8",
            )
            binary.chmod(0o755)
            manifest_path = root / "toolchain.json"
            manifest_path.write_text(
                json.dumps(
                    manifest
                    if manifest is not None
                    else json.loads(MANIFEST.read_text(encoding="utf-8"))
                ),
                encoding="utf-8",
            )
            command = [
                str(CHECKER),
                "--manifest",
                str(manifest_path),
                "--bd",
                str(binary),
                "--json",
            ]
            if candidate:
                command.append("--candidate")
            return subprocess.run(command, capture_output=True, text=True)

    def test_repo_manifest_matches_skill_source(self) -> None:
        self.assertEqual(
            MANIFEST.read_bytes(), (ROOT / ".factory/toolchain.json").read_bytes()
        )

    def test_promoted_version_and_schema_are_exact(self) -> None:
        passing = self.run_checker("1.1.0")
        self.assertEqual(0, passing.returncode, passing.stderr)
        self.assertEqual("embedded", json.loads(passing.stdout)["storageMode"])

        version_drift = self.run_checker("1.0.5")
        self.assertNotEqual(0, version_drift.returncode)
        self.assertIn("expected promoted 1.1.0/1", version_drift.stderr)

        schema_drift = self.run_checker("1.1.0", 2)
        self.assertNotEqual(0, schema_drift.returncode)
        self.assertIn("expected promoted 1.1.0/1", schema_drift.stderr)

    def test_candidate_requires_offline_qualification_state(self) -> None:
        absent = self.run_checker("1.1.0", candidate=True)
        self.assertNotEqual(0, absent.returncode)
        self.assertIn("no Beads candidate", absent.stderr)

        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        manifest["beads"]["candidate"] = {
            "version": "1.2.0",
            "storageSchemaVersion": 2,
            "status": "latest",
            "releaseUrl": "https://github.com/gastownhall/beads/releases/tag/v1.2.0",
        }
        rejected = self.run_checker("1.2.0", 2, candidate=True, manifest=manifest)
        self.assertNotEqual(0, rejected.returncode)
        self.assertIn("qualified-pending-embedded-migration", rejected.stderr)

    def test_external_or_team_policy_fields_fail_closed(self) -> None:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        manifest["doltServer"] = {"version": "2.2.1"}
        rejected = self.run_checker("1.1.0", manifest=manifest)
        self.assertNotEqual(0, rejected.returncode)
        self.assertIn("embedded contract", rejected.stderr)

        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        manifest["policy"]["migrationAuthority"] = "team-administrator"
        rejected = self.run_checker("1.1.0", manifest=manifest)
        self.assertNotEqual(0, rejected.returncode)
        self.assertIn("policy", rejected.stderr)

    def test_manifest_only_never_executes_or_installs(self) -> None:
        result = subprocess.run(
            [
                str(CHECKER),
                "--manifest",
                str(MANIFEST),
                "--bd",
                "/does/not/exist",
                "--manifest-only",
                "--json",
            ],
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, result.returncode, result.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
