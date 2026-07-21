---
id: REQ-structured-reporting-model-trial
status: superseded
mode: greenfield
updated: 2026-07-17
owner: Adam Chesney
target_repo: hls-uk/structured-reporting-model-trial
delivery: one factory sprint
superseded_by: REQ-structured-reporting-laptop-agent-harness-trial
---

# Structured Reporting Model Trial

> **Superseded — do not build.** This study-shaped PRD was replaced on
> 2026-07-17 by the focused
> [Laptop-Native Structured Reporting Agent Harness Trial](structured-reporting-laptop-agent-harness-trial.md).
> It is retained only as an audit record and must not be used as factory input.

Build and run a small, reproducible real-world trial that measures how the
same AI models perform when equivalent UK corporate-reporting disclosures are
presented as structured XBRL, human-readable HTML, or PDF. The shipped product
is an evidence-producing research toolkit and a completed pilot dataset, not a
scripted showcase: the protocol is fixed before model runs, all results and
failures are retained, and the report may find that format makes little or no
difference.

## Confirmation Basis

Adam confirmed on 2026-07-17 that this should be framed and built as a genuine
trial rather than a demonstrator, and that the complete v1 should be handed to
the HLS Software Factory for delivery in one sprint. The remaining design
choices below are explicit bounded assumptions made to keep that handoff
buildable without another requirements round.

## Goals

- Produce credible, inspectable evidence about whether XBRL, HTML, or PDF
  affects model accuracy, completeness, consistency, evidence-grounding,
  latency, and cost on matched corporate-reporting tasks.
- Prove an HLS approach to fair multi-provider model evaluation: frozen inputs,
  equivalent prompts, repeated runs, deterministic scoring where possible,
  recorded provenance, and no selective omission of unfavourable results.
- Deliver a public-ready, reusable toolkit that an independent reviewer can
  inspect, rerun on a small subset, and extend with new filings, tasks, formats,
  or providers.
- Complete a candid pilot report with effect sizes, uncertainty, limitations,
  and raw evidence sufficient to support future research bids.

## Success Signals

- The full frozen matrix runs without manual editing of prompts, gold answers,
  or source packs after results begin to arrive.
- Every reported aggregate traces to a source filing, task definition, exact
  model configuration, raw response, scorer version, and trial-run receipt.
- A clean checkout can reproduce deterministic corpus validation and scoring,
  and can rerun a documented smoke subset with the user's own provider keys.
- The conclusions distinguish observed pilot evidence from general claims and
  explicitly permit a null or mixed result.

## Non-Goals

- This is not an XBRL tagging, authoring, conformance, or filing-validation
  product.
- It is not an audit, accounting opinion, investment advice, or a claim that
  model answers are suitable for regulatory decision-making.
- It is not a comprehensive model leaderboard or a statistically representative
  study of all UK companies, taxonomies, sectors, or disclosure types.
- It will not compare RAG, fine-tuning, agents, browsing, external calculators,
  or proprietary reporting-software products.
- It will not provide a hosted SaaS application, authentication, user accounts,
  or an interactive dashboard. A command-line workflow and static HTML report
  are sufficient for v1.
- It will not conceal inconvenient failures, tune prompts per format or model,
  or optimise the task bank after seeing model results.

## Users & Context

### Primary users

- **HLS research lead:** freezes the protocol, supplies provider credentials,
  executes the live trial, and approves the interpretation.
- **Independent reviewer:** checks representation equivalence, gold answers,
  raw responses, scoring, and the link between evidence and conclusions.
- **External technical reader:** clones the eventual public repository, runs
  offline validation, and reruns a smoke subset with their own API keys.

### Operating context

- The target is a new repository, `hls-uk/structured-reporting-model-trial`.
- Development and deterministic verification must work on current macOS and
  Linux environments from a clean clone.
- Live evaluation uses direct provider APIs and public UK corporate-reporting
  sources. Live calls are explicit and never run as part of ordinary CI.
- Repository creation and external publication require Adam's explicit approval
  at the point of publication; the factory may prepare everything locally first.

## Research Question and Hypotheses

### Primary question

For matched UK annual-report disclosures and a fixed set of questions, how does
input representation (structured XBRL, visible HTML, or PDF) affect the quality
and operational performance of current general-purpose AI models?

### Pre-specified hypotheses

- **H0:** Input representation does not produce a material difference in the
  primary task score after accounting for model and task type.
