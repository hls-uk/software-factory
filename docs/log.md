# Log

## [2026-07-04 12:00 BST] workflow | v0.2.0: hls- prefix, PR review stage, operating guide
- Driven by: Adam (three requested upgrades)
- Executed by: Claude
- What changed: (1) all skills renamed `hls-*` for grouping — tracker labels
  and bd-managed blocks deliberately kept unprefixed; (2) the orchestrator's
  story loop now lands every story as a PR and runs a bounded review:
  independent reviewer, blocker vs non-blocker findings, rework beads,
  delta-only follow-ups, three-round cap, coordinator decides at the cap;
  (3) new running-the-factory guide (launch via Claude `/goal`//`/loop`,
  Codex `/goal`, headless VPS) and the `.factory/agents.json` role-assignment
  convention, scaffolded by hls-process-init.
- Evidence: validator 10/10 green; local install re-test discovers all
  hls-* names; CHANGELOG 0.2.0.

## [2026-07-04 10:55 BST] sync | Published public: github.com/hls-uk/software-factory
- Driven by: Adam (confirmed publish + owner/name interactively)
- Executed by: Claude
- What changed: Created the public GitHub repo, pushed main, pushed beads
  data (`bd dolt push`). Feedback config's GitHub fallback now points at
  hls-uk/software-factory (Jira fields remain placeholders until configured).
- Evidence: `npx skills add hls-uk/software-factory --list` discovers all 10
  skills from the public repo; CI validate run 28701092149 → success. All 15
  bootstrap beads issues closed with evidence (`bd list`).
- Driven by: Adam
- Executed by: Claude
- What changed: Bootstrapped this repo from empty per
  [BOOTSTRAP-BRIEF](BOOTSTRAP-BRIEF.md). Authored all ten v1 skills
  (repo-bootstrap, requirements-interview, plan-builder, factory-orchestrate,
  beads, dev-browser, skill-feedback, skill-sweep, process-init,
  process-revamp), built `scripts/validate-skills.mjs` as the quality gate,
  initialized embedded beads tracking (15 issues, dependency graph), wrote
  README/AGENTS.md/CLAUDE.md/CHANGELOG, this wiki, and CI.
- Evidence: `node scripts/validate-skills.mjs` → 10 skills, 0 errors; beads
  issue closures each carry per-skill evidence (`bd show <id>`).
- Decisions:
  - Skills are unprefixed (`beads`, not `hls-beads`) — matches the brief's
    naming; revisit if registry collisions bite.
  - Each skill dir is fully self-contained (own `references/`, no cross-skill
    links) because `npx skills add --skill <name>` installs single dirs.
  - Skill-feedback tracker config lives in consumer repos at
    `.factory/feedback.json` with placeholder credentials — never invented.
  - AGENTS.md is canonical, CLAUDE.md is a pointer (repo-bootstrap's default
    variant); bd-managed integration blocks preserved verbatim in AGENTS.md.
  - MIT license assumed for public release — confirm before publishing.
- Learning: validator initially flagged markdown links inside fenced code
  blocks (template examples) as broken; fixed by stripping code blocks before
  link-checking and regression-testing both directions. Lesson: a skills
  validator must treat fenced content as data, not prose.
