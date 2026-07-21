---
name: hls-factory-orchestrate
description: Run the software factory as the top-level coordinating agent — dispatch planned stories through configured model lanes, then apply verification, review, promotion, and issue routing according to the delivery contract, story risk, and invariant safety stops. Use when asked to coordinate, orchestrate, or autonomously deliver a planned body of work.
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
This factory has one human operator and may use several laptops or VPS hosts.
Host identity, shared-queue coordination, and failover are defined in
[references/host-lanes.md](references/host-lanes.md); hosts add capacity,
never another decision authority.

**Integration branch:** everywhere this skill says *main*, read the repo's
integration branch — `main` unless `.factory/agents.json`
(`"integrationBranch"`) or `docs/process.md` names another (e.g. a trial or
release branch). Stories branch from it, PRs target it, the post-merge full
suite runs on it, and "never push to main" style guards apply to whatever
branch it is *plus* main itself.

## Preconditions

- A confirmed requirements doc (`docs/requirements/<slug>.md`) — else run
  hls-requirements-interview. It must record separate `operatingMode`,
  `modelRoutingProfile`, `assuranceProfile`, and `releaseStage`; missing
  assurance defaults to `standard`, never `rapid`.
- An architecture doc (`docs/architecture/<slug>-architecture.md`) with status
  `signed-off`, or `recorded` only for an eligible rapid experiment/beta; a
  plan may instead record `architecture: unchanged`. The sign-off is reserved
  for the operator: an agent never self-approves it. Any escalation trigger
  restores the signed-off architecture gate.
- A plan with per-story verification (`docs/plans/<slug>-plan.md`) and the
  current story wave registered in beads — else run hls-plan-builder.
- Working local verification: the test/lint/build commands in the plan run
  green on main before you dispatch anything. Fix the harness first otherwise.
- When a story uses a third party, its signed architecture and plan name the
  same-adapter simulator gate, the shared real non-production integration
  gate, and the approved credential/probe mechanism. Missing access leaves
  the real gate red; it never weakens or removes the local gate.
- Repo guards active: if the repo declares git hooks (a `.githooks/` dir, a
  `core.hooksPath` setup step in its docs or dev scripts), activate them in
  the coordinator checkout before the first commit — worktrees share the
  repo's git config, so one activation covers every lane, but commits made
  *on a lane's behalf* run under the coordinator's config, so the coordinator
  is the one place activation cannot be skipped. A guard that exists only as
  an opt-in local hook (derived-artifact regeneration, contract sync) is an
  escape waiting to happen: honor it during the run, and file feedback
  (hls-skill-feedback) that it belongs in the repo's verify gate.

## Resolve the Delivery Contract

Before dispatch, copy the plan's four fields into the run checkpoint and keep
their responsibilities separate:

- `operatingMode` controls human availability and interaction cadence.
- `modelRoutingProfile` controls model tier/effort selection only.
- `assuranceProfile` controls verification, review, and promotion depth.
- `releaseStage` controls the authority boundary and when re-planning is due.

Also record the first usable journey, accepted defects, release blockers,
known-issues destination, recovery path, and escalation triggers. Rapid is
eligible only for named private users, reversible experiment/beta state, and a
preserved prior authority. Do not start or continue rapid delivery if the work
becomes public, irreversible, operational without recovery, or canonical;
raise assurance, reopen architecture/planning, and obtain the required human
authority first. A profile may never be lowered to bypass a failing gate.

## The Story Loop

Repeat until done:

1. **Pick.** Sync beads if the repo is multi-session (`bd dolt pull`), then
   `bd ready --json`; claim the highest-priority ready story
   (`bd update <id> --claim`). Fill every open implementer lane from the
   ready queue — lanes, caps, and the capacity checks (provider not cooling,
   host has headroom) are defined in
   [references/parallel-dispatch.md](references/parallel-dispatch.md).
   Without config, use one preflighted lane on the current host. Never exceed
   the configured cap or three stories in flight.

