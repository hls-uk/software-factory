# Changelog

Newest first. One line per skill change, linking the feedback issue where one
exists.

## 0.5.0 — 2026-07-05

- hls-factory-orchestrate: story-time model routing. Lanes carry tiers
  (frontier / strong / fast); each story routes by its Complexity rating ×
  the repo's `deliveryProfile` (quality / balanced / throughput, default
  balanced: frontier·xhigh for high-complexity, Sonnet-5-class·high for
  standard, ·medium for low). Reviewer pinned frontier in every profile;
  cooling requeues same-tier only; high-complexity never leaves frontier.
  GPT-5.3-Codex-Spark documented as an optional disabled-by-default fast
  lane (mechanical edits/trivial rework only; research preview).
- hls-plan-builder: stories carry a Complexity line (judged by ambiguity
  and blast radius, not size).
- hls-factory-orchestrate: new `references/team-lanes.md` — optional
  multi-human mode: master plan with human-owned lanes and scope globs,
  `.factory/team.json`, gitignored `.factory/agents.local.json` per-machine
  overrides, mechanical scope-checked merge rights (lane owners merge
  in-lane; integrator merges cross-lane/shared), integrator role owning
  main health, cross-lane deps, and programme gap analysis.
- hls-process-init: factory config step covers deliveryProfile, tiered
  lanes, agents.local.json gitignore, and optional team.json.

## 0.4.0 — 2026-07-05

- hls-factory-orchestrate: parallel implementer lanes. `.factory/agents.json`
  v2 defines an implementer pool (defaults: VPS = one Claude Opus-class +
  one Codex xhigh lane, workstation = one lane); every dispatch is gated by
  two governors — provider health and host capacity (load/memory/disk) —
  detailed in new `references/parallel-dispatch.md`.
- Usage-limit awareness: advisory dispatch ledger (`.factory/usage.jsonl`)
  plus authoritative live limit signals; on a limit the provider cools and
  the queue shifts lanes; all lanes cooling → checkpoint and pause until a
  window resets (subscriptions shared with other hosts are assumed).
  Quality never downgrades — the factory waits rather than substituting a
  weaker model.
- Resource leases: per-story port blocks and per-story databases on a single
  shared host Postgres, recorded in `.worktrees/<slug>/.env.story`, dropped
  at retirement.
- Verify scope: story-scoped + affected tests in the worktree; full suite on
  main after each merge (failure is P0).
- hls-plan-builder: stories declare a Resources line; verification must be
  idempotent and parallel-safe (env-based ports/URLs, reset-own-state).
- hls-process-init: gates gain three hard properties — local-first,
  parallel-safe, idempotent; process template gains a Shared Verification
  Resources section.

## 0.3.0 — 2026-07-05

- hls-factory-orchestrate: formal worktree lifecycle. Story work always
  happens in coordinator-managed worktrees (`.worktrees/<slug>` in-repo,
  gitignored, branch `story/<slug>`) — the main checkout never does story
  work. Accept = merge + remove; park = push branch + remove, branch
  recorded in the bead; resume ritual gains worktree hygiene
  (`git worktree list`/`prune`, orphans removed). Implementers are dispatched
  into a worktree and never manage worktrees themselves.
- hls-factory-orchestrate: running-the-factory gains "Worktrees in Practice"
  (per-worktree dep installs, pnpm advantage, bd's native worktree redirect,
  port-collision guidance); goal-handoff template pins the working directory.
- hls-process-init: scaffolds the `.worktrees/` gitignore entry; process
  template gains a Worktrees section.

## 0.2.0 — 2026-07-04

- **Breaking:** all skills renamed with the `hls-` prefix (e.g. `beads` →
  `hls-beads`) so they group together among other installed skills.
  Reinstall with the new names; tracker labels stay `skill-feedback`.
- hls-factory-orchestrate: story loop gains a bounded PR review stage —
  independent reviewer, blocker/non-blocker severity split, rework tracked in
  beads, delta-only follow-up reviews, hard cap of three rounds
  (`references/review-protocol.md`).
- hls-factory-orchestrate: new `references/running-the-factory.md` — how to
  launch under Claude Code `/goal`//`/loop`, Codex `/goal`, or headless on a
  VPS, plus the `.factory/agents.json` role-assignment convention and the
  defaults chain.
- hls-process-init: scaffolds `.factory/agents.json`; process template's loop
  and dispatch sections reflect the review stage and role config.
- Fix: untracked `.agents/skills/` (bd's generated mirror, committed by
  `bd init` before the gitignore existed) — installers now discover exactly
  the ten `hls-*` skills.

## 0.1.0 — 2026-07-04

- Initial release: repo-bootstrap, requirements-interview, plan-builder,
  factory-orchestrate, beads, dev-browser, skill-feedback, skill-sweep,
  process-init, process-revamp.
- `scripts/validate-skills.mjs` quality gate + CI workflow.
