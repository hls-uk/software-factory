---
name: hls-architecture
description: Run a risk-calibrated architecture phase after requirements are confirmed and before planning — from a concise recorded architecture note for bounded rapid work to researched, signed-off architecture for standard or assured delivery. Use when no suitable architecture exists or a change crosses an architecture or safety boundary.
---

# Architecture

Architecture decisions are the expensive-to-reverse ones. This phase makes
their reasoning durable without forcing low-risk, reversible experiments
through the same ceremony as canonical systems. The output must still let a
newcomer understand *what we chose, why, the recovery path, and what would
force a deeper review*.

Position in the loop: requirements → **architecture** → plan → orchestrate
→ verify → learn.

## Preconditions

- A confirmed requirements doc (`docs/requirements/<slug>.md`) — else run
  hls-requirements-interview first. Architecture against draft requirements
  is guesswork with diagrams.
- A delivery contract with separate `operatingMode`, `modelRoutingProfile`,
  `assuranceProfile`, and `releaseStage`. If assurance was not confirmed,
  record `standard` before continuing.

## Process

1. **Choose the proportional path.** Inherit the requirements' delivery
   contract; never derive assurance from operating autonomy, model routing,
   or urgency.
   - `rapid`: for a named, private, reversible experiment or beta with a clear
     reset/repair path. Produce a concise architecture note and prioritize the
     first usable vertical slice.
   - `standard`: use the normal researched architecture and operator sign-off.
   - `assured`: use the full path, expand threat/failure/recovery evidence, and
     require sign-off before planning.

   Rapid is not available when the work handles secrets or authentication,
   creates destructive or canonical mutations, crosses a security or
   architecture boundary, affects money or human/commercial decisions, or has
   concurrency, idempotency, recovery, or cross-tenant risk. Escalate to
   `standard` or `assured` and obtain explicit authority before any public,
   irreversible, or canonical use. These triggers govern even if the intake
   selected `rapid`.

2. **Find the choices that matter.** From the requirements, list every
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

3. **Research options in proportion to risk.** For each significant,
   expensive-to-reverse choice in `standard` or `assured`,
   identify 2–4 credible candidates. Use web research where the harness
   provides it; otherwise reason from the requirements and the known proven
   set. A choice with no alternatives considered is a finding, not a
   decision. In `rapid`, record why the chosen shape is reversible and reuse
   established project conventions; research alternatives only for a choice
   that is uncertain or difficult to unwind.

4. **Evaluate against explicit decision criteria.** Use
   [references/decision-criteria.md](references/decision-criteria.md) to turn
   the requirements and operating constraints into a small scorecard. No
   language, framework, database, cloud, or model wins silently. Every choice
   gets an options table — candidates, pros, cons, recommendation, and the
   *why* spelled out in one paragraph. A rapid note may use a one-row decision
   record for a reversible convention, but MUST record its recovery path and
   revisit trigger.

5. **Write the architecture doc** to
   `docs/architecture/<slug>-architecture.md` using
   [references/architecture-doc-template.md](references/architecture-doc-template.md),
   status `draft`. For `standard` and `assured`, illustrate with Mermaid, in
   fenced ` ```mermaid ` blocks that render on GitHub: a C4-style context
   diagram and container diagram minimum, sequence diagrams for the critical
   flows. For `rapid`, include only diagrams that resolve ambiguity; the
   minimum is the boundary, chosen shape, recovery path, risks, and first
   vertical slice. Beautiful and legible beats exhaustive.

6. **Decompose into epics or a vertical slice.** Name the modules/outcomes the
   system splits into. An epic is a module plus its **design doc**
   (`docs/design/<epic>.md`): the contract, data model, security posture,
   and constraints stories will later be cut from. Write the design docs
   for the epics planning will start with; later epics get theirs
   just-in-time, before their first story is cut. Every MUST a design doc
   states will bind story acceptance criteria downstream — write them as
   requirements, not prose color. Under `rapid`, start with the smallest epic
   or story group that completes the first usable journey; do not create a
   horizontal infrastructure wave unless that journey proves it necessary.

7. **Record revisit triggers.** Each decision names what would reopen it
   ("if write volume exceeds X", "if the vendor sunsets Y"). This is what
   keeps the doc honest later — decisions age, and the trigger is the alarm.
   Third-party decisions additionally name the evidence provenance required
   for simulator calibration and the trigger that turns a newly observed real
   behaviour into a simulator fixture/profile plus regression test.

8. **Record or sign off the decision.** Present the doc — publish it to PDF
   first if the hls-publish-report skill is installed (`docs/published/`). The
   operator reads, questions, and either sends it back or signs. For `standard` and
   `assured`, set `status: signed-off` with name and date; under the factory,
   flag the sign-off as a human-decision bead (`bd human`) and never
   self-approve it. For eligible `rapid` work, set `status: recorded` after the
   delivery contract and note are internally consistent; planning may proceed
   without a separate signature. A risk trigger immediately restores the
   human sign-off gate.

## Scope of the gate

Not every piece of work reopens architecture. New system or module: use the
path selected above. A feature within an accepted recorded/signed-off
architecture records `architecture: unchanged (ARCH-<slug>)` and inherits the
doc's decisions. A story that would violate the architecture or delivery
boundary is the signal to rerun this phase — amend and record/sign it, then
plan; never quietly diverge.

## Anti-patterns

- Conclusions without options. "We'll use X" with no table is opinion, not
  architecture.
- Résumé-driven or novelty-driven choices. The burden of proof is on the
  interesting option, and the options table is where it pays or fails.
- Adding scaling tech "while we're at it". The doc records the seam and the
  trigger; it does not build the queue.
- Diagrams that don't render on GitHub, or render as spaghetti. Split them.
- Skipping sign-off because the choice "was obvious". The signature isn't
  approval theater for standard or assured work — it's the moment the *why*
  becomes the repository record instead of one agent's context. Rapid work
  substitutes an explicit bounded decision record; it does not silently skip
  the gate.
- An architecture doc that restates requirements instead of deciding.
  Requirements say what must be true; this doc says what we're building
  and why it's shaped that way.
- Calling a recording fake or an internal test stub a vendor simulator. A
  simulator speaks the vendor's protocol through the production adapter and
  carries traceable specification/observation evidence for its behaviours.