2. **Hand off.** Create the story's worktree from fresh main and dispatch the
   implementer *into* it (see Worktree Rules below). Before the story branch
   diverges, freeze its reviewer inputs in the canonical base-committed
   contract defined by
   [references/review-packets.md](references/review-packets.md): copy the
   story, criteria, every named spec, and predetermined verification-evidence
   paths from the plan. This is the last point where input paths are chosen;
   prompt assembly later has no file-list or free-prose inputs.

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
   story's Complexity rating × the repo's `modelRoutingProfile` decides model
   tier and effort. Resolve tiers to models proven available in this host's
   local profile; then run that lane's configured dispatch command:

   ```sh
   cd .worktrees/<slug> && <configured-dispatch-command> "$(cat goal.txt)"
   ```

   The contract is what matters: one whole story, one agent, one worktree,
   explicit verification, no scope beyond the story.

3. **Verify — never on trust.** When the implementer reports done, run the
   story's verification yourself *inside the story's worktree*: the plan's
   exact commands, affected tests, lint/build, and dev-browser evidence
   for anything UI-facing (the profile-required full suite runs on the
   integration branch at its merge/slice boundary, not per-worktree — see
   step 5). Check the diff for scope violations — files
   outside the story's scope, deleted tests, weakened assertions, and any
   change outside the worktree (there must be none; the coordinator checkout
   must still be clean on main). Gates failing → bounce straight back to the
   implementer with the failing output appended to the goal; don't spend a
   review on work that doesn't pass the machines.

   Verification depth follows assurance without weakening the safety floor.
   Standard and assured keep the full existing story and post-merge gates.
   For a routine rapid story, run its exact focused commands plus affected
   tests and applicable lint/type/build checks; at the first-usable slice
   boundary run the full configured suite and one real user/browser journey.
   Deleted tests, weakened assertions, falsified evidence, P0/P1 behaviour,
   and any invariant-boundary failure always bounce in every profile.

   If the plan names a real-vendor gate, run it only through the approved,
   audited probe/runner and serialize it against that shared vendor tenant.
   Capture redacted request/response semantics and provenance (environment,
   vendor spec/version, observation date, scenario, evidence link/hash), not
   credentials or PII. Compare the result with the simulator profile. Any new
   behaviour or discrepancy bounces the story until the simulator fixture/
   profile and its regression test are updated, unless the operator
   explicitly accepts a dated deferral. Simulator-only evidence cannot satisfy
   a real-integration criterion; real-vendor evidence cannot replace the
   deterministic local gate.

4. **Review when the contract requires it — bounded, then done.** Once gates
   pass, apply the review decision before merge. Independent review is
   mandatory for every standard and assured story, and in every profile when
   Risk is `mandatory-review` because the change touches authentication,
   authorisation, secrets/exposure, destructive or canonical state, money or
   human/commercial gates, concurrency/idempotency/recovery/cross-tenant
   behaviour, or an architecture/security boundary. Ensure that story is a PR
   and put it through the review protocol in
   [references/review-protocol.md](references/review-protocol.md): an
   independent reviewer — a **fresh agent session** with none of the
   implementer's context (the same human, subscription, and model are fine;
   a second human is not what independence means) — reads the diff against
   the story and its acceptance criteria. Build and verify its prompt with the
   deterministic packet tool in
   [references/review-packets.md](references/review-packets.md); dispatch
   `prompt.txt` verbatim with no coordinator prefix, suffix, selected files,
   or emphasis. The reviewer records a structured verdict pinned to the exact
   base/head, template, manifest, prompt, and diff hashes, and splits findings
   into **blockers**
   and **non-blockers**. Blockers become one rework bead blocking the story
   bead; the implementer gets exactly that list. Follow-up reviews see only
   the delta since the last reviewed commit and may not raise non-blockers on
   unchanged code. Hard cap: initial review plus two delta reviews. Rework
   that survives the cap is decided by you: fix it yourself if trivial, or
   park the story with its rework bead open. Non-blockers never block — they
   land as P2/P3 issues or PR notes and the review is still a pass.

   A routine, reversible rapid story may use coordinator verification without
   an independent packet. Record the `routine` classification, why no trigger
   applies, commands/evidence checked, exact head, and any known issue links in
   the story bead. Several small routine issues may be batched into one
   iteration slice, but batching never hides a trigger or widens scope.

