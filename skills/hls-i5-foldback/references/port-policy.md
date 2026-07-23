# HLS selective i5 fold-back policy

## Operating difference

i5 serves a team of five or more people. HLS serves one human operator who may
run isolated agent sessions across several laptops or VPS hosts. Machines add
capacity and failure isolation; they do not create owners, approvers,
administrators, or a control plane.

Translate terms as follows:

| i5 assumption | HLS adaptation |
|---|---|
| engineer/participant/team member | the operator on a particular host |
| participant-owned lane | host-local capability in `agents.local.json` |
| team requirement/default | portable repo requirement |
| independent human approval | operator approval only where authority requires it |
| reviewer independence | fresh read-only agent context with pinned evidence |
| fleet/shared service | embedded/local mechanism plus repo-approved sync |
| central metrics/dashboard | append-only local JSONL plus offline JSON rollup |
| administrator migration | one operator-selected clone, one migration at a time |

Never manufacture peer approvals, role ownership, onboarding flows, or a
second human to preserve i5 wording.

## Selected areas

### CE — context efficiency P0–P4

Keep lean Claude-harness project settings, per-host duplicate-hook hygiene,
hot/cold orchestration references, the base-committed verbatim story extract,
and deterministic context budgets. Do not mutate user settings automatically
or require a live lane probe when credentials/authority are unavailable.

### RH — rapid hardening

Keep the executable delivery contract, safe defaults, mandatory-trigger
diff-risk recheck, deterministic 1-in-N sampling for eligible rapid routine
stories, and full review on absent/invalid configuration. Rapid never weakens
authority, secrets, destructive, public, canonical, or integrity boundaries.

### LM — local metrics

Keep append-only content-addressed events, integrity checking, deterministic
offline per-story rollups, and non-blocking capture. Reject SQL flushing,
databases, shared writers, dashboards, uploads, and tuning automation.

### TC — embedded toolchain

Keep an exact local Beads writer/schema declaration, fail-closed checker,
candidate evidence, and one-clone-at-a-time migration. The checker never
downloads, installs, connects to a tracker server, or grants sync/push
authority.

### GLM — optional Claude-harness variant

Keep it disabled and visibly labelled optional. Pin `glm-5.2`, use the
per-dispatch Anthropic-compatible endpoint, preserve lean context flags, and
require local model/auth/billing proof. Never commit a token, set a user-wide
endpoint, assume a current quality ranking, or run credential/network probes
without authority.

## Mandatory rejection boundary

Reject every SD change and every change whose useful behavior depends on:

- a shared Dolt server or database fleet;
- Tailscale, AWS, RBAC, or cloud/admin infrastructure;
- multi-human onboarding, ownership, peer approval, or team administration;
- a central dashboard, shared metrics database, or control-plane coordinator;
- incomplete auto-tune behavior or automatic policy mutation.

A mixed commit is not rejected wholesale: classify every changed path, inspect
the relevant hunk, and port only separable selected behavior. If separation
would retain a forbidden assumption, reject it with that reason.

## Evidence rule

`port`, `adapt`, and `present` cite concrete HLS paths and verification.
`reject` states the excluded capability or incompatibility. The disposition
ledger must pass the bundled checker before implementation begins and again
after evidence paths are finalized.
