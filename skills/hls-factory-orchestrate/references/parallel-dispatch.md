# Parallel Dispatch & Resource Governance

How the coordinator runs multiple implementer lanes at once without blowing
subscription limits or the host. Two governors decide how many stories run:
**LLM capacity** (lanes whose provider isn't cooling) and **host capacity**
(load, memory, disk). Effective concurrency = min(open lanes, host headroom,
ready stories, the three-story cap).

## Lanes — `.factory/agents.json` v2

`implementers` is a pool; each lane names its provider and dispatch command:

```json
{
  "coordinator": { "harness": "claude-code", "launch": "/goal via hls-factory-orchestrate" },
  "implementers": [
    {
      "id": "claude-main",
      "provider": "claude",
      "dispatch": "claude -p --model claude-opus-4-8 \"$(cat goal.txt)\"",
      "maxConcurrent": 1
    },
    {
      "id": "codex-main",
      "provider": "openai",
      "dispatch": "codex exec --model gpt-5.5-codex -c model_reasoning_effort=\"xhigh\" \"$(cat goal.txt)\"",
      "maxConcurrent": 1
    }
  ],
  "reviewer": { "harness": "claude-code", "dispatch": "claude -p \"$(cat review-prompt.txt)\"" },
  "host": { "maxLoadPerCore": 0.8, "minFreeMemGb": 4, "minFreeDiskGb": 10 },
  "limits": { "claude": { "windowHours": 5 }, "openai": { "windowHours": 5 } }
}
```

Defaults when unconfigured: **autonomous VPS = 1 Claude + 1 Codex lane**
(two stories in parallel, one top-tier model each); **supervised
workstation = one lane total**, alternating providers per story. A legacy
single `implementer` object is one lane. Raise `maxConcurrent` per repo only
after its verification has proven parallel-safe.

Running both vendors in parallel is the point: it doubles effective
subscription throughput and no single provider's window stalls the factory.

## The Scheduling Loop

While ready stories exist and any lane is open:

1. **Capacity checks** (both must pass, else hold the slot and re-check when
   a running story finishes):
   - *Provider:* lane's provider is not cooling (see below).
   - *Host:* 1-min load per core < `maxLoadPerCore`, free memory >
     `minFreeMemGb`, free disk > `minFreeDiskGb`. Never reclaim capacity by
     killing running work — scale by not starting.
2. **Lease resources** for the story (see Resource Leases).
3. Create the worktree, compose the goal, dispatch into the lane, and append
   a `dispatch` entry to the usage ledger.
4. On any story completion: verify → review → accept/park per the main loop,
   drop its lease, then refill lanes.

Assignment is next-ready-story to next-open-lane — no provider affinity by
default; the plan may pin a story to a lane in its notes when it matters.

## Usage Ledger + Limit Handling

**Ledger (advisory):** append-only `.factory/usage.jsonl`, one line per
event: `{ts, provider, lane, story, event: dispatch|complete|limit}`. It
survives restarts and lets the coordinator pace itself — if this host's
dispatches cluster early in a window, prefer the other provider. It is never
authoritative: **other hosts share the same subscription**, so the window
may be consumed by work you cannot see.

**Limit signals (authoritative):** rate-limit/quota errors or usage-limit
messages in dispatch output. On a signal:

1. Append a `limit` event; mark the provider **cooling** with a `resumeAt` —
   the next window boundary if derivable from the ledger, else now + 30 min.
2. Let that lane's in-flight story finish if it can; otherwise park the
   story normally (push branch, remove worktree, note in bead).
3. Requeue the story to a healthy provider's lane — same branch and a fresh
   worktree from it; the goal gains one line noting the handover so the new
   implementer reads the existing diff first.
4. Quality never downgrades: production code is written by top-tier models
   only. If no healthy lane exists, pause — don't substitute a weaker model.

**Pause / resume (all providers cooling):** checkpoint fully (push code,
`bd dolt push`, log entry with `resumeAt` per provider), then:

- *Live session:* idle until the earliest `resumeAt`, then probe with one
  cheap dispatch before refilling lanes.
- *Headless:* exit cleanly and rely on a scheduled relaunch (cron/launchd
  every 30–60 min); the resume ritual + ledger make restart cheap — a
  relaunch inside a cooling window checks `resumeAt`, sees nothing is
  workable, and exits.

Hitting limits is a normal operating condition, not an error. Log it,
adapt, continue.

## Resource Leases

Granted at dispatch, recorded in `.worktrees/<slug>/.env.story`, injected
into the story goal, dropped at retirement:

- **Ports:** lane *n* owns block `4000+100n … 4099+100n` (`PORT`,
  `PORT_BASE`). Verification commands must take ports from env, never
  hardcode.
- **Database:** one shared host Postgres; each story gets its own database
  `story_<slug>` (`createdb` at lease, `dropdb` at retirement), injected as
  `DATABASE_URL`. Other services follow the same pattern (e.g. Redis DB
  index = lane number) before reaching for per-story docker-compose stacks —
  shared-service-with-namespacing keeps N parallel verifications cheap.
- **Idempotency contract:** a story's verification starts by resetting its
  *own* database (drop-and-migrate or truncate-and-seed), touches only its
  leased resources, and is safe to re-run at any time. hls-plan-builder
  enforces this when writing stories.

## Verify Scope Under Parallelism

- **In the worktree:** the story's verify commands plus affected tests —
  tight loops that N stories can run concurrently.
- **On main, after each merge:** the coordinator runs the full suite in its
  own checkout. A failure there is P0: revert the merge or fix forward in a
  new story worktree before dispatching anything else.
