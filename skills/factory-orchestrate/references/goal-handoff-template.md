# Story Handoff Goal Template

Compose the implementing agent's `/goal` from the plan's story entry. Keep it
under ~1,600 characters — it is a launcher, not the plan. The story detail
stays in the plan doc; the goal points at it.

```text
/goal Complete Story <N> (<name>) from docs/plans/<slug>-plan.md — read that
story entry first; it is the spec.

Context: branch <branch>; covers acceptance criteria <numbers> of
docs/requirements/<slug>.md. <One sentence of state the agent can't infer.>

Scope: <files/areas from the story>. Do not touch anything outside it; do not
modify tests except to add coverage for this story.

Preserve: <what must not break — existing behavior, API contracts, passing
suite>.

Verify: <the story's exact verification commands>. All must pass locally
before you report done. <For UI: capture dev-browser screenshots to
evidence/<date>-story-<N>/.>

Done/stop: done when verification passes and the diff is committed to
<branch> with a summary of evidence. Stop and report instead of guessing if
you need credentials, hit a design contradiction, or must touch out-of-scope
files.
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
  it back through plan-builder.
- Never include secrets in goal text; name the env var or config path instead.
- The verify section quotes commands that already run in this repo — an
  implementer should never have to invent its own definition of done.
