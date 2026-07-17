#!/usr/bin/env python3
"""End-to-end and adversarial tests for review_packet.py."""

from __future__ import annotations

import contextlib
import io
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

import review_packet as rp


class ReviewPacketTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.repo = self.root / "repo"
        self.repo.mkdir()
        self.original_skill_root = rp.SKILL_ROOT
        self.original_template_root = rp.TEMPLATE_ROOT
        self.skill_root = self.root / "skill"
        shutil.copytree(
            self.original_skill_root / "assets",
            self.skill_root / "assets",
        )
        registry_path = self.skill_root / "assets" / "review-templates" / "registry.json"
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
        for entry in registry["templates"]:
            entry["approval"] = {
                "approvedAt": "2026-07-16T00:00:00Z",
                "approvedBy": "fixture-operator",
                "separationOfDuty": "single-operator-versioned-template",
                "status": "approved",
            }
        registry_path.write_text(json.dumps(registry), encoding="utf-8")
        rp.SKILL_ROOT = self.skill_root
        rp.TEMPLATE_ROOT = self.skill_root / "assets" / "review-templates"

        self.git("init", "-b", "main")
        self.git("config", "user.email", "fixture@example.invalid")
        self.git("config", "user.name", "Fixture")
        self.write("app.py", "value = 'base'\n")
        self.write("second.py", "second = 'base'\n")
        self.write("docs/plans/story.md", "# Story 1\nImplement the bound change.\n")
        self.write(
            "docs/requirements/story.md",
            "# Criteria\nAC 1 must hold. Literal {{DIFF}} and "
            + rp.PROMPT_HASH_MARKER
            + " stay unchanged.\n",
        )
        self.write("docs/design/story.md", "# Contract\nPreserve safety.\n")
        self.write_json(
            ".factory/reviews/story-1.json",
            {
                "schemaVersion": 1,
                "reviewId": "story-1",
                "kind": "story",
                "inputs": [
                    {"role": "story", "path": "docs/plans/story.md", "snapshot": "base"},
                    {
                        "role": "criteria",
                        "path": "docs/requirements/story.md",
                        "snapshot": "base",
                    },
                    {"role": "spec", "path": "docs/design/story.md", "snapshot": "base"},
                    {
                        "role": "verification",
                        "path": "evidence/story-1.md",
                        "snapshot": "head",
                    },
                ],
            },
        )
        self.write_json(
            ".factory/reviews/promotion-1.json",
            {
                "schemaVersion": 1,
                "reviewId": "promotion-1",
                "kind": "promotion",
                "inputs": [
                    {
                        "role": "plan",
                        "path": "docs/plans/promotion.md",
                        "snapshot": "head",
                    },
                    {
                        "role": "waivers",
                        "path": "evidence/waivers.md",
                        "snapshot": "head",
                    },
                ],
            },
        )
        self.commit("base review contracts")
        self.base = self.head()

        self.write("app.py", "value = 'round-one'\n")
        self.write("second.py", "second = 'round-one'\n")
        self.write("evidence/story-1.md", "verification: green\n")
        self.write("docs/plans/promotion.md", "# Promotion plan\nAll stories.\n")
        self.write("evidence/waivers.md", "waivers: none\n")
        self.commit("round one")
        self.head_one = self.head()

    def tearDown(self) -> None:
        rp.SKILL_ROOT = self.original_skill_root
        rp.TEMPLATE_ROOT = self.original_template_root
        self.temporary.cleanup()

    def git(self, *args: str) -> str:
        result = subprocess.run(
            ["git", "-C", str(self.repo), *args],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return result.stdout.strip()

    def head(self) -> str:
        return self.git("rev-parse", "HEAD")

    def commit(self, message: str) -> None:
        self.git("add", "-A")
        self.git("commit", "-m", message)

    def write(self, path: str, content: str) -> None:
        target = self.repo / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

    def write_json(self, path: str, value: object) -> None:
        self.write(path, json.dumps(value, sort_keys=True) + "\n")

    def run_main(self, arguments: list[str]) -> int:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            result = rp.main(arguments)
        self.last_output = stdout.getvalue() + stderr.getvalue()
        return result

    def build_initial(self, review_type: str, review_id: str, head: str, name: str) -> Path:
        output = self.root / name
        result = self.run_main(
            [
                "build",
                "--repo",
                str(self.repo),
                "--type",
                review_type,
                "--review-id",
                review_id,
                "--base",
                self.base,
                "--head",
                head,
                "--out",
                str(output),
            ]
        )
        self.assertEqual(result, 0, self.last_output)
        return output

    def build_delta(self, previous: Path, head: str, name: str) -> Path:
        output = self.root / name
        result = self.run_main(
            [
                "build",
                "--repo",
                str(self.repo),
                "--type",
                "story-delta",
                "--base",
                self.base,
                "--head",
                head,
                "--previous-packet",
                str(previous),
                "--out",
                str(output),
            ]
        )
        self.assertEqual(result, 0, self.last_output)
        return output

    def write_verdict(
        self,
        packet_dir: Path,
        factory_review: str,
        findings: list[dict[str, object]],
    ) -> None:
        manifest = json.loads((packet_dir / "manifest.json").read_text(encoding="utf-8"))
        packet = json.loads((packet_dir / "packet.json").read_text(encoding="utf-8"))
        verdict = {
            "schemaVersion": 1,
            "factoryReview": factory_review,
            "reviewId": manifest["reviewId"],
            "reviewType": manifest["reviewType"],
            "round": manifest["round"],
            "head": manifest["range"]["head"],
            "templateSha256": manifest["template"]["sha256"],
            "manifestSha256": packet["manifestSha256"],
            "promptSha256": packet["promptSha256"],
            "diffSha256": manifest["diff"]["sha256"],
            "reviewer": {
                "identity": "fixture-reviewer",
                "independence": "fresh-session",
                "readOnly": True,
            },
            "findings": findings,
        }
        (packet_dir / "verdict.json").write_bytes(rp.canonical_json(verdict))

    @staticmethod
    def blocker(summary: str = "broken") -> dict[str, object]:
        return {
            "severity": "blocker",
            "file": "app.py",
            "line": 1,
            "summary": summary,
            "evidence": "fixture demonstrates the defect",
            "fix": "change the fixture value",
        }

    def verify(self, packet_dir: Path, head: str, review_id: str = "story-1") -> dict:
        return rp.verify_packet(
            self.repo,
            packet_dir,
            expected_head=head,
            expected_base=self.base,
            expected_review_id=review_id,
        )

    def test_full_delta_promotion_lifecycle_and_round_cap(self) -> None:
        full = self.build_initial("story-full", "story-1", self.head_one, "full")
        self.write_verdict(full, "BLOCKED", [self.blocker("round one blocker")])
        self.assertEqual(self.verify(full, self.head_one)["verdict"]["factoryReview"], "BLOCKED")
        self.assertEqual(
            self.run_main(
                [
                    "verify",
                    "--repo",
                    str(self.repo),
                    "--packet",
                    str(full),
                    "--expected-review-id",
                    "story-1",
                    "--expected-base",
                    self.base,
                    "--expected-head",
                    self.head_one,
                ]
            ),
            3,
        )

        self.write("app.py", "value = 'round-two'\n")
        self.commit("round two remediation")
        head_two = self.head()
        delta_two = self.build_delta(full, head_two, "delta-two")
        self.write_verdict(delta_two, "BLOCKED", [self.blocker("delta blocker")])
        self.assertEqual(
            self.verify(delta_two, head_two)["manifest"]["range"]["lastReviewed"],
            self.head_one,
        )
        tampered_lineage = self.root / "tampered-lineage"
        shutil.copytree(delta_two, tampered_lineage)
        prior_verdict_path = tampered_lineage / "previous" / "verdict.json"
        prior_verdict = json.loads(prior_verdict_path.read_text(encoding="utf-8"))
        prior_verdict["reviewer"]["identity"] = "tampered-reviewer"
        prior_verdict_path.write_bytes(rp.canonical_json(prior_verdict))
        with self.assertRaisesRegex(rp.PacketError, "manifest does not match"):
            self.verify(tampered_lineage, head_two)

        self.write("app.py", "value = 'round-three'\n")
        self.commit("round three remediation")
        head_three = self.head()
        delta_three = self.build_delta(delta_two, head_three, "delta-three")
        self.write_verdict(delta_three, "PASS", [])
        verified = self.verify(delta_three, head_three)
        self.assertEqual(verified["manifest"]["round"], 3)
        self.assertEqual(verified["verdict"]["factoryReview"], "PASS")
        self.assertEqual(
            self.run_main(
                [
                    "verify",
                    "--repo",
                    str(self.repo),
                    "--packet",
                    str(delta_three),
                    "--expected-review-id",
                    "story-1",
                    "--expected-base",
                    self.base,
                    "--expected-head",
                    head_three,
                ]
            ),
            0,
        )

        promotion = self.build_initial("promotion", "promotion-1", head_three, "promotion")
        self.write_verdict(promotion, "PASS", [])
        self.assertEqual(
            self.verify(promotion, head_three, "promotion-1")["verdict"]["factoryReview"],
            "PASS",
        )

        self.write_verdict(delta_three, "BLOCKED", [self.blocker("still blocked")])
        self.write("app.py", "value = 'forbidden-round-four'\n")
        self.commit("attempt round four")
        result = self.run_main(
            [
                "build",
                "--repo",
                str(self.repo),
                "--type",
                "story-delta",
                "--base",
                self.base,
                "--head",
                self.head(),
                "--previous-packet",
                str(delta_three),
                "--out",
                str(self.root / "round-four"),
            ]
        )
        self.assertEqual(result, 2)

    def test_selected_reordered_and_truncated_diffs_are_rejected(self) -> None:
        full = self.build_initial("story-full", "story-1", self.head_one, "full")
        self.write_verdict(full, "PASS", [])
        self.verify(full, self.head_one)
        original = (full / "prompt.txt").read_bytes()
        self.assertIn(b"Literal {{DIFF}}", original)
        self.assertIn(rp.PROMPT_HASH_MARKER.encode(), original)

        mutations = {
            "selected": original.replace(b"diff --git a/second.py", b"omitted --git a/second.py"),
            "reordered": original.replace(
                b"diff --git a/app.py",
                b"diff --git a/zz-app.py",
            ),
            "truncated": original[:-80],
        }
        for name, prompt in mutations.items():
            with self.subTest(name=name):
                tampered = self.root / f"tampered-{name}"
                shutil.copytree(full, tampered)
                (tampered / "prompt.txt").write_bytes(prompt)
                with self.assertRaisesRegex(rp.PacketError, "prompt.txt differs"):
                    self.verify(tampered, self.head_one)

    def test_manifest_template_input_and_sha_tampering_is_rejected(self) -> None:
        full = self.build_initial("story-full", "story-1", self.head_one, "full")
        self.write_verdict(full, "PASS", [])

        def resign_manifest(directory: Path, mutate) -> None:
            manifest = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
            mutate(manifest)
            raw = rp.canonical_json(manifest)
            (directory / "manifest.json").write_bytes(raw)
            packet = json.loads((directory / "packet.json").read_text(encoding="utf-8"))
            packet["manifestSha256"] = rp.sha256(raw)
            (directory / "packet.json").write_bytes(rp.canonical_json(packet))

        mutations = {
            "reordered-inputs": lambda value: value["inputs"].reverse(),
            "missing-input": lambda value: value["inputs"].pop(),
            "extra-input": lambda value: value["inputs"].append(dict(value["inputs"][0])),
            "altered-template": lambda value: value["template"].update({"sha256": "0" * 64}),
            "wrong-head": lambda value: value["range"].update({"head": self.base}),
            "wrong-range": lambda value: value["range"].update({"mode": "two-dot"}),
            "wrong-type": lambda value: value.update({"reviewType": "promotion"}),
            "boolean-round": lambda value: value.update({"round": True}),
        }
        for name, mutate in mutations.items():
            with self.subTest(name=name):
                tampered = self.root / name
                shutil.copytree(full, tampered)
                resign_manifest(tampered, mutate)
                with self.assertRaises(rp.PacketError):
                    self.verify(tampered, self.head_one)

        with self.assertRaisesRegex(rp.PacketError, "head is stale"):
            self.verify(full, self.base)
        with self.assertRaisesRegex(rp.PacketError, "base does not match"):
            rp.verify_packet(
                self.repo,
                full,
                expected_head=self.head_one,
                expected_base=self.head_one,
                expected_review_id="story-1",
            )

        template_path = self.skill_root / "assets/review-templates/v1/story-full.txt"
        template_bytes = template_path.read_bytes()
        template_path.write_bytes(template_bytes + b"altered\n")
        try:
            with self.assertRaisesRegex(rp.PacketError, "template hash mismatch"):
                rp.load_template("story-full")
        finally:
            template_path.write_bytes(template_bytes)

    def test_pending_template_approval_blocks_packet_construction(self) -> None:
        registry_path = self.skill_root / "assets/review-templates/registry.json"
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
        for entry in registry["templates"]:
            if entry["reviewType"] == "story-full":
                entry["approval"] = {
                    "approvedAt": None,
                    "approvedBy": None,
                    "separationOfDuty": "single-operator-versioned-template",
                    "status": "pending",
                }
        registry_path.write_text(json.dumps(registry), encoding="utf-8")
        with self.assertRaisesRegex(rp.PacketError, "lacks operator approval"):
            rp.load_template("story-full")

    def test_contract_and_verdict_reject_missing_extra_or_reordered_data(self) -> None:
        contract = json.loads(
            (self.repo / ".factory/reviews/story-1.json").read_text(encoding="utf-8")
        )
        missing = json.loads(json.dumps(contract))
        missing["inputs"].pop()
        with self.assertRaisesRegex(rp.PacketError, "verification/head"):
            rp.validate_contract(missing, "story", "story-1")

        extra = json.loads(json.dumps(contract))
        extra["inputs"].append(
            {"role": "commentary", "path": "docs/commentary.md", "snapshot": "base"}
        )
        with self.assertRaises(rp.PacketError):
            rp.validate_contract(extra, "story", "story-1")

        reordered = json.loads(json.dumps(contract))
        reordered["inputs"].reverse()
        with self.assertRaisesRegex(rp.PacketError, "canonical"):
            rp.validate_contract(reordered, "story", "story-1")

        full = self.build_initial("story-full", "story-1", self.head_one, "full")
        self.write_verdict(full, "PASS", [self.blocker()])
        with self.assertRaisesRegex(rp.PacketError, "PASS verdict contains blocker"):
            self.verify(full, self.head_one)

        self.write_verdict(full, "PASS", [])
        verdict_path = full / "verdict.json"
        verdict = json.loads(verdict_path.read_text(encoding="utf-8"))
        verdict["round"] = True
        verdict_path.write_bytes(rp.canonical_json(verdict))
        with self.assertRaisesRegex(rp.PacketError, "verdict round"):
            self.verify(full, self.head_one)

        self.write_verdict(full, "BLOCKED", [self.blocker()])
        verdict = json.loads(verdict_path.read_text(encoding="utf-8"))
        verdict["findings"][0]["line"] = True
        verdict_path.write_bytes(rp.canonical_json(verdict))
        with self.assertRaisesRegex(rp.PacketError, "line must be a positive integer"):
            self.verify(full, self.head_one)


if __name__ == "__main__":
    unittest.main()
