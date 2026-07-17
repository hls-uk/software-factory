# docs/process.md Template

```markdown
---
status: active
mode: autonomous | supervised
updated: YYYY-MM-DD
---

# Engineering Process

How work moves through this repo. Agents: read this and AGENTS.md before
doing anything substantive.

## Operating Mode

`autonomous` — unattended runs on <host>; verify-and-proceed within the hard
stops below.
(or) `supervised` — human reachable; confirm outward-facing actions.

## The Loop

hls-requirements-interview → hls-architecture → hls-plan-builder → hls-factory-orchestrate → (per story)
implement → verify → PR review (bounded, delta-only follow-ups) → evidence →
close.

## Verification Gates

Run all of these locally before any story is accepted:

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

Destructive or irreversible operations; production deploys; publishing;
external-service configuration; anything requiring credentials not already
provisioned. <Add repo-specific stops.>

## Skill Feedback

When an installed skill misfires, file per the hls-skill-feedback skill.
Tracker config: `.factory/feedback.json`.
```
