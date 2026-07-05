# Parallel Dispatch & Resource Governance

How the coordinator runs multiple implementer lanes at once without blowing
subscription limits or the host. Two governors decide how many stories run:
**LLM capacity** (lanes whose provider isn't cooling) and **host capacity**
(load, memory, disk). Effective concurrency = min(open lanes, host headroom,
ready stories, the three-story cap).

## Lanes — `.factory/agents.json`

`implementers` is a pool of lanes; each lane names its provider, its
**tier**, and its dispatch command:

```json
{
  "coordinator": { "harness": "claude-code", "launch": "/goal via hls-factory-orchestrate" },
  "deliveryProfile": "balanced",
  "implementers": [
    {
      "id": "claude-frontier",
      "provider": "claude",
      "tier": "frontier",
      "dispatch": "claude -p --model claude-opus-4-8 \"$(cat goal.txt)\"",
      "maxConcurrent": 1
    },
    {
      "id": "claude-strong",
      "provider": "claude",
      "tier": "strong",
      "dispatch": "claude -p --model claude-sonnet-5 \"$(cat goal.txt)\"",
      "maxConcurrent": 1
    },
    {
      "id": "codex-frontier",
      "provider": "openai",
      "tier": "frontier",
      "dispatch": "codex exec --model gpt-5.5-codex -c model_reasoning_effort=\"{effort}\" \"$(cat goal.txt)\"",
      "maxConcurrent": 1
    },
    {
      "id": "codex-spark",
      "provider": "openai",
      "tier": "fast",
      "enabled": false,
      "dispatch": "codex exec --model gpt-5.3-codex-spark \"$(cat goal.txt)\"",
      "note": "research preview — enable when your plan has access"
    }
  ],
  "reviewer": { "harness": "claude-code", "tier": "frontier", "dispatch": "claude -p \"$(cat review-prompt.txt)\"" },
  "host": { "maxLoadPerCore": 0.8, "minFreeMemGb": 4, "minFreeDiskGb": 10 },
  "limits": { "claude": { "windowHours": 5 }, "openai": { "windowHours": 5 } }
}
```

Tiers: **frontier** (best available — Opus 4.8 class, GPT-5.5-Codex at
xhigh), **strong** (near-frontier at a fraction of cost and quota — Sonnet 5
class: ~63 vs ~69 SWE-bench Pro against Opus 4.8, 40% cheaper per token),
**fast** (real-time models like GPT-5.3-Codex-Spark: 1,000+ tok/s but a
large accuracy cliff — for mechanical edits and trivial rework only, never
whole stories). `{effort}` in a dispatch command is substituted from the
routing table where the harness supports an effort flag; otherwise encode
effort as separate lane entries.

Concurrency: lanes on the same provider **share that provider's slot** —
default one in-flight story per provider (VPS: Claude + Codex = two stories
in parallel; supervised workstation: one story total). Raise per-repo only
after verification has proven parallel-safe. Running both vendors in
parallel is the point: it doubles effective subscription throughput and no
single provider's window stalls the factory.

## Story Routing — complexity × delivery profile

Every story carries a `Complexity` line from hls-plan-builder (`high` —
architectural, ambiguous, or high blast radius; `standard` — well-specified
feature work; `low` — mechanical, narrow, well-trodden). The repo's
`deliveryProfile` sets the trade-off. The coordinator picks lane tier +
effort per story:

| Complexity | `quality` | `balanced` (default) | `throughput` |
|---|---|---|---|
| high | frontier · xhigh | frontier · xhigh | frontier · xhigh |
| standard | frontier · xhigh | strong · high | strong · high |
| low | frontier · high | strong · medium | strong · medium; fast lane allowed for purely mechanical stories |

Rules that hold in **every** profile:

- **The reviewer is frontier, always.** Review is the cheapest stage in the
  loop and the last defence before merge; the expensive failure is rework,
  not review tokens. Never downgrade it to save quota.
- **High-complexity stories never leave the frontier tier.** Review catches
  defects; it cannot inject design quality post-hoc — quality above
  "correct" comes from the implementer and the plan, not from more
  iterations. The bounded review protocol is deliberately unable to force
  restructuring, so don't send a weak model to do an architect's story.
- **Rework rounds go back to the story's original lane** (same tier). Under
  `throughput`, a trivial mechanical fix (rename, one-liner from an exact
  reviewer instruction) may use the fast lane.
- Routing is planned selection, not degradation: provider cooling (below)
  never downgrades a story's tier — a frontier story waits for a frontier
  lane rather than running on a lesser model.

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
3. Requeue the story to a healthy lane **of the same tier** on another
   provider — same branch and a fresh worktree from it; the goal gains one
   line noting the handover so the new implementer reads the existing diff
   first.
4. Quality never downgrades: cooling never moves a story down a tier. If no
   healthy same-tier lane exists, the story waits (work other tiers'
   stories meanwhile) — don't substitute a weaker model.

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
