# Software Factory — Bootstrap Brief

This repo is Higher Level Software's public set of coding-agent skills. It must be
installable from public GitHub via the Vercel skills CLI:
`npx skills add <owner/repo>` (works with Claude Code, Copilot, Cursor, etc.; when run
inside an eve project it auto-detects and offers to install into `agent/skills/` —
see https://vercel.com/docs/agent-resources/skills).

## Repo shape

- `skills/<skill-name>/SKILL.md` per the Agent Skills spec (frontmatter: `name`,
  `description`; body = compact instructions). Per-skill `references/` and `scripts/`
  as needed — keep SKILL.md short, push depth into references.
- `README.md`: skill directory (one line each) + install instructions.
- `scripts/validate-skills.*`: lints every SKILL.md (frontmatter present/valid,
  description quality, internal links resolve). Wire into CI (GitHub Actions).
- This repo dogfoods its own patterns: beads (embedded) tracks the work; the repo
  keeps its own LLM-wiki-style docs (`docs/index.md`, `docs/log.md`).

## v1 skill set

1. **repo-bootstrap** — initialise a new software (or knowledge-work) repo using the
   LLM Wiki pattern (karpathy: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f —
   raw sources / wiki pages / schema file; `index.md` catalog, `log.md` append-only
   journal; ingest / query / lint operations) plus a compounding-learning loop: every
   session leaves the repo smarter. Study `~/dev/vdbuk/overclaude` (canonical
   `tools/agents/handbook.md` generating `CLAUDE.md` + `AGENTS.md` adapters, domain
   `overview.md` entrypoints, decision log, mandatory sync rules) and
   `~/dev/vdbuk/vdb-root` as working exemplars.
2. **requirements-interview** — build requirements by interviewing the user:
   structured questioning, assumption surfacing, output = requirements doc with
   testable acceptance criteria, stored in the host repo's wiki.
3. **plan-builder** — turn requirements into plans for high-level engineering agents:
   stories with dependencies, per-story verification strategy, sized for one-agent
   handoff.
4. **factory-orchestrate** — the long-running loop: a top-level coordinator agent
   (Fable/Opus 4.8 class) takes a requirements set and coordinates delivery by handing
   whole stories to Codex (GPT-5.5 xhigh) agents via `/goal`, with local verification
   gates (tests, lint, dev-browser checks) before accepting each story. Must support
   running for days: durable tracking (beads issues as the queue, decision log,
   current-state summary), checkpoint rhythm, resume-after-compaction, and
   evidence-based "done" per requirement — production quality, not intent.
5. **beads** — manage work with beads in embedded mode
   (https://github.com/gastownhall/beads): issue create/update, ready-work selection,
   dependencies, status flow, sync/compaction. This is the work-management substrate
   for factory-orchestrate and for consumer repos.
6. **dev-browser** — web UI verification and automation via
   https://github.com/sawyerhood/dev-browser: persistent page across scripts,
   screenshots, assertions; used as a verification gate for web-facing stories.
7. **skill-feedback** + **skill-sweep** — the evolution loop. skill-feedback: from any
   consumer project, agents file improvement issues against this repo's tracker
   (Jira; leave project key/URL as configurable placeholders — do not invent config).
   skill-sweep: periodically sweep filed issues, apply fixes to the skills here,
   validate, release. Document the cascade so consumer projects can adopt the same
   feedback→sweep pattern for their own internal skills.
8. **process-init** / **process-revamp** — initialise a new repo's engineering process,
   or revamp an existing repo's, to exploit an agentic software factory. Two operating
   modes: fully autonomous on a VPS; partially autonomous on a MacBook Pro (permission
   modes, human checkpoints, verification gates). Must fit into a host repo's existing
   processes rather than steamroll them.

## Constraints & preferences

- Stack defaults, not mandates: NestJS backend; React + TanStack + Tailwind frontend.
- Skills must adapt to the host repo's conventions; discover before prescribing.
- Survey recently changed repos under `~/dev` for patterns worth stealing:
  `incept5/`, `vdbuk/*`, `arbtechuk/`, `personal/`, `corfai/` (newest first).

## Verification (the loop)

Fast, per skill: run `scripts/validate-skills` after each skill is authored.
Slower gates: local install test (`npx skills add` against this repo / a temp clone);
each skill exercised once against a scratch target repo where feasible; README
directory complete and accurate.

Track everything in beads; log decisions in `docs/log.md`; keep `docs/index.md`
current so a fresh agent can resume without rereading history.
