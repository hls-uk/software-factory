# i5 non-SD fold-back — 2026-07-23

Status: implemented locally, awaiting any separately authorized commit/push.

## Pinned boundary

- Upstream source:
  `incept5/i5-software-factory@1d202c66f5fbc18add19531dd3f7f9db30744804`
- HLS pre-fold-back base:
  `hls-uk/software-factory@cfd59a564e60fe3ed613fef26164daf07c6cdfbe`
- HLS operating model: one human operator across laptop/VPS host capacity.
- Future machine-readable baseline:
  `skills/hls-i5-foldback/references/baseline.json`

The source pin is the start of the next audit. The target SHA records the tree
this fold-back began from; the resulting changes remain an uncommitted
reviewable handoff because this session has no commit/push authority.

## Capability dispositions

| Capability | Disposition | HLS result |
|---|---|---|
| Existing four-field delivery contract and consequence Risk | `present` | v0.8 already separated operating mode, model routing, assurance, release stage, and mandatory risk triggers. |
| CE P0–P4 | `adapt` | Lean Claude project settings; per-host hook/memory checklist; hot/cold dispatch references; verbatim base-committed story extract; deterministic static/live context budgets. |
| RH executable contract and review routing | `adapt` | Fail-safe resolver; actual-diff mandatory-trigger recheck; deterministic rapid sampling; full review when sampling is missing/invalid. |
| LM append-only metrics and rollups | `adapt` | Content-addressed local JSONL, offline integrity check/backfill/JSON rollup, capture never blocks delivery. No SQL or server. |
| TC toolchain contract | `adapt` | Exact embedded Beads writer/schema pin and local checker; no shared server, downloader, fleet, or admin role. |
| GLM-5.2 Claude-harness lane | `adapt` | Optional disabled `strong` lane, per-dispatch endpoint, lean flags, secret variable only, operator-run auth/billing proof required. |
| SD and shared control plane | `reject` | Not needed for HLS and conflicts with the one-operator embedded model. |
| Shared Dolt/Tailscale/AWS/RBAC/team onboarding/admin/dashboard coordination | `reject` | Multi-human/cloud control-plane assumptions deliberately excluded. |
| Incomplete auto-tune | `reject` | Not a completed upstream capability and conflicts with explicit operator policy control. |

## Durable evidence

- Delivery contract: `skills/hls-factory-orchestrate/scripts/delivery_contract.py`
- Rapid sampling and diff-risk rules:
  `skills/hls-factory-orchestrate/references/review-protocol.md`
- Local metrics: `skills/hls-factory-orchestrate/scripts/metrics_ledger.py`
- Context gate:
  `skills/hls-factory-orchestrate/scripts/context_baseline.py`
- Embedded toolchain: `skills/hls-beads/scripts/check-toolchain.py`
- Optional GLM variant:
  `skills/hls-tech-playbook/references/harness-clis.md`
- Repeatable audit: `skills/hls-i5-foldback/`

Future audits generate one row per later i5 commit-path change. The checker
reconstructs the pinned Git range and rejects missing/extra/reordered rows;
every row must then record `port`, `adapt`, `present`, or `reject` before any
selected implementation begins.
