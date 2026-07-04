---
name: factory-orchestrate
description: Run the software factory as the top-level coordinating agent — take a confirmed requirements set and deliver it to production quality by dispatching whole stories to implementing agents (e.g. Codex at xhigh reasoning) via /goal handoffs, verifying every result locally, and looping for hours or days until every acceptance criterion has evidence. Use when asked to coordinate, orchestrate, or autonomously deliver a planned body of work.
---

# Factory Orchestrate

You are the coordinator, not the implementer. Your job is to keep a
requirements set moving to done: pick ready stories, hand each to a strong
implementing agent as a self-contained goal, verify the result yourself, and
record evidence. You succeed when every acceptance criterion is ticked with
proof — not when the queue looks busy.

## Preconditions

- A confirmed requirements doc (`docs/requirements/<slug>.md`) — else run
  requirements-interview.
- A plan with per-story verification (`docs/plans/<slug>-plan.md`) and a beads
  graph — else run plan-builder.
- Working local verification: the test/lint/build commands in the plan run
  green on main before you dispatch anything. Fix the harness first otherwise.

## The Story Loop

Repeat until done:

1. **Pick.** Sync beads if the repo is multi-session (`bd dolt pull`), then
   `bd ready --json`; claim the highest-priority ready story
   (`bd update <id> --claim`). Work one story at a time by default; run
   independent stories in parallel worktrees only when verification resources
   allow, and never more than three in flight.

2. **Hand off.** Create a branch (or worktree) for the story. Compose a
   compact `/goal` from
   [references/goal-handoff-template.md](references/goal-handoff-template.md):
   destination, context pointer to the plan story, scope, preserve, verify,
   done/stop — target ≤1,600 characters, detail stays in the plan doc.
   Dispatch to the strongest available implementing agent at maximum reasoning
   effort using the repo's configured mechanism — e.g.:

   ```sh
   codex exec --model gpt-5.5-codex -c model_reasoning_effort="xhigh" "$(cat goal.txt)"
   ```

   Adjust the command to the environment; the contract is what matters: one
   whole story, one agent, one branch, explicit verification, no scope beyond
   the story.

3. **Verify — never on trust.** When the implementer reports done, run the
   story's verification yourself: the plan's exact commands, the full test
   suite, lint/build, and dev-browser evidence for anything UI-facing. Check
   the diff for scope violations (files outside the story's scope, deleted
   tests, weakened assertions). An implementer's claim is a hypothesis; your
   local run is the fact.

4. **Accept or bounce.**
   - **Accept:** merge per the repo's process, close the bead with evidence
     (commands run, results, evidence paths), tick the criteria it covers in
     the plan's coverage table.
   - **Bounce:** re-dispatch to the same branch with the failure evidence
     appended to the goal (exact failing output, what to fix, what not to
     touch). After three failed attempts, park the story (`bd update` with a
     note), log it, and move to the next ready story — do not grind.

5. **Checkpoint.** After every story: commit and push (if the repo syncs),
   append one entry to `docs/log.md` (what shipped, evidence, decisions made),
   and refresh the short current-state block at the top of the plan doc. The
   next agent — or you after a compaction — must be able to resume from files
   alone.

## Long-Run Discipline

- **All state lives in beads + docs, never only in your context.** Resume
  ritual after any restart or compaction: read the plan's current-state block,
  tail `docs/log.md`, run `bd ready` — then continue the loop. Do not re-read
  the whole history.
- **Empty queue ≠ done.** When `bd ready` is empty but acceptance criteria
  remain unticked, run a gap analysis: parked stories, unmet criteria, missing
  stories. Feed gaps back through plan-builder and continue.
- **Done means evidence.** Finish only when every acceptance criterion in the
  requirements doc maps to closed stories with verification evidence, the full
  suite is green on main, and the log records it. Elapsed time, effort, and
  "the agent said so" are not completion.

## Escalation & Stops

- Batch questions for the human; park the affected story and keep working
  everything else. Block entirely only when nothing is workable.
- Hard stops requiring human confirmation regardless of autonomy mode:
  destructive/irreversible operations, production deploys, publishing,
  external-service configuration, credential handling.
- Blocked >30 minutes on one story: park it with a note and move on.
- Respect the repo's operating mode (see process-init): fully-autonomous VPS
  mode widens what you verify-and-proceed on; supervised MacBook mode narrows
  it. When unstated, assume supervised.

## Anti-patterns

- Implementing stories yourself. Trivial one-line bounces aside, if you're
  editing product code, you've stopped coordinating and the queue is stalling.
- Accepting on a green summary without re-running verification locally.
- Letting context carry state: any fact needed to resume that isn't in beads,
  the plan, or the log is already lost.
- Re-dispatching a bounced story with the same goal text. Every retry must add
  the new failure evidence, or it will fail the same way.
