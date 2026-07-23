# Software Factory — Agent Operating Manual

Higher Level Software's public set of coding-agent skills: the factory loop
(requirements → architecture → plan → orchestrate → verify → learn) packaged
as installable skills. It serves one human operator who may run isolated agent
sessions across multiple laptops or VPS hosts. This file is the source of
truth for working in this repo; `CLAUDE.md` just points here.

## What This Repo Is

- `skills/<name>/SKILL.md` — the product. Seventeen skills, each self-contained
  (its own `references/`), installable individually via `npx skills add`.
- `scripts/validate-skills.mjs` — the quality gate. Run it after every skill
  edit; CI runs it on every push.
- `docs/` — this repo's wiki: [index](docs/index.md), append-only
  [log](docs/log.md), the [Factory Method](docs/factory-method.md), and the
  [bootstrap brief](docs/BOOTSTRAP-BRIEF.md).
- `.beads/` — embedded beads work tracking. `bd ready` is the queue.

## Rules

1. **Skills are the source of truth.** Edit `skills/<name>/SKILL.md`, never an
   installed mirror. Each skill must stay self-contained — no links outside
   its own directory (installers copy single skill dirs).
2. **Validate after every skill change:** `node scripts/validate-skills.mjs`
   must exit 0 before you commit.
3. **Track work in beads** (see `skills/hls-beads/SKILL.md` — this repo follows
   its own skills): claim before working, close with evidence.
4. **Log sessions** in [docs/log.md](docs/log.md) — provenance format
   (Driven by / Executed by / What changed / Evidence), newest first.
5. **Session end:** validator green, beads state reported, log entry written,
   and changes left as one reviewable handoff. Commit/push only when the active
   profile or user grants authority. Reusable lessons go in the log or a skill
   fix — an answer that lives only in chat is lost.
6. **Releases:** every skill change gets a `CHANGELOG.md` line. Feedback from
   consumer projects arrives via the tracker in `.factory/feedback.json`;
   process it with `skills/hls-skill-sweep`.
7. **Keep the method current:** any process change updates
   [docs/factory-method.md](docs/factory-method.md) in the same session.
   Published artifacts are regenerated only when that source is actually
   published; Markdown remains authoritative.

## Boundaries

- Never publish, push to new remotes, or configure external services without
  explicit approval.
- No credentials or secrets in any file, including examples — use
  placeholders like `<JIRA_BASE_URL>`.
- Skills must stay agent-neutral (usable from Claude Code, Codex, Cursor,
  etc.) — no harness-specific instructions unless labeled as variants.

<!-- BEGIN BEADS INTEGRATION v:1 profile:minimal hash:6cd5cc61 -->
## Beads Issue Tracker

This project uses **bd (beads)** for issue tracking. Run `bd prime` to see full workflow context and commands.

### Quick Reference

```bash
bd ready              # Find available work
bd show <id>          # View issue details
bd update <id> --claim  # Claim work
bd close <id>         # Complete work
```

### Rules

- Use `bd` for ALL task tracking — do NOT use TodoWrite, TaskCreate, or markdown TODO lists
- Run `bd prime` for detailed command reference and session close protocol
- Use `bd remember` for persistent knowledge — do NOT use MEMORY.md files

**Architecture in one line:** issues live in a local Dolt DB; sync uses `refs/dolt/data` on your git remote; `.beads/issues.jsonl` is a passive export. See https://github.com/gastownhall/beads/blob/main/docs/SYNC_CONCEPTS.md for details and anti-patterns.

## Agent Context Profiles

The managed Beads block is task-tracking guidance, not permission to override repository, user, or orchestrator instructions.

- **Conservative (default)**: Use `bd` for task tracking. Do not run git commits, git pushes, or Dolt remote sync unless explicitly asked. At handoff, report changed files, validation, and suggested next commands.
- **Minimal**: Keep tool instruction files as pointers to `bd prime`; use the same conservative git policy unless active instructions say otherwise.
- **Team-maintainer**: Only when the repository explicitly opts in, agents may close beads, run quality gates, commit, and push as part of session close. A current "do not commit" or "do not push" instruction still wins.

## Session Completion

This protocol applies when ending a Beads implementation workflow. It is subordinate to explicit user, repository, and orchestrator instructions.

1. **File issues for remaining work** - Create beads for anything that needs follow-up
2. **Run quality gates** (if code changed) - Tests, linters, builds
3. **Update issue status** - Close finished work, update in-progress items
4. **Handle git/sync by active profile**:
   ```bash
   # Conservative/minimal/default: report status and proposed commands; wait for approval.
   git status

   # Team-maintainer opt-in only, unless current instructions forbid it:
   git pull --rebase
   git push
   git status
   ```
5. **Hand off** - Summarize changes, validation, issue status, and any blocked sync/commit/push step

**Critical rules:**
- Explicit user or orchestrator instructions override this Beads block.
- Do not commit or push without clear authority from the active profile or the current user request.
- If a required sync or push is blocked, stop and report the exact command and error.
<!-- END BEADS INTEGRATION -->

<!-- BEGIN BEADS CODEX SETUP: generated by bd setup codex -->
## Beads Issue Tracker

Use Beads (`bd`) for durable task tracking in repositories that include it. Use the `beads` skill at `.agents/skills/hls-beads/SKILL.md` (project install) or `~/.agents/skills/beads/SKILL.md` (global install) for Beads workflow guidance, then use the `bd` CLI for issue operations.

### Quick Reference

```bash
bd ready                # Find available work
bd show <id>            # View issue details
bd update <id> --claim  # Claim work
bd close <id>           # Complete work
bd prime                # Refresh Beads context
```

### Rules

- Use `bd` for all task tracking; do not create markdown TODO lists.
- Run `bd prime` when Beads context is missing or stale. Codex 0.129.0+ can load Beads context automatically through native hooks; use `/hooks` to inspect or toggle them.
- Keep persistent project memory in Beads via `bd remember`; do not create ad hoc memory files.

**Architecture in one line:** issues live in a local Dolt DB; sync uses `refs/dolt/data` on your git remote; `.beads/issues.jsonl` is a passive export. See https://github.com/gastownhall/beads/blob/main/docs/SYNC_CONCEPTS.md for details and anti-patterns.
<!-- END BEADS CODEX SETUP -->
