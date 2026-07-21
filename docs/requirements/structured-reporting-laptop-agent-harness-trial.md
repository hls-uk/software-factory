---
id: REQ-structured-reporting-laptop-agent-harness-trial
status: confirmed
mode: greenfield
updated: 2026-07-17
owner: Adam Chesney
target_repo: hls-uk/structured-reporting-agent-harness-trial
delivery: one factory sprint
supersedes:
  - REQ-structured-reporting-evaluation-harness-validation
  - REQ-structured-reporting-model-trial
---

# Laptop-Native Structured Reporting Agent Harness Trial

Build and run a public-ready, reproducible trial on one macOS laptop that uses
locally installed agent harnesses to compare Claude and Codex model families at
multiple model and effort levels against realistic fictional
XBRL/iXBRL, HTML, and PDF reporting tasks. The active Claude Code or Codex
session acts as the top-level coordinator; a deterministic repo-local runner
plans and dispatches the experiment, preserves receipts, scores results, runs a
bounded self-improvement loop, and regenerates the README from the evidence.

The trial produces genuine engineering evidence about the tested
**harness/model/effort configurations**. It does not use real company filings,
claim a representative market sample, answer whether one reporting format is
generally superior, or substitute for a separately commissioned study.

## Confirmation Basis

Adam confirmed on 2026-07-17 that:

- Claude and Codex must be included;
- each family must be exercised across different models and effort levels;
- a top-level agent harness must orchestrate execution, collation, iteration,
  and self-improvement;
- the public README must explain the method and results with clear, attractive
  Mermaid diagrams; and
- the system must run on a laptop through installed local harnesses, with no
  Eve, hosted orchestrator, VPS, or other control-plane dependency.

## Goals

- Produce inspectable evidence about the quality, consistency, latency, usage,
  and operational reliability of locally invoked Claude and Codex
  configurations on one fixed synthetic structured-reporting workload.
- Demonstrate a fair model-selection method: start with capable configurations,
  test lower-cost/faster alternatives, and retain the cheapest configuration
  whose degradation stays inside declared thresholds.
- Demonstrate agentic experiment operations: preflight, matrix freeze,
  detached execution, interruption-safe resumption, scoring, diagnosis,
  provider-neutral improvement, promotion gates, and evidence-derived reporting.
- Publish an open, rerunnable repository whose README makes the architecture,
  experiment history, results, trade-offs, and limitations understandable.
- Complete the repository, a real local run, and the generated results in one
  HLS Software Factory sprint.

## Success Signals

- Either Claude Code or Codex can coordinate the same frozen experiment through
  documented commands without changing the matrix or result semantics.
- The full trial contains at least two exact models and two native effort levels
  for each Claude and Codex family.
- Every result cell traces to a frozen input, exact executable and model,
  provider-native effort, raw harness stream, parsed response, score, and run
  receipt.
- A killed coordinator can be restarted and resumes incomplete cells without
  rerunning verified completed cells or corrupting evidence.
- At least one bounded improvement challenger is evaluated; a rejected change
  is a valid outcome, and no challenger is promoted using held-out results.
- The README is generated from machine-readable results, renders correctly on
  GitHub, and contains Mermaid views of the laptop architecture, execution loop,
  improvement history, and actual configuration trade-offs.

## Non-Goals

- No real listed-company filing, buyer-supplied data, confidential report, FRC
  material, or procurement-specific research protocol is included or fetched.
- The three fictional reports are not a representative sample of UK companies,
  sectors, taxonomies, reporting practice, or model use in the market.
- The trial does not estimate population effects, statistical significance, or
  policy implications and does not recommend a reporting format to a regulator.
- The README must not claim that XBRL, iXBRL, HTML, or PDF is generally better
  for AI. Format is a controlled workload dimension, not the research question.
- The product is not a model training, fine-tuning, RAG, filing-validation,
  tagging, accounting-advice, audit, or investment-advice system.
- No web dashboard, hosted API, background service, cloud queue, container
  platform, user account, or always-on process is required.
- No direct provider SDK integration is required for v1. All live inference is
  made through operator-installed command-line agent harnesses and the
  subscriptions or plans already configured for them.
- No prompt, tool, timeout, retry, or scoring rule may be tuned privately for a
  specific provider or changed after held-out results are exposed.

## Users & Context

### Primary users

