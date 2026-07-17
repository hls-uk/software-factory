---
name: hls-plan-builder
description: Turn a confirmed requirements doc and signed-off architecture into an implementation plan — epics anchored by design docs, stories cut just-in-time in waves sized for one-agent handoff, each with binding acceptance criteria and its own verification — and register the current wave as a beads dependency graph. Use after requirements are confirmed and the architecture is signed off, before implementation or orchestration begins — and again whenever the ready queue drains while acceptance criteria remain uncovered.
---

# Plan Builder

Produce a plan a coordinating agent can execute story-by-story without asking
questions: which stories exist, what order they can run in, and how each one
proves itself done.

## Process

1. **Read the requirements doc** (`docs/requirements/<slug>.md`). If its status
   is not `confirmed` or it has open questions, stop and run the
   hls-requirements-interview loop first — planning against draft requirements
   compounds guesswork.

2. **Read the signed-off architecture**
   (`docs/architecture/<slug>-architecture.md`, produced by the
   hls-architecture skill). If it is missing or its status is not
   `signed-off`, stop and run that phase — planning against unsettled
   architecture relitigates it one story at a time. Plans **inherit** the
   architecture's decisions: design decisions here are deltas within it,
   never reversals; a plan that needs to reverse one sends the architecture
   doc back for amendment and re-sign first. Work with no architectural
   weight (a feature inside a signed-off architecture) records
   `architecture: unchanged (ARCH-<slug>)` in the plan and proceeds.

3. **Investigate the ground truth.** For `mode: existing`, study the codebase:
   architecture, key files, test setup, conventions, and the seams the work
   must fit into. Record risks discovered. For `mode: greenfield`, decide the
   scaffold (respect the requirements' stack constraints and preferences).

4. **Make design decisions explicitly.** Each significant choice gets a short
   entry: decision, rationale, alternatives rejected. These go in the plan doc
   — implementing agents inherit decisions, they don't re-litigate them.

5. **Lay out the epics, then cut the current wave of stories just-in-time.**
   The plan lists every epic from the architecture doc with its design doc
   (`docs/design/<epic>.md`) — but only the **next wave** of stories is
   fully specified: the ones dispatchable now, cut against the current
   state of main. Later epics stay as epic entries until their turn.
   Pre-cut backlogs go stale as merges change the ground truth, and every
   early compression step is a chance for a requirement to die
   (the just-in-time story model). When the orchestrator's ready queue drains and criteria
   remain, it returns here to cut the next wave — that is the normal
   rhythm, not a replan. A story is the unit handed to one implementing
   agent in one run:
   - Delivers a coherent, verifiable slice — ideally user-visible or
     contract-visible (an endpoint, a screen, a migration with rollback).
   - Fits one agent's context: roughly a day of focused work or less. Split
     anything bigger.
   - Names its scope (files/areas), what it must not break, and its
     **verification**: the exact commands or checks that prove it done
     (tests to pass, dev-browser evidence for UI, lint/build gates).
   - Carries a **Complexity** rating the orchestrator routes models by:
     `high` (architectural weight, genuine ambiguity, or wide blast radius —
     gets a frontier model), `standard` (well-specified feature work), or
     `low` (mechanical, narrow, well-trodden). Judge by ambiguity and blast
     radius, not size — a one-line change to an auth check is `high`.
   - Maps to acceptance criteria by number. Every criterion is covered by at
     least one story; a story with no criterion is scope creep — cut it or
     take it back to requirements.
   - Carries its **evidence inputs**: the requirement sections, design docs,
     or module deep-dives that bind it. The story's acceptance criteria must
     restate every MUST those docs impose on this slice — contract shapes,
     security defenses, rate limits, authz posture — not compress them into
     "implemented + tested". Compression is where requirements die: the
     implementer and reviewer see the story entry, not your memory of the
     source doc.
   - Delivers a slice that is **reachable end-to-end**. If a story adds a
     surface gated by wiring owned elsewhere (permission/scope minting in an
     auth module, routing, gateway config), that wiring is in the story's
     scope or a companion story exists and blocks it — otherwise the surface
     ships tested-but-unreachable and no story owns the gap.
   - For a third-party integration, carries two distinct proofs when the
     signed architecture requires them: deterministic local/CI verification
     against the vendor-protocol simulator, and a serialized shared-
     integration check against the real vendor non-production endpoint. Its
     Resources line names the approved probe/runner and evidence location,
     never a secret value. Acceptance criteria require any newly observed
     real behaviour or discrepancy to update the versioned simulator
     profile/fixture and regression tests before the integration gate is
     green (or record an explicit operator-approved deferral).

6. **Write the plan** to `docs/plans/<slug>-plan.md` using
   [references/plan-template.md](references/plan-template.md). The Criteria
   Coverage table is the **master progress ledger** — the canonical answer
   to "where are we?": the orchestrator ticks it with evidence as stories
   close, and the repo's README links to it (see hls-process-init). Epic
   status is computed from beads, never hand-maintained.

7. **Register the current wave in beads.** One issue per story in the wave,
   dependencies wired so `bd ready` yields only truly unblocked work —
   later epics enter beads when their wave is cut, not before:

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
- **Requirements-fidelity check before the plan is done:** walk every doc the
  stories cite as evidence inputs; every MUST in them (contract shape,
  security defense, NFR) maps to some story's acceptance criteria or is
  recorded in the plan as an explicit deferral with a reason. A requirement
  that lives only in a deep-dive no acceptance criterion carries will not be
  implemented and will not be reviewed.
- Verification is executable now, not aspirational: if a story's check needs
  infrastructure that doesn't exist, there's a missing story in front of it.
- A real-vendor gate is not a reason to make ordinary story verification
  cloud-dependent. Local simulator gates remain per-lane and parallel-safe;
  the shared integration environment is a named, serialized producer/
  consumer gate with synthetic or vendor-approved data and redacted evidence.
- Verification is idempotent and parallel-safe: commands reset the story's
  own state first (its own database, its own fixtures), take ports and
  connection strings from the environment (`PORT`, `DATABASE_URL` — the
  orchestrator leases them per story), never hardcode shared resources, and
  can run alongside other stories' verification without interference.
  Declare what each story needs in its Resources line.
- The riskiest story runs earliest. Front-load unknowns; back-load polish.
- Include a "story 0" when needed: scaffold, CI, test harness — the things
  that make every later story's verification possible.

## Anti-patterns

- Horizontal-layer stories ("all the models", then "all the endpoints") — they
  serialize everything and verify nothing until the end. Cut vertically.
- Effort-shaped stories ("refactor X") without an observable done-condition.
- Acceptance criteria that summarize ("ops implemented + tested") instead of
  binding ("public lookup rate-limited per user and per IP; execute consumes
  the presented lock token"). A production trial shipped an enumeration-open
  endpoint and a token-less execute path because both MUSTs lived in deep-dives
  the acceptance criteria never carried.
- A plan that only lives in beads. The graph is for scheduling; the plan doc
  carries the reasoning, and it's the doc the next agent reads after a
  compaction.
