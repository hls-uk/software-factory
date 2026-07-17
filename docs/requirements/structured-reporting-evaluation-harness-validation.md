---
id: REQ-structured-reporting-evaluation-harness-validation
status: confirmed
mode: greenfield
updated: 2026-07-17
owner: Adam Chesney
target_repo: hls-uk/structured-reporting-evaluation-harness
delivery: one factory sprint
supersedes: REQ-structured-reporting-model-trial
---

# Structured Reporting Evaluation Harness Validation

Build and validate a public-ready engineering harness that demonstrates HLS's
ability to process XBRL, HTML, and PDF inputs; invoke multiple model-provider
interfaces; capture reproducible execution receipts; and apply deterministic
quality checks. The product proves technical readiness only. It must not conduct
a real-company benchmarking study, compare format or provider performance, or
produce evidence that could answer a future commissioned research question.

## Confirmation Basis

Adam confirmed on 2026-07-17 that the earlier real-world trial PRD was too close
to the scope of a potential commissioned study and requested a new PRD. This
replacement therefore treats non-substitution as a product requirement: the
harness may prove machinery, but it may not generate substantive comparative
findings before a separately authorised research project begins.

## Goals

- Demonstrate a standards-aware, reproducible path through synthetic XBRL,
  HTML, and PDF representations generated from one canonical fictional source.
- Prove provider-neutral request/response adapters, record-and-replay testing,
  immutable receipts, deterministic parsing, and scorer quality assurance.
- Produce an inspectable engineering-validation artifact that supports a true
  claim of technical capability without claiming prior research findings.
- Leave a clean extension point for a future, independently specified study
  while shipping no real corpus, substantive task bank, comparative analysis,
  or policy interpretation now.

## Success Signals

- A clean clone validates all three generated formats, replays all provider
  fixtures, verifies receipts, and exercises scoring without provider keys.
- The same canonical fictional values and narratives can be traced through the
  XBRL, HTML, and PDF artifacts without manual editing or divergent sources.
- An independent reviewer can see exactly which engineering capabilities were
  validated and which research activities were deliberately not performed.
- Attempts to configure real-company data, a comparative trial, rankings,
  statistics, or policy findings fail before execution.

## Non-Goals

- No real listed-company or other real-entity reporting data may be included,
  fetched, processed, cached, or scored in the canonical validation.
- No representative sample, market-coverage design, population analysis,
  dual-listed-company coverage, or sample-size recommendation will be created.
- No substantive question bank covering numerical, accounting-policy,
  narrative, holistic, or cross-report research questions will be run on models.
- No repeated model runs, model-quality evaluation, format-performance
  comparison, provider ranking, winner, effect size, confidence interval,
  significance test, or statistical inference will be produced.
- No conclusion will be drawn about whether XBRL, HTML, or PDF is more accurate,
  complete, consistent, explainable, efficient, or cost-effective for AI.
- No policy insight, recommendation, market conclusion, regulator-facing
  finding, benchmarking report, or knowledge-transfer pack for a substantive
  study will be produced.
- No buyer material, tender document, buyer-supplied data, confidential method,
  or procurement-specific content will enter the target repository.
- No hosted service, dashboard, authentication, user management, or production
  deployment is required.

## Users & Context

### Primary users

- **HLS engineering lead:** validates that the complete technical path works
  and can explain the capability accurately.
- **Independent technical reviewer:** inspects fixture provenance, format
  validity, adapter behaviour, receipt integrity, scorer tests, and boundary
  enforcement.
- **Future research team:** may reuse the generic components only after a new
  requirements process separately defines and authorises a substantive study.

### Operating context

- The target is a greenfield repository named
  `hls-uk/structured-reporting-evaluation-harness`.
- Development and offline verification must work from a clean clone on current
  macOS and Linux environments.
- The canonical validation is fully offline. Provider credentials are optional
  and used only by an explicitly invoked transport-connectivity smoke command.
- The repository is prepared to be public, but creation, publication, or
  external sharing requires Adam's explicit approval after review.

## Product Boundary

The product has two layers:

1. **Generic engineering components:** format loaders, provider interfaces,
   response schema, receipt store, replay mode, deterministic scorer library,
   validators, and report generator.