- **HLS operator:** launches either Claude Code or Codex in the repository,
  reviews preflight and cost/quota estimates, authorises the run, and approves
  any later publication.
- **Coordinator agent:** invokes the local runner, monitors progress, diagnoses
  development-set failures, proposes shared improvements, and regenerates the
  report without editing evidence.
- **Independent reviewer:** verifies the frozen protocol, receipts, scorer,
  improvement decisions, generated README, and limitations from a clean clone.

### Operating context

- The target is the greenfield repository
  `hls-uk/structured-reporting-agent-harness-trial`.
- The canonical host is a current Apple Silicon macOS laptop. Linux portability
  is desirable but not an acceptance requirement for the live trial.
- Claude Code and Codex are locally installed executables and are the only live
  inference harnesses required by v1.
- Provider authentication remains in each installed harness or a gitignored
  host profile. Secrets are never copied into prompts, manifests, receipts, or
  tracked files.
- Network access is limited to inference traffic initiated by the configured
  harness. Model browsing, external search, remote file retrieval, and arbitrary
  network tools are disabled during cells.

## Product Shape

### Top-level coordination

The operator may use either Claude Code or Codex as the top-level coordinator.
The coordinator invokes a repo-local command, referred to here as `trialctl`,
instead of implementing scheduling in conversational state. `trialctl` is the
authoritative state machine for preflight, plan freeze, dispatch, resumption,
scoring, improvement gates, and report generation. This division preserves
agentic diagnosis and iteration while making execution identical whichever
coordinator is used.

Required coordinator workflow:

1. `trialctl preflight` validates executables, versions, auth mode, provider
   reachability, exact model IDs, effort mappings, structured output, tool
   restrictions, quota posture, and a nonce response.
2. `trialctl plan --dry-run` expands the complete matrix, calculates the maximum
   cell count, records exclusions, and displays the quota/cost warning.
3. `trialctl freeze` writes a content-hashed immutable protocol manifest.
4. `trialctl run` starts or resumes locally detached cell processes.
5. `trialctl score` deterministically scores verified receipts.
6. `trialctl propose` exports development-set failure clusters for the
   coordinator and records one candidate shared intervention.
7. `trialctl challenge` evaluates the candidate and applies the promotion gate.
8. `trialctl finalise` runs the sealed held-out set and consistency subset.
9. `trialctl report` regenerates results, README sections, and Mermaid from the
   frozen evidence.
10. `trialctl verify` independently checks hashes, completeness, README drift,
    boundary wording, and secret hygiene.

### Laptop-local state

- Portable protocol and profile declarations are tracked under `experiment/`.
- Absolute executable paths, provider environment bindings, and auth metadata
  live in gitignored `.trial/host.local.toml` with owner-only permissions.
- A local SQLite database provides atomic job claims and resumable state but is
  rebuildable from immutable receipt files and is not the evidence source.
- Each cell runs in an isolated temporary workspace containing only its task,
  one reporting representation, approved read-only inspection tools, and an
  output directory.
- Raw streams, final responses, receipts, scores, and decisions are append-only
  under `runs/<run-id>/`; report generation never mutates them.
- Cell processes start in their own operating-system session/process group so a
  coordinator exit does not terminate valid work. A later coordinator discovers
  and reconciles live, completed, timed-out, and orphaned cells.

## Installed Harness Adapters

### Claude family

- Invoke the absolute local `claude` executable in non-interactive print mode.
- Pin the exact harness version, exact Anthropic model ID, native effort value,
  structured-output schema, permission policy, and no-fallback setting.
- Test at least two currently accessible Claude model IDs representing a higher
  capability and a cheaper/faster tier, each at two supported effort levels.

### Codex family

- Invoke the absolute local `codex exec` executable in ephemeral,
  non-interactive, read-only mode with JSONL events and an output schema.
- Pin the exact harness version, exact OpenAI model ID, native reasoning-effort
  setting, sandbox/tool policy, and no-fallback setting.
- Test at least two currently accessible Codex model IDs representing a higher
  capability and a cheaper/faster tier, each at two supported effort levels.

### Matrix freeze rules

- Discovery aliases may be used only during preflight. Frozen runs contain
  provider-confirmed exact model IDs; a model alias or silent provider fallback
  is invalid.
- The minimum complete matrix is two families × two models × two efforts =
  **8 configurations**. A partial diagnostic may run, but it cannot generate
  the final-trial badge, headline results, or completion claim.
