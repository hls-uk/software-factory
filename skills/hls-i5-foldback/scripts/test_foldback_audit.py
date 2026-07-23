#!/usr/bin/env python3
"""Tests for exhaustive fold-back scanning and disposition validation."""

from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("foldback_audit.py")


class FoldbackAuditTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.repo = self.root / "source"
        self.repo.mkdir()
        subprocess.run(["git", "init", "-q", str(self.repo)], check=True)
        subprocess.run(
            ["git", "-C", str(self.repo), "config", "user.email", "test@example.invalid"],
            check=True,
        )
        subprocess.run(
            ["git", "-C", str(self.repo), "config", "user.name", "Test"],
            check=True,
        )
        self.write("README.md", "base\n")
        self.commit("base")
        self.base = self.sha()
        self.baseline = self.root / "baseline.json"
        self.baseline.write_text(
            json.dumps(
                {
                    "schemaVersion": 1,
                    "upstream": {"commit": self.base},
                    "dispositions": ["port", "adapt", "present", "reject"],
                    "selectedAreas": {
                        "CE": {
                            "pathTerms": ["context"],
                            "messageTerms": ["context"],
                        },
                        "TC": {
                            "pathTerms": ["toolchain"],
                            "messageTerms": ["toolchain"],
                        },
                    },
                }
            ),
            encoding="utf-8",
        )
        self.write("context/a.md", "one\n")
        self.write("unrelated.txt", "two\n")
        self.commit("context update")
        self.write("toolchain/policy.md", "three\n")
        self.commit("toolchain update")
        self.target = self.sha()
        self.ledger = self.root / "ledger.json"

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write(self, relative: str, text: str) -> None:
        path = self.repo / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def commit(self, subject: str) -> None:
        subprocess.run(["git", "-C", str(self.repo), "add", "."], check=True)
        subprocess.run(
            ["git", "-C", str(self.repo), "commit", "-q", "-m", subject],
            check=True,
        )

    def sha(self) -> str:
        return subprocess.run(
            ["git", "-C", str(self.repo), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()

    def command(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [str(SCRIPT), "--baseline", str(self.baseline), *args],
            capture_output=True,
            text=True,
        )

    def check_command(self) -> subprocess.CompletedProcess[str]:
        return self.command(
            "check",
            "--source",
            str(self.repo),
            "--ledger",
            str(self.ledger),
        )

    def scan(self) -> dict[str, object]:
        result = self.command(
            "scan",
            "--source",
            str(self.repo),
            "--to",
            self.target,
            "--out",
            str(self.ledger),
        )
        self.assertEqual(0, result.returncode, result.stderr)
        return json.loads(self.ledger.read_text(encoding="utf-8"))

    def test_scan_records_every_commit_path_deterministically(self) -> None:
        first = self.scan()
        first_bytes = self.ledger.read_bytes()
        second = self.scan()
        self.assertEqual(first, second)
        self.assertEqual(first_bytes, self.ledger.read_bytes())
        self.assertEqual(3, len(first["entries"]))
        self.assertEqual(
            ["context/a.md", "unrelated.txt", "toolchain/policy.md"],
            [entry["path"] for entry in first["entries"]],
        )

    def test_incomplete_ledger_fails_closed(self) -> None:
        self.scan()
        result = self.check_command()
        self.assertNotEqual(0, result.returncode)
        self.assertIn("no valid disposition", result.stderr)

    def test_complete_port_adapt_and_reject_ledger_passes(self) -> None:
        ledger = self.scan()
        for entry in ledger["entries"]:
            entry["rationale"] = "inspected exact upstream diff"
            if entry["path"].startswith("context/"):
                entry["disposition"] = "adapt"
                entry["selectedArea"] = "CE"
                entry["hlsEvidence"] = ["skills/hls-factory-orchestrate/SKILL.md"]
            elif entry["path"].startswith("toolchain/"):
                entry["disposition"] = "port"
                entry["selectedArea"] = "TC"
                entry["hlsEvidence"] = ["skills/hls-beads/SKILL.md"]
            else:
                entry["disposition"] = "reject"
        self.ledger.write_text(
            json.dumps(ledger, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        result = self.check_command()
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(3, json.loads(result.stdout)["entries"])

    def test_positive_disposition_requires_area_and_evidence(self) -> None:
        ledger = self.scan()
        for entry in ledger["entries"]:
            entry["disposition"] = "reject"
            entry["rationale"] = "outside selected subset"
        ledger["entries"][0]["disposition"] = "present"
        self.ledger.write_text(json.dumps(ledger), encoding="utf-8")
        result = self.check_command()
        self.assertNotEqual(0, result.returncode)
        self.assertIn("selectedArea", result.stderr)

    def test_deleted_upstream_row_is_rejected(self) -> None:
        ledger = self.scan()
        ledger["entries"].pop()
        self.ledger.write_text(json.dumps(ledger), encoding="utf-8")
        result = self.check_command()
        self.assertNotEqual(0, result.returncode)
        self.assertIn("reconstructed upstream delta", result.stderr)

    def test_non_descendant_target_is_rejected(self) -> None:
        subprocess.run(
            ["git", "-C", str(self.repo), "checkout", "-q", "--orphan", "other"],
            check=True,
        )
        for path in self.repo.iterdir():
            if path.name != ".git" and path.is_file():
                path.unlink()
        self.write("other.txt", "other\n")
        self.commit("unrelated root")
        other = self.sha()
        result = self.command(
            "scan",
            "--source",
            str(self.repo),
            "--to",
            other,
            "--out",
            str(self.ledger),
        )
        self.assertNotEqual(0, result.returncode)
        self.assertIn("does not descend", result.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
