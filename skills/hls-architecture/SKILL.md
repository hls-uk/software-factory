---
name: hls-architecture
description: Run the architecture phase — after requirements are confirmed and before any plan is built, research viable options, evaluate every significant choice against explicit project constraints, and produce a Mermaid-illustrated architecture doc that the operator signs off before planning begins. Decomposes the system into epics, each anchored by a design doc. Use when requirements are confirmed and no signed-off architecture exists, or when a change is big enough to reopen one.
---

# Architecture

Architecture decisions are the expensive-to-reverse ones. This phase exists
so they are made once, in the open, with alternatives on the table and a
operator's signature on the result — instead of implicitly, one story at a
time, where nobody can later say why. The output is a document a newcomer
can read to understand *what we chose and why*, and a gate: **no plan is
built against an architecture that isn't signed off.**

Position in the loop: requirements → **architecture** → plan → orchestrate
→ verify → learn.

## Preconditions

- A confirmed requirements doc (`docs/requirements/<slug>.md`) — else run
  hls-requirements-interview first. Architecture against draft requirements
  is guesswork with diagrams.

## Process

1. **Find the choices that matter.** From the requirements, list every
   decision that would be expensive to reverse: language/runtime, framework,
   persistence, deployment shape, auth approach, third-party services,
   integration seams, build/test toolchain. Everything else is a story-level
   decision — leave it to the plan. For every third-party service, explicitly
   distinguish unit fakes/stubs from a vendor-protocol simulator and decide:
   the local/CI simulator, the shared real non-production integration
   environment, the eventual production-mirroring staging posture, the
   observation-to-simulator feedback loop, and the secure operator-controlled
   credential/probe mechanism. The same production client/adapter must cross
   all environments; endpoint and credential binding may change, business
   logic may not.

2. **Research options, not conclusions.** For each significant choice,
   identify 2–4 credible candidates. Use web research where the harness
   provides it; otherwise reason from the requirements and the known proven
   set. A choice with no alternatives considered is a finding, not a
   decision.

3. **Evaluate against explicit decision criteria.** Use
   [references/decision-criteria.md](references/decision-criteria.md) to turn
   the requirements and operating constraints into a small scorecard. No
   language, framework, database, cloud, or model wins silently. Every choice
   gets an options table — candidates, pros, cons, recommendation, and the
   *why* spelled out in one paragraph.

4. **Write the architecture doc** to
   `docs/architecture/<slug>-architecture.md` using
   [references/architecture-doc-template.md](references/architecture-doc-template.md),
   status `draft`. Illustrate with Mermaid, in fenced ` ```mermaid ` blocks
   that render on GitHub: a C4-style context diagram and container diagram
   minimum, sequence diagrams for the critical flows. Beautiful and legible
   beats exhaustive — a diagram that needs a magnifying glass has failed.

5. **Decompose into epics.** Name the modules/outcomes the system splits
   into. An epic is a module plus its **design doc**
   (`docs/design/<epic>.md`): the contract, data model, security posture,
   and constraints stories will later be cut from. Write the design docs
   for the epics planning will start with; later epics get theirs
   just-in-time, before their first story is cut. Every MUST a design doc
   states will bind story acceptance criteria downstream — write them as
   requirements, not prose color.

6. **Record revisit triggers.** Each decision names what would reopen it
   ("if write volume exceeds X", "if the vendor sunsets Y"). This is what
   keeps the doc honest later — decisions age, and the trigger is the alarm.
   Third-party decisions additionally name the evidence provenance required
   for simulator calibration and the trigger that turns a newly observed real
   behaviour into a simulator fixture/profile plus regression test.

7. **Get operator sign-off.** Present the doc — publish it to PDF first if
   the hls-publish-report skill is installed (`docs/published/`). The operator
   reads, questions, and either sends it back or signs: set
   `status: signed-off` with name and date. Under the factory, flag the
   sign-off as a human-decision bead (`bd human`); an agent never
   self-approves it. **hls-plan-builder refuses to run without this
   signature.**

## Scope of the gate

Not every piece of work reopens architecture. New system or module: full
phase. Feature within a signed-off architecture: the plan records
`architecture: unchanged (ARCH-<slug>)` and inherits the doc's decisions.
A story that would violate the signed-off doc is the signal to rerun this
phase — amend the doc, re-sign, then plan; never quietly diverge.

## Anti-patterns

- Conclusions without options. "We'll use X" with no table is opinion, not
  architecture.
- Résumé-driven or novelty-driven choices. The burden of proof is on the
  interesting option, and the options table is where it pays or fails.
- Adding scaling tech "while we're at it". The doc records the seam and the
  trigger; it does not build the queue.
- Diagrams that don't render on GitHub, or render as spaghetti. Split them.
- Skipping sign-off because the choice "was obvious". The signature isn't
  approval theater — it's the moment the *why* becomes the repository record
  instead of one agent's context.
- An architecture doc that restates requirements instead of deciding.
  Requirements say what must be true; this doc says what we're building
  and why it's shaped that way.
- Calling a recording fake or an internal test stub a vendor simulator. A
  simulator speaks the vendor's protocol through the production adapter and
  carries traceable specification/observation evidence for its behaviours.
