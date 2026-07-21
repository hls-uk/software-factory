# Story Handoff Goal Template

Compose the implementing agent's `/goal` from the plan's story entry. Keep it
under ~1,600 characters — it is a launcher, not the plan. The story detail
stays in the plan doc; the goal points at it.

```text
/goal Complete Story <N> (<name>) from docs/plans/<slug>-plan.md — read that
story entry first; it is the spec. Also read <every spec doc the story entry
lists as evidence inputs — module deep-dives, contract docs>: their contracts
and security requirements bind this story.

Context: you are in worktree .worktrees/<slug> on branch story/<slug> —
treat this directory as the repo root and never write outside it. Covers
acceptance criteria <numbers> of docs/requirements/<slug>.md. <One sentence
of state the agent can't infer.>
Delivery contract: assurance `<rapid | standard | assured>`, release stage
`<experiment | beta | operational | canonical>`, story risk
`<routine | mandatory-review>`; do not cross its escalation triggers.

Scope: <files/areas from the story>. Do not touch anything outside it; do
not modify tests except to add coverage for this story; do not create,
remove, or switch worktrees or branches.

Preserve: <what must not break — existing behavior, API contracts, passing
suite>.

Verify: <the story's exact verification commands>. All must pass locally
before you report done. <For UI: capture dev-browser screenshots to
evidence/<date>-story-<N>/.> <For stories adding authenticated endpoints: at
least one test must authenticate through the real login/session path — a
suite that only uses test-minted tokens can be green while every real client
gets 403.>

Done/stop: done when verification passes, the diff is committed to
story/<slug>, and a PR is opened (push the branch and say so if you cannot
open PRs) with a summary of evidence in its description. Stop and report
instead of guessing if you need credentials, hit a design contradiction, or
must touch out-of-scope files. Also stop before public/external, destructive,
irreversible, canonical, human/commercial, or authority-cutover action not
already and explicitly authorised by the contract.
```

## On a bounce (retry after failed verification)

Append, don't rewrite:

```text
Previous attempt failed verification. Evidence:
<exact failing command + trimmed output>
Fix this specifically. Do not refactor unrelated code. Everything else in the
goal stands.
```

## Rules

- One story per goal. If a story won't fit the template, it's too big — send
  it back through hls-plan-builder.
- The goal names every doc the story entry lists as evidence inputs, and the
  base-committed review contract in
  [review-packets.md](review-packets.md) freezes that same list before the
  story branch diverges. The reviewer later gets exact committed bytes from
  that contract — a spec the implementer never saw won't be implemented, and
  a spec the reviewer never saw won't be enforced. (One factory trial shipped a
  token-less execute endpoint because the goal omitted the pricing deep-dive
  that mandated token binding.)
- Never include secrets in goal text; name the env var or config path instead.
- The verify section quotes commands that already run in this repo — an
  implementer should never have to invent its own definition of done.
