# Software Factory

Higher Level Software's coding-agent skills: a complete loop for evidence-led
delivery — **requirements → architecture → plan → orchestrate → verify →
learn** — packaged as installable [Agent Skills](https://vercel.com/docs/agent-resources/skills).

This factory is designed for **one human operator**. The operator may run many
isolated agent sessions across a laptop, additional laptops, or VPS hosts;
machines add capacity and resilience, never another decision authority.

New here? Read [The Factory Method](docs/factory-method.md).

## Install

```sh
npx skills add hls-uk/software-factory                    # choose interactively
npx skills add hls-uk/software-factory --skill '*'        # install everything
npx skills add hls-uk/software-factory --skill hls-beads --skill hls-factory-orchestrate
```

Consumer repos record the installed source commit and skill list in
`.factory/skills-lock.json`. The lifecycle is **install** (`hls-process-init`),
**update** (`hls-skill-update`), and **feed back** (`hls-skill-feedback` →
`hls-skill-sweep`).

## Skills

### Delivery loop

| Skill | What it does |
|---|---|
| [hls-requirements-interview](skills/hls-requirements-interview/SKILL.md) | Interviews the operator into confirmed, testable requirements. |
| [hls-architecture](skills/hls-architecture/SKILL.md) | Evaluates expensive-to-reverse choices against explicit project criteria and produces an operator-signed architecture. |
| [hls-plan-builder](skills/hls-plan-builder/SKILL.md) | Turns requirements and architecture into criteria-traced, just-in-time story waves and a Beads graph. |
| [hls-factory-orchestrate](skills/hls-factory-orchestrate/SKILL.md) | Runs the long-lived story loop: dispatch, verify, deterministic review, promotion, evidence, repeat. |
| [hls-factory-status](skills/hls-factory-status/SKILL.md) | Produces a fixed-shape, read-only report across repos, hosts, lanes, gates, and queues. |
| [hls-tech-playbook](skills/hls-tech-playbook/SKILL.md) | Reusable stack-specific failure diagnoses and proven workarounds. |

### Substrate

| Skill | What it does |
|---|---|
| [hls-repo-bootstrap](skills/hls-repo-bootstrap/SKILL.md) | Adds durable repo memory, entrypoints, logs, decisions, and learnings. |
| [hls-process-init](skills/hls-process-init/SKILL.md) | Installs the factory process in a new repo, including gates and per-host configuration. |
| [hls-process-revamp](skills/hls-process-revamp/SKILL.md) | Adopts the factory incrementally in an established repo. |
| [hls-beads](skills/hls-beads/SKILL.md) | Embedded durable work tracking: queue, claims, dependencies, blockers, and evidence closes. |
| [hls-dev-browser](skills/hls-dev-browser/SKILL.md) | Browser-driven UI verification with assertions and screenshot evidence. |
| [hls-publish-report](skills/hls-publish-report/SKILL.md) | Builds stakeholder PDFs from selected Markdown sources while keeping Markdown authoritative. |

### Evolution loop

| Skill | What it does |
|---|---|
| [hls-skill-feedback](skills/hls-skill-feedback/SKILL.md) | Files structured field feedback and registers local stopgaps. |
| [hls-skill-sweep](skills/hls-skill-sweep/SKILL.md) | Triages feedback, fixes skills, validates, and releases. |
| [hls-skill-update](skills/hls-skill-update/SKILL.md) | Checks the committed install record, reads the release delta, reinstalls, and reconciles stopgaps. |

## How it fits together

Requirements provide numbered acceptance criteria. Architecture makes the
choices that stories must inherit. Planning cuts only the next dispatchable
wave and restates every applicable MUST. Orchestration gives each story to an
agent in an isolated worktree, re-runs its gates, and sends a mechanically
bound packet to a fresh read-only reviewer session. Any commit invalidates the
review until the exact new head is reviewed.

One operator retains requirement sign-off, architecture sign-off, risk waiver,
promotion, and external-action authority. The same operator, subscription,
provider, and host may be used for every agent role; independence comes from
fresh context, read-only permissions, and pinned evidence—not a second human.

Multiple hosts share one Beads queue and one active coordinator lease. Each
host records its actual commands and capabilities in a gitignored
`.factory/agents.local.json`; the committed `.factory/agents.json` holds only
portable requirements. See [host lanes](skills/hls-factory-orchestrate/references/host-lanes.md),
[lane setup](skills/hls-factory-orchestrate/references/lane-setup.md), and
[review packets](skills/hls-factory-orchestrate/references/review-packets.md).

The factory has no prescribed product stack. Architecture options are judged
against the confirmed requirements, existing estate, operator/host constraints,
security, cost, reversibility, and verification evidence.

## Development

```sh
node scripts/validate-skills.mjs
python3 skills/hls-factory-orchestrate/scripts/test_review_packet.py -v
bd ready
```

This repo follows its own process: work is in Beads, sessions are recorded in
[docs/log.md](docs/log.md), and each skill change is released in
[CHANGELOG.md](CHANGELOG.md). See [AGENTS.md](AGENTS.md) and the
[wiki index](docs/index.md).

## License

MIT — see [LICENSE](LICENSE).
