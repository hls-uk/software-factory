# Log

## [2026-07-05 13:00 BST] workflow | v0.5.0: complexity-routed model tiers + multi-human team lanes
- Driven by: Adam (research requested; four design choices confirmed)
- Executed by: Claude
- What changed: lanes gained tiers (frontier/strong/fast); plan-builder
  rates each story's Complexity; routing table selects tier+effort from
  Complexity × deliveryProfile (quality/balanced/throughput, default
  balanced). Reviewer pinned frontier everywhere; cooling requeues
  same-tier only. Spark documented as optional disabled fast lane. New
  team-lanes reference: master plan with human-owned scope-globbed lanes,
  team.json, gitignored agents.local.json, mechanical merge rights,
  integrator owns main health + cross-lane deps + programme gaps.
- Decisions (research-backed): blanket weak-coder + strong-reviewer
  rejected — review catches defects but cannot inject design quality, and
  our bounded no-nitpick protocol deliberately can't force restructuring;
  iterations are the expensive lever. Sonnet 5 (63.2 vs Opus 4.8's 69.2
  SWE-bench Pro, 40% cheaper, lighter quota) makes complexity-routing the
  right economics; GPT-5.3-Codex-Spark (1000+ tok/s, ~56% SWE-bench Pro)
  is a mechanical-edits lane, never a story implementer. Caveat: Sonnet 5
  tokenizer spends ~30% more tokens, and at xhigh it can be slower than
  Opus at high — another reason not to force strong-tier onto hard stories.
- Evidence: validator 10/10 green; CHANGELOG 0.5.0; sources logged in the
  session (Anthropic model docs, llm-stats, Vellum, OpenAI Spark
  announcement, remio/turingcollege benchmarks).

## [2026-07-05 11:00 BST] workflow | v0.4.0: parallel lanes, usage governance, resource leases
- Driven by: Adam (four design choices confirmed interactively)
- Executed by: Claude
- What changed: implementer pool with parallel lanes (VPS 1 Claude + 1
  Codex, workstation 1); two dispatch governors (provider cooling state,
  host load/mem/disk); usage ledger advisory + live limit signals
  authoritative — shift-provider-then-pause, never model downgrade for
  production code; per-story resource leases (port blocks, story_<slug> DBs
  on shared host Postgres, .env.story); verify split (story-scoped in
  worktree, full suite on main post-merge, main failure = P0); plan-builder
  Resources line + idempotent/parallel-safe verification contract;
  process-init local-first/parallel-safe/idempotent gate properties.
- Decisions: reactive limit signals beat any local ledger because
  subscriptions are shared across hosts; scale by not starting, never by
  killing; namespaced shared services (one Postgres, many DBs) over
  per-story docker stacks.
- Evidence: validator 10/10 green; CHANGELOG 0.4.0; new
  references/parallel-dispatch.md.

## [2026-07-05 09:30 BST] workflow | v0.3.0: formal worktree lifecycle for story work
- Driven by: Adam (proposed; three design choices confirmed interactively)
- Executed by: Claude
- What changed: worktrees are now mandatory for story work.
  Coordinator-owned lifecycle: create `.worktrees/<slug>` + `story/<slug>`
  from fresh main at dispatch; implementers dispatched into the worktree and
  barred from leaving/managing it; verify runs in-worktree; accept = merge +
  remove + branch delete; park = push branch + remove (branch in bead);
  resume ritual includes worktree hygiene. In-repo location chosen so
  harness permission scopes cover it; parked worktrees removed to stop
  long-run accumulation; "worktrees always" chosen over
  only-when-parallel to keep one code path.
- Evidence: validator 10/10 green; CHANGELOG 0.3.0; edits across
  hls-factory-orchestrate (SKILL.md Worktree Rules + both references) and
  hls-process-init (step 7 + process template), repo .gitignore.

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
