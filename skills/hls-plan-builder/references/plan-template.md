# Plan: <Title>

```markdown
---
id: PLAN-<slug>
requirements: docs/requirements/<slug>.md
architecture: docs/architecture/<slug>-architecture.md   # or: unchanged (ARCH-<slug>)
status: draft | active | done
operatingMode: supervised | autonomous
modelRoutingProfile: quality | balanced | throughput
assuranceProfile: rapid | standard | assured
spotReviewRate: 3-10 | full-review
releaseStage: experiment | beta | operational | canonical
updated: YYYY-MM-DD
---

# Plan: <Title>

## Current State

Two or three lines, refreshed at every checkpoint: wave in flight, stories
merged, where to resume. The first thing a resuming agent reads.

## Delivery Contract

- **First usable target:** <active-time target plus one observable end-to-end
  operator journey>
- **Exposure / data criticality:** <current boundary>
- **Prior authority and recovery:** <what remains authoritative; reset,
  repair, or rollback>
- **Accepted defects:** <P2/P3 categories and their issue destination>
- **Release blockers:** <P0/P1 plus invariant or contract-specific blockers>
- **Escalation triggers:** <conditions that require raised assurance and
  re-planning before release>

For `rapid`, wave 1 must complete the first usable target; a foundation-only
wave is invalid unless no safe user journey exists or the operator approves a
recorded reason. Standard and assured retain the repo's full protections.

## Design Decisions

Deltas within the recorded/signed-off architecture — never reversals (a needed
reversal reopens the architecture doc first).

### D1: <decision>
- **Choice:** ...
- **Rationale:** ...
- **Rejected:** <alternative> because ...

## Risks

- <risk> — mitigation / early-warning signal.

## Epics

Every epic from the architecture doc, whether or not its stories are cut
yet. Status is computed from beads — never hand-edited here.

| Epic | Design doc | Wave | Stories (from beads) |
|---|---|---|---|
| <epic> | docs/design/<epic>.md | 1 (current) | 3 open / 1 merged |
| <epic> | docs/design/<epic>.md | later | not yet cut |

## Stories — current wave

Only the wave dispatchable now is specified; the next wave is cut
just-in-time when the queue drains, against the repo as it is then.

### Story 0: <scaffold/harness, if needed>
- **Covers:** enables verification for all stories
- **Scope:** ...
- **Verification:** <exact commands>

### Story 1: <name>
- **Epic:** <epic> (docs/design/<epic>.md — its MUSTs bind the ACs below)
- **Covers:** AC 1, AC 2
- **Acceptance criteria:** binding restatements traced to the design doc —
  "public lookup rate-limited per user and per IP", never
  "implemented + tested"
- **Depends on:** Story 0
- **Complexity:** high | standard | low — <one line: why this rating>
- **Risk:** routine | mandatory-review — <consequence and exact trigger; this
  is independent of Complexity>
- **Scope:** <files/areas to touch; what must not break>
- **Approach:** 2–5 bullets, enough to keep an implementer on the rails.
- **Resources:** <db / ports / services verification needs — all from env,
  leased per story by the orchestrator; "none" if pure>
- **Verification:** <exact commands / dev-browser checks / evidence to
  capture — idempotent and parallel-safe>
- **Done when:** <observable condition tying back to the ACs>

### Story 2: ...

## Criteria Coverage — the master progress ledger

The canonical progress view: progress is criteria ticked with evidence,
not stories closed. The orchestrator updates Evidence as stories merge;
the repo README links here.

| Acceptance criterion | Required milestone | Stories | Evidence / issue link |
|---|---|---|---|
| AC 1 | first-usable | 1 | <PR/test/log link, or blank until proven> |
| AC 2 | operational | 1, 3 | |
| AC 3 | deferred | — | <visible issue link and reason> |

## Test Strategy

How the suite grows with the stories; what runs per-story vs. at the end.
For rapid, name the focused story checks, full configured suite at the usable-
slice boundary, and real user/browser journey. For standard and assured,
retain all existing story, integration, review, and promotion gates.
```
