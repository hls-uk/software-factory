# Log

## [2026-07-23 16:00 BST] release | v0.9.0 non-SD i5 fold-back
- Driven by: Adam (activated the pinned Goalcraft objective to port every
  selected i5 upgrade except SD and make the same subset repeatable)
- Executed by: Codex
- What changed: folded CE/RH/LM/TC and the optional labelled GLM variant from
  `incept5/i5-software-factory@1d202c66f5fbc18add19531dd3f7f9db30744804`
  onto HLS base `cfd59a564e60fe3ed613fef26164daf07c6cdfbe`.
  The factory now has an executable four-field contract, actual-diff risk
  escalation, deterministic rapid sampling, content-addressed local metrics
  and offline JSON rollups, context P0–P4, an exact embedded Beads
  writer/schema check, and a disabled GLM-5.2 Claude-harness variant. Added
  installable `hls-i5-foldback`, whose checker reconstructs every later i5
  commit-path row before accepting `port`/`adapt`/`present`/`reject`.
- Decisions: HLS remains one human across laptop/VPS capacity; host identity
  never becomes ownership or decision authority. SD, shared Dolt server,
  Tailscale, AWS, RBAC, team onboarding/admin, central dashboard/control-plane
  coordination, and incomplete auto-tune are rejected. Metrics stay offline,
  the toolchain checker never installs/downloads/connects, and GLM remains
  disabled until a separately authorized local credential/billing/model probe.
- Evidence: Beads epic `software-factory-gbp` and children `.1`–`.5` closed
  with tranche evidence. Final gates: skill validator 17/17 with 0 errors and
  0 warnings; delivery-contract 9/9; metrics 8/8; review-packet 5/5; embedded
  toolchain 5/5 plus actual `bd 1.1.0`/schema 1; fold-back audit 6/6 plus a
  pinned zero-delta reconstruction; context budgets green at 5,914 estimated
  tokens for orchestrator SKILL.md, 8,296 hot working set, and 20,494 bundle.
  The separate offline proof appended five events and derived 2 gate runs/1
  failure/1 review/1 non-blocker/merged/30 seconds. An isolated local
  `/opt/homebrew/bin/skills` install was byte-identical, discoverable, valid,
  and passed the installed audit suite. Exclusion scans, trailing-whitespace
  scan, `git diff --check`, and dependency-cycle check were clean. No live GLM
  probe, credentials, external service, reset/clean/overwrite, commit, or push
  occurred.

## [2026-07-23 15:27 BST] planning | Non-SD fold-back Goalcraft launcher
- Driven by: Adam (selected every audited i5 upgrade except SD and requested
  a reusable skill for future selective fold-backs)
- Executed by: Codex
- What changed: created Bead `software-factory-lwd` and drafted a compact
  activation-ready goal for CE/RH/LM/TC/GLM plus a new self-contained
  `hls-i5-foldback` skill. The goal pins i5 `1d202c6` and HLS `cfd59a5`,
  requires future per-delta `port`/`adapt`/`present`/`reject` decisions, and
  makes the one-human/many-host distinction an implementation invariant.
- Decisions: SD includes the shared Dolt/Tailscale/AWS/RBAC/onboarding/admin/
  central-dashboard/control-plane track and stays excluded. Incomplete i5
  auto-tune AC8-AC10 is not treated as a completed upgrade. GLM-5.2 remains
  an optional labelled harness variant, never an HLS default or credential
  requirement. The goal preserves the current worktree and requires explicit
  approval before commit, push, or external change.
- Evidence: Goalcraft's normal draft measured 1,688 objective characters and
  exceeded its strict 1,600 target, so the required emergency compact shape
  was used; the final exact launcher passed at 1,453 characters against the
  3,999 hard limit. The goal was drafted and recorded, not activated.

## [2026-07-23 15:06 BST] planning | Selective post-v0.8 i5 upgrade audit
- Driven by: Adam (asked to inspect recent updates in
  `../../incept5/i5-software-factory` and choose upgrades before any port)
- Executed by: Codex
- What changed: audited the complete i5 range after the last HLS fold-back
  baseline (`fe52b93..1d202c6`) against HLS `cfd59a5`; recorded the work in
  Bead `software-factory-72p`; and classified the delta into independently
  selectable capabilities. No skill, runtime, tracker-authority, host,
  credential, remote, or external-service change was made.
- Decisions: the HLS v0.8 four-field delivery contract, story Risk
  classification, and assurance/risk routing are already present. The
  selectable incremental upgrades are: context-efficiency P0-P4; executable
  contract and review-routing hardening; local append-only metrics and
  rollups; multi-host toolchain policy; an optional GLM-5.2 Claude-harness
  lane; and, only as an explicit architecture programme, the shared
  Dolt/Tailscale control plane plus central dashboard. Auto-tune remains an
  i5 design/open implementation track, not a completed port candidate.
