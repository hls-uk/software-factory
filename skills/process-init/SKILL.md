---
name: process-init
description: Initialise a new repo's engineering process to run as an agentic software factory — operating mode (fully autonomous on a VPS or supervised on a workstation), work tracking, LLM wiki, verification gates, evidence conventions, and agent entrypoints. Use when starting a repo that agents will build in, or when asked to "set up the process" for agent-driven delivery.
---

# Process Init

Give a new repo everything an agent workforce needs to deliver production
quality without a human re-explaining the rules each session. The output is
not ceremony — it is a small set of files and conventions that make the
factory loop (requirements → plan → orchestrate → verify → learn) runnable.

## 1. Choose the Operating Mode

Ask the user (or read the brief), then record the choice — it changes agent
behavior everywhere downstream:

| | `autonomous` (VPS) | `supervised` (workstation) |
|---|---|---|
| Human availability | none during runs | reachable, may be away |
| Agent stance | verify-and-proceed | confirm outward-facing actions |
| Hard stops | destructive ops, deploys, external services, credentials | the same, plus anything the human flagged |
| Browser verification | dev-browser `--headless` | dev-browser `--connect` to real Chrome |
| Blocked story | park, log, continue; batch questions | park or ask, human is near |
| Sync cadence | push after every accepted story | push at session boundaries minimum |

Both modes keep the same hard-stop core: autonomy never widens into
irreversible or outward-facing actions without standing authorization.

## 2. Install the Substrate

In order, each verified before the next:

1. **Knowledge base** — run the repo-bootstrap skill: wiki (`index.md`,
   `log.md`), decisions, learnings ledger, agent entrypoints
   (AGENTS.md/CLAUDE.md). This is the repo's memory; everything else logs
   into it.
2. **Work tracking** — run the beads skill's setup (`bd init`, embedded).
3. **Skills** — install the factory skills where agents discover them:
   `npx skills add <owner>/<skills-repo>` (all agents), and commit the
   install choice to the repo docs so future sessions repeat it.
4. **Feedback loop** — create `.factory/feedback.json` pointing at the
   tracker that owns skill improvements (see the skill-feedback skill).
   Leave credentials out; name the access mechanism.
5. **Verification harness** — the factory cannot run without executable
   gates. Ensure `test`, `lint`, and `build` commands exist and run green
   (even if the suite is one smoke test), and record them in the process doc.
   For stacks: default to NestJS (backend) and React + TanStack + Tailwind
   (frontend) unless the requirements say otherwise — defaults, not mandates.
6. **Evidence convention** — create `evidence/` with a one-line README:
   dated subdirectories per story, screenshots and verification write-ups.
7. **CI** — a workflow that runs the verification commands on every push.

## 3. Write the Process Doc

Create `docs/process.md` from
[references/process-template.md](references/process-template.md) and link it
prominently from the agent entrypoint. It must state: the operating mode, the
exact verification commands, the dispatch mechanism for implementing agents,
the session rituals (start: sync + `bd ready`; end: push + log), and the hard
stops. An agent reading only AGENTS.md and docs/process.md must be able to
work correctly.

## 4. Prove It

Initialization is done when you have run one story through the whole loop —
even a trivial one ("add a health endpoint"): requirements noted, planned,
dispatched or implemented, verified through the gates, evidence captured,
bead closed, log written. A process that has never executed is a hypothesis.

## Anti-patterns

- Scaffolding every convention but never running the loop (see step 4).
- Copying another repo's process doc verbatim, gates and all, into a repo
  whose stack can't run those commands.
- Setting `autonomous` mode without CI and a real test gate — autonomy
  without verification is just speed toward the wrong thing.
