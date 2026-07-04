# Software Factory

Higher Level Software's coding-agent skills: a complete loop for agent-driven
delivery — **requirements → plan → orchestrate → verify → learn** — packaged
as [Agent Skills](https://vercel.com/docs/agent-resources/skills) installable
into Claude Code, Codex, Cursor, and 70+ other agents.

## Install

```sh
npx skills add hls-uk/software-factory                    # pick skills interactively
npx skills add hls-uk/software-factory --skill '*'        # everything
npx skills add hls-uk/software-factory --skill hls-beads --skill hls-factory-orchestrate
```

Run from an [eve](https://vercel.com/docs/eve) project directory and the CLI
offers to install into your eve building agent.

## The Skills

**Delivery loop**

| Skill | What it does |
|---|---|
| [hls-requirements-interview](skills/hls-requirements-interview/SKILL.md) | Build requirements by interviewing the user — testable acceptance criteria, surfaced assumptions. |
| [hls-plan-builder](skills/hls-plan-builder/SKILL.md) | Requirements → stories sized for one-agent handoff, each with its own verification, registered as a beads graph. |
| [hls-factory-orchestrate](skills/hls-factory-orchestrate/SKILL.md) | The long-running coordinator: dispatch whole stories to implementing agents via `/goal`, verify locally, run each PR through a bounded review, loop for days until every criterion has evidence. |

**Substrate**

| Skill | What it does |
|---|---|
| [hls-repo-bootstrap](skills/hls-repo-bootstrap/SKILL.md) | LLM Wiki + compounding-learning loop for new repos — every session leaves the repo smarter. |
| [hls-process-init](skills/hls-process-init/SKILL.md) | Set up a repo's engineering process for the factory: autonomous (VPS) or supervised (workstation) mode, gates, rituals. |
| [hls-process-revamp](skills/hls-process-revamp/SKILL.md) | Adopt the factory in an existing repo without steamrolling working conventions. |
| [hls-beads](skills/hls-beads/SKILL.md) | Work tracking with [beads](https://github.com/gastownhall/beads) in embedded mode — ready queue, claims, evidence-based closes. |
| [hls-dev-browser](skills/hls-dev-browser/SKILL.md) | Web UI verification with [dev-browser](https://github.com/sawyerhood/dev-browser) — persistent pages, Playwright assertions, screenshot evidence. |

**Evolution loop**

| Skill | What it does |
|---|---|
| [hls-skill-feedback](skills/hls-skill-feedback/SKILL.md) | File structured improvement issues from any consumer project back to this repo's tracker. |
| [hls-skill-sweep](skills/hls-skill-sweep/SKILL.md) | Sweep filed feedback, apply fixes, validate, release — the same loop any repo can run on its own internal skills. |

## How It Fits Together

An agent in a consumer project runs `hls-requirements-interview`, then
`hls-plan-builder`, then hands the plan to `hls-factory-orchestrate`, which dispatches
stories to implementing agents, verifies each against local gates
(`dev-browser` for UI), and puts every story through a bounded PR review —
blockers fixed, follow-ups delta-only, capped rounds — tracking everything in
`beads`. When a skill misfires
along the way, `hls-skill-feedback` files it here; `hls-skill-sweep` turns those
reports into released fixes. `hls-repo-bootstrap` and `hls-process-init`/
`hls-process-revamp` set new and existing repos up to run this way.

Stack defaults where skills need one: NestJS (backend), React + TanStack +
Tailwind (frontend) — defaults, not mandates.

## Running the Factory

Launch the coordinator with a durable directive — `/goal` (or `/loop` for
recurring sweeps) in Claude Code, `/goal` in Codex, or headless
(`claude -p` / `codex exec`) on a VPS. Agent roles — who coordinates, who
implements, who reviews, and the exact dispatch commands — live in the host
repo's `.factory/agents.json`, scaffolded by `hls-process-init`. Full guide:
[running-the-factory](skills/hls-factory-orchestrate/references/running-the-factory.md);
review rules:
[review-protocol](skills/hls-factory-orchestrate/references/review-protocol.md).

## Development

```sh
node scripts/validate-skills.mjs   # quality gate — must pass before commit
bd ready                           # work queue (beads, embedded)
```

This repo follows its own skills: work is tracked in beads, sessions are
logged in [docs/log.md](docs/log.md), and skill changes land in
[CHANGELOG.md](CHANGELOG.md). See [AGENTS.md](AGENTS.md) for the operating
manual and [docs/index.md](docs/index.md) for the wiki.

## License

MIT — see [LICENSE](LICENSE).