5. **Accept or park.**
   - **Accept:** merge the PR per the repo's process. For standard and assured,
     run the **full suite on main** in your own checkout after every merge, as
     before. For rapid, run affected integration gates after each merge and
     the full suite plus the named real user/browser journey at the first-
     usable slice and release boundaries. A required post-merge gate failure
     is P0: revert or fix forward before any new dispatch. Then retire the story: drop its
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

   Treat a real-vendor observation as durable product learning: record it in
   the host repo's vendor/contract evidence, update the simulator in the same
   story or a blocking correction story, and file hls-skill-feedback only when
   the lesson changes the generic factory method rather than one vendor's
   behaviour.

   Under rapid, keep a visible known-issues set in the human-facing tracker.
   P0/P1 findings and invariant-boundary failures cannot be deferred. A P2/P3
   may cross the current reversible private release boundary only when its
   issue records impact, reproduction, desired outcome, severity, release
   milestone, and the shipped head/slice; link it from the bead and plan
   ledger. No per-finding waiver is needed when the delivery contract already
   accepts that severity/category. A new kind of defect requires an updated
   contract or explicit operator decision.

## Profile Promotion Gates

Story reviews split findings by severity. Under standard and assured,
non-blockers become finding beads and never block a story's merge to the
integration branch, but that debt has a hard boundary: **it does not cross the
promotion boundary unfixed.** A live factory trial exposed this failure:
reviewer-caught findings remained open while the roll-up shipped, so a later
review rediscovered known bugs.

Rapid uses a different, explicit release gate for a reversible private
experiment/beta: block every P0/P1 and invariant-boundary failure; require the
full configured suite and named real user/browser journey; require every
accepted P2/P3 to be linked in the visible known-issues set and plan ledger;
confirm the prior authority and reset/repair path still work; and pin the
decision to the released head. Run the integrated independent review when any
story or combined interaction has a mandatory-review trigger; otherwise record
the coordinator's integrated risk check. Rapid must raise assurance and
re-plan before public, irreversible, operational-without-recovery, or
canonical promotion.

- **Drain standard/assured findings continuously.** A free lane with no ready story is a drain
  opportunity: batch open finding beads into a bounded sweep story (same
  scope discipline, safety valve on money paths) and dispatch it through the
  normal loop — verify, review, merge. Don't let the debt pile up for a
  big-bang drain at the end.
- **Gate the standard/assured promotion PR.** Before pushing the PR that promotes the
  integration branch to main — or before declaring the run done when main
  *is* the integration branch — every finding bead opened during the run must
  be **closed** (fixed by dispatched implementer agents through the
  normal verify + review loop) or **explicitly waived by the human**. Fixing
  is the default; waiving is the operator's decision, never an agent's. A
  requirement-traced finding may be fixed or explicitly accepted by the
  operator; there is no peer or alternate-host waiver path.
- **Disclose what remains.** The promotion PR body lists every waived bead
  with a one-line risk statement. An outside reviewer should be able to
  rediscover nothing the factory already knows.
- **Review the standard/assured union.** The promotion diff — everything since main diverged —
  gets one independent review at the same bar as story reviews
  ([references/review-protocol.md](references/review-protocol.md)). Merged
  stories interact in ways no per-story review saw: shared-file unions,
  cross-module reachability, contract drift between stories.

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
  the repo's `modelRoutingProfile` selects lane tier and effort (routing table
  in the reference). When independent review applies, the reviewer uses the
  highest review-capable configured lane; no product/model name is assumed.
