---
name: hls-issue-iteration
description: Deliver selected product bugs and improvements through a bounded, risk-calibrated iteration loop — reproduce, classify, implement, verify the affected user journey, and close or requeue with durable evidence. Use after a product has a usable slice and its human-facing GitHub Issues backlog is driving the next fixes.
---

# Issue Iteration

Turn observed product feedback into verified improvements without recreating
the full factory for every bug. Reuse the repo's delivery contract,
architecture, plan, orchestration rules, and safety stops; this skill selects
and bounds the next iteration slice.

## Preconditions

- Read the repo's requirements/process/plan and recover separate
  `operatingMode`, `modelRoutingProfile`, `assuranceProfile`, and
  `releaseStage`. Missing assurance defaults to `standard`.
- Identify the human-facing issue backlog. Use GitHub Issues when the product
  repo is hosted on GitHub; do not invent a parallel tracker abstraction.
- Confirm authority before creating, editing, labelling, or closing remote
  issues. Reading and drafting do not grant external-write authority.
- Keep the current authority and recovery path explicit. A reversible beta
  must not mutate or disable the system it is replacing.

## Loop

### 1. Select

Choose the highest-impact issue that is ready and belongs to the current
release milestone. Several small issues may form one batch only when they
share the same product surface, risk class, and verification journey and the
combined scope still fits one bounded iteration.

GitHub Issues own the user-facing feedback lifecycle. Beads owns active agent
execution and dependencies. Do not mirror the whole GitHub backlog into
Beads. When selected work needs durable multi-session execution, create one
Bead for the issue or bounded batch, put the issue URLs in its external
reference/description, and claim it before implementation. Follow stricter
repo-local tracking rules when present.

### 2. Reproduce

Reproduce against the current integration head and record the smallest
reliable steps, expected/actual behaviour, environment, and evidence. If it
does not reproduce, do not guess at a fix: request missing evidence or requeue
it with the attempted checks. Redact secrets and personal data.

Use [references/issue-contract.md](references/issue-contract.md) for the issue
and execution record. The desired outcome must be observable from the user's
point of view, not an implementation task.

### 3. Classify consequence risk

Classify defect severity separately from implementation complexity:

- `P0`: active security/data loss, authority corruption, or unusable critical
  path — stop release and fix/revert immediately.
- `P1`: release-blocking incorrect behaviour or invariant failure — fix before
  the current release boundary.
- `P2`: material defect with a safe workaround in the current reversible
  boundary — may be scheduled by the delivery contract.
- `P3`: minor defect, polish, or improvement — may be scheduled normally.

Mark independent review `mandatory` in every assurance profile if the change
touches authentication/authorisation, secrets/exposure, destructive or
canonical state, money or human/commercial gates, concurrency/idempotency/
recovery/cross-tenant behaviour, or an architecture/security boundary. A
public, irreversible, operational-without-recovery, or canonical transition
is not an issue-sized shortcut: raise assurance and return through
architecture/planning before implementation.

### 4. Bound the iteration

Write acceptance criteria, scope/preserve boundaries, exact verification, and
the user journey that proves the outcome. For multi-session work, put the
durable contract in the plan or Bead and make dependencies explicit. Reuse
hls-plan-builder when the issue changes multiple contracts or needs more than
one independently dispatchable story; reuse hls-architecture only when a
recorded trigger fires.

### 5. Implement

Follow the repo's worktree, dispatch, and change-authority rules. Use
hls-factory-orchestrate for dispatched/multi-story work. Keep the diff bounded
to the selected issue contract; newly discovered unrelated work becomes a
linked issue, not opportunistic scope.

### 6. Verify proportionately

Always run the issue's focused regression, affected checks, and the affected
real user/browser journey. Standard and assured retain their configured
story, review, full-suite, and promotion gates. Under rapid, a routine,
reversible issue may use coordinator verification, but a batch/slice boundary
must run the full configured suite and one real user journey. Every mandatory
risk trigger gets independent review through hls-factory-orchestrate.

No profile permits deleted tests, weakened assertions, fabricated evidence,
credential leakage, destructive action, external configuration, public
release, canonical mutation, or bypassing a human/commercial decision.

### 7. Close or requeue

Close the human-facing issue only after the user-visible outcome passes on the
intended release head. Link the verification commands/evidence, head or PR,
release milestone, and any follow-up issues. Close the execution Bead when its
bounded work and evidence are complete; a remote issue may remain open when
the outcome is not yet released or verified.

If verification fails, the risk changes, or the outcome is only partial,
update/requeue the issue with exact evidence and next condition. Never turn a
partial result into a closed issue to empty the queue.

## Release Check

For rapid private releases, block P0/P1 and every invariant failure. P2/P3 may
ship only when the delivery contract accepts their category, each is visible
as a linked human-facing issue, the known-issues set is readable without
review transcripts, and reset/repair remains proven. Record issue time to
reproduction, time to verified fix, verification/review time, and any
assurance or release-stage transition.

## Anti-patterns

- Copying every GitHub issue into Beads.
- Treating a model-routing choice as an assurance decision.
- Batching unrelated issues because they are individually small.
- Closing on unit tests without checking the affected user journey.
- Using an issue label to authorize public, destructive, or canonical action.
- Running a full architecture phase for routine copy/layout/CRUD fixes when no
  trigger fired.