- **H1:** Structured XBRL improves numerical accuracy, answer completeness, and
  evidence location relative to equivalent HTML and PDF evidence.
- **H2:** Any format advantage varies by task class; narrative and
  accounting-policy questions may not follow the pattern seen in numerical
  extraction.
- **H3:** Models differ in how much they benefit from structured data, so a
  format result must not be presented as provider-independent without evidence.

The shipped report must evaluate all four statements. It must not be written to
confirm H1.

## Trial Scope

### Corpus

The v1 corpus contains four real, publicly available UK annual reports from
four issuers and at least two sectors. Each admitted report must have:

- a public iXBRL/XBRL source;
- a corresponding published PDF covering the same entity, reporting period,
  currency, consolidation scope, and disclosed values;
- a human-readable HTML representation derived from the visible iXBRL content;
- sufficient tagged numerical and narrative content for all task classes; and
- stable source URLs plus downloaded-file hashes.

Prefer a mix of reporting/taxonomy profiles if four genuinely matched reports
can still be admitted without weakening the equivalence gate. Corpus diversity
must never take precedence over source equivalence.

Full third-party filings should be fetched during corpus build and cached
locally rather than committed when redistribution rights are unclear. The
repository stores source URLs, acquisition timestamps, content hashes,
licensing notes, and only the minimum lawful fixtures needed for offline tests.

### Three matched representations

Each task is backed by a disclosure pack in all three representations:

1. **XBRL:** standards-aware extraction of the relevant facts, contexts, units,
   dimensions, concept names, human labels, and necessary relationships,
   serialized deterministically without adding an answer or interpretation.
2. **HTML:** the corresponding visible XHTML/HTML disclosure with inline XBRL
   metadata removed while preserving headings, tables, footnotes, ordering, and
   visible text.
3. **PDF:** the corresponding pages from the issuer's published annual-report
   PDF, supplied through the provider's documented PDF/file interface.

A pack contains a complete disclosure section (or the two complete sections
needed for a cross-disclosure task), not an answer-adjacent sentence. Raw token
counts may differ because representation efficiency is part of the question;
serialized bytes, pages, extracted text length, and provider-reported tokens
must be recorded.

### Equivalence gate

A task may enter the frozen trial only when an independent check confirms that
all three packs:

- refer to the same entity, period, currency, unit, and consolidation scope;
- contain enough evidence to answer the question without outside knowledge;
- have the same gold answer after accounting for presentation differences; and
- contain no format-specific annotation that gives away the expected answer.

Failed candidates are retained in an exclusion log with a machine-readable
reason. They are not silently repaired or replaced after trial execution starts.

### Task bank

The frozen bank contains 48 questions, 12 per report:

| Task class | Per report | Total | Typical question |
|---|---:|---:|---|
| Numerical extraction and comparison | 5 | 20 | Value, unit, period, change, or ratio from a statement or note |
| Accounting-policy or standard-related disclosure | 2 | 8 | Identify the disclosed policy, basis, judgement, or standard treatment |
| Narrative comprehension | 3 | 12 | Extract a stated risk, driver, commitment, or explanation |
| Cross-disclosure consistency | 2 | 8 | Reconcile or identify an inconsistency across two related sections |

Questions must be answerable solely from their supplied packs. Each task stores
the question, task class, expected answer type, gold answer, accepted tolerance
or proposition rubric, format-specific source locators, and exclusion-sensitive
metadata.

### Gold-answer control

- Numerical gold answers include value, scale, unit, period, sign convention,
  and an explicit tolerance (normally exact after scale normalisation).
- Categorical answers use a controlled accepted-value set.
- Narrative answers use required and prohibited propositions rather than a
  single reference paragraph or an LLM similarity score.
- Gold answers and locators receive a separate fresh-session review before the
  protocol is frozen. A model under test must not create or approve its own gold
  answer.
- Gold changes after freeze create a new protocol version and invalidate the old
  result set; they are never applied in place.

## Model and Run Design

### Model matrix

Use one current, generally available production model from each of OpenAI,
Anthropic, and Google. Exact immutable model identifiers and provider API
versions are selected and recorded when `trial-v1` is frozen. An open-weight
model is a stretch addition only if all Must requirements are already complete.

Each of 48 tasks is run against:

- 3 formats;
- 3 model providers; and
- 3 independent repetitions.

The planned matrix therefore contains **1,296 model responses**. Transient
transport failures may be retried under the frozen retry policy; failed attempts
remain in the audit trail and do not count as repetitions.

