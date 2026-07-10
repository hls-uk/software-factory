---
name: hls-tech-playbook
description: Technology-specific pitfalls and proven workarounds for factory delivery — schema migrations under parallel lanes, JVM/Gradle test-heap and cache walls, Quarkus test-port collisions, git worktrees under sandboxed CLIs, macOS process durability, harness-CLI auth quirks. Use when a factory run hits a failure that smells stack-specific (build tool, migration framework, test harness, OS, agent CLI), before dispatching stories in a stack listed here, and to record a newly solved stack-specific issue so the playbook grows.
---

# Tech Playbook

The factory's process rules are technology-neutral; real runs fail on
technology-specific walls. This skill is the growing memory of those walls
and their proven fixes, one reference file per stack, consulted on demand —
not loaded into every session.

## How to use it

- **On a stack-specific failure:** open the matching reference below and
  scan the Symptom lines before debugging from scratch. Most walls here cost
  a prior run hours; the fix is usually one config line or one dispatch-flag.
- **Before dispatching into a listed stack:** skim the file once and fold
  the applicable guards into the story goal's verify/scope lines (e.g.
  migration naming rules, test-port env vars, heap settings).
- **Entry shape:** every entry is `Symptom → Root cause → Fix → Coordinator
  notes` (what the coordinator can apply non-invasively vs what needs a
  tracked build change filed as a story/sweep issue).

## Index

| Stack | File | Covers |
|---|---|---|
| Schema migrations | [references/migrations.md](references/migrations.md) | Version-namespace collisions under parallel lanes and branches; timestamp versioning (preferred), range leases (fallback), out-of-order trade-offs |
| JVM / Gradle | [references/jvm-gradle.md](references/jvm-gradle.md) | Forked-test-heap OOMs, init-script overrides, caches outside sandboxed workspaces, daemon and capacity notes |
| Quarkus testing | [references/quarkus-testing.md](references/quarkus-testing.md) | Fixed test-port collisions, coupled service URLs, dev-services/testcontainers memory footprint |
| Git worktrees | [references/git-worktrees.md](references/git-worktrees.md) | Sandboxed lanes vs the shared git common dir, worktree lifecycle, branch-in-use rules |
| macOS processes | [references/macos-processes.md](references/macos-processes.md) | Durable detached lanes without `setsid`, missing GNU tools, `pgrep` self-match traps |
| Harness CLIs | [references/harness-clis.md](references/harness-clis.md) | Auth-dependent model availability, PATH/version pinning, codex sandbox flags |

## Growth protocol — how the playbook compounds

An entry earns its place when a real run lost time to it. When a factory run
solves a stack-specific failure that is not in these files:

1. Record it in the run's ledger/log as usual (symptom, root cause, fix,
   evidence).
2. File it back to this repo with the hls-skill-feedback skill (or edit the
   reference directly when working in this repo), in the entry shape above.
3. New stack → new reference file plus an index row; existing stack → new
   entry in its file. Keep entries evidence-based — name the failure output,
   not just the advice.

Entries are workarounds and configurations, not tutorials: assume the reader
knows the stack and needs the trap, the one-line fix, and whether the
coordinator can apply it without touching tracked build files.
