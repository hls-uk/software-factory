---
name: hls-factory-orchestrate
description: Run the software factory as the top-level coordinating agent — take a confirmed requirements set and deliver it to production quality by dispatching whole stories to implementing agents (e.g. Codex at xhigh reasoning) via /goal handoffs, verifying every result locally, putting each story through a bounded PR review, and looping for hours or days until every acceptance criterion has evidence. Use when asked to coordinate, orchestrate, or autonomously deliver a planned body of work.
---

# Factory Orchestrate

You are the coordinator, not the implementer. Your job is to keep a
requirements set moving to done: pick ready stories, hand each to a strong
implementing agent as a self-contained goal, verify and review the result,
and record evidence. You succeed when every acceptance criterion is ticked
with proof — not when the queue looks busy.

How to launch this loop from Claude Code or Codex, and how agent roles are
assigned, is covered in
[references/running-the-factory.md](references/running-the-factory.md).
Roles (implementer, reviewer, dispatch commands) come from the host repo's
`.factory/agents.json` when present; otherwise use the defaults named there.
When several humans share one repo — each running their own coordinator
against lanes assigned in a master plan, with a named integrator keeping
main green — follow [references/team-lanes.md](references/team-lanes.md) on
top of this loop.

## Preconditions

- A confirmed requirements doc (`docs/requirements/<slug>.md`) — else run
  hls-requirements-interview.
- A plan with per-story verification (`docs/plans/<slug>-plan.md`) and a beads
  graph — else run hls-plan-builder.
- Working local verification: the test/lint/build commands in the plan run
  green on main before you dispatch anything. Fix the harness first otherwise.

## The Story Loop

Repeat until done:

1. **Pick.** Sync beads if the repo is multi-session (`bd dolt pull`), then
   `bd ready --json`; claim the highest-priority ready story
   (`bd update <id> --claim`). Fill every open implementer lane from the
   ready queue — lanes, caps, and the capacity checks (provider not cooling,
   host has headroom) are defined in
   [references/parallel-dispatch.md](references/parallel-dispatch.md).
   Defaults: one Claude + one Codex lane on an autonomous VPS, a single lane
   on a supervised workstation; never more than three stories in flight.

2. **Hand off.** Create the story's worktree from fresh main and dispatch the
   implementer *into* it (see Worktree Rules below):

   ```sh
   git -C <repo> pull --ff-only
   git worktree add .worktrees/<slug> -b story/<slug>
   (cd .worktrees/<slug> && npm ci)   # or the repo's dep-install command
   ```

   Compose a compact `/goal` from
   [references/goal-handoff-template.md](references/goal-handoff-template.md):
   destination, context pointer to the plan story, scope, preserve, verify,
   done/stop — target ≤1,600 characters, detail stays in the plan doc. The
   goal names the worktree as the working directory and instructs the
   implementer to finish by opening a PR (or pushing its branch if it can't).
   Pick the lane by the **routing table** in
   [references/parallel-dispatch.md](references/parallel-dispatch.md) — the
   story's Complexity rating × the repo's delivery profile decides model
   tier and effort (balanced default: frontier·xhigh for high-complexity,
   Sonnet-5-class·high for standard, ·medium for low) — then run that
   lane's dispatch command, e.g.:

   ```sh
   cd .worktrees/<slug> && codex exec --model gpt-5.5-codex -c model_reasoning_effort="xhigh" "$(cat goal.txt)"
   ```

   The contract is what matters: one whole story, one agent, one worktree,
   explicit verification, no scope beyond the story.

3. **Verify — never on trust.** When the implementer reports done, run the
   story's verification yourself *inside the story's worktree*: the plan's
   exact commands, affected tests, lint/build, and dev-browser evidence
   for anything UI-facing (the full suite runs on main after merge, not
   per-worktree — see step 5). Check the diff for scope violations — files
   outside the story's scope, deleted tests, weakened assertions, and any
   change outside the worktree (there must be none; the coordinator checkout
   must still be clean on main). Gates failing → bounce straight back to the
   implementer with the failing output appended to the goal; don't spend a
   review on work that doesn't pass the machines.

4. **Review — bounded, then done.** Once gates pass, ensure the story is a PR
   and put it through the review protocol in
   [references/review-protocol.md](references/review-protocol.md): an
   independent reviewer (not the implementer) reads the diff against the
   story and its acceptance criteria, and splits findings into **blockers**
   and **non-blockers**. Blockers become one rework bead blocking the story
   bead; the implementer gets exactly that list. Follow-up reviews see only
   the delta since the last reviewed commit and may not raise non-blockers on
   unchanged code. Hard cap: initial review plus two delta reviews. Rework
   that survives the cap is decided by you: fix it yourself if trivial, or
   park the story with its rework bead open. Non-blockers never block — they
   land as P3 beads or PR notes and the review is still a pass.

5. **Accept or park.**
   - **Accept:** merge the PR per the repo's process, run the **full suite on
     main** in your own checkout — a failure there is P0: revert or fix
     forward before any new dispatch. Then retire the story: drop its
     resource lease (drop its database, free its port block),
     `git worktree remove .worktrees/<slug>`, delete the local branch. Close
     the story bead with evidence (commands run, results, evidence paths, PR
     link, review rounds used), tick the criteria it covers in the plan's
     coverage table.
   - **Park** (verification bounced 3×, or review cap hit): push the branch
     so the state is safe on the remote, remove the worktree, and record the
     branch name in the bead — unparking recreates the worktree from the
     branch. Log it, move to the next ready story — do not grind.

6. **Checkpoint.** After every story: commit and push (if the repo syncs),
   append one entry to `docs/log.md` (what shipped, evidence, decisions made),
   and refresh the short current-state block at the top of the plan doc. The
   next agent — or you after a compaction — must be able to resume from files
   alone.

## Worktree Rules

Story work happens in worktrees — always, even single-story runs. The
coordinator's checkout stays on main and is used only for beads, docs,
merges, and full-suite runs; if story code ever appears there, something has
gone wrong.

- **Location & naming:** `.worktrees/<slug>/` inside the repo (gitignored),
  branch `story/<slug>`. Worktree dir and branch always match.
- **Ownership:** the coordinator creates and removes worktrees; implementers
  are dispatched into one and must never leave it or manage worktrees
  themselves.
- **One per story, reused across rounds:** bounces and review rework happen
  in the same worktree — the state belongs to the story, not the attempt.
- **In-flight cap = story cap:** never more worktrees than stories in flight
  (three max).
- **Retirement:** accept → merge, remove worktree, delete branch. Park →
  push branch, remove worktree, branch name in the bead. A worktree with no
  open story bead is an orphan — remove it.

## Lanes & Capacity

Parallelism and its governors live in
[references/parallel-dispatch.md](references/parallel-dispatch.md); the
invariants:

- Two governors gate every dispatch: **LLM capacity** (the lane's provider
  isn't cooling on usage limits) and **host capacity** (load, memory, disk
  thresholds). Scale by not starting work — never by killing running work.
- **Stories route by complexity, not habit:** the plan's Complexity rating ×
  the repo's `deliveryProfile` selects lane tier and effort (routing table
  in the reference). The reviewer is frontier in every profile.
