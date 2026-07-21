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
  "coordinator": { "launch": "<durable goal command>" },
  "operatingMode": "supervised",
  "modelRoutingProfile": "balanced",
  "assuranceProfile": "standard",
  "releaseStage": "beta",
  "billingPolicy": "subscriptions-only",
  "implementers": [
    {
      "id": "local-frontier",
      "provider": "<provider-a>",
      "tier": "frontier",
      "dispatch": "<absolute command using goal.txt>",
      "maxConcurrent": 1
    },
    {
      "id": "local-strong",
      "provider": "<provider-a>",
      "tier": "strong",
      "dispatch": "<absolute command using goal.txt>",
      "maxConcurrent": 1
    },
    {
      "id": "local-fast",
      "provider": "<provider-b>",
      "tier": "fast",
      "enabled": false,
      "dispatch": "<absolute command using goal.txt>",
      "note": "enable only after local evaluation proves the allowed low-risk scope"
    }
  ],
  "reviewer": { "tier": "frontier", "dispatch": "<absolute read-only fresh-session command>" },
  "host": { "maxLoadPerCore": 0.8, "minFreeMemGb": 4, "minFreeDiskGb": 10 },
  "limits": { "<provider-a>": { "windowHours": "<observed>" } }
}
```

These four fields are independent. `modelRoutingProfile` only selects model
tier/effort; it never grants autonomy, lowers assurance, or authorizes a later
release stage. Migrate a legacy `deliveryProfile` value only when it is one of
`quality`, `balanced`, or `throughput`; otherwise stop and resolve the
ambiguous config. Missing assurance defaults to `standard`.

Tiers are local capability classes, not permanent model names: **frontier**
is the strongest verified coding/reasoning lane available to the operator;
**strong** is a lower-cost lane proven on normal well-specified stories;
**fast** is an optional lane proven only for narrow mechanical work. Record
the evaluation date and evidence in the host profile, because model names and
capabilities drift. `{effort}` may be substituted where a harness supports it;
otherwise encode effort as separate lane entries.

Concurrency: lanes on the same provider may share limits. Start with one
in-flight story on the current host and raise the cap only after verification
has proven the repo, host, and provider limits parallel-safe. Multiple healthy
providers or hosts add resilience, but are never required.

## Billing Guardrail — subscriptions only, by default

The factory defaults to the operator's configured **subscription** plans.
Per-token API billing is never used unless a lane explicitly opts
in with `"billing": "api"` in `agents.json`; the default for every lane,
coordinator, and reviewer is `"billing": "subscription"` whether stated or
not. Three rules enforce it:

- **Sanitize the dispatch environment.** Headless lanes and coordinators
  inherit the launching shell's environment — a stray `ANTHROPIC_API_KEY` /
  `OPENAI_API_KEY` silently flips the CLI to per-token billing with no
  visible change in behavior. Unless a lane declares `"billing": "api"`,
  dispatch and supervisor launch commands strip the keys:
  `env -u ANTHROPIC_API_KEY -u OPENAI_API_KEY <dispatch cmd>`. Repos that
  prohibit AI API-key configuration outright declare
  `"billingPolicy": "subscriptions-only"`: a set key is then a **preflight
  failure** — refuse and have the operator remove it from their shell config
  ([lane-setup.md](lane-setup.md)) — not something to strip around.
- **Preflight the auth mode, not just the model.** Before wave 1, verify
  each provider is on subscription auth through the same shell the
  dispatches use (concrete per-CLI commands are in the hls-tech-playbook
  skill's harness-clis reference). A lane whose auth mode can't be
  confirmed is disabled with a note, like any other failed preflight.
- **Cooling never escalates billing.** Usage-limit cooling is resolved by
  shifting to healthy same-tier lanes or waiting for the window — never by
  switching a lane to API credits. This is the billing analog of "quality
  never downgrades": a paused factory costs time; a silent billing
  escalation costs money nobody approved. If a repo genuinely wants an
  API-billed overflow lane, it declares one explicitly (`"billing": "api"`,
  ideally `"enabled": false` until the operator turns it on).

## Lane Preflight

Preflight assumes each host's lanes exist, are authenticated as configured,
and reflect that host's actual CLIs and models — that is the per-host
lane-setup ritual ([lane-setup.md](lane-setup.md)), run once when adding the
host and after any tool/model/subscription change.

Before the first dispatch of a run — and after any `agents.json` change —
probe every lane with a trivial exec ("Reply with exactly: OK") using the
lane's dispatch command verbatim. A lane that can't answer cheaply will not
deliver a story expensively. The probe catches, before a story burns tokens
on it:

- **Model availability varies by auth.** Subscription-authenticated CLIs
  often expose different model ids than API keys (e.g. a ChatGPT-account
  Codex rejects model ids an API key accepts). The CLI's own configured
  default model is the best first guess for what the account can run.
- **Sandbox walls.** A sandboxed lane must be able to write the repo's build
  caches — Gradle/Maven/npm homes live *outside* the workspace, so grant them
  as extra writable roots — and reach services verification needs (e.g. the
  Docker socket for testcontainers). After the echo probe passes, run one
  build-tool probe (`--version` is enough) through the same lane. When
  stories run in git *worktrees*, the worktree's git metadata lives in the
  main repo's common dir — outside the workspace — so a lane cannot even
  `git add` without that common dir granted as a writable root (probe with a
  no-op commit, not just a build).
- **Propagate environment fixes into later goals.** When a run discovers an
  environment fix (a heap flag, an init script, a port variable), every
  *subsequent* goal's verify line must carry it — a lane runs its goal
  verbatim and will faithfully re-hit the fixed problem otherwise (seen
  live: a sweep lane re-hit a solved OOM because its goal carried the
  pre-fix verify command).

Probe through the SAME shell and launcher the real dispatches will use — a
supervisor's non-login shell can resolve a different (older) binary than
your interactive shell; prefer absolute paths in dispatch commands.

Record probe results in the usage ledger. A failing lane is disabled with a
note, never worked around silently.

## Story Routing — complexity × model routing profile

Every story carries a `Complexity` line from hls-plan-builder (`high` —
architectural, ambiguous, or high blast radius; `standard` — well-specified
feature work; `low` — mechanical, narrow, well-trodden). The repo's
`modelRoutingProfile` sets the trade-off. The coordinator picks lane tier +
effort per story:

| Complexity | `quality` | `balanced` (default) | `throughput` |
|---|---|---|---|
| high | frontier · xhigh | frontier · xhigh | frontier · xhigh |
| standard | frontier · xhigh | strong · high | strong · high |
| low | frontier · high | strong · medium | strong · medium; fast lane allowed for purely mechanical stories |

Rules that hold in **every** profile:

- **When independent review is required, the reviewer is frontier, always.** Review is the cheapest stage in the
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
- **Datastore/service state:** follow the plan's repo-specific isolation
  scheme. Each story gets its own namespace or disposable instance, injected
  through environment variables and removed at retirement. Prefer cheap
  namespacing where it provides real isolation; use separate instances when
  the technology cannot isolate safely.
- **Idempotency contract:** a story's verification starts by resetting its
  *own* database (drop-and-migrate or truncate-and-seed), touches only its
  leased resources, and is safe to re-run at any time. hls-plan-builder
  enforces this when writing stories.
- **Schema-migration versions:** when the repo has one global migration
  namespace (Flyway/Liquibase-style `V<N>` ordering), two concurrent stories
  following "next free number" from the same base both pick it — a collision
  the second merge discovers, not the first verify. **Prefer coordination-
  free timestamp versions** (`V<yyyyMMddHHmm>__desc`) where the migration
  tool orders numerically — no allocation authority, no gaps, safe across
  lanes, branches, and machines (trade-offs and the fallback integer-range
  lease scheme are in the hls-tech-playbook skill's migrations reference).
  Where a repo stays on small integers, lease each story a range at
  dispatch, state it in the goal, record it in `.env.story` — and remember
  **leases only work within a single allocation authority**: one observed
  run allocated independently on its integration branch and `main`, and both
  took the same version. Whatever the scheme, the goal must state the naming rule
  explicitly or implementers revert to next-free-integer.

## Verify Scope Under Parallelism

- **In the worktree:** the story's verify commands plus affected tests —
  tight loops that N stories can run concurrently.
- **On main, after each merge:** the coordinator runs the full suite in its
  own checkout. A failure there is P0: revert the merge or fix forward in a
  new story worktree before dispatching anything else.

**The second story to merge gets re-based and re-gated.** Concurrent stories
routinely touch the same shared files (scope catalogues, OpenAPI specs,
config); additive edits auto-merge cleanly — into a combined tree that
*neither* lane ever verified. Before merging story N+1, rebase it onto the
integration branch and run its gate against the combined tree; a
non-additive overlap surfaces here as a conflict and bounces instead of
corrupting the branch.

**Two kinds of interference — partition one, serialize the other.**
*Correctness* interference (ports, databases, migration numbers) is fixed by
the leases above: partition the resource and N lanes coexist. *Capacity*
interference — above all **memory** — has no lease: two full-suite gates
each booting an app + test containers can OOM both JVMs while every lease
holds (seen live: 48 GB host, two `@QuarkusTest` gates, both dead of heap
exhaustion; zero port/migration collisions). The host governor checks
capacity at *dispatch* time, but the heavy step is the *verify gate*, so:

- Run at most ONE full-suite gate at a time, regardless of how many lanes
  are implementing — implementation is cheap, gates are heavy. Queue gates.
- **Check the forked-test heap before blaming concurrency.** Build tools
  fork test JVMs with small default heaps (Gradle: 512m) that no one has
  ever set; a growing suite crosses that cliff and then OOMs even run
  *alone* — concurrency just gets there first. Confirmed live: a "parallel
  interference" OOM reproduced serially, root-caused to the 512m default,
  fixed by right-sizing the fork heap.
- Right-size non-invasively: the coordinator applies the heap setting via
  its own mechanism (e.g. a Gradle `--init-script` raising
  `Test.maxHeapSize`) so gate runs are fixed without out-of-scope edits to
  the tracked build — and files the permanent build change as a sweep bead.
  With per-fork heap known, N-concurrent-gates capacity math is possible;
  until then, serialize.
- A gate that dies of OOM after its story tests passed is a bounce, not a
  failure of the story — preserve the worktree diff, free the memory, and
  re-gate with the heap fix.
