# Dispatch Operations — preflight, ledgers, and limits

Occurrence-driven procedures split out of
[parallel-dispatch.md](parallel-dispatch.md) so the coordinator's always-loaded
context stays small. Read this file at run start, after lane configuration
changes, at checkpoints, and when a provider limit fires.

## Lane preflight

Preflight assumes the current host's lanes exist, are authenticated as
configured, and reflect that host's actual CLIs and models. Run the per-host
ritual in [lane-setup.md](lane-setup.md) when adding a laptop/VPS and after
any tool, model, subscription, or auth change.

Before the first dispatch of a run — and after any `agents.json` change —
probe every lane with a trivial exec ("Reply with exactly: OK") using the
lane's dispatch command verbatim. A lane that cannot answer cheaply will not
deliver a story expensively. The probe catches:

- model ids unavailable under the configured authentication mode;
- sandbox denial of build caches, services, or the Git common directory used
  by worktrees;
- a supervisor/non-login shell resolving a different binary than the
  interactive shell;
- required environment fixes missing from the exact command later goals will
  execute.

After the echo probe, run one build-tool probe through the same lane and
verify worktree Git access. Prefer absolute binary paths. Record redacted
results in Beads and the local metrics ledger. A failing lane is disabled with
a note, never worked around silently.

For Claude Code harness lanes, the verbatim command must carry
`--strict-mcp-config --setting-sources project`. A story-specific MCP server
must be declared at repo level or passed with an explicit `--mcp-config`.
After a harness or settings change, the optional live probe is:

```sh
python3 <skill-dir>/scripts/context_baseline.py --probe-lane <lane-id>
```

It requires the lane's normal local authentication and must stay at or below
30,000 input plus cache tokens. Never run a live lane probe without the
operator's existing authorization and local credentials.

## Offline append-only metrics

`.factory/metrics.jsonl` is the structured, content-addressed local record.
It is append-only, standard-library-only, and never opens a network or
database connection. Use the installed skill helper rather than hand-writing
events:

```sh
python3 <skill-dir>/scripts/metrics_ledger.py append \
  --repo <repo> --bead-id <story-bead> \
  --event <dispatch|gate_pass|gate_fail|review|close|limit> \
  [--lane <lane>] [--provider <provider>] [--model <model>] \
  [--tier <tier>] [--effort <effort>] \
  [--complexity <Complexity>] [--risk-class <Risk>] \
  [--operating-mode <operatingMode>] \
  [--routing-profile <modelRoutingProfile>] \
  [--assurance-profile <assuranceProfile>] \
  [--release-stage <releaseStage>] [--duration-s <seconds>] \
  [--detail '<json object>']
```

Capture `dispatch` after launch; `gate_pass`/`gate_fail` after each
verification attempt; `review` after packet verdict verification; `close`
when accepting or parking; and `limit` when a provider limit fires. Put
round, verdict, finding counts, head SHA, outcome, and similar event-specific
fields in `detail`. Resolve contract fields with `delivery_contract.py show`;
do not guess them.

Append failures warn and exit successfully: telemetry must never stall
delivery. Integrity checking and deterministic per-story rollups stay fully
offline:

```sh
python3 <skill-dir>/scripts/metrics_ledger.py check \
  --ledger .factory/metrics.jsonl
python3 <skill-dir>/scripts/metrics_ledger.py rollup \
  --ledger .factory/metrics.jsonl --out evidence/factory-rollups.json
```

Legacy `.factory/usage.jsonl` can be imported idempotently:

```sh
python3 <skill-dir>/scripts/metrics_ledger.py backfill \
  --repo <repo> --usage-ledger .factory/usage.jsonl \
  --ledger .factory/metrics.jsonl
```

No flush, upload, SQL, shared dashboard, or central service is part of this
workflow. Keep the ledger and rollup under the consumer repo's own evidence
policy.

## Provider limits

Live rate/quota messages are authoritative; the local ledger only helps pace
the operator's subscriptions across hosts. On a signal:

1. Append a `limit` event and note a conservative `resumeAt` in Beads.
2. Let the in-flight story finish if safe; otherwise park it with branch,
   worktree, and verification evidence.
3. Requeue only to a healthy lane of the same tier, retaining the branch and
   adding a handover line to the goal.
4. If no healthy same-tier lane exists, work other ready stories or wait.
   Never downgrade quality or silently switch billing.

If every provider is cooling, checkpoint according to the active repo's
commit/push/sync authority, record the earliest recheck time in Beads and the
log, and pause. A live session may resume after one cheap probe; a headless
host may exit for its repo-approved scheduler to relaunch. Multi-host capacity
does not create an external coordination service or grant push authority.