2. **Readiness-validation protocol:** one fictional source, three generated
   representations, synthetic response fixtures, scorer truth cases, and
   transport-only smoke prompts.

Only the readiness-validation protocol ships. There is no bundled real-company
corpus, research protocol, substantive prompt bank, comparative analysis module,
or hidden result set. A future study must begin with a separate confirmed PRD
and may not be activated merely by changing a configuration flag.

## Canonical Fictional Reference Pack

### Source of truth

Create one clearly fictional entity, **HLS Reference Company Ltd**, represented
by a small canonical data file containing:

- 12 typed numerical facts covering instant and duration periods, GBP and pure
  units, positive and negative values, scale, and one dimensional breakdown;
- four short fictional narrative disclosures covering accounting policy, risk,
  governance, and performance commentary; and
- explicit entity, reporting-period, currency, unit, and provenance metadata.

Every rendered artifact must state prominently that the company and data are
fictional, unaudited, and unsuitable for financial or research conclusions.

### Generated representations

Generate all representations deterministically from the canonical source:

- a standards-conformant XBRL/iXBRL package using a minimal local test taxonomy
  or suitably licensed conformance taxonomy;
- accessible semantic HTML preserving headings, tables, notes, and ordering;
  and
- a paginated PDF preserving the same visible information and identifiers.

Each generated file receives a content hash and provenance record. A manifest
maps every canonical fact and narrative block to its locator in each format.
Equivalence is true by construction and validated mechanically; it is not a
research finding.

## Validation Cases

The offline suite validates engineering behaviour rather than model ability:

- XBRL fact, context, unit, dimension, label, scale, and sign parsing;
- HTML table, heading, footnote, and text-order preservation;
- PDF page generation, text presence, table readability, and locator mapping;
- provider request construction and response parsing through recorded fixtures;
- handling of correct, incomplete, malformed, refused, truncated, and
  transport-error responses;
- deterministic scoring of synthetic truth cases, including wrong unit, period,
  scale, sign, and missing evidence; and
- content-addressed receipts, replay, interruption, resumption, and tamper
  detection.

These are software test cases. They are not a model benchmark and must not be
aggregated into model or format performance measures.

## Provider Interfaces and Live Smoke

### Offline record-and-replay

Implement provider adapters for OpenAI, Anthropic, and Google behind one
provider-neutral request and response contract. The canonical test suite uses
synthetic recorded responses and deterministic replay; it makes no network call
and expresses no view about current provider performance.

### Optional connectivity smoke

If credentials are available, an operator may explicitly run a bounded live
smoke that:

- sends one synthetic nonce-retrieval request per provider and representation;
- makes at most 3 providers × 3 representations × 1 call = **9 calls**;
- asks only for the embedded nonce and a source locator;
- records transport, schema conformance, latency, token use, and cost;
- performs no retry intended to improve a model result;
- reports only pass/fail interface compatibility; and
- never aggregates, ranks, compares, interprets, or publishes model outputs.

Live-smoke receipts remain local by default. Public fixtures use redacted
synthetic replay records, not paid-provider outputs.

## Receipt and Audit Contract

Each offline replay or optional live attempt records:

- protocol and fixture identifiers plus their SHA-256 hashes;
- provider, exact model identifier, API version, and request parameters;
- representation, input hash, prompt hash, and response-schema version;
- start/end timestamps, duration, terminal status, and error classification;
- provider-reported token use and cost where available;
- immutable raw response plus separately parsed response; and
- parent receipt when an explicitly authorised replay or rerun occurs.

Receipts are content-addressed and append-only. Replaying or re-scoring a
receipt never mutates its raw evidence.

## Deterministic Scoring Validation

The scorer library is tested against authored synthetic truth tables. It must
correctly handle exact values, tolerances, units, periods, scale, sign,
controlled categories, required/prohibited propositions, evidence locators,
missing components, malformed responses, and explicit refusal states.

The engineering report may state scorer test coverage and whether predefined
truth cases passed. It may not state that a provider or format achieved a
quality score, even if the same library could support that work later.

## Research-Boundary Guard

The readiness protocol and its CLI must reject any configuration containing one
or more of the following:

- a source classified as real, public-company, confidential, or buyer-supplied;
- more than one reporting entity or reporting period;
- a substantive financial, accounting, narrative, holistic, or policy task;
- repeated live runs intended to measure consistency;
- comparative aggregation by provider, model, or format;
- rankings, winners, effect sizes, confidence intervals, significance tests,
  population estimates, or market-generalisation fields;
- policy insight, recommendation, or research-conclusion output sections; or
- a request to describe the validation as a completed benchmark or study.

The guard is enforced by schema validation and tested with negative fixtures.
Documentation warnings alone are not sufficient.

## Engineering Validation Report

Generate a concise Markdown and static HTML report containing only:

- build identity and environment;
- fictional fixture inventory and provenance;
- format-validation results;
- provider-adapter replay coverage;
- receipt-integrity and scorer truth-case results;
- optional transport-smoke compatibility, if run;
- limitations and the research-boundary declaration; and
- commands for independent offline reproduction.

The report contains no table or chart that compares model or format quality.
Its title must include **Engineering Validation**, and every rendered version
must state: **This artifact does not contain comparative research findings and
must not be used to infer the relative performance of XBRL, HTML, PDF, or any
model provider.**

## Public Positioning

### Permitted claim

> HLS has validated a reproducible engineering harness for processing
> standards-based XBRL, HTML, and PDF fixtures, exercising multiple provider
> interfaces, preserving model-call audit receipts, and testing deterministic
> scoring mechanics. The validation used fictional data and did not compare
> model or format performance.

### Prohibited claims

- “HLS has completed an XBRL versus PDF versus HTML benchmarking study.”
- “The trial found that one format or provider performs better.”
- “The results are representative, statistically meaningful, or policy-ready.”
- “The artifact answers how structured data performs in an AI-driven reporting
  environment.”

## Deliverables

The target repository must contain:

- a README with the permitted claim, prohibited interpretations, setup,
  offline-validation path, optional live-cost warning, and publication gate;
- the canonical fictional source and deterministic three-format generator;
- XBRL/iXBRL, HTML, and PDF validators plus the cross-format locator manifest;
- provider-neutral request/response contracts and three replay-tested adapters;
- synthetic response fixtures covering success and failure states;
- append-only, content-addressed receipt storage and verification;
- deterministic scorer truth tables and negative tests;
- an executable research-boundary guard with negative fixtures;
- the generated Engineering Validation report in Markdown and static HTML;
- a limitations, data-rights, security, and future-extension statement; and
- offline CI covering generation, validation, replay, scoring, receipts,
  boundary enforcement, report safety, and secret hygiene.

## Acceptance Criteria

1. **AC-01 — Clean offline setup:** Given a clean macOS or Linux clone without
   provider credentials, when the documented setup and validation commands run,
   then all canonical artifacts are generated and all offline checks pass
   without a provider or source-data network call.
2. **AC-02 — Fictional source only:** Given the tracked data and generated
   artifacts, when provenance validation runs, then exactly one entity named HLS
   Reference Company Ltd is present, every artifact is labelled fictional and
   unaudited, and no real-company or buyer-supplied data is detected.
3. **AC-03 — Deterministic representations:** Given the canonical source, when
   generation runs twice in equivalent environments, then XBRL/iXBRL, HTML, PDF,
   locator manifest, and hashes are reproducible according to the documented
   deterministic-build rules.
4. **AC-04 — Format validity and equivalence:** Given the generated pack, when
   validators run, then XBRL semantics, HTML structure, PDF content/layout, and
   all 16 canonical numerical/narrative items pass their format-specific checks
   and map to equivalent locators across all three representations.
5. **AC-05 — Three replay-tested adapters:** Given the recorded synthetic
   fixtures, when offline replay runs, then OpenAI, Anthropic, and Google adapter
   requests validate against one neutral contract and all success/error response
   states parse into the expected terminal records.
6. **AC-06 — Bounded optional live smoke:** Given valid provider credentials,
   when live smoke is explicitly invoked, then its dry run shows no more than
   nine nonce-retrieval calls, its execution cannot exceed that bound, and its
   output contains interface pass/fail records but no comparative aggregate.
7. **AC-07 — Immutable receipts:** Given replay, interruption, resumption, and
   tamper fixtures, when receipt verification runs, then completed calls are
   reused by content hash, raw evidence remains unchanged, lineage is preserved,
   and any altered input or receipt is rejected.