- Effort is stored twice: the provider-native value and a descriptive trial
  tier (`standard` or `highest`). The README must state that similarly named
  effort levels are not assumed to represent equal compute across providers.
- Unsupported combinations are rejected or explicitly excluded before freeze;
  they are never silently remapped.

## Realistic Fictional Reporting Pack

Create three explicitly fictional UK-listed-style annual-report packs from
canonical typed data. Together they cover:

- at least 90 numerical facts across instant and duration contexts, GBP and
  pure units, scaling, signs, comparatives, segments, and dimensions;
- at least 24 narrative sections across policies, risks, governance,
  performance, estimates, and non-financial measures;
- ordinary, multi-segment, and deliberately awkward-but-valid presentation
  patterns; and
- controlled missing, ambiguous, duplicated-label, and malformed negative
  fixtures kept outside the main valid pack.

Generate matched iXBRL/XBRL, semantic HTML, and paginated accessible PDF
representations deterministically from each canonical source. A cross-format
manifest maps every scored item to its canonical identity and representation
locator. Every artifact names the company and data as fictional and unaudited.

The public repository may use suitably licensed taxonomy/conformance material,
but it must not redistribute a real filing or imitate an identifiable company.

## Task Bank and Split

Define eight matched task specifications, each run against XBRL/iXBRL, HTML,
and PDF, yielding 24 representation-specific cases:

- two numerical extraction and reconciliation tasks;
- two unit, period, scale, sign, or dimensional-context tasks;
- two narrative evidence and qualification tasks; and
- two multi-step tasks combining facts and narrative while remaining
  deterministically or proposition-scoreable.

Four task specifications form the development set and four form the held-out
set. The split, prompts, answer schemas, gold data, weights, timeouts, and random
seed are frozen before baseline execution. The coordinator may see development
failure details but receives no held-out scores or gold-answer material until
all interventions are frozen.

Each cell receives the same instruction template and an isolated workspace with
one representation. The model may use only read/search operations and the
bundled provider-neutral report-inspection command. All tool calls are captured.
No cell can read another cell, a score, a gold answer, or a prior response.

## Execution Protocol and Call Bound

The default complete run is bounded as follows:

- baseline: 8 configurations × 12 development cases = **96 cells**;
- up to two challenger rounds: 8 × 12 × 2 = **192 cells** maximum;
- final held-out run: 8 × 12 held-out cases = **96 cells**; and
- consistency subset: 8 × 4 predeclared cases = **32 cells**.

The default maximum is therefore **416 live cells**, excluding bounded nonce
preflights. The dry run displays the exact count and subscription/quota warning,
and requires explicit operator confirmation before the first live cell.

Execution order is deterministically shuffled by the frozen seed and
interleaves families to reduce time-of-day bias. Concurrency defaults to two
cells overall and one per provider profile. Provider cooling, rate-limit, and
subscription exhaustion signals pause future dispatch rather than changing
models, effort, prompts, billing mode, or results.

Timeouts and retries are predeclared. A transport retry preserves the same cell
identity and records lineage; a new model response after a valid terminal
response is a new repetition, never a replacement. Failures, refusals,
malformed outputs, timeouts, and quota exhaustion remain in the denominator.

## Scoring and Measures

### Primary score

Each answer receives a 0–1 deterministic weighted score from exact/tolerance
values, required units/periods/entities, controlled propositions, and evidence
locators. A wrong entity, period, unit, scale, sign, unsupported material claim,
or missing required component receives a predeclared penalty. An LLM is never
the sole judge of the primary score.

### Secondary measures

- schema-valid and terminal-success rates;
- answer completeness and evidence-locator correctness;
- consistency on the repeated subset;
- unsupported-claim, refusal, timeout, and tool-error rates;
- wall-clock latency and time-to-first/final output where exposed;
- provider-reported input/output/cached tokens and quota/cost metadata where
  exposed; and
- orchestration reliability: start, completion, recovery, duplicate-avoidance,
  and receipt-integrity rates.

Results are reported by exact configuration and round. Format-level data may be
shown only as synthetic diagnostic strata with cell counts and the mandatory
non-generalisation notice; the README must not rank formats, estimate a format
effect, or recommend a format.

### Fit recommendation

