# docs/process.md Template

```markdown
---
status: active
operatingMode: autonomous | supervised
modelRoutingProfile: quality | balanced | throughput
assuranceProfile: rapid | standard | assured
releaseStage: experiment | beta | operational | canonical
updated: YYYY-MM-DD
---

# Engineering Process

How work moves through this repo. Agents: read this and AGENTS.md before
doing anything substantive.

## Operating Mode

`autonomous` — unattended runs on <host>; verify-and-proceed within the hard
stops below.
(or) `supervised` — human reachable; confirm outward-facing actions.

## Delivery Contract

- **Model routing:** `<quality | balanced | throughput>` selects configured
  lanes; it does not grant autonomy or lower assurance.
- **Assurance:** `<rapid | standard | assured>`; unknown defaults to
  `standard`.
- **Release stage:** `<experiment | beta | operational | canonical>`.
- **Exposure / users:** <named private users, internal group, or public>.
- **Data criticality:** <disposable, recoverable, authoritative, or canonical>.
- **First usable target:** <one end-to-end user journey and observable signal>.
- **Accepted defects:** <P2/P3 issues that may be linked and deferred>.
- **Release blockers:** <P0/P1 defects and required evidence for this stage>.
- **Recovery:** <reset, repair, or rollback path>.
- **Escalation triggers:** <risk changes that restore deeper review or require
  human authority>.

`rapid` is limited to bounded, reversible experiment/beta delivery for named
private users. It prioritizes the first usable vertical slice, focused checks,
risk-triggered review, and linked P2/P3 follow-up. Escalate before public,
irreversible, operational-without-recovery, or canonical use. Standard and
assured retain their full configured protections.

## The Loop

hls-requirements-interview → hls-architecture → hls-plan-builder →
hls-factory-orchestrate → (per story) implement → verify → applicable review
(bounded, delta-only follow-ups) → evidence → close. Rapid cuts the first wave
as an end-to-end usable journey; standard and assured follow the full gates.

## Verification Gates

Run all of these locally before any standard/assured story is accepted. Rapid
may use story-scoped and affected checks while assembling the slice, but runs
the full configured suite and its user-journey check before accepting the first
usable slice. A risk trigger restores the full review and verification path.

- Tests: `<command>` (story-scoped + affected tests in the worktree;
  full suite on main after each merge — a main failure is P0)
- Lint: `<command>`
- Build: `<command>`
- UI evidence (when frontend changed): dev-browser checks +
  screenshots into `evidence/<date>-<story>/`

All gates run on a laptop with no cloud dependency; they are idempotent and
parallel-safe (ports and connection strings from env only).

## Third-Party Integration Ladder

- Developer lanes and CI use vendor-protocol simulators through the same
  production adapter; only endpoint and credential binding changes.
- `<shared integration environment>` uses real vendor sandbox/test endpoints,
  synthetic or vendor-approved subjects, and a serialized `<probe command or
  protected workflow>` gate.
- Staging, when established, mirrors production deployment and uses the closest
  authorised non-production vendor environment.
- Credentials live in `<operator-controlled secret store>` and are reached with temporary,
  least-privilege, audited identity. Agents normally invoke probes that resolve
  secret values server-side; values never enter source, prompts, CLI arguments,
  logs, screenshots, or evidence.
- Every new redacted real-world observation updates the vendor evidence record,
  simulator profile/fixture, and regression tests before the affected gate is
  green. Production is never exploratorily probed without explicit authority.

## Shared Verification Resources

- Primary datastore/service: `<repo-specific shared or isolated scheme>`;
  each story receives its own namespace or disposable instance through env.
- Ports: leased per story as `PORT`/`PORT_BASE` — never hardcoded.
- <other shared services and their namespacing scheme>

## Work Tracking

Beads, embedded mode. `bd ready` is the queue; close with evidence.
Intent lives in docs/requirements and docs/plans; beads carries readiness.

## Worktrees

Story work happens in coordinator-managed worktrees: `.worktrees/<slug>`
(gitignored) on branch `story/<slug>` — always, even single-story runs. The
main checkout stays on main. Accept = merge + remove worktree; park = push
branch + remove worktree.

## Dispatch

Agent roles (coordinator / implementer / reviewer) and their dispatch
commands are defined in `.factory/agents.json` — that file is authoritative;
this section records the same choices for the operator.
Coordinator: <strongest locally available configured lane>; implementer:
<configured lane selected by complexity/capability>; reviewer: <independent
agent — a fresh read-only session that never sees the implementer context;
same operator, provider, and model allowed; PASS pinned to the head SHA>.
Each host binds these roles to its actual CLIs and subscriptions in the
gitignored `.factory/agents.local.json`; rerun lane setup after any host,
CLI, model, subscription, or capability change.

## Session Rituals

- Start: pull/sync, `bd ready --json`, read the current-state block of the
  active plan.
- End: push, append to docs/log.md, report created/claimed/closed issues.

## Hard Stops (regardless of mode)

Destructive or irreversible operations; canonical-source mutation; production
deploys; public release or publishing; external-service configuration;
anything requiring credentials not already provisioned; bypassing human or
commercial decisions; weakening or falsifying tests/evidence. These stops
apply regardless of operating mode, model routing, assurance, or release
stage. <Add repo-specific stops.>

## Skill Feedback

When an installed skill misfires, file per the hls-skill-feedback skill.
Tracker config: `.factory/feedback.json`.
```
