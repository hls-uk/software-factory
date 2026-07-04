---
name: requirements-interview
description: Build requirements by interviewing the user — structured questioning, assumption surfacing, and a requirements doc with numbered, testable acceptance criteria. Use when a feature request, product idea, or project brief is underspecified, before planning or implementation begins, or when asked to "gather requirements" or "write a spec".
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

3. **Interview in small batches.** Ask at most 3–4 questions per round, most
   load-bearing first. For every question offer a sensible default so the user
   can answer with one word. Prefer "I'll assume X unless you say otherwise"
   over open-ended questions for anything you can infer.

4. **Surface assumptions explicitly.** Keep a running list, each marked
   `confirmed` or `assumed`. Anything still `assumed` at the end goes in the
   doc — silent assumptions are how projects go wrong.

5. **Draft acceptance criteria as you go.** Each criterion is numbered and
   testable — Given/When/Then preferred, or an observable check ("`GET /health`
   returns 200"). If you cannot say how a criterion would be verified, it is
   not a criterion yet; refine or ask.

6. **Write the doc** to `docs/requirements/<slug>.md` using
   [references/requirements-template.md](references/requirements-template.md).
   If the repo keeps an LLM wiki, add it to the index and log the ingest.

7. **Close the loop.** Show the user the goals and criteria list (not the whole
   doc), confirm, and record the confirmation in the doc's status field.

## Quality Bar

- Every acceptance criterion is independently verifiable by an agent with
  repo access — no criterion requires reading the user's mind.
- Non-goals are explicit. What you decline to build is as load-bearing as what
  you build.
- Constraints distinguish hard (must) from preference (should). Record stack
  preferences as defaults, not mandates, unless the user says otherwise.
- The doc states `mode: greenfield` or `mode: existing` (does the repo already
  have source code?) — downstream planning behaves differently.
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
