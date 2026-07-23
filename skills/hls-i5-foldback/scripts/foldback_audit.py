#!/usr/bin/env python3
"""Generate and validate exhaustive commit-path i5 fold-back ledgers."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

SKILL = Path(__file__).resolve().parents[1]
DEFAULT_BASELINE = SKILL / "references" / "baseline.json"
ALLOWED_DISPOSITIONS = {"port", "adapt", "present", "reject"}


class AuditError(RuntimeError):
    """The source history or disposition ledger violates the audit contract."""


def read_json(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise AuditError(f"{label} is unreadable or invalid JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise AuditError(f"{label} must be a JSON object")
    return value


def git(repo: Path, *args: str, check: bool = True) -> str:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo), *args],
            capture_output=True,
            check=False,
            text=True,
            timeout=60,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise AuditError(f"cannot run git: {exc}") from exc
    if check and result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        raise AuditError(f"git {' '.join(args)} failed: {detail}")
    return result.stdout.strip()


def load_baseline(path: Path) -> dict[str, Any]:
    baseline = read_json(path, "baseline")
    if baseline.get("schemaVersion") != 1:
        raise AuditError("baseline schemaVersion must be 1")
    upstream = baseline.get("upstream")
    areas = baseline.get("selectedAreas")
    if not isinstance(upstream, dict) or not isinstance(upstream.get("commit"), str):
        raise AuditError("baseline must declare upstream.commit")
    if not isinstance(areas, dict) or not areas:
        raise AuditError("baseline must declare selectedAreas")
    if set(baseline.get("dispositions", [])) != ALLOWED_DISPOSITIONS:
        raise AuditError("baseline dispositions do not match the audit contract")
    return baseline


def resolve_commit(repo: Path, revision: str) -> str:
    return git(repo, "rev-parse", f"{revision}^{{commit}}")


def suggested_areas(
    baseline: dict[str, Any], subject: str, paths: list[str]
) -> list[str]:
    haystack_paths = "\n".join(paths).lower()
    haystack_message = subject.lower()
    matches = []
    for code, config in baseline["selectedAreas"].items():
        path_terms = config.get("pathTerms", [])
        message_terms = config.get("messageTerms", [])
        if any(str(term).lower() in haystack_paths for term in path_terms) or any(
            str(term).lower() in haystack_message for term in message_terms
        ):
            matches.append(code)
    return sorted(matches)


def changed_paths(repo: Path, commit: str) -> list[dict[str, str]]:
    output = git(
        repo,
        "diff-tree",
        "--root",
        "--no-commit-id",
        "--name-status",
        "-r",
        "-M",
        commit,
    )
    rows = []
    for line in output.splitlines():
        fields = line.split("\t")
        if not fields or not fields[0]:
            continue
        status = fields[0]
        if status.startswith(("R", "C")) and len(fields) == 3:
            rows.append(
                {
                    "changeType": status,
                    "path": fields[2],
                    "previousPath": fields[1],
                }
            )
        elif len(fields) == 2:
            rows.append({"changeType": status, "path": fields[1]})
        else:
            raise AuditError(f"cannot parse diff-tree row: {line!r}")
    return rows


def verify_range(source: Path, base: str, target: str) -> None:
    ancestor = subprocess.run(
        ["git", "-C", str(source), "merge-base", "--is-ancestor", base, target],
        capture_output=True,
        check=False,
        text=True,
        timeout=60,
    )
    if ancestor.returncode != 0:
        raise AuditError(f"target {target} does not descend from baseline {base}")


def history_entries(
    source: Path, base: str, target: str, baseline: dict[str, Any]
) -> tuple[list[str], list[dict[str, Any]]]:
    verify_range(source, base, target)
    commits = git(
        source, "rev-list", "--reverse", "--topo-order", f"{base}..{target}"
    ).splitlines()
    entries: list[dict[str, Any]] = []
    for commit in commits:
        subject = git(source, "show", "-s", "--format=%s", commit)
        changes = changed_paths(source, commit)
        paths = [
            item.get("previousPath", "") + "\n" + item["path"] for item in changes
        ]
        hints = suggested_areas(baseline, subject, paths)
        for item in changes:
            entries.append(
                {
                    "id": f"{commit}:{item['path']}",
                    "commit": commit,
                    "subject": subject,
                    **item,
                    "suggestedAreas": hints,
                    "disposition": None,
                    "selectedArea": None,
                    "rationale": None,
                    "hlsEvidence": [],
                }
            )
    return commits, entries


def scan(source: Path, revision: str, baseline_path: Path, out: Path) -> int:
    baseline = load_baseline(baseline_path)
    base = resolve_commit(source, baseline["upstream"]["commit"])
    target = resolve_commit(source, revision)
    commits, entries = history_entries(source, base, target, baseline)

    ledger = {
        "schemaVersion": 1,
        "baselineCommit": base,
        "targetCommit": target,
        "auditUnit": "commit-path",
        "entries": entries,
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(ledger, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "status": "generated",
                "commits": len(commits),
                "entries": len(entries),
                "out": str(out),
            },
            sort_keys=True,
        )
    )
    return 0


def validate_ledger(ledger: dict[str, Any], baseline: dict[str, Any]) -> dict[str, int]:
    if ledger.get("schemaVersion") != 1:
        raise AuditError("ledger schemaVersion must be 1")
    if ledger.get("baselineCommit") != baseline["upstream"]["commit"]:
        raise AuditError("ledger baseline does not match the pinned upstream commit")
    if ledger.get("auditUnit") != "commit-path":
        raise AuditError("ledger auditUnit must be commit-path")
    target = ledger.get("targetCommit")
    if not isinstance(target, str) or len(target) != 40:
        raise AuditError("ledger targetCommit must be a full SHA")
    entries = ledger.get("entries")
    if not isinstance(entries, list):
        raise AuditError("ledger entries must be an array")

    counts = {name: 0 for name in sorted(ALLOWED_DISPOSITIONS)}
    ids: set[str] = set()
    areas = set(baseline["selectedAreas"])
    for index, entry in enumerate(entries):
        label = f"entry {index + 1}"
        if not isinstance(entry, dict):
            raise AuditError(f"{label} must be an object")
        identifier = entry.get("id")
        if not isinstance(identifier, str) or not identifier:
            raise AuditError(f"{label} has no id")
        if identifier in ids:
            raise AuditError(f"duplicate ledger id {identifier}")
        ids.add(identifier)
        disposition = entry.get("disposition")
        if disposition not in ALLOWED_DISPOSITIONS:
            raise AuditError(f"{identifier} has no valid disposition")
        rationale = entry.get("rationale")
        if not isinstance(rationale, str) or not rationale.strip():
            raise AuditError(f"{identifier} requires a rationale")
        evidence = entry.get("hlsEvidence")
        selected = entry.get("selectedArea")
        if disposition in {"port", "adapt", "present"}:
            if selected not in areas:
                raise AuditError(f"{identifier} requires one selectedArea")
            if (
                not isinstance(evidence, list)
                or not evidence
                or not all(isinstance(item, str) and item for item in evidence)
            ):
                raise AuditError(f"{identifier} requires HLS evidence paths")
        elif selected is not None and selected not in areas:
            raise AuditError(f"{identifier} names unknown selectedArea {selected!r}")
        counts[disposition] += 1
    return counts


def check(source: Path, ledger_path: Path, baseline_path: Path) -> int:
    baseline = load_baseline(baseline_path)
    ledger = read_json(ledger_path, "ledger")
    base = resolve_commit(source, baseline["upstream"]["commit"])
    target = resolve_commit(source, str(ledger.get("targetCommit", "")))
    _, expected = history_entries(source, base, target, baseline)
    stable_fields = (
        "id",
        "commit",
        "subject",
        "changeType",
        "path",
        "previousPath",
        "suggestedAreas",
    )

    def stable(entry: dict[str, Any]) -> dict[str, Any]:
        return {name: entry[name] for name in stable_fields if name in entry}

    actual_entries = ledger.get("entries")
    if not isinstance(actual_entries, list) or [
        stable(entry) for entry in actual_entries if isinstance(entry, dict)
    ] != [stable(entry) for entry in expected]:
        raise AuditError(
            "ledger rows do not exactly match the reconstructed upstream delta"
        )
    counts = validate_ledger(ledger, baseline)
    print(
        json.dumps(
            {
                "status": "pass",
                "entries": sum(counts.values()),
                "dispositions": counts,
                "targetCommit": ledger["targetCommit"],
            },
            sort_keys=True,
        )
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", default=str(DEFAULT_BASELINE))
    subparsers = parser.add_subparsers(dest="command", required=True)
    scan_parser = subparsers.add_parser("scan")
    scan_parser.add_argument("--source", required=True)
    scan_parser.add_argument("--to", required=True)
    scan_parser.add_argument("--out", required=True)
    check_parser = subparsers.add_parser("check")
    check_parser.add_argument("--source", required=True)
    check_parser.add_argument("--ledger", required=True)
    args = parser.parse_args()
    try:
        if args.command == "scan":
            return scan(
                Path(args.source),
                args.to,
                Path(args.baseline),
                Path(args.out),
            )
        return check(Path(args.source), Path(args.ledger), Path(args.baseline))
    except (AuditError, OSError, subprocess.SubprocessError) as exc:
        print(f"foldback-audit: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