### Fairness controls

- The question, system instruction, output schema, and substantive prompt text
  are identical across providers and formats. Adapters may change transport
  syntax only.
- Each call receives one format only and has no browsing, tools, memory, code
  execution, or access to another response.
- PDF is sent through the selected provider model's documented native file/PDF
  interface. A provider/model without that capability is ineligible for v1.
- Sampling temperature is zero or the provider's lowest supported value. Other
  generation limits are aligned where supported and all exceptions are logged.
- Execution order is randomized from a recorded seed and blocked so that time
  or provider throttling does not systematically favour a format.
- A response uses a provider-neutral schema containing answer, concise
  justification, confidence, evidence locators, and answer status. The trial
  asks for inspectable evidence, not hidden chain-of-thought.
- Prompt changes, model substitutions, and provider-version changes require a
  new protocol version rather than an in-place rerun.

### Budget and execution controls

- A dry run reports exact planned calls, estimated input/output volume, and an
  estimated cost by provider before live execution.
- Live execution requires an explicit command and an environment-supplied
  `TRIAL_BUDGET_GBP`; v1 defaults to a maximum of **£250**.
- The runner refuses to start when its estimate exceeds the cap and stops
  dispatching before recorded spend would cross it.
- Calls are content-addressed, resumable, and idempotent. Restarting the runner
  must not pay for an already completed cell unless an explicit, audited rerun
  is requested.

## Measures and Scoring

### Primary outcome

The primary outcome is a pre-specified task score on a 0–1 scale:

- deterministic exact/tolerance scoring for numerical and controlled answers;
- proposition-based scoring for narrative and policy answers; and
- explicit penalties for wrong unit, period, entity, scope, unsupported claim,
  or missing required answer component.

The score definition and task-class weights are frozen before live execution.

### Secondary outcomes

- **Accuracy:** correctness of required answer components.
- **Completeness:** proportion of required components supplied.
- **Consistency:** agreement among the three independent repetitions for the
  same model, format, and task.
- **Evidence grounding / explainability:** whether cited facts, concepts, pages,
  tables, or sections exist and support the answer.
- **Unsupported-claim rate:** material claims not supported by the supplied pack.
- **Failure rate:** refusal, malformed output, truncation, provider error, or
  inability to process a representation.
- **Operational measures:** latency, input/output tokens, serialized input size,
  and estimated/actual provider cost.

An LLM may assist proposition extraction only as a separately reported aid. It
must not be the sole judge of correctness. The deterministic scoring path and
all human/fresh-session overrides remain inspectable.

### Analysis

- Report results by format, model, task class, and their interactions.
- Compare formats on matched tasks using paired effect sizes and 95% uncertainty
  intervals, with resampling clustered by report rather than treating every
  response as wholly independent.
- Show the distribution and the underlying cell counts, not only headline
  averages.
- Separate model-output variability from scorer uncertainty and provider
  transport failures.
- Do not use statistical significance as a substitute for practical effect or
  claim population-wide generality from four reports.

## Reproducibility and Audit Requirements

- Freeze a versioned protocol and SHA-256 manifest before live model calls. The
  manifest binds source files, disclosure packs, tasks, prompts, gold answers,
  scorer version, model IDs, parameters, and randomization seed.
- Store every attempt as an immutable receipt containing content hashes,
  provider/model identifiers, timestamps, parameters, status, duration, token
  usage, estimated cost, raw response, parsed response, and error details.
- Keep raw outputs separate from scored/derived results. Re-scoring must never
  mutate raw evidence.
- Make aggregation deterministic from the frozen receipts and scorer version.
- Generate a machine-readable results table plus a static HTML and Markdown
  report from the same analysis data.
- Record all exclusions, retries, overrides, protocol deviations, and known
  limitations in append-only logs that the report summarizes.
- Define reproducibility honestly: model outputs may vary on a later date, but
  the exact inputs/configuration are recoverable and scoring of a retained run
  is deterministic.

## Deliverables

The target repository must contain:

- a concise README with trial purpose, status, quick start, live-cost warning,
  and commands for offline validation, smoke rerun, and full execution;
