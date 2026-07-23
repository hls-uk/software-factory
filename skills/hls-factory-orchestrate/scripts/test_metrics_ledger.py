#!/usr/bin/env python3
"""Tests for the HLS offline metrics ledger."""

from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import metrics_ledger as ml  # noqa: E402


class MetricsLedgerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.root = Path(tempfile.mkdtemp(prefix="hls-metrics-"))
        self.ledger = self.root / "metrics.jsonl"

    def record(self, **overrides: object) -> dict[str, object]:
        fields: dict[str, object] = {
            "ts": "2026-07-23T10:00:00Z",
            "repo": "example",
            "bead_id": "example-1",
            "event": "dispatch",
            "lane": "lane-1",
            "provider": "provider",
            "model": "model",
            "tier": "strong",
            "effort": "high",
            "complexity": "standard",
            "risk_class": "routine",
            "operating_mode": "supervised",
            "routing_profile": "balanced",
            "assurance_profile": "standard",
            "release_stage": "operational",
            "duration_s": None,
            "host": "host-1",
            "detail": None,
        }
        fields.update(overrides)
        return ml.make_record(fields)

    def run_main(self, args: list[str]) -> tuple[int, str, str]:
        out = io.StringIO()
        err = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = ml.main(args)
        return code, out.getvalue(), err.getvalue()

    def test_content_id_is_deterministic_and_tamper_evident(self) -> None:
        first = self.record()
        second = self.record()
        self.assertEqual(first["id"], second["id"])
        changed = self.record(model="other")
        self.assertNotEqual(first["id"], changed["id"])

    def test_append_and_check_round_trip(self) -> None:
        record = self.record()
        self.assertTrue(ml.append_record(self.ledger, record))
        self.assertFalse(ml.append_record(self.ledger, record))
        self.assertEqual([record], ml.load_ledger(self.ledger))
        code, out, err = self.run_main(["check", "--ledger", str(self.ledger)])
        self.assertEqual(0, code, err)
        self.assertEqual(1, json.loads(out)["events"])

    def test_append_capture_failure_never_blocks_delivery(self) -> None:
        code, out, err = self.run_main(
            [
                "append",
                "--ledger",
                str(self.ledger),
                "--repo",
                "example",
                "--bead-id",
                "example-1",
                "--event",
                "dispatch",
                "--detail",
                "{bad",
            ]
        )
        self.assertEqual(0, code)
        self.assertEqual("", out)
        self.assertIn("append skipped", err)
        self.assertFalse(self.ledger.exists())

    def test_check_rejects_tampering(self) -> None:
        record = self.record()
        record["model"] = "tampered"
        self.ledger.write_text(json.dumps(record) + "\n", encoding="utf-8")
        code, _, err = self.run_main(["check", "--ledger", str(self.ledger)])
        self.assertEqual(1, code)
        self.assertIn("content id mismatch", err)

    def test_rollup_derives_story_without_prose_parsing(self) -> None:
        rows = [
            self.record(),
            self.record(
                ts="2026-07-23T10:01:00Z",
                event="gate_fail",
                duration_s=10,
            ),
            self.record(
                ts="2026-07-23T10:02:00Z",
                event="gate_pass",
                duration_s=20,
            ),
            self.record(
                ts="2026-07-23T10:03:00Z",
                event="review",
                detail={"round": 1, "blockers": 1, "nonblockers": 2},
            ),
            self.record(
                ts="2026-07-23T10:05:00Z",
                event="close",
                detail={"outcome": "merged"},
            ),
        ]
        for row in rows:
            ml.append_record(self.ledger, row)
        result = ml.build_rollups(ml.load_ledger(self.ledger))[0]
        self.assertEqual(300, result["active_seconds"])
        self.assertEqual(2, result["gate_runs"])
        self.assertEqual(1, result["gate_failures"])
        self.assertEqual(1, result["review_rounds"])
        self.assertEqual(1, result["blockers"])
        self.assertEqual(2, result["nonblockers"])
        self.assertEqual("merged", result["outcome"])

    def test_rollup_command_is_offline_json(self) -> None:
        ml.append_record(self.ledger, self.record())
        code, out, err = self.run_main(["rollup", "--ledger", str(self.ledger)])
        self.assertEqual(0, code, err)
        parsed = json.loads(out)
        self.assertEqual(ml.SCHEMA_VERSION, parsed["schemaVersion"])
        self.assertEqual("example-1", parsed["stories"][0]["bead_id"])
        self.assertNotIn("sql", out.lower())

    def test_backfill_is_idempotent_and_honest_about_missing_fields(self) -> None:
        usage = self.root / "usage.jsonl"
        usage.write_text(
            "\n".join(
                [
                    json.dumps(
                        {
                            "ts": "2026-07-22T09:00:00Z",
                            "provider": "openai",
                            "lane": "lane-1",
                            "story": "legacy-1",
                            "event": "dispatch",
                        }
                    ),
                    json.dumps(
                        {
                            "ts": "2026-07-22T09:05:00Z",
                            "provider": "openai",
                            "lane": "lane-1",
                            "story": "legacy-1",
                            "event": "complete",
                        }
                    ),
                ]
            )
            + "\n",
            encoding="utf-8",
        )
        args = [
            "backfill",
            "--repo",
            "example",
            "--usage-ledger",
            str(usage),
            "--ledger",
            str(self.ledger),
        ]
        first, out, err = self.run_main(args)
        self.assertEqual(0, first, err)
        self.assertEqual(2, json.loads(out)["appended"])
        second, out, err = self.run_main(args)
        self.assertEqual(0, second, err)
        self.assertEqual(0, json.loads(out)["appended"])
        self.assertEqual(2, json.loads(out)["duplicates_skipped"])
        rollup = ml.build_rollups(ml.load_ledger(self.ledger))[0]
        self.assertIsNone(rollup["outcome"])
        self.assertEqual(300, rollup["active_seconds"])

    def test_backfill_skips_invalid_lines_and_missing_file_is_noop(self) -> None:
        missing = self.root / "missing.jsonl"
        code, out, err = self.run_main(
            [
                "backfill",
                "--repo",
                "example",
                "--usage-ledger",
                str(missing),
                "--ledger",
                str(self.ledger),
            ]
        )
        self.assertEqual(0, code, err)
        self.assertEqual(0, json.loads(out)["appended"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
