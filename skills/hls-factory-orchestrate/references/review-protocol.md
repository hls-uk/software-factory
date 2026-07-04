# Story Review Protocol

Every story lands as a PR and gets an independent review before merge. The
protocol is designed to terminate: severity discipline stops nitpicking,
delta-only follow-ups stop relitigating, and a hard round cap stops loops.

## Roles

- **Coordinator** — owns the process: dispatches the reviewer, wires beads,
  decides at the cap. Does not review code it dispatched if a reviewer agent
  is available.
- **Reviewer** — an agent independent of the implementer (different session;
  ideally the reviewer role from `.factory/agents.json`). Reads; never edits.
- **Implementer** — fixes blockers on the same branch/PR.

## Round 1 — full review

Dispatch the reviewer with: the PR diff, the story entry from the plan, the
acceptance criteria it covers, and this instruction set. The reviewer checks,
in order:

1. Does the diff satisfy each acceptance criterion it claims to cover?
2. Correctness: bugs, unhandled failure paths, race conditions, security,
   data loss.
3. Contract fit: scope respected, conventions of the surrounding code
   followed, tests genuinely assert the new behavior.

Every finding is classified:

- **Blocker** — wrong behavior, unmet criterion, security/data risk, broken
  or gutted tests, scope violation. Must be fixed before merge.
- **Non-blocker** — style, naming, structure preferences, optional
  hardening, "could be simpler". Recorded, never fixed in this PR's loop.

Finding format (one per finding):

```
[blocker|non-blocker] <file>:<line> — <what is wrong, one sentence>
Evidence: <why it's wrong — failing case, violated criterion, or risk>
Fix: <the smallest change that resolves it>
```

## Wiring the result into beads

- **No blockers:** review passes. Non-blockers become P3 beads (or PR notes
  if trivial); merge proceeds.
- **Blockers:** create ONE rework bead per round —
  `bd create "Rework: <story> round <n>" -p 1 -d "<blocker list + PR link>"`,
  `bd dep add <story-bead> <rework-bead>` — post the findings on the PR, and
  re-dispatch the implementer with exactly the blocker list appended to the
  story goal. Close the rework bead when its blockers are verified fixed.

## Rounds 2–3 — delta only

Follow-up reviews receive only:

- the diff since the last reviewed commit
  (`git diff <last-reviewed-sha>..HEAD`), and
- the previous round's blocker list.

The reviewer answers two questions: *are the prior blockers actually fixed?*
and *does the new delta introduce new blockers?* Explicitly forbidden in
follow-up rounds:

- raising anything on code unchanged since the last round;
- new non-blockers of any kind;
- upgrading a finding that was available in round 1 but not raised — the
  reviewer had its chance.

## The cap

Initial review + at most two delta rounds. If blockers remain after round 3,
the coordinator decides — this is a judgment call, not a fourth round:

- **Fix it directly** when the remaining blockers are small and mechanical.
- **Park the story** with the rework bead open and a note on the PR when they
  are not — a story that can't clear review in three rounds usually has a
  plan problem, not a code problem; send what you learned back through
  hls-plan-builder.

Record in the story bead's close (or park) reason: rounds used, blockers
found/fixed, and non-blocker beads created. Review effort is evidence too.