For each family and overall, report the highest-scoring configuration and the
least-expensive/faster configuration whose primary score is no more than 0.03
below that family leader, whose schema-valid rate is no more than one percentage
point lower, and whose unsupported-claim rate is no more than one percentage
point higher. Where usage or cost is unavailable, label the fit conclusion
`quality/latency only` rather than inventing economics.

## Bounded Self-Improvement Loop

The coordinator may propose at most one provider-neutral intervention per
challenger round. Eligible interventions are shared prompt wording, answer
schema clarification, common report-inspection guidance, timeout policy, or
deterministic preprocessing applied identically to every configuration.

The proposal record contains the development failure cluster, hypothesis,
changed artifact hashes, expected benefit, risk, and rollback. Provider- or
model-specific prompt changes, hidden examples, held-out inspection, gold-answer
exposure, and scorer changes are prohibited after baseline.

A challenger is promoted only when all of these gates pass on the development
set:

- macro primary score improves by at least 0.02;
- no model family loses more than 0.03 primary score;
- schema-valid rate falls by no more than one percentage point;
- unsupported-claim rate rises by no more than one percentage point; and
- no boundary, receipt, or fairness check fails.

Failed challengers remain in the evidence and the prior version stays active.
After at most two challengers, the active version is frozen before the held-out
set is released. Held-out performance is reported once and cannot trigger a new
intervention in the same trial.

## Reproducibility and Receipt Contract

Every attempt records:

- run, round, cell, task, representation, and repetition identifiers;
- hashes of the protocol, source pack, prompt, schema, tool policy, and gold
  definition used by the scorer;
- host OS/architecture, runner commit, absolute executable identity and hash,
  harness version, provider, family, exact model ID, native effort, and trial
  effort tier;
- random seed and dispatch-order position;
- start/end timestamps, duration, process ID/group, exit status, terminal class,
  and retry/parent lineage;
- raw event/stdout/stderr content hashes and paths, parsed final response, tool
  transcript, and validation status;
- token, cache, quota, and cost metadata actually exposed by the harness; and
- scorer version, component scores, penalties, and final score.

Receipts are content-addressed and append-only. Scoring and reporting operate
from verified receipts. Re-scoring creates a new derived result linked to the
same raw receipt and never changes original evidence.

## Generated README and Results

The README is the public report and is regenerated from `results/summary.json`
and verified receipts. Human-authored context and generated sections are
separated by stable markers; `trialctl verify` fails if generated content has
been hand-edited or is stale.

It must contain:

- the question, synthetic corpus, exact frozen matrix, execution dates, call
  counts, exclusions, scoring method, and prominent limitations;
- an attractive colour-blind-safe Mermaid laptop architecture flowchart;
- a Mermaid sequence or state diagram of baseline, proposal, challenger,
  promotion/rejection, freeze, held-out run, and report generation;
- a generated Mermaid results map grouped by family, with every node labelled
  by exact model, native effort, primary score, completion rate, and median
  latency, plus accessible Markdown tables containing the same values;
- baseline-to-final deltas and an iteration ledger showing accepted and rejected
  interventions;
- the fit recommendation and the explicit caveat where cost/quota evidence is
  unavailable;
- links from each aggregate to the frozen manifest and underlying receipts;
- rerun, resume, verify, and report-regeneration commands; and
- this notice near every headline result:

> This is a synthetic engineering trial of specific laptop agent-harness,
> model, and effort configurations. It is not evidence about UK companies or a
> representative comparison of XBRL, HTML, and PDF, and it must not be used to
> infer regulatory or market-wide conclusions.

Mermaid source must render in GitHub's supported syntax. A generated SVG may be
added as an accessibility/fallback artifact, but it does not replace the
Mermaid source or result tables.

## Security, Billing, and Publication

- The repository stores environment-variable names and redacted auth mode only,
  never credential values, cookies, tokens, account identifiers, or global
  harness configuration.
- Each adapter receives an explicit allowlist of environment variables. API-key
  fallbacks and a change of billing mode are prohibited unless the operator
  explicitly adds and freezes that profile before the trial.
- Harness processes receive read-only task inputs and no access to home-folder
  credentials beyond what the harness itself needs for provider authentication.
- Logs redact environment values and known secret patterns before persistence;
  secret scanning is a release gate.
- Local creation and execution are authorised by this PRD. Repository creation,
  push, publication, or external sharing still requires Adam's explicit later
  approval.

## Deliverables

The target repository must contain:

