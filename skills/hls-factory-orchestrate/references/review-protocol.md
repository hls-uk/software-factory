# Story Review Protocol

Every story subject to this protocol lands as a PR and gets an independent
review before merge. The protocol is designed to terminate: severity discipline stops nitpicking,
delta-only follow-ups stop relitigating, and a hard round cap stops loops.
All review prompts and verdict checks use the deterministic builder/verifier
in [review-packets.md](review-packets.md); this file defines the fixed human
review rules that its versioned templates encode.

## Applicability

Use this protocol for every standard and assured story. Under rapid, use it
for any story or integrated slice touching authentication/authorisation,
secrets/exposure, destructive or canonical state, money or human/commercial
gates, concurrency/idempotency/recovery/cross-tenant behaviour, or an explicit
architecture/security boundary. A routine reversible rapid story may instead
use the coordinator evidence contract in the main skill. Once this protocol
is invoked, its independence, packet, severity, and round-cap protections do
not change with assurance profile.

## Roles

- **Coordinator** — owns the process: dispatches the reviewer, wires beads,
  decides at the cap. Does not review code it dispatched if a reviewer agent
  is available.
- **Reviewer** — an agent independent of the implementer (different session;
  ideally the reviewer role from `.factory/agents.json`). Reads; never edits.
- **Implementer** — fixes blockers on the same branch/PR.

## Independence — fresh context, not a second human

Independent review is **agent-context separation, not human separation**.
The rules, exactly:

- Implementation and review run in **separate fresh agent sessions**. The
  review session must never resume, continue, or receive the implementer's
  conversation, scratch notes, or any other hidden context.
- The reviewer receives **only** the mechanically rendered `prompt.txt`: the
  acceptance criteria, exact diff, verification evidence, and durable
  repository documents frozen in the base-committed review contract. No
  coordinator-authored preface, suffix, emphasis, or selected excerpt.
- **The same operator, subscription, provider, and model are allowed.** One
  subscription can operate implementer and reviewer as two fresh sessions
  and the review is independent. Cross-provider pairing is
  a preference (different failure modes catch more), never a requirement.
- Reviewer sessions default to **read-only**: dispatch commands for the
  reviewer role must not grant write/edit permissions to the repo.
- A routine story review never requires a second human. Human approval is a
  **separate gate** reserved for explicitly human decisions — architecture
  sign-off, acceptance waivers, production, PII, vendor/external services,
  and versioned reviewer-template changes — and is not how per-story review
  independence is achieved.

## Review evidence — pinned to the exact head

Every review verdict is recorded as the strict JSON object requested by the
packet's `VERDICT CONTRACT` (PR/CI artifact, mirrored into the story bead).
It binds the decision to the complete packet rather than only describing the
inputs from memory:

```json
{
  "factoryReview": "PASS",
  "head": "<full reviewed SHA>",
  "templateSha256": "<approved fixed-template hash>",
  "manifestSha256": "<canonical manifest hash>",
  "promptSha256": "<normalized prompt hash>",
  "diffSha256": "<literal Git diff hash>",
  "reviewer": {"identity": "<lane id>", "independence": "fresh-session", "readOnly": true},
  "findings": []
}
```

The actual object also carries `schemaVersion`, review id/type, and round;
copy the exact bound values from `prompt.txt`, never this abbreviated example.

Validity rules:

- A PASS is valid **only while `head` equals the branch's current head**.
  Any new commit — even a one-line fix — invalidates it; re-merging on a
  stale PASS is a protocol violation, not a shortcut.
- The CI event's actual base SHA and review id must also match, and the packet
  verifier must recompute every bound Git blob, diff, manifest, and prompt
  hash. A structurally plausible comment is not review evidence.
- Re-review after new commits is a **fresh reviewer session** (the delta
  rules below say what it receives). Never "ask the same session to look
  again".
- Evidence that shows the reviewer had implementer context (resumed session,
  shared transcript, implementer self-review) is invalid regardless of
  verdict.

The verifier rejects stale/wrong SHAs, a resumed or writable reviewer,
template/manifest/prompt/diff mismatches, and verdict/severity contradictions.

## Round 1 — full review

