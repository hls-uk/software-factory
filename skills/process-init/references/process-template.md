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

requirements-interview → plan-builder → factory-orchestrate → (per story)
implement → verify → evidence → close.

## Verification Gates

Run all of these locally before any story is accepted:

- Tests: `<command>`
- Lint: `<command>`
- Build: `<command>`
- UI evidence (when frontend changed): dev-browser checks +
  screenshots into `evidence/<date>-<story>/`

## Work Tracking

Beads, embedded mode. `bd ready` is the queue; close with evidence.
Intent lives in docs/requirements and docs/plans; beads carries readiness.

## Dispatch

Implementing agents are launched via: `<command / mechanism>`
Coordinator model: <e.g. strongest available Claude>; implementer:
<e.g. Codex at xhigh reasoning>.

## Session Rituals

- Start: pull/sync, `bd ready --json`, read the current-state block of the
  active plan.
- End: push, append to docs/log.md, report created/claimed/closed issues.

## Hard Stops (regardless of mode)

Destructive or irreversible operations; production deploys; publishing;
external-service configuration; anything requiring credentials not already
provisioned. <Add repo-specific stops.>

## Skill Feedback

When an installed skill misfires, file per the skill-feedback skill.
Tracker config: `.factory/feedback.json`.
```
