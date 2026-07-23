# Embedded Beads version policy

## Contract

HLS uses Beads in embedded mode. There is no shared Dolt server, service
administrator, fleet rollout, or network installer in this contract. The one
operator may work from several laptops/VPS hosts, but every writable clone
uses the exact promoted `bd` version and storage schema declared in
`.factory/toolchain.json`.

The bundled declaration is [toolchain.json](toolchain.json). A consumer copies
it to `.factory/toolchain.json` and runs
[`../scripts/check-toolchain.py`](../scripts/check-toolchain.py) before the
first write in a session and after changing hosts or binaries. The checker:

- validates an exact promoted version and schema;
- rejects a missing, ranged, malformed, or unqualified candidate;
- executes only the selected local `bd version --json` probe;
- never installs, downloads, connects to a server, or mutates tracker state.

`binaryAcquisition: operator-managed` is deliberate. Installation and upgrade
remain separate operator-authorized actions; the checker only proves what is
already present.

## Candidate and promotion

Latest upstream is only a source of candidates. A candidate may be recorded
with an exact version/schema, its official tagged release URL, and status
`qualified-pending-embedded-migration`. Promotion is one operator decision,
not a team administrator role.

Qualification stays offline and disposable:

1. Preserve the promoted binary and a recoverable copy of representative
   embedded state according to the repo's backup policy.
2. Create disposable representative state with the promoted client.
3. Open a copy with the candidate and prove issue content, history,
   dependencies, comments, claims, atomic failures, export, and restore.
4. Prove the promoted client remains the default and that a version/schema
   mismatch fails closed.
5. Record evidence before replacing `beads.promoted` and clearing the
   candidate.

For a repo whose embedded data syncs through Git refs, only one operator-
selected clone migrates at a time. Other hosts stop writing, adopt the
published result through the repo's normal approved sync path, then run the
checker before resuming. Do not independently migrate multiple clones or
infer push authority from this policy.

If qualification fails after a disposable migration, discard the disposable
copy. If an authorized real migration fails, keep other writers stopped and
restore the repo's verified backup or roll forward under an explicit recovery
decision; do not guess by downgrading a client against changed state.

## Cadence

- Monthly: inspect releases/security notes and record a useful candidate.
- Operator-planned window: promote only after the offline qualification.
- Security exception: accelerate the same evidence gates, never remove them.

Skip a window when there is no useful candidate. Predictable, evidence-backed
changes matter more than keeping every host on “latest”.
