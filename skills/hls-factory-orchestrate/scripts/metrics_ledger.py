#!/usr/bin/env python3
"""Maintain the HLS offline, append-only, content-addressed metrics ledger.

Commands:
  append    Add one event without ever blocking delivery on capture failure.
  check     Verify every stored event and content id.
  rollup    Derive deterministic per-story JSON from the local ledger.
  backfill  Import the legacy `.factory/usage.jsonl` ledger idempotently.

The tool is Python-standard-library-only and never opens a network or database
connection.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import socket
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA_VERSION = 1
DEFAULT_LEDGER = Path(".factory/metrics.jsonl")
DEFAULT_USAGE_LEDGER = Path(".factory/usage.jsonl")
EVENTS = ("dispatch", "gate_pass", "gate_fail", "review", "close", "limit")
OUTCOMES = ("merged", "parked")
EVENT_FIELDS = (
    "ts",
    "repo",
    "bead_id",
    "event",
    "lane",
    "provider",
    "model",
    "tier",
    "effort",
    "complexity",
    "risk_class",
    "operating_mode",
    "routing_profile",
    "assurance_profile",
    "release_stage",
    "duration_s",
    "host",
    "detail",
)
LEGACY_EVENTS = {"dispatch": "dispatch", "complete": "close", "limit": "limit"}


class MetricsError(RuntimeError):
    """Ledger data is malformed or has failed integrity checks."""


def canonical_json(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
        + "\n"
    ).encode("utf-8")


def content_id(fields: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_json(fields)).hexdigest()


def now_ts() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def require_text(value: str | None, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise MetricsError(f"{label} must be a non-empty string")
    return value


def parse_duration(value: str | int | float | None) -> int | float | None:
    if value is None:
        return None
    try:
        parsed = float(value)
    except (TypeError, ValueError) as exc:
        raise MetricsError("duration_s must be numeric") from exc
    if parsed < 0 or parsed != parsed or parsed in (float("inf"), float("-inf")):
        raise MetricsError("duration_s must be finite and non-negative")
    return int(parsed) if parsed.is_integer() else parsed


def parse_detail(value: str | dict[str, Any] | None) -> dict[str, Any] | None:
    if value is None or isinstance(value, dict):
        return value
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError as exc:
        raise MetricsError(f"detail is not valid JSON: {exc}") from exc
    if not isinstance(parsed, dict):
        raise MetricsError("detail must be a JSON object")
    return parsed


def make_record(fields: dict[str, Any]) -> dict[str, Any]:
    ordered = {name: fields.get(name) for name in EVENT_FIELDS}
    require_text(ordered["ts"], "ts")
    require_text(ordered["repo"], "repo")
    require_text(ordered["bead_id"], "bead_id")
    event = require_text(ordered["event"], "event")
    if event not in EVENTS:
        raise MetricsError(f"event must be one of {', '.join(EVENTS)}")
    ordered["duration_s"] = parse_duration(ordered["duration_s"])
    ordered["detail"] = parse_detail(ordered["detail"])
    return {"id": content_id(ordered), **ordered}


def validate_record(value: Any, line_number: int | None = None) -> dict[str, Any]:
    label = f"line {line_number}: " if line_number is not None else ""
    if not isinstance(value, dict):
        raise MetricsError(f"{label}record must be a JSON object")
    expected_keys = {"id", *EVENT_FIELDS}
    if set(value) != expected_keys:
        raise MetricsError(f"{label}record fields do not match schema")
    try:
        record = make_record({name: value[name] for name in EVENT_FIELDS})
    except MetricsError as exc:
        raise MetricsError(f"{label}{exc}") from exc
    if value["id"] != record["id"]:
        raise MetricsError(f"{label}content id mismatch")
    return value


def load_ledger(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    records = []
    seen: set[str] = set()
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise MetricsError(f"cannot read {path}: {exc}") from exc
    for line_number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            raise MetricsError(f"line {line_number}: invalid JSON: {exc}") from exc
        record = validate_record(value, line_number)
        if record["id"] in seen:
            raise MetricsError(f"line {line_number}: duplicate content id")
        seen.add(record["id"])
        records.append(record)
    return records


def append_record(path: Path, record: dict[str, Any]) -> bool:
    records = load_ledger(path)
    if any(existing["id"] == record["id"] for existing in records):
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("ab") as handle:
            handle.write(canonical_json(record))
            handle.flush()
    except OSError as exc:
        raise MetricsError(f"cannot append to {path}: {exc}") from exc
    return True


def iso_seconds(start: str | None, end: str | None) -> int | None:
    if not start or not end:
        return None
    try:
        left = datetime.fromisoformat(start.replace("Z", "+00:00"))
        right = datetime.fromisoformat(end.replace("Z", "+00:00"))
    except ValueError:
        return None
    return max(0, int((right - left).total_seconds()))


def build_rollups(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for record in records:
        grouped.setdefault((record["repo"], record["bead_id"]), []).append(record)
    rollups = []
    for (repo, bead_id), events in sorted(grouped.items()):
        events.sort(key=lambda row: (row["ts"], row["id"]))
        dispatch = next((row for row in events if row["event"] == "dispatch"), None)
        close = next((row for row in reversed(events) if row["event"] == "close"), None)
        reviews = [row for row in events if row["event"] == "review"]
        gates = [row for row in events if row["event"] in ("gate_pass", "gate_fail")]

        blockers = 0
        nonblockers = 0
        for review in reviews:
            detail = review["detail"] or {}
            blockers += int(detail.get("blockers", 0))
            nonblockers += int(detail.get("nonblockers", 0))

        close_detail = (close or {}).get("detail") or {}
        outcome = close_detail.get("outcome")
        if outcome not in OUTCOMES:
            outcome = None
        first = dispatch or events[0]
        dispatched_at = dispatch["ts"] if dispatch else None
        closed_at = close["ts"] if close else None
        rollups.append(
            {
                "repo": repo,
                "bead_id": bead_id,
                "complexity": first["complexity"],
                "risk_class": first["risk_class"],
                "lane": first["lane"],
                "provider": first["provider"],
                "model": first["model"],
                "tier": first["tier"],
                "effort": first["effort"],
                "dispatched_at": dispatched_at,
                "closed_at": closed_at,
                "active_seconds": iso_seconds(dispatched_at, closed_at),
                "gate_runs": len(gates),
                "gate_failures": sum(
                    row["event"] == "gate_fail" for row in gates
                ),
                "review_rounds": len(reviews),
                "blockers": blockers,
                "nonblockers": nonblockers,
                "outcome": outcome,
            }
        )
    return rollups


def write_json(value: Any, out: str | None = None) -> None:
    text = json.dumps(value, indent=2, sort_keys=True) + "\n"
    if out:
        path = Path(out)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


def event_from_args(args: argparse.Namespace) -> dict[str, Any]:
    fields = {
        name: getattr(args, name, None)
        for name in EVENT_FIELDS
    }
    fields["ts"] = fields["ts"] or now_ts()
    fields["host"] = fields["host"] or socket.gethostname()
    return make_record(fields)


def run_append(args: argparse.Namespace) -> int:
    try:
        record = event_from_args(args)
        appended = append_record(Path(args.ledger), record)
        write_json({"appended": appended, "id": record["id"]})
    except Exception as exc:  # capture must never stop delivery
        print(f"metrics-ledger: append skipped: {exc}", file=sys.stderr)
    return 0


def run_check(args: argparse.Namespace) -> int:
    records = load_ledger(Path(args.ledger))
    write_json({"schemaVersion": SCHEMA_VERSION, "events": len(records)})
    return 0


def run_rollup(args: argparse.Namespace) -> int:
    records = load_ledger(Path(args.ledger))
    write_json(
        {
            "schemaVersion": SCHEMA_VERSION,
            "stories": build_rollups(records),
        },
        args.out,
    )
    return 0


def run_backfill(args: argparse.Namespace) -> int:
    usage_path = Path(args.usage_ledger)
    if not usage_path.exists():
        write_json({"appended": 0, "duplicates_skipped": 0, "invalid_skipped": 0})
        return 0
    appended = duplicates = invalid = 0
    for line_number, line in enumerate(
        usage_path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        if not line.strip():
            continue
        try:
            legacy = json.loads(line)
            event = LEGACY_EVENTS[legacy["event"]]
            record = make_record(
                {
                    "ts": legacy["ts"],
                    "repo": args.repo,
                    "bead_id": legacy["story"],
                    "event": event,
                    "lane": legacy.get("lane"),
                    "provider": legacy.get("provider"),
                    "model": legacy.get("model"),
                    "tier": legacy.get("tier"),
                    "effort": legacy.get("effort"),
                    "host": legacy.get("host", "legacy"),
                    "detail": None,
                }
            )
            if append_record(Path(args.ledger), record):
                appended += 1
            else:
                duplicates += 1
        except (KeyError, TypeError, json.JSONDecodeError, MetricsError) as exc:
            invalid += 1
            print(
                f"metrics-ledger: backfill skipped line {line_number}: {exc}",
                file=sys.stderr,
            )
    write_json(
        {
            "appended": appended,
            "duplicates_skipped": duplicates,
            "invalid_skipped": invalid,
        }
    )
    return 0


def add_common_event_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--ledger", default=str(DEFAULT_LEDGER))
    parser.add_argument("--ts")
    parser.add_argument("--repo", required=True)
    parser.add_argument("--bead-id", required=True)
    parser.add_argument("--event", required=True)
    for name in (
        "lane",
        "provider",
        "model",
        "tier",
        "effort",
        "complexity",
        "risk-class",
        "operating-mode",
        "routing-profile",
        "assurance-profile",
        "release-stage",
        "duration-s",
        "host",
        "detail",
    ):
        parser.add_argument(f"--{name}", dest=name.replace("-", "_"))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    append = commands.add_parser("append")
    add_common_event_args(append)
    check = commands.add_parser("check")
    check.add_argument("--ledger", default=str(DEFAULT_LEDGER))
    rollup = commands.add_parser("rollup")
    rollup.add_argument("--ledger", default=str(DEFAULT_LEDGER))
    rollup.add_argument("--out")
    backfill = commands.add_parser("backfill")
    backfill.add_argument("--repo", required=True)
    backfill.add_argument("--usage-ledger", default=str(DEFAULT_USAGE_LEDGER))
    backfill.add_argument("--ledger", default=str(DEFAULT_LEDGER))
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return {
            "append": run_append,
            "check": run_check,
            "rollup": run_rollup,
            "backfill": run_backfill,
        }[args.command](args)
    except (MetricsError, OSError) as exc:
        print(f"metrics-ledger: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