- a Python-based `trialctl` CLI with preflight, plan, freeze, run, resume,
  watch, score, propose, challenge, finalise, report, and verify commands;
- portable experiment declarations and a documented gitignored host profile;
- Claude Code and Codex adapters behind one contract;
- three generated fictional report packs in XBRL/iXBRL, HTML, and PDF plus
  equivalence and conformance validation;
- the eight-task development/held-out bank, answer schemas, gold data, and
  deterministic scorer;
- isolated cell workspaces, detached process supervision, SQLite state index,
  append-only receipts, raw streams, resumption, and tamper verification;
- the bounded improvement proposal and promotion workflow;
- machine-readable full results, the generated README, Mermaid source, and
  accessible tables;
- offline unit/integration tests, record-and-replay adapter fixtures, negative
  boundary tests, and one small opt-in live preflight test per profile;
- the completed frozen local trial and results, not merely an empty framework;
  and
- licence, limitations, data provenance, security, billing, contribution, and
  independent reproduction documentation.

## Acceptance Criteria

1. **AC-01 — Laptop-only clean setup:** Given a clean current Apple Silicon
   macOS clone with Python and the documented local harnesses, when setup runs,
   then all offline tests and synthetic-pack generation pass without a server,
   daemon, VPS, container platform, or Eve dependency.
2. **AC-02 — Explicit host preflight:** Given configured local profiles, when
   `trialctl preflight` runs, then it reports absolute executable paths and
   versions, redacted auth mode, exact reachable models, supported effort
   values, schema/tool capability, nonce success, and quota posture; a missing
   or incompatible harness configuration fails with a specific remediation
   message.
3. **AC-03 — Complete frozen matrix:** Given successful preflight, when the plan
   freezes, then it contains at least two exact models × two native efforts for
   each Claude and Codex family, contains no alias or fallback, and expands to
   exactly the declared cells and exclusions.
4. **AC-04 — Coordinator parity:** Given the same frozen manifest, when Claude
   Code and Codex independently invoke dry-run/report commands, then both
   produce identical cell IDs, order, hashes, scores, and generated README
   content without coordinator-specific state.
5. **AC-05 — Realistic fictional equivalence:** Given the three canonical
   fictional reports, when generation and validators run, then at least 90
   facts and 24 narrative sections map to valid, equivalent XBRL/iXBRL, HTML,
   and PDF locators, and no real-company or buyer material is present.
6. **AC-06 — Fair isolated cells:** Given any trial cell, when it executes, then
   it sees only its task and one representation, uses the frozen common prompt,
   schema, timeout, retry, and read-only tool policy, cannot see gold answers or
   other runs, and records every tool call and terminal state.
7. **AC-07 — Durable local execution:** Given running cells, when the top-level
   coordinator exits or is killed and a new coordinator resumes, then verified
   completed cells are reused, valid detached cells are reconciled, orphaned or
   timed-out cells are classified, and no completed response is overwritten or
   silently duplicated.
8. **AC-08 — Complete bounded live trial:** Given operator confirmation after
   the exact dry-run count, when the complete trial runs, then baseline, at
   least one challenger, final held-out, and consistency phases complete within
   the 416-cell default cap; every failure remains represented and any partial
   matrix prevents a full-trial completion claim.
9. **AC-09 — Deterministic scoring:** Given authored truth cases and live
   receipts, when scoring runs repeatedly, then exact/tolerance, entity, unit,
   period, scale, sign, proposition, evidence, refusal, malformed, and timeout
   cases produce identical declared component and aggregate scores without an
   LLM as the sole judge.
10. **AC-10 — Fair execution order and no silent adaptation:** Given the frozen
    seed and provider constraints, when dispatch runs, then cell order is
    reproducible and family-interleaved, rate limits pause dispatch rather than
    changing model/effort/billing, and every retry or exclusion has explicit
    lineage and remains auditable.
11. **AC-11 — Bounded self-improvement:** Given baseline development results,
    when the coordinator proposes a challenger, then exactly one shared
    intervention with hypothesis and changed hashes is recorded, all 8
    configurations receive it, held-out material remains unavailable, and no
    scorer or provider-specific tuning occurs.
12. **AC-12 — Mechanical promotion gate:** Given challenger results, when the
    promotion gate runs, then it accepts only interventions meeting all declared
    score, family-regression, schema-validity, unsupported-claim, fairness, and
    integrity thresholds; rejected versions remain reproducible and held-out
    results cannot reopen iteration.
