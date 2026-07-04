---
name: hls-beads
description: Manage work with the beads issue tracker (bd) in embedded mode — ready queue, claiming, dependencies, evidence-based closes, and multi-machine sync. Use whenever a repo tracks agent work in beads, when setting up work tracking for a new project, or when coordinating multiple agent sessions on one backlog.
---

# Beads Work Tracking

Beads (`bd`) is a repo-local, dependency-aware issue tracker built for agents
(https://github.com/gastownhall/beads). It is the executable work queue; it is
**not** the source of truth for product intent — keep epics, requirements, and
durable synthesis in markdown and link to them from issues.

## Setup (once per repo)

```sh
command -v bd || brew install beads   # or: npm install -g @beads/bd
bd init                                # embedded mode — data in .beads/, no server
```

Embedded mode is the default and the only mode to use. If the git repo has a
remote, `bd init` auto-configures a matching Dolt remote named `origin`.

Commit `.beads/` config per the repo's convention; never hand-edit files in it.

## Core Rules

- Create issues only when they have evidence, impact, a concrete next step, and
  a done condition. No speculative filler issues.
- Use markdown docs for intent (requirements, plans, decisions); use beads for
  ownership, readiness, dependencies, and discovered follow-up work. Link, don't
  duplicate.
- Close with evidence: the `--reason` must say what was done and how it was
  verified (command run, test result, artifact path) — not just "done".
- Use `--json` for programmatic reads.

## The Work Loop

```sh
bd ready --json                 # issues with no open blockers, by priority
bd show <id>                    # read full detail before starting
bd update <id> --claim          # atomically claim so parallel agents don't collide
# ... do the work ...
bd close <id> --reason "What was done + verification evidence"
```

Discovered work goes back into the queue, wired into the graph:

```sh
bd create "Title" -p 1 -d "Context, next step, done condition" --json
bd dep add <new-id> <blocker-id>     # new-id is blocked by blocker-id
bd dep cycles                        # sanity-check after bulk graph edits
```

Priorities: `-p 0` (drop everything) through `-p 3` (someday). Default new
discoveries to `-p 2` unless they block claimed work.

## Multi-Session Sync

Solo, single-machine repos need nothing extra. When multiple agents or machines
share a backlog:

- `bd dolt pull` before reading the queue at session start, and again
  immediately before claiming — claims from a stale queue are invalid.
- `bd dolt push` after every batch of mutations, not just at session end.
- On conflict, never blanket-resolve ours/theirs: inspect conflicts row by row
  and preserve other sessions' claims and closes unless demonstrably superseded.
- Sync is the agent's job. A human should never need to remember a `bd dolt`
  command; wire pull into the repo's session-start ritual (hook or checklist).

Never leave issue state local-only without saying so in your session summary.

## Session Rituals

Start: `bd prime` (prints workflow context), then `bd ready --json`.
End: `bd status --json`, push if the repo syncs, and report any issues you
created, claimed, or closed.

## Anti-patterns

- Claiming more than one issue at a time per agent.
- Closing an issue whose acceptance evidence you did not personally produce or
  verify this session.
- Recording plans or design rationale only in an issue comment — put durable
  content in the repo's docs and link it.
