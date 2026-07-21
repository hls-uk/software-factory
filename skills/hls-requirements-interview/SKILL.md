---
name: hls-requirements-interview
description: Build requirements and a risk-calibrated delivery contract by interviewing the user — structured questioning, assumption surfacing, and numbered, testable acceptance criteria. Use when a feature request, product idea, or project brief is underspecified, before planning or implementation begins, or when asked to "gather requirements" or "write a spec".
---

# Requirements Interview

Turn a rough intent into a requirements document another agent can plan and
build from without asking follow-up questions. The interview is a dialogue, not
a form: propose defaults, surface assumptions, and only ask what you cannot
responsibly assume.

## Process

1. **Absorb what exists.** Read the request, any linked docs, and the repo
   (README, wiki, existing requirements) before asking anything. Never ask a
   question the repo already answers.

2. **Assess completeness.** A buildable requirement needs: who it's for, what
   must be true at the end, how you'd observe success, what's out of scope, and
   hard constraints. List the gaps.

3. **Establish the delivery contract.** Confirm these four decisions, using
   repo evidence and proposed defaults where possible:
   - Who will use the result, and how exposed will it be?
   - What authority, reset, repair, or rollback path exists?
   - Which consequences are unacceptable even in an early version?
   - What is the first usable user journey, and which polish or defects may be
     deferred?

   Record `operatingMode` (`supervised` or `autonomous`),
   `modelRoutingProfile` (`quality`, `balanced`, or `throughput`),
   `assuranceProfile` (`rapid`, `standard`, or `assured`), and `releaseStage`
   (`experiment`, `beta`, `operational`, or `canonical`) as separate fields.
   Also record exposure, data criticality, the first usable target, accepted
   defects, release blockers, and escalation triggers. An unknown or
   unconfirmed `assuranceProfile` defaults to `standard`; never infer `rapid`
   from urgency alone.

4. **Interview in small batches.** Ask at most 3–4 questions per round, most
   load-bearing first. For every question offer a sensible default so the user
   can answer with one word. Prefer "I'll assume X unless you say otherwise"
   over open-ended questions for anything you can infer.

5. **Surface assumptions explicitly.** Keep a running list, each marked
   `confirmed` or `assumed`. Anything still `assumed` at the end goes in the
   doc — silent assumptions are how projects go wrong.

6. **Draft acceptance criteria as you go.** Each criterion is numbered and
   testable — Given/When/Then preferred, or an observable check ("`GET /health`
   returns 200"). If you cannot say how a criterion would be verified, it is
   not a criterion yet; refine or ask.

   Tag each criterion with the earliest milestone where it must pass:
   `first-usable`, `operational`, `canonical`, or `deferred`. A rapid profile
   still needs an end-to-end first-usable journey; it changes sequencing and
   evidence depth, not the observable outcome.

7. **Write the doc** to `docs/requirements/<slug>.md` using
   [references/requirements-template.md](references/requirements-template.md).
   If the repo keeps an LLM wiki, add it to the index and log the ingest.

8. **Close the loop.** Show the user the goals, delivery contract, and criteria
   list (not the whole doc), confirm, and record the confirmation in the doc's
   status field. Requirements cannot become `confirmed` without an explicit
   delivery contract or a recorded `standard` default.

## Quality Bar

- Every acceptance criterion is independently verifiable by an agent with
  repo access — no criterion requires reading the user's mind.
- Non-goals are explicit. What you decline to build is as load-bearing as what
  you build.
- Constraints distinguish hard (must) from preference (should). Record stack
  preferences as defaults, not mandates, unless the user says otherwise.
- The doc states `mode: greenfield` or `mode: existing` (does the repo already
  have source code?) — downstream planning behaves differently.
- The four delivery fields remain orthogonal. Operating autonomy is not model
  quality, assurance depth, or release authority.
- Safety is invariant across profiles: no profile grants authority for secrets,
  destructive changes, public release, external configuration, canonical data
  mutation, or bypassing human/commercial gates.
- Ten criteria that matter beat forty that pad. Split large scopes into
  separately-deliverable requirement docs.

## Anti-patterns

- The twenty-question opening volley. Batch, default, assume-and-confirm.
- Solution-shaped requirements ("use Redis") when the need is a quality
  ("survive restarts"). Capture the need; note the suggestion under constraints.
- Criteria that measure effort ("refactor the module") instead of outcome
  ("module X has no callers of deprecated API Y").
- Leaving the requirements only in the conversation. An answer that lives only
  in chat is lost.
