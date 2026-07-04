---
name: hls-repo-bootstrap
description: Bootstrap a new repo — software project or any knowledge work — with the LLM Wiki pattern and a compounding-learning loop, so every agent session leaves the repo smarter. Sets up the wiki (index, log, decisions, learnings), thin agent entrypoints (AGENTS.md/CLAUDE.md), and the session rituals that make knowledge accumulate. Use when creating a repo, or when an existing repo has no durable agent memory.
---

# Repo Bootstrap

A repo agents work in needs a memory that outlives every session. This skill
installs one: an LLM-maintained wiki plus the operating rules that make it
compound. The test of success is simple — six months of sessions later, a
fresh agent reads the entrypoint and the wiki index and knows more than any
single session ever did.

Two principles govern everything here: **every interaction should leave the
system smarter than before**, and **an answer that lives only in chat is
lost**.

## 1. Ask What Layer This Repo Is

- **Project repo** (software or knowledge work) — the common case; scaffold
  below. For software, follow with the hls-process-init skill for the delivery
  process; this skill provides the knowledge substrate.
- **Shared playbook** (conventions/skills reused across projects) — same
  scaffold, plus versioning (`VERSION`, `CHANGELOG.md`) so consumers can track
  drift.
- **Launcher/workspace** (thin root that mounts other things) — wiki-lite:
  entrypoint, log, and pointers only.

## 2. Scaffold the Wiki

The three-layer shape: **raw sources** (immutable inputs) → **wiki**
(LLM-maintained pages) → **schema** (the entrypoint file defining the rules).
Formats for every file are in
[references/wiki-templates.md](references/wiki-templates.md).

```
wiki/
  index.md        catalog of every page, one-line gloss each — read first
  log.md          reverse-chronological provenance log — append only
  overview.md     the one-page picture of the project
  decisions/      DEC-### — what/why/alternatives/revisit-when
  learnings/      LRN-### — the compounding ledger (see §4)
  topics/         concept pages as they emerge
  entities/       people/systems/domain objects as they emerge
sources/          immutable raw inputs; never edited in place
```

Rules that keep it healthy:

- Every page except `index.md`/`log.md` carries frontmatter with a **stable
  ID** (`DEC-003`, `LRN-012`, `TOPIC-<slug>`), `status`, `updated`, `tags`.
  Cross-link by relative markdown links — never `[[wiki-links]]`, never bare
  un-linked paths. IDs survive renames; links must be clickable.
- The wiki holds extracted facts that link back to sources — never pasted
  copies of whole documents.
- `index.md` is updated in the same session as any page add or rename.
- Wrong external data is recorded as a `data_quality` note, never silently
  "corrected".

## 3. Install Thin Agent Entrypoints

One canonical surface, generated mirrors, both agents equal:

- **Default:** author `AGENTS.md` as the canonical operating manual;
  `CLAUDE.md` is a two-line pointer: *"Read AGENTS.md in this folder and
  follow it. It is the source of truth."*
- **When per-agent wording must diverge:** keep a canonical
  `tools/agents/handbook.md` with `{{AGENT_NAME}}` placeholders and a small
  render script that generates both files, each stamped with a
  *generated — edit the source* banner, plus a `--check` drift mode wired
  into CI.

Keep the entrypoint thin — rules and pointers, not procedures. Procedures
live in skills and wiki pages loaded on demand; a fat entrypoint taxes every
session. It must state: what the repo is, the wiki rules above, the session
rituals below, and the hard boundaries (secrets, external actions).

## 4. Wire the Compounding Loop

The wiki without the loop is a graveyard. The loop is three rituals and a
ledger:

- **Session start:** sync first (pull before reading anything substantive),
  then read `wiki/index.md` and the tail of `wiki/log.md`.
- **In the moment:** hit a snag, learn something reusable, or make a decision
  → write the page *now*, in the smallest durable file that prevents
  rediscovery. A three-line learning written today beats a perfect one never
  written. Do not make the same mistake twice — write it down.
- **Session end — the closeout check:** Did this session create durable wiki
  knowledge? Did it reveal a repeatable process worth promoting? Is every
  reusable lesson written as an `LRN-###` rather than left in chat? Then log
  the session in `wiki/log.md`, commit, and push — never leave work unpushed.
- **The learnings ledger:** each `LRN-###` carries a status — `candidate`
  (may be generic), `project-only`, `promoted`, or `rejected` (kept, so the
  reasoning isn't re-litigated). On a cadence (weekly early on, monthly at
  steady state) run a **gardening pass**: triage candidates, promote what's
  generic into skills or process docs — via the hls-skill-feedback skill when the
  improvement belongs upstream — and mark them `promoted`. An untriaged old
  candidate is a lint finding, not a silent loss.

## 5. Lint

Periodically (and in CI where possible) check: index entries match pages on
disk; no broken relative links; no page stale-dated beyond its status; no
directory of documents without an entry point; no `candidate` learnings older
than the gardening cadence. Stale memory is worse than missing memory.

## Anti-patterns

- Scaffolding the full taxonomy for a repo with three files — start with
  `index.md`, `log.md`, `overview.md` and let structure emerge from need.
- Wiki pages that duplicate source documents instead of distilling them.
- A log that records activity ("worked on X") instead of change + provenance
  (what changed, driven by whom, executed by whom, evidence).
- Treating the wiki as documentation to write later. It is the working
  memory; later never comes.
