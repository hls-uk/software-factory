# Requirements: <Title>

```markdown
---
id: REQ-<slug>
status: draft | confirmed | superseded
mode: greenfield | existing
updated: YYYY-MM-DD
owner: <who confirmed these requirements>
---

# <Title>

One-paragraph summary: who this is for and what changes for them when it ships.

## Goals

- 2–5 bullets. Outcomes, not tasks.

## Non-Goals

- What is explicitly out of scope, and why if not obvious.

## Users & Context

Who uses this, in what environment. Existing systems it must fit into.

## Acceptance Criteria

Numbered, testable. Given/When/Then preferred.

1. Given <precondition>, when <action>, then <observable result>.
2. ...

## Constraints

- **Hard:** non-negotiables (compliance, budget, existing API contracts, stack mandates).
- **Preferences:** project-specific preferences that may be overridden with
  evidence (existing runtime, deployment environment, approved libraries).

## Assumptions

- [confirmed] ...
- [assumed] ... — flagged to the user on YYYY-MM-DD, not yet confirmed.

## Open Questions

Anything that blocks planning if unanswered. Empty when status is `confirmed`.
```
