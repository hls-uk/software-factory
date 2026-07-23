#!/usr/bin/env python3
"""Measure and enforce the HLS factory's static context budgets.

This is a deterministic file-size proxy (UTF-8 characters / 4), plus optional
host-local probes. It never changes host or repository configuration.

Usage:
  python3 scripts/context-baseline.py
  python3 scripts/context-baseline.py --check
  python3 scripts/context-baseline.py --probe
  python3 scripts/context-baseline.py --probe-lane <lane-id>
  python3 scripts/context-baseline.py --memory-tokens <observed-host-value>
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

REPO = Path.cwd().resolve()
CHARS_PER_TOKEN = 4

SKILL_BUDGET = 6_000
REFERENCE_BUDGET = 5_000
BUNDLE_BUDGET = 26_000
LANE_BUDGET = 30_000
WORKING_SETS = {
    "hls-factory-orchestrate": (
        ["SKILL.md", "references/parallel-dispatch.md"],
        10_000,
    )
}


def tokens(characters: int) -> int:
    """Return the stable coarse token estimate used by the gate."""
    return round(characters / CHARS_PER_TOKEN)


def size(path: Path) -> int:
    return len(path.read_text(encoding="utf-8")) if path.is_file() else 0


def bundle(skill: str) -> dict[str, int]:
    root = REPO / "skills" / skill
    result = {"SKILL.md": size(root / "SKILL.md")}
    references = root / "references"
    if references.is_dir():
        for path in sorted(references.glob("*.md")):
            result[f"references/{path.name}"] = size(path)
    return result


def markdown_sizes(directory: Path) -> tuple[int, int, int, int]:
    values = sorted(size(path) for path in directory.glob("*.md"))
    if not values:
        return (0, 0, 0, 0)
    return (len(values), values[0], values[len(values) // 2], values[-1])


def table(title: str, rows: list[tuple[str, int]]) -> None:
    print(f"\n## {title}\n")
    print("| source | chars | ~tokens |")
    print("|---|---:|---:|")
    for name, characters in sorted(rows, key=lambda row: -row[1]):
        print(f"| {name} | {characters:,} | {tokens(characters):,} |")
    total = sum(characters for _, characters in rows)
    print(f"| **total** | **{total:,}** | **{tokens(total):,}** |")


def check_budgets() -> int:
    violations: list[str] = []
    for skill_dir in sorted((REPO / "skills").iterdir()):
        if not (skill_dir / "SKILL.md").is_file():
            continue
        files = bundle(skill_dir.name)
        for name, characters in files.items():
            estimate = tokens(characters)
            budget = SKILL_BUDGET if name == "SKILL.md" else REFERENCE_BUDGET
            if estimate > budget:
                violations.append(
                    f"{skill_dir.name}/{name}: {estimate:,} > {budget:,} tokens"
                )
        bundle_tokens = tokens(sum(files.values()))
        if bundle_tokens > BUNDLE_BUDGET:
            violations.append(
                f"{skill_dir.name} bundle: {bundle_tokens:,} > "
                f"{BUNDLE_BUDGET:,} tokens"
            )
        if skill_dir.name in WORKING_SETS:
            names, budget = WORKING_SETS[skill_dir.name]
            working_tokens = tokens(sum(files.get(name, 0) for name in names))
            if working_tokens > budget:
                violations.append(
                    f"{skill_dir.name} working set ({'+'.join(names)}): "
                    f"{working_tokens:,} > {budget:,} tokens"
                )
    if violations:
        print("context budget violations:")
        for violation in violations:
            print(f"  FAIL {violation}")
        return 1
    print(
        "context budgets OK "
        "(SKILL <= 6K, reference <= 5K, working set <= 10K, bundle <= 26K)"
    )
    return 0


def probe_bd_prime() -> int:
    try:
        result = subprocess.run(
            ["bd", "prime"],
            capture_output=True,
            check=False,
            cwd=REPO,
            text=True,
            timeout=60,
        )
        return len(result.stdout)
    except (OSError, subprocess.SubprocessError) as exc:
        print(f"(bd prime probe failed: {exc})", file=sys.stderr)
        return 0


def load_lanes() -> list[dict[str, Any]]:
    lanes: list[dict[str, Any]] = []
    for path in (
        REPO / ".factory" / "agents.local.json",
        REPO / ".factory" / "agents.json",
    ):
        if not path.is_file():
            continue
        try:
            config = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise RuntimeError(f"cannot read {path}: {exc}") from exc
        for lane in config.get("implementers", []):
            if isinstance(lane, dict):
                lanes.append(lane)
        reviewer = config.get("reviewer")
        if isinstance(reviewer, dict) and reviewer.get("id"):
            lanes.append(reviewer)
    return lanes


def probe_lane(lane_id: str) -> int:
    try:
        lane = next(
            (item for item in load_lanes() if item.get("id") == lane_id), None
        )
    except RuntimeError as exc:
        print(exc)
        return 2
    if lane is None or not isinstance(lane.get("dispatch"), str):
        print(f"lane {lane_id!r} not found or has no dispatch command")
        return 2

    with tempfile.TemporaryDirectory() as directory:
        Path(directory, "goal.txt").write_text(
            "Reply with exactly: OK\n", encoding="utf-8"
        )
        command = f"{lane['dispatch']} --output-format json"
        try:
            result = subprocess.run(
                ["/bin/sh", "-lc", command],
                capture_output=True,
                check=False,
                cwd=directory,
                text=True,
                timeout=300,
            )
            payload = json.loads(result.stdout.strip().splitlines()[-1])
            usage = payload["usage"]
            total = sum(
                int(usage.get(name, 0))
                for name in (
                    "input_tokens",
                    "cache_creation_input_tokens",
                    "cache_read_input_tokens",
                )
            )
        except (
            OSError,
            subprocess.SubprocessError,
            ValueError,
            KeyError,
            IndexError,
            json.JSONDecodeError,
        ) as exc:
            print(f"lane probe failed: {exc}")
            return 2
    verdict = "OK" if total <= LANE_BUDGET else "FAIL"
    print(
        f"lane {lane_id}: total_context={total:,} tokens "
        f"(budget {LANE_BUDGET:,}) {verdict}"
    )
    return 0 if total <= LANE_BUDGET else 1


def report(probe: bool, memory_tokens: int) -> None:
    print("# HLS factory context baseline (characters / 4 token estimate)")
    orchestrate = bundle("hls-factory-orchestrate")
    table("Coordinator skill bundle", list(orchestrate.items()))
    working_names, _ = WORKING_SETS["hls-factory-orchestrate"]
    table(
        "Coordinator hot working set",
        [(name, orchestrate.get(name, 0)) for name in working_names],
    )

    overhead = [
        ("AGENTS.md", size(REPO / "AGENTS.md")),
        ("CLAUDE.md", size(REPO / "CLAUDE.md")),
    ]
    if probe:
        overhead.append(("bd prime output (live probe)", probe_bd_prime()))
    if memory_tokens:
        overhead.append(
            ("memory injection (caller-supplied observation)", memory_tokens * 4)
        )
    table("Every-session repo overhead", overhead)

    plans = markdown_sizes(REPO / "docs" / "plans")
    requirements = markdown_sizes(REPO / "docs" / "requirements")
    table(
        "Story inputs",
        [
            (
                f"plan median ({plans[0]} docs; "
                f"{tokens(plans[1]):,}-{tokens(plans[3]):,} token range)",
                plans[2],
            ),
            (
                f"requirements median ({requirements[0]} docs; "
                f"{tokens(requirements[1]):,}-{tokens(requirements[3]):,} range)",
                requirements[2],
            ),
            ("handoff goal target", 1_600),
        ],
    )
    print(
        "\nNotes: estimates are intentionally coarse and deterministic. "
        "Code, diffs, and live harness injection are excluded unless probed."
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--probe", action="store_true")
    parser.add_argument("--probe-lane", metavar="LANE_ID")
    parser.add_argument("--memory-tokens", type=int, default=0)
    args = parser.parse_args()
    if args.check:
        raise SystemExit(check_budgets())
    if args.probe_lane:
        raise SystemExit(probe_lane(args.probe_lane))
    if args.memory_tokens < 0:
        parser.error("--memory-tokens must be non-negative")
    report(args.probe, args.memory_tokens)


if __name__ == "__main__":
    main()