- frozen protocol and manifest files for `trial-v1`;
- source acquisition and corpus-building code plus provenance/exclusion data;
- the 48-task bank, gold-answer pack, and equivalence-review evidence;
- provider-neutral runner with OpenAI, Anthropic, and Google adapters;
- deterministic parsers, scorers, consistency/evidence checks, and analysis;
- content-addressed raw attempt receipts and machine-readable results;
- a completed pilot report in Markdown and static HTML;
- a limitations, ethics, data-rights, and reproducibility statement;
- an offline smoke fixture and automated test suite; and
- CI that validates fixtures, schemas, hashes, scoring, analysis generation, and
  secret hygiene without making provider calls.

The internal layout is an implementation choice, but protocol, corpus, raw
evidence, derived results, and report outputs must remain visibly separated.

## Acceptance Criteria

1. **AC-01 — Clean setup:** Given a clean macOS or Linux clone with no provider
   credentials, when the documented setup and offline verification commands run,
   then dependencies install reproducibly and all non-live checks pass without
   making a network model call.
2. **AC-02 — Real public corpus:** Given the v1 source manifest, when its
   validator runs, then it identifies four real UK issuers across at least two
   sectors, one report per issuer, stable source URLs, acquisition timestamps,
   reporting metadata, rights notes, and SHA-256 hashes for every acquired file.
3. **AC-03 — Matched representations:** Given any admitted task, when its
   disclosure-pack validator runs, then XBRL, HTML, and PDF packs are present,
   their entity/period/currency/scope metadata agree, and the independent
   equivalence review and three format-specific evidence locators are recorded.
4. **AC-04 — Transparent exclusions:** Given a candidate that fails an
   admission rule, when corpus build completes, then it is absent from the
   frozen bank and appears in a machine-readable exclusion log with the failed
   rule and supporting evidence.
5. **AC-05 — Frozen task bank:** Given `trial-v1`, when protocol validation runs,
   then exactly 48 admitted tasks exist with the required 20/8/12/8 class split,
   complete gold-answer metadata, answer rubrics, and independent review status.
6. **AC-06 — Protocol integrity:** Given the frozen manifest, when any bound
   source, pack, prompt, task, gold answer, scorer, model configuration, or seed
   changes, then validation fails and instructs the operator to create a new
   protocol version.
7. **AC-07 — Fair run plan:** Given valid provider configuration, when a dry run
   is requested, then it reports 1,296 planned successful responses, the
   randomized order seed, exact model IDs/parameters, estimated tokens and cost,
   and refuses live execution if the estimate exceeds `TRIAL_BUDGET_GBP`.
8. **AC-08 — Complete live matrix:** Given funded, working provider credentials,
   when the full trial completes under the frozen retry policy, then every one
   of the 48 × 3 × 3 × 3 cells has a successful terminal response, while every
   failed/retried attempt is also retained and distinguishable.
9. **AC-09 — Resumable receipts:** Given a deliberately interrupted live run,
   when execution resumes, then completed cells are reused by content hash,
   missing cells continue, and no completed provider call is repeated without
   an explicit audited rerun flag.
10. **AC-10 — Traceable scoring:** Given any result row or report figure, when a
    reviewer follows its identifiers, then they can reach the task, three input
    packs, exact prompt/configuration, raw response, parsed response, scorer
    version, score components, and source-filing locators.
11. **AC-11 — Required measures:** Given the completed matrix, when analysis
    runs, then it emits accuracy, completeness, repeat consistency,
    evidence-grounding, unsupported-claim, failure, latency, token, and cost
    measures by format, model, and task class in machine-readable form.
12. **AC-12 — Candid paired analysis:** Given the results table, when the report
    is generated, then it includes matched format effects, clustered 95%
    uncertainty intervals, distributions and cell counts, model/task
    interactions, protocol deviations, and a conclusion that is valid even when
    H0 is not rejected.
13. **AC-13 — Independent smoke rerun:** Given a reviewer with their own API
    keys, when they run the documented 12-call smoke subset, then the same frozen
    inputs and scoring path are used, new immutable receipts are produced, and
    their result is kept separate from the canonical v1 run.
14. **AC-14 — Secret and data hygiene:** Given CI and repository scans, when all
    tracked files are inspected, then no provider key, environment secret, or
    disallowed full third-party filing is present; logs redact credentials and
    all required secrets are documented through placeholders only.
15. **AC-15 — Public-ready package:** Given the repository prepared for review,
    when an independent reader follows the README, then they can understand the
    question, methods, corpus boundaries, costs, results, limitations, and exact
    reproduction path without access to HLS-internal material.
