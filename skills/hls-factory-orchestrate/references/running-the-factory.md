# Running the Factory

How to launch and sustain the orchestration loop from each harness, and how
agent roles are assigned.

## Launching from Claude Code (coordinator)

The coordinator needs a directive that survives a long session. In order of
preference:

- **`/goal`** — set a durable session goal; the harness blocks stopping until
  the condition holds. Compose it from the plan, e.g.:

  ```
  /goal Deliver docs/plans/<slug>-plan.md via the hls-factory-orchestrate
  skill. Done when every acceptance criterion in
  docs/requirements/<slug>.md maps to a closed beads issue with verification
  evidence and the suite is green on main. Stop for deploys, publishing, or
  external services.
  ```

- **`/loop`** — for recurring sweeps rather than one continuous run (e.g.
  re-enter the story loop every 30 minutes, or self-paced). Useful on a
  workstation where sessions get interrupted.
- **Headless / VPS:** `claude -p "<the same goal text>"` in tmux (or a
  scheduled run) for fully-autonomous mode. The loop's durability does not
  depend on the session: state is in beads + docs, so a killed session
  resumes with the resume ritual in the skill.

## Launching from Codex (coordinator)

- **`/goal`** in the Codex TUI — same objective text; Codex keeps working
  until the goal's done/stop conditions hold.
- **Headless:** `codex exec "<goal text>"` from tmux/cron on a VPS.

Either harness can coordinate. Pick the strongest reasoning model you have
for the coordinator; it makes judgment calls (review caps, parking, gap
analysis) that cheaper models fumble.

## Agent Role Assignment

Roles live in the host repo at `.factory/agents.json`. Example:

```json
{
  "coordinator": {
    "harness": "claude-code",
    "model": "<strongest available, e.g. claude-fable-5>",
    "launch": "/goal via hls-factory-orchestrate"
  },
  "implementer": {
    "harness": "codex",
    "dispatch": "codex exec --model gpt-5.5-codex -c model_reasoning_effort=\"xhigh\" \"$(cat goal.txt)\""
  },
  "reviewer": {
    "harness": "claude-code",
    "dispatch": "claude -p \"$(cat review-prompt.txt)\"",
    "note": "must not be the implementer; cross-vendor pairing catches more"
  }
}
```

`dispatch` is the literal command the coordinator runs (goal/prompt text
substituted). Any harness/CLI works if it can take a prompt and work a
branch.

## Where Defaults Live

Precedence, most specific wins:

1. `.factory/agents.json` in the host repo — the authoritative assignment
   (hls-process-init scaffolds it).
2. `docs/process.md` — the human-readable record of the same choices plus
   operating mode; keep the two consistent.
3. The skill defaults — what this skill assumes when neither exists:
   coordinator = the strongest model in the session you launched from;
   implementer = `codex exec` at xhigh (command in the SKILL.md);
   reviewer = a fresh session of the coordinator's harness.

Cross-vendor role pairing (e.g. Claude coordinates and reviews, Codex
implements) is deliberate: an independent reviewer with different failure
modes catches what the implementer's own family misses. Same-vendor works;
prefer separation of *sessions* at minimum — an agent must never review its
own diff.

## Worktrees in Practice

The lifecycle rules live in the SKILL.md (Worktree Rules); the operational
details:

- Each worktree needs its own dependency install (`npm ci` in the worktree
  after `git worktree add`). With pnpm this is nearly free (shared content-
  addressed store) — worth preferring in repos built for the factory. Budget
  the install time into story dispatch either way.
- Worktrees share the repo's object store — creating one is cheap and does
  not duplicate history. Disk cost is the checkout plus `node_modules`.
- beads supports worktrees natively: `bd` run inside a worktree finds the
  main repo's `.beads/` via a redirect file. Beads mutations still belong to
  the coordinator, not implementers.
- Port collisions: two stories running dev servers in parallel worktrees
  will fight over default ports. The story's verification commands should
  set distinct ports (or the plan should not parallelize two
  server-occupying stories).

## Practical Notes for Days-Long Runs

- Run the coordinator where the verification gates run (same machine/VPS) —
  it must execute tests and dev-browser checks itself.
- `git push` + `bd dolt push` at every checkpoint; a crashed VPS then costs
  minutes, not the run.
- On workstations, expect interruption: the resume ritual (plan
  current-state block → `docs/log.md` tail → `bd ready`) is the contract that
  makes interruption cheap.
- Watch spend: one story = one implementer dispatch + gates + at most three
  review rounds. If a story is burning multiples of that, it's a plan
  problem — park and re-plan rather than paying for grind.
