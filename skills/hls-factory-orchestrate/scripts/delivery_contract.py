#!/usr/bin/env python3
"""Resolve and validate the four-field HLS delivery contract.

The contract lives at `.factory/agents.json`. Missing or invalid values resolve
to safe defaults; only an explicit valid `rapid` assurance can reduce review.
`deliveryProfile` remains a read alias for `modelRoutingProfile`.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

CONTRACT_RELATIVE = Path(".factory") / "agents.json"
OPERATING_MODES = ("supervised", "autonomous")
ROUTING_PROFILES = ("quality", "balanced", "throughput")
ASSURANCE_PROFILES = ("rapid", "standard", "assured")
RELEASE_STAGES = ("experiment", "beta", "operational", "canonical")
DEFAULTS = {
    "operatingMode": "supervised",
    "modelRoutingProfile": "balanced",
    "assuranceProfile": "standard",
    "releaseStage": "operational",
}
FIELDS = {
    "operatingMode": OPERATING_MODES,
    "modelRoutingProfile": ROUTING_PROFILES,
    "assuranceProfile": ASSURANCE_PROFILES,
    "releaseStage": RELEASE_STAGES,
}
SPOT_REVIEW_MIN = 3
SPOT_REVIEW_MAX = 10


class ContractError(RuntimeError):
    """The contract cannot be read safely."""


def contract_path(repo: str | Path = ".") -> Path:
    return Path(repo) / CONTRACT_RELATIVE


def load_raw(repo: str | Path = ".") -> dict[str, Any]:
    path = contract_path(repo)
    if not path.is_file():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ContractError(f"{path} is unreadable or invalid JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise ContractError(f"{path} must contain a JSON object")
    return value


def resolve(raw: dict[str, Any]) -> dict[str, Any]:
    resolved: dict[str, str] = {}
    sources: dict[str, str] = {}
    for field, allowed in FIELDS.items():
        declared = raw.get(field)
        if field == "modelRoutingProfile" and declared is None:
            declared = raw.get("deliveryProfile")
            source = "deliveryProfile alias" if declared is not None else "default"
        else:
            source = "declared" if declared is not None else "default"
        if isinstance(declared, str) and declared in allowed:
            resolved[field] = declared
            sources[field] = source
        else:
            resolved[field] = DEFAULTS[field]
            sources[field] = "default" if declared is None else "invalid-defaulted"
    return {"contract": resolved, "sources": sources}


def spot_review_rate(raw: dict[str, Any], assurance: str) -> int | None:
    if assurance != "rapid":
        return None
    rate = raw.get("spotReviewRate")
    if isinstance(rate, bool) or not isinstance(rate, int):
        return None
    return rate if SPOT_REVIEW_MIN <= rate <= SPOT_REVIEW_MAX else None


def read_contract(repo: str | Path = ".") -> dict[str, Any]:
    raw = load_raw(repo)
    result = resolve(raw)
    assurance = result["contract"]["assuranceProfile"]
    result["spotReviewRate"] = spot_review_rate(raw, assurance)
    result["declared"] = any(
        source != "default" for source in result["sources"].values()
    )
    return result


def invalid_fields(repo: str | Path = ".") -> list[str]:
    return [
        field
        for field, source in read_contract(repo)["sources"].items()
        if source == "invalid-defaulted"
    ]


def spot_review_problem(repo: str | Path = ".") -> str | None:
    raw = load_raw(repo)
    if "spotReviewRate" not in raw:
        return None
    assurance = resolve(raw)["contract"]["assuranceProfile"]
    rate = raw["spotReviewRate"]
    if assurance != "rapid":
        return (
            f"spotReviewRate is declared but assuranceProfile is "
            f"{assurance!r}, so it is ignored"
        )
    if isinstance(rate, bool) or not isinstance(rate, int):
        return (
            f"spotReviewRate must be an integer, not {type(rate).__name__}; "
            "full review applies"
        )
    if not SPOT_REVIEW_MIN <= rate <= SPOT_REVIEW_MAX:
        return (
            f"spotReviewRate {rate} is outside "
            f"{SPOT_REVIEW_MIN}-{SPOT_REVIEW_MAX}; full review applies"
        )
    return None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("show", "check"))
    parser.add_argument("--repo", default=".")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        result = read_contract(args.repo)
    except ContractError as exc:
        print(f"delivery-contract: {exc}", file=sys.stderr)
        return 1

    problems = []
    if args.command == "check":
        bad = [
            field
            for field, source in result["sources"].items()
            if source == "invalid-defaulted"
        ]
        if bad:
            problems.append(
                "invalid values defaulted to the safe end: " + ", ".join(sorted(bad))
            )
        sampling = spot_review_problem(args.repo)
        if sampling:
            problems.append(sampling)
        for problem in problems:
            print(f"delivery-contract: {problem}", file=sys.stderr)
        if problems:
            return 1

    if args.json or args.command == "show":
        print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