16. **AC-16 — One-sprint definition of done:** The factory may not call the
    sprint complete with only scaffolding or synthetic sample output. Completion
    requires all Must deliverables, a completed canonical live matrix, generated
    reports, passing offline CI, and an evidence-backed review of every criterion
    above. Publication itself waits for Adam's explicit approval.

## Constraints

### Hard

- Deliver the complete v1 in one HLS factory sprint; reduce Should scope before
  deferring a Must acceptance criterion.
- Use real public UK reporting data for the canonical trial. Synthetic data is
  permitted only for offline unit and failure-path tests.
- Test XBRL, HTML, and PDF against one model from each of three providers with
  the same substantive task and no provider-specific prompt tuning.
- Freeze the trial before results, preserve failures, and make all headline
  claims traceable to raw evidence.
- Do not commit secrets or make live model calls in CI.
- Do not publish the repository or report externally without Adam's explicit
  approval.

### Preferences

- Prefer Python and established standards-aware libraries such as Arelle for
  XBRL/iXBRL processing, with a small typed CLI rather than a web application.
- Prefer declarative YAML/JSON task and protocol files, JSONL/Parquet result
  data, and static Markdown/HTML reporting.
- Prefer exact deterministic checks over LLM judging; where judgement remains,
  expose the rubric, reviewer, and override trail.
- Prefer direct, documented provider APIs over harness UIs so exact model IDs,
  parameters, tokens, latency, and cost are capturable.

## Assumptions

- [confirmed] The product should look and behave like a genuine real-world trial,
  not a predetermined XBRL showcase.
- [confirmed] The HLS Software Factory will build the full v1 in one sprint.
- [confirmed] The work sits under the HLS banner and is intended for an eventual
  `hls-uk` GitHub repository, subject to explicit publication approval.
- [assumed] Four issuers, 48 tasks, three providers, three formats, and three
  repetitions provide the smallest credible matrix for this one-sprint pilot.
- [assumed] Adam/HLS will provide funded API credentials for OpenAI, Anthropic,
  and Google before the live-run story reaches its acceptance gate.
- [assumed] A default £250 API cap is acceptable; it may be lowered before the
  protocol is frozen without changing the research design.
- [assumed] Public filings can be fetched and processed for research, while the
  repository avoids redistributing full third-party documents unless permitted.
- [assumed] Fresh-session independent review is acceptable for corpus and gold
  QA in v1; the report will not imply external peer review or regulator approval.

## Open Questions

None block factory planning. All unconfirmed choices are bounded assumptions
above; changing corpus size, providers, repetitions, or the budget after freeze
requires a new protocol version.

## Factory Handoff

- **Requirements source:** this document.
- **Delivery mode:** greenfield consumer repository, one sprint.
- **Required factory path:** bootstrap target repo → initialise factory process →
  build a story plan mapped to AC-01–AC-16 → orchestrate implementation and
  independent review → retain criterion-level evidence.
- **Prioritisation:** every Acceptance Criterion and Hard constraint is Must.
  Preferences and the open-weight-model stretch are Should and are cut first.
- **Release gate:** local build and trial evidence may be completed autonomously;
  creating/publishing the public GitHub repository and report remains a separate
  explicit approval step.

## Research Context and Public Source Interfaces

- [Companies House Free Accounts Data Product](https://download.companieshouse.gov.uk/en_accountsdata.html)
  provides public electronically filed accounts as iXBRL/HTML, XBRL/XML, or
  packaged iXBRL files.
- [FRC digital reporting glossary](https://www.frc.org.uk/library/digital-reporting/digital-reporting-education-outreach/digital-reporting-glossary/)
  defines XBRL, iXBRL, facts, contexts, taxonomies, and Arelle in the UK
  reporting context.
- [FRC: What is XBRL?](https://www.frc.org.uk/library/digital-reporting/digital-reporting-education-outreach/introduction-to-digital-reporting/what-is-xbrl/)
  explains that iXBRL embeds machine-readable tags in a human-readable XHTML
  report and links facts to concepts, entities, periods, and units.
- [FRC taxonomies and guidance](https://www.frc.org.uk/library/standards-codes-policy/accounting-and-reporting/frc-taxonomies/frc-taxonomies-documentation-and-guidance/)
  is the authoritative source for current UK taxonomy documentation.
- [FRC Structured Digital Reporting Insights 2025/26](https://www.frc.org.uk/library/digital-reporting/structured-digital-reporting-insights-202526/)
  provides current UK market and regulatory context for structured annual
  reports and AI-enabled use of machine-readable reporting data.