8. **AC-08 — Scorer truth cases:** Given the authored synthetic response matrix,
   when scoring tests run, then exact, tolerance, unit, period, scale, sign,
   proposition, locator, refusal, and malformed cases produce their declared
   expected outcomes with no model judge required.
9. **AC-09 — Enforced non-substitution boundary:** Given negative configurations
   for real data, multiple entities, substantive tasks, repetition, comparison,
   rankings, statistics, policy findings, or benchmark wording, when validation
   runs, then each is rejected before source loading or provider dispatch with a
   specific boundary error.
10. **AC-10 — Research-safe report:** Given all offline validation outputs, when
    the report is generated, then it contains only engineering coverage,
    limitations, reproduction commands, and the mandatory non-inference notice;
    an automated safety check confirms the absence of performance rankings,
    effect estimates, market conclusions, and policy recommendations.
11. **AC-11 — Secret and publication hygiene:** Given repository and CI scans,
    when tracked content is inspected, then no credential, live provider output,
    buyer material, real-company source, or publication action is present;
    required secrets use placeholders and publication remains a manual gate.
12. **AC-12 — Independent reproduction:** Given an independent reviewer with no
    HLS-internal context, when they follow the README, then they can regenerate
    the fictional pack, replay adapters, verify receipts, run scorer truth cases,
    exercise negative boundary tests, and reproduce the Engineering Validation
    report.
13. **AC-13 — One-sprint definition of done:** The factory may close the sprint
    only when AC-01–AC-12 have evidence, offline CI passes, an independent review
    finds no path to a substantive benchmark through the readiness protocol, and
    the repository is ready for Adam's publication decision. Live smoke and
    publication are not required for completion.

## Constraints

### Hard

- Deliver the complete local, public-ready artifact in one HLS factory sprint.
- Use only clearly fictional canonical financial data and suitably licensed
  schemas/conformance material.
- Keep the canonical path offline and deterministic.
- Enforce the research boundary in executable validation, not prose alone.
- Make no substantive model or format comparison and produce no research or
  policy finding.
- Do not include procurement-specific or buyer-supplied material.
- Do not publish or externally share the repository or report without Adam's
  explicit approval.

### Preferences

- Prefer Python, Arelle or another established standards-aware XBRL processor,
  declarative YAML/JSON fixtures, typed schemas, and a small command-line tool.
- Prefer HTML and PDF generation from a shared presentation model to minimise
  accidental divergence while still validating distinct ingestion paths.
- Prefer JSONL receipts and a static Markdown/HTML report.
- Prefer record-and-replay provider testing over paid calls; live smoke is an
  optional manual verification, not a CI or release dependency.

## Assumptions

- [confirmed] The previous real-world model-trial PRD must not be built because
  it could duplicate the substance of a potential commissioned study.
- [confirmed] The replacement should prove technical capability without
  generating comparative evidence or conclusions.
- [confirmed] The HLS Software Factory should deliver the complete replacement
  in one sprint.
- [assumed] One fictional entity, 12 numerical facts, four narratives, and three
  generated formats provide enough coverage to validate the engineering path.
- [assumed] Replay-tested adapters are sufficient for acceptance; optional live
  connectivity depends on credentials and is not a release gate.
- [assumed] The eventual repository may be public after Adam's separate review
  and approval.

## Open Questions

None block factory planning. Any request to add real data, substantive model
tasks, comparative results, or research conclusions is out of scope and
requires a separately confirmed post-authorisation PRD.

## Factory Handoff

- **Requirements source:** this document only. The superseded model-trial PRD
  must not be used as a planning source.
- **Delivery mode:** greenfield consumer repository, one sprint.
- **Required factory path:** bootstrap repository → initialise factory process →
  plan stories against AC-01–AC-13 → implement and independently review → retain
  criterion-level evidence.
- **Stop condition:** if any story introduces real-company data, substantive
  research tasks, comparative aggregation, performance findings, or policy
  interpretation, stop and return to requirements rather than implementing it.
- **Release gate:** local completion is authorised; repository creation,
  publication, external sharing, and live provider smoke require their stated
  human approvals.
