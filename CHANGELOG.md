# Changelog

Newest first. One line per skill change, linking the feedback issue where one
exists.

## 0.8.0 — 2026-07-21

- hls-requirements-interview: adds the delivery interview/contract, separates `operatingMode`, `modelRoutingProfile`, `assuranceProfile`, and `releaseStage`, defaults unknown assurance to standard, and milestones criteria by first-use/operational/canonical/deferred.
- hls-architecture: adds a concise recorded rapid architecture for bounded reversible work, retains signed standard/assured paths, and restores deeper review on consequence triggers.
- hls-plan-builder: makes the first usable journey a rapid wave gate, separates story consequence risk from model-routing complexity, and carries release milestones plus linked deferrals.
- hls-factory-orchestrate: routes verification/review/promotion by assurance plus risk, preserves standard/assured protections, blocks rapid P0/P1/invariants, permits contract-accepted linked P2/P3, and migrates model routing from legacy `deliveryProfile` to `modelRoutingProfile`.
- hls-process-init: installs the four-field delivery contract, profile-specific verification guidance, first-usable proof, invariant stops, and explicit legacy config migration without inferring assurance or authority.
- **New skill: hls-issue-iteration** — selects GitHub feedback without mirroring the backlog into Beads, then reproduces, classifies, implements, proportionately verifies, checks the affected user journey, and closes or requeues with evidence.
- docs/validation: Factory Method, README/wiki/design/log, release notes, and the skill validator now make risk-calibrated delivery authoritative and keep the Vita pilot as a separate unclaimed follow-up (`software-factory-5sp`).

## 0.7.0 — 2026-07-17

- **Breaking operating-model simplification:** HLS now supports one human
  operator across one or more laptops/VPS hosts, not multi-human teams.
  `team-lanes.md`, human-owned source lanes, `.factory/team.json`, integrator/
  architect split authority, cross-human approvals, and CODEOWNERS generation
  are removed. New `host-lanes.md` treats machines as capacity/failover
  domains with one Beads queue, one active coordinator lease, and one operator
  retaining sign-off, waiver, promotion, credential, deploy, and external-
  action authority.
- hls-factory-orchestrate: adds the promotion gate, evidence-input and plan-
  fidelity checks, real-auth-path ownership, repo-hook preflight, calibrated
  simulator/real-vendor evidence loop, per-host lane setup, and fresh read-only
  review sessions. Review independence is context separation; the same
  operator, host, provider, subscription, and model are allowed.
- hls-factory-orchestrate: deterministic tamper-evident review packets freeze
  plan-owned inputs before branching, build canonical full/delta/promotion
  prompts from exact Git objects and versioned templates, bind hashes and
  verdicts to base/head, and verify the whole lineage. One operator reviews
  template-version changes; agents cannot approve their own rulebook.
- **New skill: hls-architecture** — explicit options and evidence before
  planning, operator sign-off, Mermaid architecture/design docs, revisit
  triggers, and third-party simulator calibration. No product stack wins by
  house policy; requirements and recorded decision criteria decide.
- hls-plan-builder: requires signed architecture (or an explicit unchanged
  reference), uses epic design-doc anchors and just-in-time story waves, makes
  criteria coverage the progress ledger, and carries every evidence-input MUST
  plus end-to-end reachability and simulator/real-integration proofs.
- hls-process-init: installs the architecture phase, committed skills lock,
  portable agent requirements plus per-host local profiles, self-documenting
  README links, published-report convention, third-party environment ladder,
  and SHA-pinned fresh-agent review gates without team machinery or fixed
  product-stack defaults.
- **New skill: hls-factory-status** — fixed-shape, read-only status across
  repos, hosts, lanes, gates, PRs, branches, and Beads queues, including local
  delta snapshots and the per-delivery-repo collector fix.
- **New skill: hls-publish-report** — optional Markdown-to-PDF convention for
  documents that genuinely leave a repo, with recorded regeneration and
  staleness discipline; no PDF was added for this release.
- **New skill: hls-skill-update** — committed `.factory/skills-lock.json`,
  Git-native private-repo CHANGELOG inspection, safe run-boundary updates,
  local-stopgap reconciliation, and a single Beads update lease across hosts.
- hls-skill-feedback: reads installed versions from the committed skills lock
  and registers every local stopgap in its divergence list.
- hls-skill-sweep: releases behavioural changelog entries that consumers read
  before uptake and routes consumers through hls-skill-update.
- hls-repo-bootstrap: human-browsable README orientation and a closeout ritual
  that follows active commit/push authority instead of assuming it.
- docs: README and AGENTS describe fifteen skills and the single-operator
  multi-host model; new `docs/factory-method.md` is the authoritative process
  explanation. Fold-back decisions for every pinned fork commit are recorded
  in Bead `software-factory-nhb`.

*Versions 0.5.1–0.6.1 were folded back on 2026-07-10 from the
incept5/i5-software-factory fork (bootstrapped from this repo at 0.5.0),
which hardened them in a live factory trial ("chivo"); `i5sf-*` evidence
ids refer to that fork's tracker.*

## 0.6.1 — 2026-07-09

