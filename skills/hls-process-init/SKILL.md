---
name: hls-process-init
description: Initialise a new repo's risk-calibrated agentic software factory — separate operating mode, model routing, assurance profile, and release stage; then install work tracking, verification gates, evidence conventions, and agent entrypoints. Use when starting a repo agents will build in or when asked to "set up the process" for agent-driven delivery.
---

# Process Init

Give a new repo everything an agent workforce needs to deliver production
quality without a human re-explaining the rules each session. The output is
not ceremony — it is a small set of files and conventions that make the
factory loop (requirements → architecture → plan → orchestrate → verify →
learn) runnable.

## 1. Choose the Delivery Contract

Ask the user (or read the brief), then record four orthogonal choices. Never
use one as a proxy for another:

- `operatingMode`: `autonomous` or `supervised` — human availability and
  interaction cadence.
- `modelRoutingProfile`: `quality`, `balanced`, or `throughput` — lane/model
  selection only.
- `assuranceProfile`: `rapid`, `standard`, or `assured` — sequencing, review,
  and evidence depth. Unknown defaults to `standard`; urgency does not imply
  `rapid`.
- `releaseStage`: `experiment`, `beta`, `operational`, or `canonical` — the
  current authority and promotion boundary.

Also record exposure, data criticality, the first usable journey, accepted
defects, release blockers, escalation triggers, and the reset/repair/rollback
path. Ask who uses it, what can be recovered, which consequences are
unacceptable, and what can wait until after first use.

Operating mode changes agent behaviour everywhere downstream:

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

Assurance changes delivery depth without changing those hard stops:

| Profile | Default delivery behaviour |
|---|---|
| `rapid` | Named private users, reversible experiment/beta, first usable vertical slice first, focused verification, risk-triggered review, P2/P3 defects linked for iteration |
| `standard` | Normal architecture, planning, independent review, and existing verification gates |
| `assured` | Full architecture/review/evidence path with expanded security, failure, recovery, and traceability checks |

Rapid must escalate before public, irreversible, or canonical use. Secrets,
destructive operations, external configuration, human/commercial gates, test
integrity, and credentials remain invariant stops in every profile.

## 2. Install the Substrate

In order, each verified before the next:

1. **Knowledge base** — run the hls-repo-bootstrap skill: wiki (`index.md`,
   `log.md`), decisions, learnings ledger, agent entrypoints
   (AGENTS.md/CLAUDE.md). This is the repo's memory; everything else logs
   into it.
2. **Work tracking** — run the hls-beads skill's setup (`bd init`, embedded).
3. **Skills** — install the factory skills where agents discover them:
   `npx skills add <owner>/<skills-repo>` (all agents), and commit the
   install choice to the repo docs so future sessions repeat it. Record the
   install in `.factory/skills-lock.json` — source, HEAD commit, skill list —
   per the hls-skill-update skill: project-level installs are invisible to
   the skills CLI's own tracking, and this record is what update checks and
   feedback reports read.
4. **Factory config** — create `.factory/feedback.json` pointing at the
   tracker that owns skill improvements (see the hls-skill-feedback skill),
   and `.factory/agents.json` assigning the coordinator, implementer lanes
   (with tiers), reviewer, `operatingMode`, `modelRoutingProfile`,
   `assuranceProfile`, `releaseStage`, and the billing policy
   (format, routing table, and defaults: the hls-factory-orchestrate skill's
   `references/running-the-factory.md` and `references/parallel-dispatch.md`).
   The committed file states **portable factory requirements** — tiers,
   profiles, independence, billing rules, and required capabilities — never
   an assumption that every host has every CLI or subscription. Gitignore
   `.factory/agents.local.json`; run the orchestrate skill's per-host
   lane-setup ritual (`references/lane-setup.md`) on each laptop/VPS to
   verify auth, models, worktrees, and capabilities before writing local
   overrides. For multiple hosts, follow its `references/host-lanes.md`
   single-operator coordination rules. Leave credentials out; name only the
   access mechanism. If an older config uses `deliveryProfile`, migrate only
   its model-routing value (`quality`, `balanced`, or `throughput`) to
   `modelRoutingProfile`. Do not infer assurance, autonomy, or release
   authority from the legacy field; record those decisions separately.