- Evidence: live `git ls-remote` matched both inspected heads
  (`hls-uk/software-factory@cfd59a5`,
  `Incept5/i5-software-factory@1d202c6`); i5 changelog `0.13.0–0.26.0`,
  `docs/plans/factory-delta-uptake-plan.md`, context-efficiency and GLM lane
  verification, and the metrics/dashboard acceptance ledger were inspected.
  The i5 context probe recorded a lane reduction from 44,431 to 23,636 input
  tokens; its auto-tune AC8-AC10 remain open.

## [2026-07-21 22:04 BST] release | v0.8.0 risk-calibrated delivery implementation
- Driven by: Adam (approved `DESIGN-risk-calibrated-delivery` on Bead
  `software-factory-aly`, then activated the repo-only implementation goal)
- Executed by: Codex
- What changed: implemented the four-field delivery contract across
  requirements, architecture, planning, orchestration, and process setup;
  added proportional rapid/standard/assured paths; added installable
  `hls-issue-iteration`; made the Factory Method authoritative; updated the
  public catalog, validator, operating manual, design status, and 0.8.0 release
  notes. Rapid now prioritises a reversible first usable vertical slice,
  retains consequence-triggered independent review, blocks P0/P1/invariants,
  and permits only contract-accepted, visible linked P2/P3 issues.
- Decisions: `operatingMode`, `modelRoutingProfile`, `assuranceProfile`, and
  `releaseStage` are orthogonal; unknown assurance defaults to standard;
  standard/assured protections remain intact; rapid must re-plan before public,
  irreversible, operational-without-recovery, or canonical use. GitHub Issues
  own human-facing feedback, while Beads owns only selected multi-session
  execution/dependencies.
- Acceptance evidence: AC1 → `hls-requirements-interview` confirmation gate;
  AC2 → four-field templates plus validator enforcement; AC3 → plan-builder's
  foundation-only rejection; AC4 → rapid P0/P1 block and linked P2/P3 release
  gate; AC5 → mandatory consequence triggers in orchestrator/review protocol;
  AC6 → architecture/plan/orchestrator escalation gates; AC7 → explicit
  preservation of standard/assured story review, full-suite, and promotion
  rules; AC8 → `hls-issue-iteration` and Factory Method tracker ownership.
  AC9–10 remain intentionally pending on unclaimed Vita follow-up
  `software-factory-5sp`; this session did not edit Vita.
- Evidence: Beads epic `software-factory-1ih` and children; validator passed
  after every skill edit and final checks reported 16 skills, 0 errors, 0
  warnings; review-packet adversarial tests passed 5/5; tracked/untracked
  whitespace checks passed; link and delivery-residue checks passed; a clean
  temporary Git repo installed and discovered `hls-issue-iteration` with its
  self-contained reference. No deploy, credentials, external configuration,
  commit, push, Vita edit, reset, clean, or overwrite was performed; existing
  structured-reporting changes were preserved.

## [2026-07-21 21:36 BST] design | Risk-calibrated delivery proposal from the Vita trial
- Driven by: Adam (asked why `vdb-uk/vita-platform` was taking too long, then
  asked for the resulting plan as a Software Factory design document)
- Executed by: Codex
- What changed: added proposed design `DESIGN-risk-calibrated-delivery`, which
  separates operating mode, model routing, assurance profile, and release
  stage; adds an upfront delivery/risk contract; makes the first usable journey
  a rapid-plan invariant; preserves consequence-triggered review and hard
  safety boundaries; defines non-duplicative GitHub Issues/Beads roles; and
  proposes a bounded Vita beta pilot plus one future issue-iteration skill.
- Decisions: the current Factory Method remains authoritative until the proposal
  is approved and released; rapid means reversible beta rather than permanently
  lower quality; unknown risk defaults to standard; secrets, public exposure,
  destructive actions, legacy mutation, canonical data, and human commercial
  gates never become low-assurance shortcuts.
- Evidence: Bead `software-factory-6cd`; live Vita snapshot `b489d67` showed 110
  post-setup commits, 28 review verdicts, about 21,025 API-source lines versus
  37 web-source lines, and E3-3 starting before a usable dashboard. Before the
  Bead was created, this designated clone exported 30 issues, migrated Beads
  from v49 to the v1.1.0 schema, and pushed the migrated Dolt state so other
  clones can bootstrap instead of migrating independently.

## [2026-07-17 11:24 BST] requirements | Laptop-native Claude/Codex structured-reporting trial
- Driven by: Adam (reframed the trial as an installed-harness laptop workflow,
  then simplified the model scope to Claude and Codex only)