Build `story-full` from the base-committed contract and exact PR base/head,
then dispatch its `prompt.txt` verbatim. The contract contains the whole plan
file carrying the story, the requirements/criteria file, verification evidence
from the gates, and **every spec doc the story named as required reading**
(evidence inputs, module deep-dives, contract docs). The reviewer judges
against the same immutable spec surface the implementer had — a reviewer
anchored only on a compressed story summary cannot catch a deviation from the
contract the summary compressed away. The fixed template checks, in order:

1. Does the diff satisfy each acceptance criterion it claims to cover?
2. Correctness: bugs, unhandled failure paths, race conditions, security,
   data loss.
3. Plan fidelity: the implementation matches the contract and posture the
   referenced spec docs state — API shapes and token binding, rate limits,
   authz wiring, security defenses. "Works, but not the mechanism the plan
   specified" is a finding, not a taste call.
4. Contract fit: scope respected, conventions of the surrounding code
   followed, tests genuinely assert the new behavior — through the real
   auth/session path where the story adds authenticated surface, not only
   via test-minted credentials.

Every finding is classified:

- **Blocker** — wrong behavior, unmet criterion, security/data risk, broken
  or gutted tests, scope violation. On money or security stories, add:
  deviation from the planned contract (e.g. an execute path that ignores the
  token the plan says binds it, a mandated rate limit that is absent) — even
  when the implemented behavior is internally consistent. Must be fixed
  before merge.
- **Non-blocker** — style, naming, structure preferences, optional
  hardening, "could be simpler". Recorded, never fixed in this PR's loop.

Finding shape (one object per finding in the verdict JSON):

```json
{
  "severity": "blocker",
  "file": "path/to/file",
  "line": 42,
  "summary": "what is wrong, in one sentence",
  "evidence": "failing case, violated criterion, or risk",
  "fix": "smallest change that resolves it"
}
```

## Wiring the result into beads

- **No blockers:** review passes. Classify non-blockers P2/P3. Under rapid,
  each accepted finding becomes a visible human-facing issue linked from the
  plan/bead and governed by the delivery contract. Under standard/assured it
  becomes a finding bead (or PR note if truly trivial). Filing is deferral,
  not disposal: apply the profile's Promotion Gate in the skill body.
- **Blockers:** create ONE rework bead per round —
  `bd create "Rework: <story> round <n>" -p 1 -d "<blocker list + PR link>"`,
  `bd dep add <story-bead> <rework-bead>` — post the findings on the PR, and
  re-dispatch the implementer with exactly the blocker list appended to the
  story goal. Close the rework bead when its blockers are verified fixed.

## Rounds 2–3 — delta only

Each follow-up round is a **fresh reviewer session** (the same lane is fine).
Build `story-delta` from the prior packet; the builder recursively verifies
that lineage, infers the next round, and supplies only:

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

## The promotion review

For standard/assured, the PR that promotes the integration branch to main gets
one more independent review — of the combined diff since main diverged, not a
re-read of the already-reviewed stories. It exists because merged stories
interact in ways no per-story review saw. The reviewer receives the combined
diff, plan doc, and list of waived finding beads frozen by the promotion
contract. Build a `promotion` packet from the actual main base and integration
head and dispatch `prompt.txt` verbatim.

For rapid, run this promotion packet when any story or combined interaction
has a mandatory-review trigger. Otherwise the coordinator records the
integrated risk check, full-suite result, named journey, known-issues links,
recovery confirmation, and exact released head.

When the promotion packet runs, its fixed template checks:

1. Cross-story interactions: shared-file unions, contract drift between
   stories, a surface one story added that another story's change gates.
2. End-to-end reachability: every new user-facing surface is exercisable
   through the real auth/session path, not just in tests.
3. Repo-declared derived artifacts (generated specs, collections, lockfiles)
   are in sync with their sources — check the repo's hooks and generator
   scripts for what should have been regenerated.
4. Disclosure: every open or waived finding bead appears in the PR body.
   Anything the factory knows that the PR doesn't say is a blocker on the
   PR body, not the code.

Same severity split, same finding format. Blockers here go back through
sub-agent dispatch before the PR is pushed for human/outside review.
