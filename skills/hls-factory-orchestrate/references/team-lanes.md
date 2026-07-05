# Team Lanes — Multiple Humans on One Repo

Optional mode for large projects: several named humans, each running their
own coordinator (on their own machine and subscriptions), working one shared
repo in parallel. The default single-human factory needs none of this —
adopt it when a second coordinator shows up.

The structure is three things: a **master plan** that cuts the work into
human-owned lanes, a **team config** that makes ownership machine-readable,
and an **integrator** — a named human whose coordinator keeps main healthy
and owns everything that crosses lane boundaries.

## The Master Plan

`docs/plans/master-plan.md`, owned and maintained by the integrator. It sits
above per-lane plans:

```markdown
---
id: PLAN-master
integrator: <name>
status: active
updated: YYYY-MM-DD
---

# Master Plan: <Programme>

## Lanes

### Lane: backend
- **Owner:** <human name>
- **Scope:** `apps/api/**`, `libs/domain/**`
- **Interfaces owned:** REST API contract (openapi.yaml)
- **Plan:** docs/plans/backend-plan.md

### Lane: web
- **Owner:** <human name>
- **Scope:** `apps/web/**`
- **Consumes:** REST API contract
- **Plan:** docs/plans/web-plan.md

## Cross-Lane Dependencies

- web Story 3 depends on backend Story 5 (reports endpoint) — tracked as a
  beads dep across lanes.

## Shared Surfaces

Files/contracts no lane owns alone: `openapi.yaml`, `libs/shared/**`,
migrations touching shared tables. Changes here land only through
integrator-approved stories.

## Programme Criteria

The top-level acceptance criteria, each mapping to lane plans.
```

Lanes are cut to **minimize shared files** — a lane is a scope boundary
(directories, modules, features), not a job title. Cross-lane needs become
explicit interface stories, not casual edits to someone else's lane.

## Team Config — `.factory/team.json`

```json
{
  "integrator": "adam",
  "lanes": [
    { "name": "backend", "owner": "adam",  "scope": ["apps/api/**", "libs/domain/**"] },
    { "name": "web",     "owner": "sofia", "scope": ["apps/web/**"] }
  ],
  "shared": ["openapi.yaml", "libs/shared/**", "db/migrations/**"]
}
```

Per-human machine differences (which subscriptions, which dispatch commands)
live in `.factory/agents.local.json` — **gitignored** — which overrides the
committed `agents.json` field-by-field. The repo carries team defaults; each
human's machine carries their reality.

## How Each Coordinator Behaves

- **Claim only your lane.** Story beads carry their lane (label or title
  prefix); the coordinator filters `bd ready` to its human's lanes. Beads
  sync discipline becomes mandatory: `bd dolt pull` before every claim,
  `bd dolt push` after every batch (multi-machine claims collide otherwise).
- **Namespace by lane:** branch `story/<lane>/<slug>`, worktree
  `.worktrees/<lane>-<slug>`. Port blocks and story databases already
  key by slug, so parallel humans don't collide on resources — but two
  humans' dev servers on one shared VPS should confirm distinct port
  ranges in their local configs.
- **Merge rights are scope-checked and mechanical:** before merging a story
  PR, run `git diff --name-only main...` and match against the lane's
  `scope` globs. Diff entirely inside your lane → your coordinator merges.
  Any file in `shared` or another lane → hand the PR to the integrator
  (request their review, note it in the bead) and move on to your next
  story. No judgment calls: the globs decide.
- Everything else — worktrees, review protocol, verification, usage
  governance — is unchanged from the single-human loop.

## The Integrator

A named human (their coordinator runs the same skill with these extra
duties). The integrator:

- **Owns main.** Runs the full-suite-on-main gate after merges; a red main
  **freezes all lane merges** until green — announce it in beads (P0 issue),
  fix forward or revert, then unfreeze.
- **Merges cross-lane and shared-surface PRs**, reviewing against the master
  plan's interface contracts, not just the story.
- **Arbitrates cross-lane dependencies:** keeps the beads dep graph honest
  across lanes so `bd ready` never offers a story whose upstream lane
  hasn't delivered.
- **Runs programme-level gap analysis:** when lanes finish their plans but
  programme criteria remain unticked, the gap becomes new lane stories via
  hls-plan-builder.
- **Keeps the master plan current** — lane scope changes, re-assignments,
  and completed lanes are edits to the master plan, logged in the wiki.

Integration duty is real work; on small teams the integrator also owns a
lane, but their integration duties take priority over their lane when main
is red.

## Failure Modes to Watch

- **Scope drift:** a lane keeps needing "one small change" outside its
  globs. That's a mis-cut lane — redraw the boundary in the master plan
  rather than accumulating integrator exceptions.
- **Stale claims:** a human stops running their coordinator with stories
  claimed. Claims don't expire; the integrator audits `bd list` for
  claimed-but-idle stories at checkpoint and releases them explicitly.
- **Two sources of plan truth:** lane plans that contradict the master plan.
  The master plan wins; lane plans are its children.
