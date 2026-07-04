# Changelog

Newest first. One line per skill change, linking the feedback issue where one
exists.

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

## 0.1.0 — 2026-07-04

- Initial release: repo-bootstrap, requirements-interview, plan-builder,
  factory-orchestrate, beads, dev-browser, skill-feedback, skill-sweep,
  process-init, process-revamp.
- `scripts/validate-skills.mjs` quality gate + CI workflow.
