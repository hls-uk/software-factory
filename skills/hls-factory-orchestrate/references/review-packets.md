# Deterministic Review Packets

Use this protocol whenever a story or promotion reaches independent review.
The reviewer prompt is a build artifact, not coordinator-authored prose. The
packet builder has no flags for adding, omitting, or reordering reviewer
inputs.

## Control boundary

The packet has two mechanically checked sources:

1. A review contract committed before the reviewed branch diverges, at
   `.factory/reviews/<review-id>.json`. It freezes the allowed input paths.
2. Git objects identified by full SHA. Source documents are read exactly from
   the merge base; verification and promotion evidence are read exactly from
   the reviewed head. Deltas obtain their blocker list only from the verified
   prior verdict carried in their packet lineage.

The builder renders one approved, fixed template for each review type. It
does not accept free-form emphasis, file lists, finding summaries, or extra
instructions. Never prefix or append coordinator commentary when dispatching
`prompt.txt`.

## Freeze the contract before implementation

Create the contract while cutting the story, commit it to the integration
base, then branch the story. Copy paths from the plan and its evidence-input
list; do not reinterpret that list at review time. Contract inputs must be in
the role/path order shown below.

Story contract:

```json
{
  "schemaVersion": 1,
  "reviewId": "story-42",
  "kind": "story",
  "inputs": [
    {"role": "story", "path": "docs/plans/payments-plan.md", "snapshot": "base"},
    {"role": "criteria", "path": "docs/requirements/payments.md", "snapshot": "base"},
    {"role": "spec", "path": "docs/design/token-binding.md", "snapshot": "base"},
    {"role": "verification", "path": "evidence/story-42/verification.md", "snapshot": "head"}
  ]
}
```

The story contract requires exactly one `story/base`, exactly one
`criteria/base`, every named `spec/base` in canonical path order, and at least
one `verification/head`. All inputs are UTF-8 text committed at the indicated
snapshot. The whole named file is bound; section extraction and pasted
summaries are forbidden.

Create the promotion contract before the integration branch diverges from
main. Its paths are frozen at the base but its changing evidence is read from
the promotion head:

```json
{
  "schemaVersion": 1,
  "reviewId": "promotion-payments-1",
  "kind": "promotion",
  "inputs": [
    {"role": "plan", "path": "docs/plans/payments-plan.md", "snapshot": "head"},
    {"role": "waivers", "path": "evidence/promotion/waivers.md", "snapshot": "head"}
  ]
}
```

## Build packets

Resolve `<skill-dir>` to the installed `hls-factory-orchestrate` directory.
Use the PR target's current SHA as `--base` and the PR's exact current head as
`--head`:

```sh
python3 <skill-dir>/scripts/review_packet.py build \
  --repo . --type story-full --review-id story-42 \
  --base <pr-base-sha> --head <pr-head-sha> \
  --out evidence/reviews/story-42/round-1
```

The full and promotion builders run one literal `git diff <fixed-flags>
<base>...<head> --` and record the expanded command in the manifest. Fixed
flags disable external diff/textconv, colour, rename heuristics, configurable
hunk algorithms/order/prefixes, and other machine-local presentation choices;
no flag selects a path. The builder resolves the merge base, reads the
canonical contract there, reads every contracted input from its declared
snapshot, and records byte counts plus SHA-256 hashes in canonical
`manifest.json`.

For remediation, keep the prior packet with its `verdict.json`. The next
packet infers its round, last-reviewed SHA, review id, and blocker list from
that verified lineage:

```sh
python3 <skill-dir>/scripts/review_packet.py build \
  --repo . --type story-delta --base <pr-base-sha> \
  --head <new-pr-head-sha> \
  --previous-packet evidence/reviews/story-42/round-1 \
  --out evidence/reviews/story-42/round-2
```

Delta packets use the same fixed flags with the literal
`<last-reviewed>..<head>` range. They require a `BLOCKED` prior verdict, carry
only its blockers into reviewer prose, content-address the complete prior
packet and verdict bytes as immutable nested lineage, and refuse a fourth
review round.

Build promotion packets with `--type promotion`, its promotion review id,
the actual main/base SHA, and the integration head SHA.

Every output directory contains exactly:

- `manifest.json` — canonical review type, round, full SHAs, Git command,
  contract, template, inputs, byte counts, and hashes;
- `packet.json` — the manifest hash and normalized plus raw prompt hashes;
- `prompt.txt` — the only text dispatched to the fresh reviewer session;
- `previous/` — delta packets only, containing the verified prior lineage.

After review, store the reviewer's JSON-only response as `verdict.json` in
the packet directory. Its fixed fields must match the `VERDICT CONTRACT`
inside `prompt.txt`; it also records reviewer identity, `fresh-session`,
`readOnly: true`, and structured findings. Do not hand-edit its bound hashes.

## Verify in CI

Keep packet evidence outside the reviewed branch—adding it to that branch
would move the head and invalidate the review. Transfer it as a CI/PR artifact
or other repo-approved immutable evidence, then run:

```sh
python3 <skill-dir>/scripts/review_packet.py verify \
  --repo . --packet <packet-dir> \
  --expected-review-id <story-or-promotion-id> \
  --expected-base <actual-pr-base-sha> \
  --expected-head <actual-pr-head-sha>
```

The base, head, and review id must come from the CI event or repository-owned
PR metadata, never from the coordinator's review post. Exit 0 means a valid
`PASS`; exit 3 means a structurally valid `BLOCKED`; exit 2 means invalid or
tampered evidence. Make exit 0 the required merge check.

Verification rebuilds the manifest and prompt from Git, checks template,
contract, input, diff, manifest, and prompt hashes, recursively checks delta
lineage, and validates verdict semantics. It rejects stale heads, wrong bases
or ranges, wrong review types/rounds, altered templates, noncanonical or
missing/extra/reordered inputs, truncated or selected diffs, PASS with a
blocker, BLOCKED without one, and delta findings outside changed files.

## Template governance

Templates live under `assets/review-templates/<version>/`; their hashes and
operator-approval records live in `assets/review-templates/registry.json`. The builder
hard-fails if a template hash differs or its approval status is not
`approved`.

A template change is the rulebook change. Add a new version rather than
silently replacing an approved template. In this single-operator factory,
the operator inspects the exact fixed prose as a dedicated repository change
and records the approval timestamp in the registry; an agent may propose but
never approve its own template change. Routine packet construction, review
dispatch, and PASS verification require no further approval. Version control,
the registry hash, and the packet verifier enforce the boundary without
inventing a second human or configuring an external service.

## Self-test

Run the lifecycle and tamper fixtures after changing the packet code,
templates, registry, contract, or verdict rules:

```sh
python3 <skill-dir>/scripts/test_review_packet.py -v
```