13. **AC-13 — Immutable receipts and rebuild:** Given an interrupted or complete
    run, when verification and index rebuild run, then every derived score and
    aggregate traces to verified append-only raw evidence, tampering is
    detected, and the disposable SQLite state can be reconstructed from files.
14. **AC-14 — Evidence-derived README:** Given verified final results, when
    reporting runs, then the README and `results/summary.json` agree exactly,
    all required Mermaid diagrams render, accessible tables carry the same
    values, aggregates link to receipts, generated-section drift is detected,
    and the synthetic non-generalisation notice is prominent.
15. **AC-15 — Security and boundary:** Given repository, process, and generated
    artifact scans, when release verification runs, then no secret, global
    config, real filing, procurement content, external-search result, format
    ranking, population inference, policy recommendation, or unapproved
    publication action is present.
16. **AC-16 — One-sprint definition of done:** The factory may close the sprint
    only when AC-01–AC-15 have criterion-linked evidence, CI and an independent
    review pass, the full local trial and generated results are present, and the
    repository is ready for Adam's separate publication decision.

## Constraints

### Hard

- Deliver and execute the complete v1 in one HLS Software Factory sprint.
- Run on one laptop through installed local harnesses; no external orchestrator
  or always-on infrastructure.
- Include Claude and Codex, at least two models per family, and at least two
  effort levels per model in a complete trial.
- Use fictional data only and preserve the non-substitution boundary with the
  potential commissioned study.
- Freeze exact model IDs, parameters, protocol, scoring, and seed before live
  execution; prohibit silent fallback.
- Preserve all failures and raw evidence, and make scoring/reporting
  deterministic from verified receipts.
- Require explicit operator confirmation after dry-run count/quota warning and
  explicit later approval before repository publication or external sharing.

### Preferences

- Prefer Python 3.12+, `uv`, typed schemas, SQLite from the standard library,
  and small auditable dependencies.
- Prefer the installed Claude Code and Codex executables without adding another
  provider or harness to v1.
- Prefer subscription-plan authentication already held by the harness and
  provider cooling over API-key billing or concurrency escalation.
- Prefer GitHub-rendered Mermaid plus accessible Markdown tables over a custom
  dashboard or JavaScript report application.

## Assumptions

- [confirmed] The system must not use Eve and must run on a laptop via installed
  harnesses.
- [confirmed] Claude, Codex, multiple family models, and multiple effort levels
  are required.
- [confirmed] The top-level harness must orchestrate execution, result
  collation, iteration, and self-improvement.
- [confirmed] The open-source README must show the method and actual results
  with clear Mermaid diagrams.
- [confirmed] HLS Software Factory should deliver the complete trial in one
  sprint.
- [confirmed] Other model families and harnesses are excluded from v1 to keep
  the trial focused and simple.
- [assumed] Three fictional reports, eight matched tasks, 8 configurations,
  and a maximum of 416 live cells balance credible evidence with laptop and
  subscription constraints.
- [assumed] Two challenger opportunities are enough to demonstrate bounded
  self-improvement without turning the trial into indefinite prompt search.
- [assumed] The target repository may become public only after Adam reviews the
  completed evidence and explicitly approves publication.

## Open Questions

None block architecture or factory planning. Exact Claude and Codex model IDs
are deliberately selected by live preflight and frozen before execution because
subscription availability changes over time.

## Factory Handoff

- **Requirements source:** this document. Both earlier structured-reporting
  PRDs are retained as superseded audit records and must not be planned.
- **Delivery mode:** greenfield repository, one complete factory sprint.
- **Architecture source:**
  `docs/architecture/structured-reporting-laptop-agent-harness-trial-architecture.md`
  after operator sign-off.
- **Required factory path:** sign off architecture → bootstrap target repo →
  initialise factory → cut stories from AC-01–AC-16 → implement and review →
  run the full authorised local trial → generate and verify results → present
  the local repository for Adam's publication decision.
- **Stop condition:** stop before live execution if the exact matrix, cell cap,
  auth/billing mode, or harness profile cannot be frozen; stop before release if a
  real filing, secret, format-ranking claim, or untraceable aggregate appears.
- **Release gate:** local implementation and the confirmed full trial are in
  scope; repository creation, push, publication, and external sharing are not
  authorised by this PRD.
