# Requirements: <Title>

```markdown
---
id: REQ-<slug>
status: draft | confirmed | superseded
mode: greenfield | existing
operatingMode: supervised | autonomous
modelRoutingProfile: quality | balanced | throughput
assuranceProfile: rapid | standard | assured
spotReviewRate: 3-10 | full-review
releaseStage: experiment | beta | operational | canonical
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

## Delivery Contract

- **Routine rapid review:** <every Nth story, N=3–10; or full review>
- **Exposure:** <named private users | internal group | public>
- **Data criticality:** <disposable | recoverable | authoritative | canonical>
- **Authority and recovery:** <what the agent may change; reset, repair, or
  rollback path>
- **Unacceptable consequences:** <outcomes forbidden even in an early version>
- **First usable target:** <one end-to-end user journey and its observable
  completion signal>
- **Accepted defects:** <P2/P3 defects or polish that may be linked and deferred>
- **Release blockers:** <defects or missing evidence that block this stage>
- **Escalation triggers:** <conditions requiring more review or explicit human
  authority>

If assurance is not explicitly confirmed, use `standard`. `rapid` is only for
bounded, reversible delivery; it never authorizes secrets, destructive or
canonical changes, public release, external configuration, or bypassing a
human/commercial gate.

## Acceptance Criteria

Numbered, testable. Given/When/Then preferred. Prefix each item with the
earliest required milestone: `[first-usable]`, `[operational]`, `[canonical]`,
or `[deferred]`.

1. [first-usable] Given <precondition>, when <action>, then <observable result>.
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
