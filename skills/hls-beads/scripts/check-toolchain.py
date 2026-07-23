#!/usr/bin/env python3
"""Fail closed unless local embedded Beads matches the pinned manifest."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

SEMVER = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
CANDIDATE_STATUS = "qualified-pending-embedded-migration"
POLICY = {
    "writerPin": "exact",
    "mixedWritableClients": "deny",
    "migrationAuthority": "single-operator-one-clone-at-a-time",
    "candidateCheckCadence": "monthly",
    "promotionCadence": "operator-planned-or-security",
    "binaryAcquisition": "operator-managed",
}


class ToolchainError(RuntimeError):
    """The manifest or selected local client violates the contract."""


def object_value(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ToolchainError(f"{label} must be an object")
    return value


def exact_version(value: Any, label: str) -> str:
    if not isinstance(value, str) or not SEMVER.fullmatch(value):
        raise ToolchainError(f"{label} must be exact semver")
    return value


def track(value: Any, label: str, candidate: bool = False) -> dict[str, Any]:
    entry = object_value(value, label)
    allowed = {"version", "storageSchemaVersion"}
    if candidate:
        allowed |= {"status", "releaseUrl"}
    if set(entry) != allowed:
        raise ToolchainError(f"{label} fields do not match the embedded contract")
    exact_version(entry.get("version"), f"{label}.version")
    schema = entry.get("storageSchemaVersion")
    if not isinstance(schema, int) or isinstance(schema, bool) or schema < 1:
        raise ToolchainError(
            f"{label}.storageSchemaVersion must be a positive integer"
        )
    if candidate:
        if entry.get("status") != CANDIDATE_STATUS:
            raise ToolchainError(f"{label}.status must be {CANDIDATE_STATUS}")
        release = entry.get("releaseUrl")
        if not isinstance(release, str) or not release.startswith(
            "https://github.com/gastownhall/beads/releases/tag/v"
        ):
            raise ToolchainError(f"{label}.releaseUrl must be an official tag")
    return entry


def load_manifest(path: Path) -> dict[str, Any]:
    try:
        manifest = object_value(
            json.loads(path.read_text(encoding="utf-8")), "manifest"
        )
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ToolchainError(f"manifest is unreadable or invalid JSON: {exc}") from exc
    if set(manifest) != {"schemaVersion", "storageMode", "beads", "policy"}:
        raise ToolchainError("manifest fields do not match the embedded contract")
    if manifest.get("schemaVersion") != 1:
        raise ToolchainError("manifest schemaVersion must be 1")
    if manifest.get("storageMode") != "embedded":
        raise ToolchainError("storageMode must be embedded")

    beads = object_value(manifest.get("beads"), "beads")
    if set(beads) != {"promoted", "candidate"}:
        raise ToolchainError("beads fields must be promoted and candidate")
    promoted = track(beads.get("promoted"), "beads.promoted")
    candidate = beads.get("candidate")
    if candidate is not None:
        candidate = track(candidate, "beads.candidate", candidate=True)
        if (
            candidate["version"],
            candidate["storageSchemaVersion"],
        ) == (
            promoted["version"],
            promoted["storageSchemaVersion"],
        ):
            raise ToolchainError("candidate and promoted tracks must differ")
    if manifest.get("policy") != POLICY:
        raise ToolchainError("policy does not match the embedded fail-closed contract")
    return manifest


def client_version(binary: str) -> tuple[str, int]:
    try:
        completed = subprocess.run(
            [binary, "version", "--json"],
            capture_output=True,
            check=False,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise ToolchainError(f"cannot execute Beads client {binary!r}: {exc}") from exc
    if completed.returncode != 0:
        raise ToolchainError(f"Beads version probe exited {completed.returncode}")
    try:
        payload = object_value(json.loads(completed.stdout), "bd version output")
    except json.JSONDecodeError as exc:
        raise ToolchainError("Beads version probe did not return JSON") from exc
    version = exact_version(payload.get("version"), "bd version")
    schema = payload.get("schema_version")
    if not isinstance(schema, int) or isinstance(schema, bool) or schema < 1:
        raise ToolchainError("Beads version probe omitted a valid schema_version")
    return version, schema


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", default=".factory/toolchain.json")
    parser.add_argument("--bd", default="bd")
    parser.add_argument("--candidate", action="store_true")
    parser.add_argument("--manifest-only", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        manifest = load_manifest(Path(args.manifest))
        name = "candidate" if args.candidate else "promoted"
        selected = manifest["beads"].get(name)
        if selected is None:
            raise ToolchainError(f"no Beads {name} is declared")
        expected = (selected["version"], selected["storageSchemaVersion"])
        actual = expected if args.manifest_only else client_version(args.bd)
        if actual != expected:
            raise ToolchainError(
                "unsupported Beads version/schema "
                f"{actual[0]}/{actual[1]}; expected {name} "
                f"{expected[0]}/{expected[1]}"
            )
    except ToolchainError as exc:
        print(f"beads-toolchain: {exc}; failing closed", file=sys.stderr)
        return 1
    if args.json:
        print(
            json.dumps(
                {
                    "schemaVersion": 1,
                    "status": "pass",
                    "storageMode": "embedded",
                    "track": name,
                    "beads": actual[0],
                    "storageSchemaVersion": actual[1],
                },
                sort_keys=True,
            )
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