- hls-factory-orchestrate (parallel-dispatch): **Billing Guardrail** — the
  factory runs on subscriptions only; per-token API billing requires an
  explicit `"billing": "api"` lane. Dispatch/supervisor environments strip
  `ANTHROPIC_API_KEY`/`OPENAI_API_KEY` (`env -u`), preflight verifies auth
  mode per lane, and usage-limit cooling never escalates billing. Example
  agents.json gains a disabled explicit API-overflow lane.
- hls-tech-playbook (harness-clis): silent-API-billing entry with concrete
  per-CLI verification commands (`codex login status`, env grep,
  apiKeyHelper check) run through the dispatch shell.
- hls-factory-orchestrate (running-the-factory): headless launches are
  billing-sanitized.

## 0.6.0 — 2026-07-09

- **New skill: hls-tech-playbook** — the factory's growing per-stack memory
  of technology-specific pitfalls and proven workarounds, consulted on
  demand (entry shape: Symptom → Root cause → Fix → Coordinator notes;
  growth via hls-skill-feedback). Seeded from the fork's chivo trial
  (i5sf-h5c/i5sf-147) with six references: schema migrations (timestamp
  versioning preferred over leased integer ranges — no allocation
  authority, no gaps; out-of-order trade-off documented), JVM/Gradle (512m
  forked-test-heap cliff, init-script override, sandbox cache roots),
  Quarkus testing (fixed test-port + coupled-URL leases, dev-services
  memory), git worktrees (common-dir sandbox access, lifecycle), macOS
  processes (os.setsid spawn helper, GNU-tool gaps, pgrep self-match),
  harness CLIs (auth-dependent model ids, version pinning, known-good
  codex sandbox flags, print-mode child lifetime).
- hls-factory-orchestrate: Long-Run Discipline now consults
  hls-tech-playbook on stack-smelling failures and feeds new fixes back;
  parallel-dispatch's migration guidance now prefers timestamp versions
  over range leases.

## 0.5.5 — 2026-07-09

- hls-factory-orchestrate (parallel-dispatch): trial-close findings —
  version leases need a single allocation authority (two branches
  independently took the same Flyway number); the second-merged concurrent
  story must be rebased onto integration and re-gated (auto-merged shared
  files produce a combined tree neither lane verified); sandboxed worktree
  lanes need the git common dir writable to self-commit; environment fixes
  discovered mid-run must propagate into later goals' verify lines.
- hls-factory-orchestrate (running-the-factory): durable dispatch upgraded
  to the proven `os.setsid()` spawn-helper pattern — nohup+disown guards
  only SIGHUP and macOS lacks a setsid binary.

## 0.5.4 — 2026-07-08

- hls-factory-orchestrate (parallel-dispatch): OOM guidance refined with the
  proven root cause — build tools fork test JVMs at small default heaps
  (Gradle 512m) that a growing suite crosses even run alone; check the fork
  heap before blaming concurrency, right-size it non-invasively from the
  coordinator (e.g. Gradle --init-script) and file the permanent build
  change as a sweep bead. Verified live: GL-B5 re-gated green on 2g and
  merged (chivo trial, i5sf-h5c).

## 0.5.3 — 2026-07-08

- hls-factory-orchestrate (parallel-dispatch): Verify Scope gains the
  correctness-vs-capacity interference distinction — leases partition
  ports/databases/migrations, but memory has no lease: run at most one
  full-suite gate at a time (or cap per-suite heap so N provably fit), and
  treat an OOM'd gate after passing story tests as a bounce, not a story
  failure. From the chivo trial's live 2-gate OOM on a 48 GB host
  (i5sf-h5c).

## 0.5.2 — 2026-07-08

- hls-factory-orchestrate (parallel-dispatch): Resource Leases gains
  schema-migration version-range leases — concurrent stories in a global
  Flyway/Liquibase namespace both pick the same "next" number; lease each
  story a range at dispatch and state it in the goal. Promoted from a live
  coordinator invention in the chivo trial (i5sf-18j).
- hls-factory-orchestrate (running-the-factory): headless coordinators must
  dispatch lanes process-durably — print-mode sessions kill harness
  background tasks and their children at end of reply (chivo trial run 1
  killed both lanes mid-story). New rules: nohup+pid-file dispatch, pid
  liveness in the resume ritual, crashed-lane re-dispatch, supervisor
  relaunch loop with a coordinator-only process match, absolute harness
  paths. Lane Preflight now requires probing through the dispatch shell.

## 0.5.1 — 2026-07-08

- hls-factory-orchestrate: integration branch made configurable —
  everywhere the skill says *main*, read the repo's integration branch
  (`.factory/agents.json` `"integrationBranch"` or `docs/process.md`);
  guards apply to that branch plus main itself. (Trial finding, i5sf-h5c.)
- hls-factory-orchestrate (parallel-dispatch): new Lane Preflight section —
  probe every lane cheaply before the first dispatch; model availability
  varies by auth (subscription CLIs reject ids API keys accept), and
  sandboxed lanes need build caches (Gradle/Maven/npm homes) granted as
  writable roots plus Docker-socket reach for testcontainers.
  (Trial finding, i5sf-h5c.)
- hls-beads: setup gains a `bd ready` probe and a template-copy recovery
  recipe (config without database → *database not initialized*, phantom
  remote-history refusal; reinit steps documented). (i5sf-9k1.)

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
