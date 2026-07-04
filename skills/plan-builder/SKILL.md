---
name: plan-builder
description: Turn a confirmed requirements doc into an implementation plan — design decisions with rationale, stories sized for one-agent handoff, each with dependencies and its own verification — and register the stories as a beads dependency graph. Use after requirements are confirmed and before implementation or orchestration begins.
---

# Plan Builder

Produce a plan a coordinating agent can execute story-by-story without asking
questions: which stories exist, what order they can run in, and how each one
proves itself done.

## Process

1. **Read the requirements doc** (`docs/requirements/<slug>.md`). If its status
   is not `confirmed` or it has open questions, stop and run the
   requirements-interview loop first — planning against draft requirements
   compounds guesswork.

2. **Investigate the ground truth.** For `mode: existing`, study the codebase:
   architecture, key files, test setup, conventions, and the seams the work
   must fit into. Record risks discovered. For `mode: greenfield`, decide the
   scaffold (respect the requirements' stack constraints and preferences).

3. **Make design decisions explicitly.** Each significant choice gets a short
   entry: decision, rationale, alternatives rejected. These go in the plan doc
   — implementing agents inherit decisions, they don't re-litigate them.

4. **Cut the work into stories.** A story is the unit handed to one
   implementing agent in one run:
   - Delivers a coherent, verifiable slice — ideally user-visible or
     contract-visible (an endpoint, a screen, a migration with rollback).
   - Fits one agent's context: roughly a day of focused work or less. Split
     anything bigger.
   - Names its scope (files/areas), what it must not break, and its
     **verification**: the exact commands or checks that prove it done
     (tests to pass, dev-browser evidence for UI, lint/build gates).
   - Maps to acceptance criteria by number. Every criterion is covered by at
     least one story; a story with no criterion is scope creep — cut it or
     take it back to requirements.

5. **Write the plan** to `docs/plans/<slug>-plan.md` using
   [references/plan-template.md](references/plan-template.md).

6. **Register the graph in beads.** One issue per story, dependencies wired so
   `bd ready` yields only truly unblocked work:

   ```sh
   bd create "Story 3: Report submission endpoint" -p 1 \
     -d "See docs/plans/<slug>-plan.md#story-3. Covers AC 4,5. Verify: npm test -- reports" --json
   bd dep add <story-3-id> <story-1-id>
   bd dep cycles
   ```

   Keep issue descriptions as pointers into the plan — don't duplicate it.

## Quality Bar

- Two stories with no dependency between them must be safe to run in parallel
  in separate worktrees. If they'd conflict, add the dependency.
- Verification is executable now, not aspirational: if a story's check needs
  infrastructure that doesn't exist, there's a missing story in front of it.
- The riskiest story runs earliest. Front-load unknowns; back-load polish.
- Include a "story 0" when needed: scaffold, CI, test harness — the things
  that make every later story's verification possible.

## Anti-patterns

- Horizontal-layer stories ("all the models", then "all the endpoints") — they
  serialize everything and verify nothing until the end. Cut vertically.
- Effort-shaped stories ("refactor X") without an observable done-condition.
- A plan that only lives in beads. The graph is for scheduling; the plan doc
  carries the reasoning, and it's the doc the next agent reads after a
  compaction.
