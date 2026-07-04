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

hls-requirements-interview → hls-plan-builder → hls-factory-orchestrate → (per story)
implement → verify → PR review (bounded, delta-only follow-ups) → evidence →
close.

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

Agent roles (coordinator / implementer / reviewer) and their dispatch
commands are defined in `.factory/agents.json` — that file is authoritative;
this section records the same choices for humans.
Coordinator model: <e.g. strongest available Claude>; implementer:
<e.g. Codex at xhigh reasoning>; reviewer: <independent agent — never the
implementer>.

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