- Executed by: Codex
- What changed: added confirmed requirement
  `REQ-structured-reporting-laptop-agent-harness-trial`, a draft architecture,
  and first-wave protocol/runner designs. The product is one local Python runner
  controlled by either Claude Code or Codex, with two models and two efforts per
  family, an eight-configuration frozen matrix, detached/resumable cells,
  deterministic scoring, at most two shared improvement challengers, and an
  evidence-generated README with Mermaid and accessible tables. The earlier
  validation and study-shaped PRDs are both marked superseded.
- Decisions: no external orchestrator, VPS, daemon, third model provider, direct
  provider SDK, or dashboard; immutable files are evidence and SQLite is only a
  rebuildable local index. The maximum default live run is 416 cells. Only
  fictional reporting packs are allowed, and results describe the tested
  harness/model/effort configurations without a general format or market claim.
- Evidence: Bead `software-factory-qxh`; requirements AC-01–AC-16; local probes
  found installed Claude Code and Codex CLIs with explicit model, effort, and
  structured-output controls. Architecture remains draft pending Adam's sign-off.

## [2026-07-17 10:38 BST] release | v0.7.0 commit and remote alignment
- Driven by: Adam (authorised commit and push and asked to get the remote
  sorted)
- Executed by: Codex
- What changed: committed the HLS v0.7.0 product release as `b968171` and the
  structured-reporting requirements plus session evidence as `36a155e`; pushed
  both to `origin/main`; closed Bead `software-factory-0rh`. The Beads Dolt
  push initially found newer remote state, so pulled it without force,
  confirmed the closure survived the merge and no work remained in progress,
  then pushed the integrated data branch successfully.
- Evidence: skill validator passed 15/15 with zero errors or warnings;
  review-packet tests passed 5/5; staged and working-tree whitespace checks
  passed; Git advanced from `a2a979a` to `36a155e`; no force push, fork edit,
  publication, or external configuration change was used.

## [2026-07-17 10:24 BST] workflow | v0.7.0 single-operator post-copy fold-back
- Driven by: Adam (activated the goal to audit `72df369..fe52b93`, fold useful
  generic changes back, remove team support, and retain multiple laptop/VPS
  execution under one human authority)
- Executed by: Codex
- What changed: classified every pinned fork commit in Bead
  `software-factory-nhb`; preserved the already-landed v0.5.1-v0.6.1 fixes;
  adapted promotion/fidelity gates, calibrated simulator evidence, fresh-
  context SHA-pinned review, deterministic review packets, architecture and
  JIT planning, consumer skill updates, and read-only factory status. Added
  `hls-architecture`, `hls-publish-report`, `hls-skill-update`, and
  `hls-factory-status`. Replaced multi-human `team-lanes.md` with per-host
  setup/failover under one operator and one coordinator lease. Removed house
  stack and named-model defaults from active factory policy. Added the HLS
  Factory Method and 0.7.0 release notes; no PDF was published.
- Decisions: laptops/VPSs are capacity and failure domains, never ownership or
  decision domains; review independence is fresh read-only context rather
  than another human; the operator alone signs architecture/templates, waives
  findings, promotes, and authorises external actions. Fork-only tracker/docs
  commits and the multi-human team release were rejected with reasons.
- Evidence: `node scripts/validate-skills.mjs` — 15 skills, 0 errors, 0
  warnings; review-packet adversarial suite — 5/5 pass; `git diff --check`
  clean; active skill/README/Factory Method residue scan clean; sibling fork
  remained clean at `fe52b93`. No commit, push, remote change, publication, or
  fork edit was performed. Concurrent structured-reporting requirements work
  already present in the shared worktree was preserved untouched.

## [2026-07-17 10:22 BST] requirements | Research-safe structured-reporting harness PRD
- Driven by: Adam (confirmed the earlier real-world trial was too close to a
  potential commissioned study and requested a new PRD)
- Executed by: Codex
- What changed: added the confirmed greenfield requirements contract at
  `docs/requirements/structured-reporting-evaluation-harness-validation.md`,
  indexed it, and marked `REQ-structured-reporting-model-trial` superseded with
  a prominent do-not-build warning. The replacement validates one fictional
  company's generated XBRL/HTML/PDF pack, three replay-tested provider adapters,
  immutable receipts, deterministic scorer truth cases, and an Engineering
  Validation report in one sprint.
- Decisions: non-substitution is executable, not just narrative. The readiness
  protocol rejects real/buyer data, multiple entities, substantive research
  tasks, repeated live runs, comparative aggregation, rankings, statistics,
  policy findings, and benchmark claims. Optional live smoke is capped at nine
  nonce-retrieval calls and cannot produce comparative output. Publication and
  external sharing remain explicit approval gates.
