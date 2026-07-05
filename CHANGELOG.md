# Changelog

Newest first. One line per skill change, linking the feedback issue where one
exists.

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