5. **Verification harness** — the factory cannot run without executable
   gates. Ensure `test`, `lint`, and `build` commands exist and run green
   (even if the suite is one smoke test), and record them in the process doc.
   Standard and assured retain the repo's existing protections. Rapid may run
   story-scoped and affected gates while assembling the slice, but the full
   configured suite and first usable user journey must pass before the slice
   is accepted; any risk trigger restores the full review path.
   Three hard properties, designed in from day one:
   - **Local-first:** every gate runs on a laptop with no cloud dependency —
     anything that can't gets a fake/stub or is non-gating. Deployment shape
     must never demote the local loop; it is what code-change throughput
     lives on.
   - **Parallel-safe:** ports and connection strings come from env
     (`PORT`, `DATABASE_URL`), never hardcoded. Shared services are
     namespaced where practical, not blindly duplicated; the plan records
     the repo-specific scheme.
   - **Idempotent:** verification resets its own state first and is safe to
     re-run at any time.
   If the product has third-party integrations, also establish the environment
   ladder before delivery starts: local lanes/CI use evidence-calibrated
   vendor-protocol simulators through the production adapter; one durable
   shared non-production integration environment exercises real vendor test
   endpoints with synthetic/vendor-approved data; staging, when created,
   mirrors production deployment. Record an observation manifest format and
   require each new real behaviour to update the simulator and regression
   tests. Put credentials in an operator-controlled secret store with temporary,
   least-privilege, audited access; prefer allowlisted probes/runners that
   resolve values server-side, and keep all secret values out of repo config.
6. **Evidence convention** — create `evidence/` with a one-line README:
   dated subdirectories per story, screenshots and verification write-ups.
7. **Self-documenting README** — the top-level README carries a short
   "Where things are" section from which a human reaches, in one or two
   clicks, at any point in the project: **(a) the architecture**
   (`docs/architecture/` — the recorded/signed-off doc, diagrams rendered inline),
   **(b) the tech choices and why** (the architecture doc's options tables
   and `docs/decisions/`), **(c) the master plan and progress so far**
   (`docs/plans/` — its Criteria Coverage table is the live progress
   ledger). Add the links now, pointing at the paths the loop will fill —
   a reader should never need repo archaeology to answer those three
   questions. Alongside it, adopt the published-reports convention
   (`docs/published/` PDFs for documents that leave the repo — the
   hls-publish-report skill).
8. **Worktree convention** — add `.worktrees/` to `.gitignore`. Story work
   happens in coordinator-managed worktrees there (branch `story/<slug>`,
   dir `.worktrees/<slug>`); the main checkout never does story work. Rules:
   the hls-factory-orchestrate skill's Worktree Rules section.
9. **CI** — a workflow that runs the verification commands on every push and,
   where the assurance profile or a risk trigger requires PR review, verifies
   a fresh-agent review PASS pinned to
   the current head plus promotion disclosures. Review independence is agent-
   context separation, so do not invent a second-human approval requirement.
   Gates that live only in one coordinator session do not survive host or
   session failover.

## 3. Write the Process Doc

Create `docs/process.md` from
[references/process-template.md](references/process-template.md) and link it
prominently from the agent entrypoint. It must state: the operating mode, the
exact verification commands, the dispatch mechanism for implementing agents,
the session rituals (start: sync + `bd ready`; end: push + log), and the hard
stops. For third-party systems it must also name the local simulator, shared
integration gate, staging posture, observation-feedback rule, and credential/
probe mechanism. It must also state the four delivery fields, first usable
target, profile-specific acceptance behaviour, promotion boundary, and
escalation triggers. An agent reading only AGENTS.md and docs/process.md must
be able to work correctly.

## 4. Prove It

Initialization is done when you have run one first-usable vertical slice
through the chosen loop — even a trivial one ("open the dashboard and observe
health"): requirements noted, planned, dispatched or implemented, verified
through the profile-appropriate gates, evidence captured, bead closed, log
written. A process that has never executed is a hypothesis.

## Anti-patterns

- Scaffolding every convention but never running the loop (see step 4).
- Copying another repo's process doc verbatim, gates and all, into a repo
  whose stack can't run those commands.
- Setting `autonomous` mode without CI and a real test gate — autonomy
  without verification is just speed toward the wrong thing.