- Evidence: requirement
  `REQ-structured-reporting-evaluation-harness-validation`; bead
  `software-factory-a44`; 13 independently testable acceptance criteria.

## [2026-07-17 10:02 BST] requirements | Structured Reporting Model Trial PRD
- Driven by: Adam (requested a PRD for an HLS XBRL/PDF/HTML build, framed as a
  real-world trial rather than a demonstrator, for complete delivery in one
  factory sprint)
- Executed by: Codex
- What changed: added the confirmed greenfield requirements contract at
  `docs/requirements/structured-reporting-model-trial.md` and indexed it. The
  PRD defines a four-report, 48-task matched corpus; three formats, three model
  providers and three repetitions (1,296 responses); frozen protocol,
  equivalence gate, deterministic/proposition-based scoring, raw receipts,
  paired uncertainty analysis, public-ready outputs, one-sprint scope, and 16
  testable acceptance criteria. Publication remains an explicit approval gate.
- Decisions: the product is a candid research pilot whose null result is valid,
  not an XBRL showcase; full filings are fetched rather than redistributed when
  rights are unclear; exact model IDs are selected at protocol freeze; default
  live-call cap is £250; an open-weight fourth model is stretch-only.
- Evidence: requirement `REQ-structured-reporting-model-trial`; bead
  `software-factory-obq`; official Companies House accounts-data and FRC
  taxonomy/digital-reporting sources linked from the PRD.

## [2026-07-17 10:03 BST] planning | Goal for post-copy Incept5 fold-back and HLS simplification
- Driven by: Adam (asked for a Goalcraft objective to inspect every change
  since `i5-software-factory` was copied from this repo, fold useful generic
  changes back, and simplify HLS for one operator across laptops/VPS hosts)
- Executed by: Codex
- What changed: inspected both clean repositories and their histories; pinned
  the Incept5 bootstrap at `72df369` (copied from HLS v0.5.0) and current
  inspected head at `fe52b93`; confirmed HLS `bf44283` already adapted the
  v0.5.1-v0.6.1 trial fixes. Drafted a non-activated `/goal` that requires an
  evidence-backed port/adapt/already-present/reject decision for every fork
  commit, manual HLS-normalized integration, and removal of multi-human
  governance in favour of one decision-maker with multiple host/agent lanes.
- Evidence: Bead `software-factory-j4y`; both worktrees were clean and at their
  tracked `main`; inspected fork changelog and per-commit file stats through
  v0.12.0; Goalcraft fallback validation passed the 3,999-character hard gate
  at 1,963 objective characters. No goal was activated and no product files
  were changed.

## [2026-07-10 10:30 BST] workflow | v0.5.1–v0.6.1: fold-back of generic fixes from the incept5 fork
- Driven by: Adam (asked to fold back non-Incept5-specific updates from
  ../../incept5/i5-software-factory)
- Executed by: Claude
- What changed: ported every post-bootstrap change from the
  incept5/i5-software-factory fork (bootstrapped from this repo at v0.5.0,
  hardened in its live "chivo" factory trial), rename-normalized i5-→hls-.
  hls-factory-orchestrate: configurable integration branch; Lane Preflight
  (echo probe, auth-dependent model ids, sandbox cache/Docker/git-common-dir
  writable roots, env-fix propagation into later goals); Billing Guardrail
  (subscriptions only — `env -u` key stripping, auth-mode preflight,
  cooling never escalates billing, explicit `"billing": "api"` opt-in
  lane); migration timestamp-versioning preferred over range leases;
  second-merge rebase+re-gate; correctness-vs-capacity interference
  (serialize full-suite gates, 512m forked-test-heap root cause, OOM'd
  gate = bounce); process-durable headless dispatch via os.setsid spawn
  helper + supervisor relaunch loop. hls-beads: `bd ready` probe +
  template-copy recovery recipe. New skill hls-tech-playbook (six stack
  references + growth protocol). README/AGENTS/.gitignore/CHANGELOG
  updated to match. Skipped as repo-local: fork's bd-regenerated
  AGENTS/CLAUDE beads blocks, its docs/log entries, LICENSE/branding.
- Also: this repo's `.beads/` was config-without-database (the exact state
  the folded-back hls-beads recipe documents); remote had real history so
  recovery was `bd bootstrap` from `refs/dolt/data`, not reinit.
- Evidence: baseline check — fork bootstrap files diff-clean against this
  repo's HEAD after rename normalization, so all ports applied verbatim;
  validator 11/11 green; CHANGELOG 0.5.1–0.6.1; bead software-factory-0sx.

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
