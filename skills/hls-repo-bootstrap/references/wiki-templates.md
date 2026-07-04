# Wiki File Templates

## wiki/index.md — the catalog (no frontmatter)

```markdown
# Wiki Index

The catalog of every wiki page. Read this first. Chronological history is in
[log.md](log.md). Update this file in the same session as any page add or
rename.

## Start here

- [overview](overview.md) — the one-page picture of the project.

## Decisions

- [DEC-001 — <title>](decisions/DEC-001-<slug>.md) — one-line gloss.

## Learnings

- [LRN-001 — <title>](learnings/LRN-001-<slug>.md) — one-line gloss (candidate).

## Topics

- [TOPIC-<slug>](topics/<slug>.md) — one-line gloss.
```

## wiki/log.md — provenance log (no frontmatter, newest first, append only)

```markdown
# Log

## [YYYY-MM-DD HH:MM TZ] <type> | <one-line summary>
- Driven by: <the human who asked — never omit>
- Executed by: Claude | Codex | Human | Script
- What changed: <concise, factual, durable>
- Evidence: <files, commands, checks>
- Effort saved: ~2h (optional, agent entries only)
```

Types: `setup, ingest, workflow, decision, tooling, lint, sync, learning`.

## Standard page frontmatter (every page except index.md / log.md)

```yaml
---
id: DEC-003            # stable ID; survives renames — cross-link by ID
status: draft | active | candidate | promoted | project-only | rejected | superseded
updated: YYYY-MM-DD
owner: <name or Unassigned>
tags: [list]
source_refs: []        # links back to sources/ where applicable
---
```

ID schemes: `DEC-###` decisions · `LRN-###` learnings · `TOPIC-<slug>` ·
`ENT-<kind>-<slug>` entities · `RISK-###` risks.

## Decision page — decisions/DEC-NNN-<slug>.md

```markdown
# DEC-NNN: <Title>

## What
The decision, stated plainly.

## Why
Reasoning, constraints, context at the time.

## Alternatives Considered
What was rejected, and why.

## Revisit When
Conditions that would make us reconsider.
```

## Learning page — learnings/LRN-NNN-<slug>.md

```markdown
# LRN-NNN: <Title>

## What happened
The concrete situation — enough that an outsider can follow.

## The lesson
Stated so someone who wasn't there can apply it.

## What should change
Concrete: a skill edit, a process note, a template, a tool —
or "nothing beyond this record".

## Effort / value signal (optional)
~<time> saved or lost; what it cost to learn.
```

Frontmatter `status` drives the gardening pass: `candidate` → triaged on a
cadence → `promoted` (with `promoted_to: <where>`), `project-only`, or
`rejected` (kept — the reasoning must not be re-litigated).

## CLAUDE.md — the pointer variant (entire file)

```markdown
Read `AGENTS.md` in this folder and follow it. It is the source of truth for
this workspace's purpose, boundaries, and operating rules.
```
