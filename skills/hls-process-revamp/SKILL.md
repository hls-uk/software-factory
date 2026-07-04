---
name: hls-process-revamp
description: Revamp an existing repo's engineering process to take full advantage of agentic delivery — audit what exists, map gaps against the factory target state, and adopt incrementally without steamrolling working conventions. Use on established codebases adopting agent-driven workflows, or when a repo's agent process has drifted or underperforms.
---

# Process Revamp

The existing repo has processes that work — some by design, some by habit.
Your job is to add the factory's missing load-bearing pieces while fitting
into (not replacing) what already functions. An adoption that fights the
team's conventions will be reverted; one that slots in will compound.

## 1. Audit — discover before prescribing

Read before proposing anything: CI config, test/lint/build setup, contribution
docs, existing AGENTS.md/CLAUDE.md, issue tracking in use, branch/review
conventions, and the git log (it shows the *real* process). Score the repo
against the factory target state:

| Capability | Target | Common existing form |
|---|---|---|
| Agent entrypoint | AGENTS.md canonical, thin, current | stale or missing CLAUDE.md |
| Verification gates | test/lint/build green and documented | exists but undocumented or flaky |
| Work tracking | dependency-aware queue (beads) | GitHub/Jira issues, TODO files |
| Durable memory | wiki: index, log, decisions, learnings | tribal knowledge, stale README |
| Requirements→plan flow | docs with testable criteria | tickets with prose |
| Evidence | `evidence/` per story | screenshots in PR comments, or nothing |
| Skill loop | installed skills + feedback config | none |
| Operating mode | declared in docs/process.md | implicit |

For each row: `present` / `partial` / `absent`, with the file paths that prove
it.

## 2. Map — respect what works

For every `partial`, decide **adapt** (wrap the existing convention — e.g.
keep Jira as the human-facing tracker, add beads for agent execution order and
link ticket IDs) or **replace** (only when the existing form actively blocks
agents, and say why). Flaky verification is priority zero: agents amplify
whatever gate quality exists.

Produce a staged adoption plan — each stage independently valuable, verified,
and revertible:

1. Stabilize gates (make test/lint/build green and documented).
2. Agent entrypoint + docs/process.md (operating mode, gates, rituals — use
   the hls-process-init skill's template).
3. Work tracking + wiki (beads init; hls-repo-bootstrap's wiki layer; backfill
   only the decisions that still bind — not history for its own sake).
4. Skills install + feedback config.
5. First orchestrated story end-to-end (the proof — same bar as hls-process-init:
   a process that has never executed is a hypothesis).

## 3. Confirm, then apply

Present the audit table and staged plan to the owner before changing process —
this is their team's working agreement, not just files. Then apply stage by
stage, running the repo's own verification after each, logging each stage in
the wiki once it exists.

## Rules

- Never delete or bypass an existing quality gate because it's inconvenient;
  fix it or flag it.
- Keep the team's naming and locations where they exist (their `docs/adr/` is
  fine — don't move it to `decisions/`; link it from the wiki index instead).
- Migrate tracking data, don't fork it: if tickets remain in Jira/GitHub,
  beads issues reference them rather than duplicating content.
- One story through the full loop before declaring the revamp done.

## Anti-patterns

- The big-bang PR that restructures docs, tracking, and CI at once — nothing
  is attributable, everything is contested.
- Auditing by checklist without reading the git log; the log is where the
  real process lives.
- Treating "the team does it differently" as a gap. Different and working
  beats canonical and resented.