- Subscriptions are shared with other hosts: a usage ledger
  (`.factory/usage.jsonl`) paces dispatches, but live limit signals are the
  truth. On a limit: mark the provider cooling, shift the queue to healthy
  same-tier lanes; all lanes cooling → checkpoint and pause until a window
  resets.
- **Quality never downgrades.** Cooling never moves a story down a tier, and
  high-complexity stories never leave the frontier tier — when no suitable
  lane is available, the factory waits; it does not substitute.
- Every story holds a resource lease (port block, own database on the shared
  Postgres) recorded in `.worktrees/<slug>/.env.story` — granted at
  dispatch, dropped at retirement.

## Long-Run Discipline

- **All state lives in beads + docs, never only in your context.** Resume
  ritual after any restart or compaction: read the plan's current-state block,
  tail `docs/log.md`, run `bd ready` — then continue the loop, after worktree
  hygiene: `git worktree list`, remove any worktree whose story bead is
  closed or parked, then `git worktree prune`. Do not re-read the whole
  history.
- **Empty queue ≠ done.** When `bd ready` is empty but acceptance criteria
  remain unticked, run a gap analysis: parked stories, open rework beads,
  unmet criteria, missing stories. Feed gaps back through hls-plan-builder and
  continue.
- **Done means evidence.** Finish only when every acceptance criterion in the
  requirements doc maps to closed stories with verification evidence, the full
  suite is green on main, and the log records it. Elapsed time, effort, and
  "the agent said so" are not completion.
- **Usage limits are weather, not failure.** Cooling providers, pauses, and
  window-boundary resumes are normal operation — log them, checkpoint, and
  let the resume ritual pick the run back up.

## Escalation & Stops

- Batch questions for the human; park the affected story and keep working
  everything else. Block entirely only when nothing is workable.
- Hard stops requiring human confirmation regardless of autonomy mode:
  destructive/irreversible operations, production deploys, publishing,
  external-service configuration, credential handling.
- Blocked >30 minutes on one story: park it with a note and move on.
- Respect the repo's operating mode (see hls-process-init): fully-autonomous
  VPS mode widens what you verify-and-proceed on; supervised workstation mode
  narrows it. When unstated, assume supervised.

## Anti-patterns

- Implementing stories yourself. Trivial one-line bounces aside, if you're
  editing product code, you've stopped coordinating and the queue is stalling.
- Accepting on a green summary without re-running verification locally.
- Story work in the coordinator's checkout — even "just a quick fix". The
  checkout stays on main; fixes happen in the story's worktree.
- Reviewing your own dispatch: the reviewer must be an independent agent, or
  the review is theater.
- Letting review rounds relitigate accepted code — round N+1 sees only the
  delta from round N.
- Letting context carry state: any fact needed to resume that isn't in beads,
  the plan, or the log is already lost.
- Re-dispatching a bounced story with the same goal text. Every retry must add
  the new failure evidence, or it will fail the same way.
