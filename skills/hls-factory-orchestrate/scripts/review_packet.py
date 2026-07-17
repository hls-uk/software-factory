#!/usr/bin/env python3
"""Build and verify deterministic, content-addressed review packets."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path, PurePosixPath
from typing import Any


SCHEMA_VERSION = 1
SCRIPT_PATH = Path(__file__).resolve()
SKILL_ROOT = SCRIPT_PATH.parent.parent
TEMPLATE_ROOT = SKILL_ROOT / "assets" / "review-templates"
PROMPT_HASH_MARKER = "__FACTORY_PROMPT_SHA256_PLACEHOLDER__"
REVIEW_TYPES = ("story-full", "story-delta", "promotion")
TEMPLATE_VERSION = "v1"
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
REVIEW_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
ROLE_ORDER = {
    "story": 0,
    "criteria": 1,
    "spec": 2,
    "verification": 3,
    "plan": 0,
    "waivers": 1,
    "prior-blockers": 0,
}
PLACEHOLDERS = (
    "{{PACKET_SUMMARY}}",
    "{{MANIFEST}}",
    "{{INPUTS}}",
    "{{DIFF}}",
    "{{VERDICT_CONTRACT}}",
)
DIFF_FLAGS = (
    "--no-ext-diff",
    "--no-textconv",
    "--no-color",
    "--no-renames",
    "--no-indent-heuristic",
    "--diff-algorithm=myers",
    "-U3",
    "--inter-hunk-context=0",
    "--src-prefix=a/",
    "--dst-prefix=b/",
    "--submodule=short",
    "-O/dev/null",
)


class PacketError(RuntimeError):
    pass


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
        + "\n"
    ).encode("utf-8")


def load_json_bytes(data: bytes, label: str) -> Any:
    try:
        return json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise PacketError(f"{label} is not valid UTF-8 JSON: {exc}") from exc


def strict_object(value: Any, keys: set[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise PacketError(f"{label} must be a JSON object")
    actual = set(value)
    if actual != keys:
        missing = sorted(keys - actual)
        extra = sorted(actual - keys)
        raise PacketError(f"{label} keys differ; missing={missing}, extra={extra}")
    return value


def require_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise PacketError(f"{label} must be a non-empty string")
    return value


def require_sha(value: Any, label: str) -> str:
    text = require_string(value, label)
    if not SHA_RE.fullmatch(text):
        raise PacketError(f"{label} must be a full lowercase commit SHA")
    return text


def safe_repo_path(value: Any, label: str) -> str:
    text = require_string(value, label)
    path = PurePosixPath(text)
    if path.is_absolute() or ".." in path.parts or "." in path.parts:
        raise PacketError(f"{label} must be a normalized repo-relative path")
    if "\n" in text or "\r" in text or ":" in text:
        raise PacketError(f"{label} contains a forbidden character")
    return text


def git(repo: Path, *args: str) -> bytes:
    env = os.environ.copy()
    env.update({"LC_ALL": "C", "LANG": "C"})
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
        check=False,
    )
    if result.returncode:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        raise PacketError(f"git {' '.join(args)} failed: {detail}")
    return result.stdout


def resolve_commit(repo: Path, ref: str) -> str:
    resolved = git(repo, "rev-parse", "--verify", f"{ref}^{{commit}}").decode().strip()
    return require_sha(resolved, f"resolved commit for {ref}")


def merge_base(repo: Path, base: str, head: str) -> str:
    resolved = git(repo, "merge-base", base, head).decode().strip()
    return require_sha(resolved, "merge base")


def git_blob(repo: Path, commit: str, path: str) -> bytes:
    return git(repo, "show", f"{commit}:{path}")


def git_diff(repo: Path, expression: str) -> tuple[list[str], bytes]:
    command = ["git", "diff", *DIFF_FLAGS, expression, "--"]
    data = git(repo, "--no-pager", *command[1:])
    if not data:
        raise PacketError(f"review range {expression} has an empty diff")
    return command, data


def changed_files(repo: Path, expression: str) -> set[str]:
    raw = git(
        repo,
        "--no-pager",
        "diff",
        *DIFF_FLAGS,
        "--name-only",
        "-z",
        expression,
        "--",
    )
    try:
        return {item for item in raw.decode("utf-8").split("\0") if item}
    except UnicodeDecodeError as exc:
        raise PacketError("changed file names must be UTF-8") from exc


def canonical_contract_path(review_id: str) -> str:
    if not REVIEW_ID_RE.fullmatch(review_id):
        raise PacketError("review id must use letters, digits, dot, underscore, or hyphen")
    return f".factory/reviews/{review_id}.json"


def contract_sort_key(item: dict[str, Any]) -> tuple[int, str]:
    return ROLE_ORDER.get(str(item.get("role")), 999), str(item.get("path"))


def validate_contract(contract: Any, expected_kind: str, expected_id: str) -> dict[str, Any]:
    obj = strict_object(
        contract,
        {"schemaVersion", "reviewId", "kind", "inputs"},
        "review contract",
    )
    if type(obj["schemaVersion"]) is not int or obj["schemaVersion"] != SCHEMA_VERSION:
        raise PacketError("unsupported review contract schemaVersion")
    if obj["reviewId"] != expected_id:
        raise PacketError("review contract id does not match the requested review id")
    if obj["kind"] != expected_kind:
        raise PacketError(f"review contract kind must be {expected_kind}")
    if not isinstance(obj["inputs"], list):
        raise PacketError("review contract inputs must be an array")

    inputs: list[dict[str, Any]] = []
    for index, raw in enumerate(obj["inputs"]):
        item = strict_object(raw, {"role", "path", "snapshot"}, f"contract input {index}")
        role = require_string(item["role"], f"contract input {index}.role")
        path = safe_repo_path(item["path"], f"contract input {index}.path")
        snapshot = item["snapshot"]
        if snapshot not in ("base", "head"):
            raise PacketError(f"contract input {index}.snapshot must be base or head")
        inputs.append({"role": role, "path": path, "snapshot": snapshot})

    if inputs != sorted(inputs, key=contract_sort_key):
        raise PacketError("review contract inputs are not in canonical role/path order")
    paths = [item["path"] for item in inputs]
    if len(paths) != len(set(paths)):
        raise PacketError("review contract contains a duplicate input path")

    role_snapshots = [(item["role"], item["snapshot"]) for item in inputs]
    if expected_kind == "story":
        allowed = {"story", "criteria", "spec", "verification"}
        if any(role not in allowed for role, _ in role_snapshots):
            raise PacketError("story contract contains an unsupported input role")
        required = {
            ("story", "base"): 1,
            ("criteria", "base"): 1,
        }
        for pair, count in required.items():
            if role_snapshots.count(pair) != count:
                raise PacketError(f"story contract requires exactly one {pair} input")
        if role_snapshots.count(("verification", "head")) < 1:
            raise PacketError("story contract requires at least one verification/head input")
        if any(
            snapshot != ("head" if role == "verification" else "base")
            for role, snapshot in role_snapshots
        ):
            raise PacketError("story/criteria/spec inputs use base; verification uses head")
    else:
        if role_snapshots != [("plan", "head"), ("waivers", "head")]:
            raise PacketError("promotion contract requires plan/head then waivers/head")

    return {**obj, "inputs": inputs}


def load_registry() -> list[dict[str, Any]]:
    path = TEMPLATE_ROOT / "registry.json"
    raw = path.read_bytes()
    registry = strict_object(
        load_json_bytes(raw, str(path)), {"schemaVersion", "templates"}, "template registry"
    )
    if type(registry["schemaVersion"]) is not int or registry["schemaVersion"] != SCHEMA_VERSION or not isinstance(
        registry["templates"], list
    ):
        raise PacketError("invalid template registry schema")
    return registry["templates"]


def load_template(review_type: str) -> tuple[dict[str, Any], bytes]:
    matches = [
        item
        for item in load_registry()
        if isinstance(item, dict)
        and item.get("reviewType") == review_type
        and item.get("version") == TEMPLATE_VERSION
    ]
    if len(matches) != 1:
        raise PacketError(f"template registry must contain one {review_type}/{TEMPLATE_VERSION}")
    entry = strict_object(
        matches[0],
        {"version", "reviewType", "path", "sha256", "approval"},
        "template registry entry",
    )
    approval = strict_object(
        entry["approval"],
        {"status", "approvedBy", "approvedAt", "separationOfDuty"},
        "template approval",
    )
    if approval["status"] != "approved":
        raise PacketError(f"template {review_type}/{TEMPLATE_VERSION} lacks operator approval")
    require_string(approval["approvedBy"], "template approval.approvedBy")
    require_string(approval["approvedAt"], "template approval.approvedAt")
    if approval["separationOfDuty"] != "single-operator-versioned-template":
        raise PacketError("template approval lacks single-operator governance assertion")

    relative = safe_repo_path(entry["path"], "template path")
    path = SKILL_ROOT / relative
    try:
        path.resolve().relative_to(SKILL_ROOT.resolve())
    except ValueError as exc:
        raise PacketError("template path escapes the skill directory") from exc
    data = path.read_bytes()
    if sha256(data) != entry["sha256"]:
        raise PacketError(f"template hash mismatch for {relative}")
    for placeholder in PLACEHOLDERS:
        if data.count(placeholder.encode()) != 1:
            raise PacketError(f"template must contain {placeholder} exactly once")
    if PROMPT_HASH_MARKER.encode() in data:
        raise PacketError("template contains the reserved prompt hash marker")
    return entry, data


def template_manifest(entry: dict[str, Any]) -> dict[str, Any]:
    return {
        "approval": entry["approval"],
        "path": entry["path"],
        "sha256": entry["sha256"],
        "version": entry["version"],
    }


def contract_inputs(
    repo: Path, contract: dict[str, Any], base_snapshot: str, head: str
) -> tuple[list[dict[str, Any]], list[bytes]]:
    entries: list[dict[str, Any]] = []
    contents: list[bytes] = []
    for item in contract["inputs"]:
        commit = base_snapshot if item["snapshot"] == "base" else head
        content = git_blob(repo, commit, item["path"])
        try:
            content.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise PacketError(f"review input {item['path']} is not UTF-8 text") from exc
        entries.append(
            {
                "bytes": len(content),
                "commit": commit,
                "path": item["path"],
                "role": item["role"],
                "sha256": sha256(content),
                "snapshot": item["snapshot"],
            }
        )
        contents.append(content)
    return entries, contents


def blockers_from_verdict(verdict: dict[str, Any]) -> list[dict[str, Any]]:
    return [item for item in verdict["findings"] if item["severity"] == "blocker"]


def lineage_bytes(previous: dict[str, Any]) -> bytes:
    return canonical_json(
        {
            "packetBytes": previous["packetBytes"],
            "packetFileSha256": previous["packetFileSha256"],
            "verdictBytes": previous["verdictBytes"],
            "verdictFileSha256": previous["verdictFileSha256"],
        }
    )


def render_inputs(entries: list[dict[str, Any]], contents: list[bytes]) -> bytes:
    chunks: list[bytes] = []
    for index, (entry, content) in enumerate(zip(entries, contents, strict=True), 1):
        chunks.append(f"--- INPUT {index} ---\n".encode())
        chunks.append(canonical_json(entry))
        chunks.append(content)
        if not content.endswith(b"\n"):
            chunks.append(b"\n")
        chunks.append(f"--- END INPUT {index} ---\n".encode())
    return b"".join(chunks)


def verdict_contract(
    manifest: dict[str, Any], manifest_sha: str, prompt_sha: str
) -> dict[str, Any]:
    return {
        "findingKeys": ["severity", "file", "line", "summary", "evidence", "fix"],
        "findingSeverity": (
            ["blocker"]
            if manifest["reviewType"] == "story-delta"
            else ["blocker", "non-blocker"]
        ),
        "requiredVerdict": {
            "diffSha256": manifest["diff"]["sha256"],
            "head": manifest["range"]["head"],
            "manifestSha256": manifest_sha,
            "promptSha256": prompt_sha,
            "reviewId": manifest["reviewId"],
            "reviewType": manifest["reviewType"],
            "round": manifest["round"],
            "schemaVersion": SCHEMA_VERSION,
            "templateSha256": manifest["template"]["sha256"],
        },
        "reviewerKeys": ["identity", "independence", "readOnly"],
        "verdictKeys": [
            "schemaVersion",
            "factoryReview",
            "reviewId",
            "reviewType",
            "round",
            "head",
            "templateSha256",
            "manifestSha256",
            "promptSha256",
            "diffSha256",
            "reviewer",
            "findings",
        ],
    }


def fill_template(template: bytes, replacements: dict[str, bytes]) -> bytes:
    """Replace template-owned placeholders once without touching inserted bytes."""
    locations = sorted(
        (template.index(placeholder.encode()), placeholder, replacement)
        for placeholder, replacement in replacements.items()
    )
    chunks: list[bytes] = []
    cursor = 0
    for offset, placeholder, replacement in locations:
        token = placeholder.encode()
        chunks.extend((template[cursor:offset], replacement))
        cursor = offset + len(token)
    chunks.append(template[cursor:])
    return b"".join(chunks)


def render_prompt(
    template: bytes,
    manifest: dict[str, Any],
    contents: list[bytes],
    diff: bytes,
) -> tuple[bytes, str]:
    manifest_bytes = canonical_json(manifest)
    manifest_sha = sha256(manifest_bytes)
    input_bytes = render_inputs(manifest["inputs"], contents)

    def replacements(prompt_sha: str) -> dict[str, bytes]:
        summary = {
            "diffSha256": manifest["diff"]["sha256"],
            "head": manifest["range"]["head"],
            "manifestSha256": manifest_sha,
            "promptHashMode": "sha256-placeholder-normalized-v1",
            "promptSha256": prompt_sha,
            "reviewId": manifest["reviewId"],
            "reviewType": manifest["reviewType"],
            "round": manifest["round"],
            "templateSha256": manifest["template"]["sha256"],
        }
        return {
            "{{PACKET_SUMMARY}}": canonical_json(summary),
            "{{MANIFEST}}": manifest_bytes,
            "{{INPUTS}}": input_bytes,
            "{{DIFF}}": diff,
            "{{VERDICT_CONTRACT}}": canonical_json(
                verdict_contract(manifest, manifest_sha, prompt_sha)
            ),
        }

    normalized = fill_template(template, replacements(PROMPT_HASH_MARKER))
    prompt_sha = sha256(normalized)
    prompt = fill_template(template, replacements(prompt_sha))
    return prompt, prompt_sha


def initial_material(
    repo: Path, review_type: str, review_id: str, base_ref: str, head_ref: str
) -> tuple[dict[str, Any], list[bytes], bytes, bytes]:
    expected_kind = "story" if review_type == "story-full" else "promotion"
    base = resolve_commit(repo, base_ref)
    head = resolve_commit(repo, head_ref)
    common = merge_base(repo, base, head)
    contract_path = canonical_contract_path(review_id)
    contract_raw = git_blob(repo, common, contract_path)
    contract = validate_contract(
        load_json_bytes(contract_raw, contract_path), expected_kind, review_id
    )
    input_entries, contents = contract_inputs(repo, contract, common, head)
    expression = f"{base}...{head}"
    command, diff = git_diff(repo, expression)
    template_entry, template = load_template(review_type)
    manifest = {
        "contract": {
            "bytes": len(contract_raw),
            "commit": common,
            "path": contract_path,
            "sha256": sha256(contract_raw),
        },
        "diff": {
            "bytes": len(diff),
            "command": command,
            "sha256": sha256(diff),
        },
        "inputs": input_entries,
        "range": {
            "base": base,
            "head": head,
            "lastReviewed": None,
            "mergeBase": common,
            "mode": "three-dot",
        },
        "reviewId": review_id,
        "reviewType": review_type,
        "round": 1,
        "schemaVersion": SCHEMA_VERSION,
        "template": template_manifest(template_entry),
    }
    return manifest, contents, diff, template


def read_json_file(path: Path, label: str) -> tuple[dict[str, Any], bytes]:
    raw = path.read_bytes()
    value = load_json_bytes(raw, label)
    if not isinstance(value, dict):
        raise PacketError(f"{label} must be a JSON object")
    return value, raw


def validate_verdict(
    verdict: Any,
    manifest: dict[str, Any],
    packet: dict[str, Any],
    repo: Path,
) -> dict[str, Any]:
    obj = strict_object(
        verdict,
        {
            "schemaVersion",
            "factoryReview",
            "reviewId",
            "reviewType",
            "round",
            "head",
            "templateSha256",
            "manifestSha256",
            "promptSha256",
            "diffSha256",
            "reviewer",
            "findings",
        },
        "verdict",
    )
    expected = verdict_contract(manifest, packet["manifestSha256"], packet["promptSha256"])[
        "requiredVerdict"
    ]
    for key, value in expected.items():
        if type(obj[key]) is not type(value) or obj[key] != value:
            raise PacketError(f"verdict {key} does not match the packet")
    if obj["factoryReview"] not in ("PASS", "BLOCKED"):
        raise PacketError("factoryReview must be PASS or BLOCKED")

    reviewer = strict_object(
        obj["reviewer"], {"identity", "independence", "readOnly"}, "verdict reviewer"
    )
    require_string(reviewer["identity"], "verdict reviewer.identity")
    if reviewer["independence"] != "fresh-session" or reviewer["readOnly"] is not True:
        raise PacketError("verdict must attest to a fresh, read-only reviewer session")
    if not isinstance(obj["findings"], list):
        raise PacketError("verdict findings must be an array")

    findings: list[dict[str, Any]] = []
    allowed_severity = (
        {"blocker"} if manifest["reviewType"] == "story-delta" else {"blocker", "non-blocker"}
    )
    changed = (
        changed_files(repo, f"{manifest['range']['lastReviewed']}..{manifest['range']['head']}")
        if manifest["reviewType"] == "story-delta"
        else set()
    )
    for index, raw in enumerate(obj["findings"]):
        finding = strict_object(
            raw,
            {"severity", "file", "line", "summary", "evidence", "fix"},
            f"finding {index}",
        )
        if finding["severity"] not in allowed_severity:
            raise PacketError(f"finding {index} has a forbidden severity")
        file_name = safe_repo_path(finding["file"], f"finding {index}.file")
        if type(finding["line"]) is not int or finding["line"] < 1:
            raise PacketError(f"finding {index}.line must be a positive integer")
        for field in ("summary", "evidence", "fix"):
            require_string(finding[field], f"finding {index}.{field}")
        if changed and file_name not in changed:
            raise PacketError(f"delta finding {index} names a file outside the delta")
        findings.append(finding)

    blockers = [item for item in findings if item["severity"] == "blocker"]
    if obj["factoryReview"] == "PASS" and blockers:
        raise PacketError("PASS verdict contains blocker findings")
    if obj["factoryReview"] == "BLOCKED" and not blockers:
        raise PacketError("BLOCKED verdict contains no blocker findings")
    return {**obj, "findings": findings}


def verify_packet(
    repo: Path,
    packet_dir: Path,
    expected_head: str,
    expected_base: str,
    expected_review_id: str,
    require_verdict: bool = True,
) -> dict[str, Any]:
    if not packet_dir.is_dir():
        raise PacketError(f"packet directory does not exist: {packet_dir}")
    allowed = {"manifest.json", "packet.json", "prompt.txt"}
    if require_verdict:
        allowed.add("verdict.json")
    names = {item.name for item in packet_dir.iterdir()}
    if "previous" in names:
        allowed.add("previous")
    if names != allowed:
        raise PacketError(
            f"packet artifacts differ; missing={sorted(allowed - names)}, extra={sorted(names - allowed)}"
        )

    manifest, manifest_raw = read_json_file(packet_dir / "manifest.json", "manifest.json")
    if manifest_raw != canonical_json(manifest):
        raise PacketError("manifest.json is not canonical JSON")
    manifest = strict_object(
        manifest,
        {
            "schemaVersion",
            "reviewId",
            "reviewType",
            "round",
            "range",
            "contract",
            "template",
            "inputs",
            "diff",
        },
        "manifest",
    )
    if type(manifest["schemaVersion"]) is not int or manifest["schemaVersion"] != SCHEMA_VERSION:
        raise PacketError("unsupported manifest schemaVersion")
    review_type = manifest["reviewType"]
    if review_type not in REVIEW_TYPES:
        raise PacketError("unsupported manifest reviewType")
    if manifest["reviewId"] != expected_review_id:
        raise PacketError("packet review id does not match the expected review id")

    range_obj = strict_object(
        manifest["range"],
        {"base", "head", "lastReviewed", "mergeBase", "mode"},
        "manifest range",
    )
    head = require_sha(range_obj["head"], "manifest range.head")
    if head != expected_head:
        raise PacketError("packet head is stale or does not match the expected PR head")
    if resolve_commit(repo, head) != head:
        raise PacketError("manifest head is not present in the repository")

    template_entry, template = load_template(review_type)
    contents: list[bytes]
    if review_type in ("story-full", "promotion"):
        if type(manifest["round"]) is not int or manifest["round"] != 1 or range_obj["mode"] != "three-dot":
            raise PacketError("full and promotion packets must use round 1/three-dot")
        base = require_sha(range_obj["base"], "manifest range.base")
        common = require_sha(range_obj["mergeBase"], "manifest range.mergeBase")
        if base != expected_base:
            raise PacketError("packet base does not match the expected PR base")
        if range_obj["lastReviewed"] is not None:
            raise PacketError("full and promotion packets cannot set lastReviewed")
        if merge_base(repo, base, head) != common:
            raise PacketError("manifest merge base is stale or incorrect")
        review_id = require_string(manifest["reviewId"], "manifest reviewId")
        contract_path = canonical_contract_path(review_id)
        contract_raw = git_blob(repo, common, contract_path)
        contract_kind = "story" if review_type == "story-full" else "promotion"
        contract = validate_contract(
            load_json_bytes(contract_raw, contract_path), contract_kind, review_id
        )
        input_entries, contents = contract_inputs(repo, contract, common, head)
        command, diff = git_diff(repo, f"{base}...{head}")
        expected_manifest = {
            "contract": {
                "bytes": len(contract_raw),
                "commit": common,
                "path": contract_path,
                "sha256": sha256(contract_raw),
            },
            "diff": {"bytes": len(diff), "command": command, "sha256": sha256(diff)},
            "inputs": input_entries,
            "range": {
                "base": base,
                "head": head,
                "lastReviewed": None,
                "mergeBase": common,
                "mode": "three-dot",
            },
            "reviewId": review_id,
            "reviewType": review_type,
            "round": 1,
            "schemaVersion": SCHEMA_VERSION,
            "template": template_manifest(template_entry),
        }
    else:
        if type(manifest["round"]) is not int or manifest["round"] not in (2, 3):
            raise PacketError("delta packet round must be 2 or 3")
        if range_obj["mode"] != "two-dot" or range_obj["base"] is not None:
            raise PacketError("delta packets must use lastReviewed..head")
        if range_obj["mergeBase"] is not None:
            raise PacketError("delta packets cannot set mergeBase")
        last_reviewed = require_sha(
            range_obj["lastReviewed"], "manifest range.lastReviewed"
        )
        previous_dir = packet_dir / "previous"
        previous_manifest, _ = read_json_file(previous_dir / "manifest.json", "previous manifest")
        previous_head = previous_manifest.get("range", {}).get("head")
        if previous_head != last_reviewed:
            raise PacketError("delta lastReviewed does not match previous packet head")
        previous = verify_packet(
            repo,
            previous_dir,
            expected_head=last_reviewed,
            expected_base=expected_base,
            expected_review_id=expected_review_id,
            require_verdict=True,
        )
        previous_verdict = previous["verdict"]
        if previous_verdict["factoryReview"] != "BLOCKED":
            raise PacketError("delta packet requires a BLOCKED previous verdict")
        if previous["manifest"]["round"] + 1 != manifest["round"]:
            raise PacketError("delta round is not the next review round")
        blockers = blockers_from_verdict(previous_verdict)
        blocker_bytes = canonical_json(blockers)
        prior_lineage = lineage_bytes(previous)
        input_entries = [
            {
                "bytes": len(blocker_bytes),
                "commit": last_reviewed,
                "path": "previous/verdict.json#blockers",
                "role": "prior-blockers",
                "sha256": sha256(blocker_bytes),
                "snapshot": "last-reviewed",
            }
        ]
        contents = [blocker_bytes]
        command, diff = git_diff(repo, f"{last_reviewed}..{head}")
        expected_manifest = {
            "contract": {
                "bytes": len(prior_lineage),
                "commit": last_reviewed,
                "path": "previous/packet.json+verdict.json",
                "sha256": sha256(prior_lineage),
            },
            "diff": {"bytes": len(diff), "command": command, "sha256": sha256(diff)},
            "inputs": input_entries,
            "range": {
                "base": None,
                "head": head,
                "lastReviewed": last_reviewed,
                "mergeBase": None,
                "mode": "two-dot",
            },
            "reviewId": expected_review_id,
            "reviewType": "story-delta",
            "round": manifest["round"],
            "schemaVersion": SCHEMA_VERSION,
            "template": template_manifest(template_entry),
        }

    if canonical_json(manifest) != canonical_json(expected_manifest):
        raise PacketError("manifest does not match mechanically recomputed repository inputs")

    packet, packet_raw = read_json_file(packet_dir / "packet.json", "packet.json")
    if packet_raw != canonical_json(packet):
        raise PacketError("packet.json is not canonical JSON")
    packet = strict_object(
        packet,
        {
            "schemaVersion",
            "manifestSha256",
            "promptSha256",
            "promptFileSha256",
        },
        "packet record",
    )
    expected_manifest_sha = sha256(manifest_raw)
    if (
        type(packet["schemaVersion"]) is not int
        or packet["schemaVersion"] != SCHEMA_VERSION
        or packet["manifestSha256"] != expected_manifest_sha
    ):
        raise PacketError("packet record does not match manifest.json")

    prompt, prompt_sha = render_prompt(template, manifest, contents, diff)
    actual_prompt = (packet_dir / "prompt.txt").read_bytes()
    if actual_prompt != prompt:
        raise PacketError("prompt.txt differs from the mechanically rendered prompt")
    if packet["promptSha256"] != prompt_sha:
        raise PacketError("packet prompt hash does not match the rendered prompt")
    if packet["promptFileSha256"] != sha256(prompt):
        raise PacketError("packet raw prompt file hash does not match prompt.txt")

    verdict = None
    verdict_raw = b""
    if require_verdict:
        verdict_obj, verdict_raw = read_json_file(packet_dir / "verdict.json", "verdict.json")
        verdict = validate_verdict(verdict_obj, manifest, packet, repo)
    return {
        "manifest": manifest,
        "packet": packet,
        "packetBytes": len(packet_raw),
        "packetFileSha256": sha256(packet_raw),
        "verdictBytes": len(verdict_raw),
        "verdictFileSha256": sha256(verdict_raw) if verdict_raw else None,
        "verdict": verdict,
    }


def write_packet(
    output: Path,
    manifest: dict[str, Any],
    contents: list[bytes],
    diff: bytes,
    template: bytes,
    previous: Path | None = None,
) -> None:
    if output.exists():
        raise PacketError(f"output already exists: {output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix=f".{output.name}.", dir=output.parent))
    try:
        manifest_raw = canonical_json(manifest)
        prompt, prompt_sha = render_prompt(template, manifest, contents, diff)
        packet = {
            "manifestSha256": sha256(manifest_raw),
            "promptFileSha256": sha256(prompt),
            "promptSha256": prompt_sha,
            "schemaVersion": SCHEMA_VERSION,
        }
        (temporary / "manifest.json").write_bytes(manifest_raw)
        (temporary / "packet.json").write_bytes(canonical_json(packet))
        (temporary / "prompt.txt").write_bytes(prompt)
        if previous is not None:
            shutil.copytree(previous, temporary / "previous")
        temporary.replace(output)
    except Exception:
        shutil.rmtree(temporary, ignore_errors=True)
        raise


def build_delta_material(
    repo: Path, previous_dir: Path, head_ref: str, expected_base_ref: str
) -> tuple[dict[str, Any], list[bytes], bytes, bytes]:
    previous_manifest, _ = read_json_file(previous_dir / "manifest.json", "previous manifest")
    review_id = require_string(previous_manifest.get("reviewId"), "previous reviewId")
    previous_head = require_sha(
        previous_manifest.get("range", {}).get("head"), "previous range.head"
    )
    base = resolve_commit(repo, expected_base_ref)
    previous = verify_packet(
        repo,
        previous_dir,
        expected_head=previous_head,
        expected_base=base,
        expected_review_id=review_id,
        require_verdict=True,
    )
    prior_manifest = previous["manifest"]
    prior_verdict = previous["verdict"]
    if prior_verdict["factoryReview"] != "BLOCKED":
        raise PacketError("a remediation delta requires a BLOCKED previous verdict")
    round_number = prior_manifest["round"] + 1
    if round_number not in (2, 3):
        raise PacketError("review cap reached: initial review plus two deltas")
    head = resolve_commit(repo, head_ref)
    if head == previous_head:
        raise PacketError("delta head must differ from the last reviewed commit")
    blockers = blockers_from_verdict(prior_verdict)
    blocker_bytes = canonical_json(blockers)
    prior_lineage = lineage_bytes(previous)
    input_entries = [
        {
            "bytes": len(blocker_bytes),
            "commit": previous_head,
            "path": "previous/verdict.json#blockers",
            "role": "prior-blockers",
            "sha256": sha256(blocker_bytes),
            "snapshot": "last-reviewed",
        }
    ]
    command, diff = git_diff(repo, f"{previous_head}..{head}")
    template_entry, template = load_template("story-delta")
    manifest = {
        "contract": {
            "bytes": len(prior_lineage),
            "commit": previous_head,
            "path": "previous/packet.json+verdict.json",
            "sha256": sha256(prior_lineage),
        },
        "diff": {"bytes": len(diff), "command": command, "sha256": sha256(diff)},
        "inputs": input_entries,
        "range": {
            "base": None,
            "head": head,
            "lastReviewed": previous_head,
            "mergeBase": None,
            "mode": "two-dot",
        },
        "reviewId": review_id,
        "reviewType": "story-delta",
        "round": round_number,
        "schemaVersion": SCHEMA_VERSION,
        "template": template_manifest(template_entry),
    }
    return manifest, [blocker_bytes], diff, template


def build_command(args: argparse.Namespace) -> int:
    repo = Path(args.repo).resolve()
    output = Path(args.out).resolve()
    if args.type == "story-delta":
        if not args.previous_packet or not args.base or args.review_id:
            raise PacketError("story-delta requires --previous-packet and --base only")
        previous = Path(args.previous_packet).resolve()
        manifest, contents, diff, template = build_delta_material(
            repo, previous, args.head, args.base
        )
        write_packet(output, manifest, contents, diff, template, previous=previous)
    else:
        if not args.review_id or not args.base or args.previous_packet:
            raise PacketError(f"{args.type} requires --review-id and --base")
        manifest, contents, diff, template = initial_material(
            repo, args.type, args.review_id, args.base, args.head
        )
        write_packet(output, manifest, contents, diff, template)
    print(
        json.dumps(
            {
                "head": manifest["range"]["head"],
                "output": str(output),
                "reviewId": manifest["reviewId"],
                "reviewType": manifest["reviewType"],
                "round": manifest["round"],
            },
            sort_keys=True,
        )
    )
    return 0


def verify_command(args: argparse.Namespace) -> int:
    repo = Path(args.repo).resolve()
    result = verify_packet(
        repo,
        Path(args.packet).resolve(),
        expected_head=resolve_commit(repo, args.expected_head),
        expected_base=resolve_commit(repo, args.expected_base),
        expected_review_id=args.expected_review_id,
        require_verdict=True,
    )
    verdict = result["verdict"]
    print(
        json.dumps(
            {
                "factoryReview": verdict["factoryReview"],
                "head": result["manifest"]["range"]["head"],
                "manifestSha256": result["packet"]["manifestSha256"],
                "promptSha256": result["packet"]["promptSha256"],
                "reviewId": result["manifest"]["reviewId"],
                "reviewType": result["manifest"]["reviewType"],
                "round": result["manifest"]["round"],
                "valid": True,
            },
            sort_keys=True,
        )
    )
    return 0 if verdict["factoryReview"] == "PASS" else 3


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(
        description="Build or verify deterministic factory review packets."
    )
    subparsers = root.add_subparsers(dest="command", required=True)
    build = subparsers.add_parser("build")
    build.add_argument("--repo", default=".")
    build.add_argument("--type", choices=REVIEW_TYPES, required=True)
    build.add_argument("--review-id")
    build.add_argument("--base", help="PR base ref; required for every packet lineage")
    build.add_argument("--head", required=True)
    build.add_argument("--previous-packet")
    build.add_argument("--out", required=True)
    build.set_defaults(handler=build_command)

    verify = subparsers.add_parser("verify")
    verify.add_argument("--repo", default=".")
    verify.add_argument("--packet", required=True)
    verify.add_argument("--expected-head", required=True)
    verify.add_argument("--expected-base", required=True)
    verify.add_argument("--expected-review-id", required=True)
    verify.set_defaults(handler=verify_command)
    return root


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        return args.handler(args)
    except (OSError, PacketError) as exc:
        print(f"review-packet: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
