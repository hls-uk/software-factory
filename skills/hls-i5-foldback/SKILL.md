---
name: hls-i5-foldback
description: Audit changes after the pinned i5-software-factory baseline and selectively fold only HLS's context efficiency, rapid hardening, local metrics, embedded toolchain, and optional GLM Claude-harness subset into the single-operator factory. Use when i5 evolves and HLS needs an exhaustive delta ledger before deciding what to port.
---

# HLS i5 Fold-back

Audit first, classify every upstream commit-path change, then port only the
approved subset. HLS serves one human across several laptops/VPS hosts; never
copy i5's 5+-person governance or external control-plane assumptions.

Read [references/baseline.json](references/baseline.json) and
[references/port-policy.md](references/port-policy.md) before inspecting the
upstream repo.

## 1. Establish both repositories

- Treat the current HLS tree as valuable state. Inspect status and active Beads
  work before editing; never reset, clean, or overwrite it.
- Resolve the i5 source locally. The common sibling-path hint is only a hint;
  the baseline's full commit SHA
  `1d202c66f5fbc18add19531dd3f7f9db30744804` is authoritative.
- Confirm the requested upstream revision exists and descends from the pinned
  i5 baseline. Do not fetch or change remotes without authority.
- Create/claim one HLS Bead for the audit and dependent Beads for accepted
  tranches. Beads is the ledger of execution; the generated disposition file
  is the exhaustive source-delta record.

## 2. Generate the exhaustive delta

Run from the HLS repo:

```sh
python3 <skill-dir>/scripts/foldback_audit.py scan \
  --source <local-i5-repo> --to <new-i5-revision> \
  --out <repo-approved-evidence-path>/i5-foldback-ledger.json
```

The deterministic ledger has one row per changed path per upstream commit.
This is intentionally broader than the selected subset: nothing may disappear
because a file-name heuristic missed it.

## 3. Classify before porting

For every ledger row, record exactly one disposition:

- `port` — reproduce the upstream behavior substantially as written;
- `adapt` — carry the capability but change team/server/control-plane
  assumptions for HLS;
- `present` — HLS already has equivalent behavior; cite exact HLS evidence;
- `reject` — outside the five-area subset or incompatible with HLS; explain.

`port`, `adapt`, and `present` require a selected area and HLS evidence paths.
Every disposition requires a rationale. Suggested areas are hints only;
inspect the actual commit and diff. Validate the completed ledger:

```sh
python3 <skill-dir>/scripts/foldback_audit.py check \
  --source <local-i5-repo> \
  --ledger <repo-approved-evidence-path>/i5-foldback-ledger.json
```

`check` reconstructs the baseline-to-target history and rejects missing,
extra, changed, or reordered rows before validating dispositions. Do not edit
a selected skill until it reports that every upstream change is classified.
Record the checked ledger path and summary in the audit Bead.

## 4. Port only the HLS subset

The only eligible areas are:

- `CE` — context P0–P4 and deterministic context budgets;
- `RH` — executable delivery contract, diff-risk recheck, deterministic rapid
  sampling;
- `LM` — local append-only metrics, integrity checks, offline JSON rollups;
- `TC` — exact embedded Beads toolchain policy and offline checker;
- `GLM` — optional, labelled GLM-5.2 through Claude Code, disabled until local
  auth/billing/model probes pass.

Apply the adaptation table and exclusions in the port policy literally. Port
behavior and tests, not i5 names or team topology. Keep all skills
self-contained and agent-neutral; harness-specific material belongs only in a
clearly labelled variant.

After every skill edit, run the HLS skill validator. Update the changed skill's
CHANGELOG line, the Factory Method when process changes, catalog/index, and the
newest-first session log. Never copy secrets or live credentials.

## 5. Prove and advance the baseline

Run proportionate focused tests plus the repository release gates: skill
validation; delivery-contract, metrics, context, review-packet, and toolchain
suites; offline metrics proof; local install/discovery; `git diff --check`;
and `git status`. Add exclusion scans proving no SD/team/control-plane residue
was introduced.

Close implementation Beads only with exact commands/results. Advance
`references/baseline.json` to the audited full i5 commit only after every
ledger row is classified, every accepted change is implemented or explicitly
`present`, tests are green, release docs are updated, and the audit Bead cites
the durable ledger. A baseline change is itself a skill edit and must be
validated.

Do not commit, push, publish, fetch, install, probe credentials/network
services, or change external systems unless current authority explicitly
allows it. Stop for unavailable source, conflicting existing work,
destructive/credential/external needs, or an approval gate; otherwise continue.
