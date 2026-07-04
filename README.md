# Software Factory

Higher Level Software's coding-agent skills: a complete loop for agent-driven
delivery — **requirements → plan → orchestrate → verify → learn** — packaged
as [Agent Skills](https://vercel.com/docs/agent-resources/skills) installable
into Claude Code, Codex, Cursor, and 70+ other agents.

## Install

```sh
npx skills add hls-uk/software-factory                    # pick skills interactively
npx skills add hls-uk/software-factory --skill '*'        # everything
npx skills add hls-uk/software-factory --skill beads --skill factory-orchestrate
```

Run from an [eve](https://vercel.com/docs/eve) project directory and the CLI
offers to install into your eve building agent.

## The Skills

**Delivery loop**

| Skill | What it does |
|---|---|
| [requirements-interview](skills/requirements-interview/SKILL.md) | Build requirements by interviewing the user — testable acceptance criteria, surfaced assumptions. |
| [plan-builder](skills/plan-builder/SKILL.md) | Requirements → stories sized for one-agent handoff, each with its own verification, registered as a beads graph. |
| [factory-orchestrate](skills/factory-orchestrate/SKILL.md) | The long-running coordinator: dispatch whole stories to implementing agents via `/goal`, verify locally, loop for days until every criterion has evidence. |

**Substrate**

| Skill | What it does |
|---|---|
| [repo-bootstrap](skills/repo-bootstrap/SKILL.md) | LLM Wiki + compounding-learning loop for new repos — every session leaves the repo smarter. |
| [process-init](skills/process-init/SKILL.md) | Set up a repo's engineering process for the factory: autonomous (VPS) or supervised (workstation) mode, gates, rituals. |
| [process-revamp](skills/process-revamp/SKILL.md) | Adopt the factory in an existing repo without steamrolling working conventions. |
| [beads](skills/beads/SKILL.md) | Work tracking with [beads](https://github.com/gastownhall/beads) in embedded mode — ready queue, claims, evidence-based closes. |
| [dev-browser](skills/dev-browser/SKILL.md) | Web UI verification with [dev-browser](https://github.com/sawyerhood/dev-browser) — persistent pages, Playwright assertions, screenshot evidence. |

**Evolution loop**

| Skill | What it does |
|---|---|
| [skill-feedback](skills/skill-feedback/SKILL.md) | File structured improvement issues from any consumer project back to this repo's tracker. |
| [skill-sweep](skills/skill-sweep/SKILL.md) | Sweep filed feedback, apply fixes, validate, release — the same loop any repo can run on its own internal skills. |

## How It Fits Together

An agent in a consumer project runs `requirements-interview`, then
`plan-builder`, then hands the plan to `factory-orchestrate`, which dispatches
stories to implementing agents and verifies each against local gates
(`dev-browser` for UI), tracking everything in `beads`. When a skill misfires
along the way, `skill-feedback` files it here; `skill-sweep` turns those
reports into released fixes. `repo-bootstrap` and `process-init`/
`process-revamp` set new and existing repos up to run this way.

Stack defaults where skills need one: NestJS (backend), React + TanStack +
Tailwind (frontend) — defaults, not mandates.

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