- Subscriptions are shared with other hosts: a usage ledger
  (`.factory/usage.jsonl`) paces dispatches, but live limit signals are the
  truth. On a limit: mark the provider cooling, shift the queue to healthy
  same-tier lanes; all lanes cooling → checkpoint and pause until a window
  resets.
- **Quality never downgrades.** Cooling never moves a story down a tier, and
  high-complexity stories never leave the frontier tier — when no suitable
  lane is available, the factory waits; it does not substitute.
- Every story holds a resource lease (for example a port block and its own
  datastore namespace or disposable instance) recorded in
  `.worktrees/<slug>/.env.story` — granted at dispatch, dropped at retirement.

## Long-Run Discipline

- **All state lives in beads + docs, never only in your context.** Resume
  ritual after any restart or compaction: read the plan's current-state block,
  tail `docs/log.md`, run `bd ready` — then continue the loop, after worktree
  hygiene: `git worktree list`, remove any worktree whose story bead is
  closed or parked, then `git worktree prune`. Do not re-read the whole
  history.
- **Empty queue ≠ done — cut the next wave.** Stories are cut just-in-time:
  when `bd ready` drains but acceptance criteria remain
  unticked, returning to hls-plan-builder to cut the next wave from the epic
  design docs — against main as it is *now* — is the normal rhythm, not a
  replan. Fold in the gap analysis while you're there: parked stories, open
  rework and finding beads, criteria no wave has covered yet.
- **Done means evidence.** Finish only when every criterion required for the
  current release stage in the requirements doc maps to closed stories with
  verification evidence, every
  finding is handled by the applicable Promotion Gate (closed/waived for
  standard/assured; P2/P3 visibly issue-linked for eligible rapid), the full
  suite is green at its required boundary, the named journey passes, and the
  log records it. Later-stage/deferred criteria remain linked, not silently
  treated as complete. Elapsed time, effort, and "the agent said so" are not
  completion.
- **Usage limits are weather, not failure.** Cooling providers, pauses, and
  window-boundary resumes are normal operation — log them, checkpoint, and
  let the resume ritual pick the run back up.
- **Stack-specific walls have a playbook.** When a failure smells like the
  technology rather than the story (build tool, migration framework, test
  harness, OS, agent CLI), consult the hls-tech-playbook skill if installed
  before debugging from scratch — and fold its applicable guards into goals
  when dispatching into a stack it covers. A stack-specific fix you solve
  that isn't in the playbook gets fed back (hls-skill-feedback) so the
  playbook grows.

## Escalation & Stops

- Batch questions for the human; park the affected story and keep working
  everything else. Block entirely only when nothing is workable.
- Hard stops requiring human confirmation regardless of autonomy mode:
  destructive/irreversible or canonical operations, production deploys,
  public release/publishing, external-service configuration, credential or
  secret handling, and human/commercial/cutover decisions. Never delete tests,
  weaken assertions, falsify evidence, or mutate/disable an existing authority
  to make a reversible beta pass.
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
  the review is theater. Independence is a fresh session judging only the
  durable inputs — not a second human; equally, demanding a non-author human
  approval for routine story review is the same misreading inverted.
- Hand-writing or decorating a reviewer prompt. Review contracts freeze the
  plan-owned input paths before implementation; the packet tool and approved
  templates own all review prose and bytes after that point.
- Letting review rounds relitigate accepted code — round N+1 sees only the
  delta from round N.
- Letting context carry state: any fact needed to resume that isn't in beads,
  the plan, or the log is already lost.
- Re-dispatching a bounced story with the same goal text. Every retry must add
  the new failure evidence, or it will fail the same way.
- Letting a shared vendor sandbox become an implicit per-lane dependency.
  Lanes stay deterministic on simulators; the coordinator schedules the real
  integration gate with explicit tenant/rate-limit ownership.
