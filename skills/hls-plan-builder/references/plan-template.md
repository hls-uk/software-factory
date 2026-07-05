# Plan: <Title>

```markdown
---
id: PLAN-<slug>
requirements: docs/requirements/<slug>.md
status: draft | active | done
updated: YYYY-MM-DD
---

# Plan: <Title>

## Design Decisions

### D1: <decision>
- **Choice:** ...
- **Rationale:** ...
- **Rejected:** <alternative> because ...

## Risks

- <risk> — mitigation / early-warning signal.

## Stories

### Story 0: <scaffold/harness, if needed>
- **Covers:** enables verification for all stories
- **Scope:** ...
- **Verification:** <exact commands>

### Story 1: <name>
- **Covers:** AC 1, AC 2
- **Depends on:** Story 0
- **Scope:** <files/areas to touch; what must not break>
- **Approach:** 2–5 bullets, enough to keep an implementer on the rails.
- **Resources:** <db / ports / services verification needs — all from env,
  leased per story by the orchestrator; "none" if pure>
- **Verification:** <exact commands / dev-browser checks / evidence to
  capture — idempotent and parallel-safe>
- **Done when:** <observable condition tying back to the ACs>

### Story 2: ...

## Criteria Coverage

| Acceptance criterion | Stories |
|---|---|
| AC 1 | 1 |
| AC 2 | 1, 3 |

## Test Strategy

How the suite grows with the stories; what runs per-story vs. at the end.
```
