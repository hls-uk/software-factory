#!/usr/bin/env python3
"""Tests for the executable HLS delivery contract."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import delivery_contract as dc  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[3]
SCRIPT = Path(__file__).resolve().parent / "delivery_contract.py"


class DeliveryContractTest(unittest.TestCase):
    def write(self, payload: object | None) -> Path:
        root = Path(tempfile.mkdtemp(prefix="hls-contract-"))
        (root / ".factory").mkdir()
        if payload is not None:
            text = payload if isinstance(payload, str) else json.dumps(payload)
            (root / ".factory" / "agents.json").write_text(text, encoding="utf-8")
        return root

    def test_fields_resolve_independently(self) -> None:
        result = dc.read_contract(
            self.write(
                {
                    "operatingMode": "autonomous",
                    "modelRoutingProfile": "throughput",
                    "assuranceProfile": "rapid",
                    "releaseStage": "beta",
                }
            )
        )
        self.assertEqual(
            {
                "operatingMode": "autonomous",
                "modelRoutingProfile": "throughput",
                "assuranceProfile": "rapid",
                "releaseStage": "beta",
            },
            result["contract"],
        )

    def test_absent_and_invalid_values_default_safely(self) -> None:
        for payload in (None, {}, {"assuranceProfile": "fast"}):
            result = dc.read_contract(self.write(payload))
            self.assertEqual("supervised", result["contract"]["operatingMode"])
            self.assertEqual("balanced", result["contract"]["modelRoutingProfile"])
            self.assertEqual("standard", result["contract"]["assuranceProfile"])
            self.assertEqual("operational", result["contract"]["releaseStage"])

    def test_release_stages_match_hls_contract(self) -> None:
        for stage in ("experiment", "beta", "operational", "canonical"):
            result = dc.read_contract(self.write({"releaseStage": stage}))
            self.assertEqual(stage, result["contract"]["releaseStage"])
        for old_i5_stage in ("prototype", "pilot"):
            result = dc.read_contract(self.write({"releaseStage": old_i5_stage}))
            self.assertEqual("operational", result["contract"]["releaseStage"])
            self.assertEqual("invalid-defaulted", result["sources"]["releaseStage"])

    def test_unknown_assurance_never_reads_below_standard(self) -> None:
        for value in ("Rapid", "rapid ", "", 3, True, [], {}):
            result = dc.read_contract(self.write({"assuranceProfile": value}))
            self.assertEqual("standard", result["contract"]["assuranceProfile"])
            self.assertEqual("invalid-defaulted", result["sources"]["assuranceProfile"])

    def test_legacy_alias_and_explicit_precedence(self) -> None:
        result = dc.read_contract(self.write({"deliveryProfile": "quality"}))
        self.assertEqual("quality", result["contract"]["modelRoutingProfile"])
        self.assertEqual(
            "deliveryProfile alias", result["sources"]["modelRoutingProfile"]
        )
        result = dc.read_contract(
            self.write(
                {
                    "deliveryProfile": "quality",
                    "modelRoutingProfile": "throughput",
                }
            )
        )
        self.assertEqual("throughput", result["contract"]["modelRoutingProfile"])

    def test_spot_sampling_only_applies_to_explicit_valid_rapid(self) -> None:
        good = dc.read_contract(
            self.write({"assuranceProfile": "rapid", "spotReviewRate": 5})
        )
        self.assertEqual(5, good["spotReviewRate"])
        for assurance, rate in (
            ("standard", 5),
            ("assured", 5),
            ("rapid", 2),
            ("rapid", 11),
            ("rapid", True),
            ("rapid", "5"),
        ):
            result = dc.read_contract(
                self.write(
                    {"assuranceProfile": assurance, "spotReviewRate": rate}
                )
            )
            self.assertIsNone(result["spotReviewRate"])

    def test_check_reports_invalid_or_ignored_sampling(self) -> None:
        for payload, expected in (
            ({"assuranceProfile": "rapid", "spotReviewRate": 100}, "outside 3-10"),
            ({"assuranceProfile": "rapid", "spotReviewRate": "5"}, "integer"),
            ({"assuranceProfile": "standard", "spotReviewRate": 5}, "ignored"),
        ):
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "check",
                    "--repo",
                    str(self.write(payload)),
                ],
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(0, result.returncode)
            self.assertIn(expected, result.stderr)

    def test_invalid_json_fails_closed(self) -> None:
        with self.assertRaises(dc.ContractError):
            dc.read_contract(self.write("{not json"))

    def test_factory_declares_valid_single_operator_contract(self) -> None:
        result = dc.read_contract(REPO_ROOT)
        self.assertTrue(result["declared"])
        self.assertEqual([], dc.invalid_fields(REPO_ROOT))
        self.assertEqual("supervised", result["contract"]["operatingMode"])
        self.assertEqual("standard", result["contract"]["assuranceProfile"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
