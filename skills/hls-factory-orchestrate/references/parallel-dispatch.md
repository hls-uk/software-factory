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

**Lean Claude-harness context (P0):** every Claude Code implementer and
reviewer command carries `--strict-mcp-config --setting-sources project`.
This retains repo instructions/settings and built-in tools while excluding
user-level MCP/plugin injection. Put a story-required MCP server in repo
configuration or pass an explicit `--mcp-config`. The static and optional
live gates are in `<skill-dir>/scripts/context_baseline.py`; lane context must
stay at or below 30,000 tokens.

**Optional labelled GLM-5.2 variant:** HLS does not enable this by default.
A host may add the following disabled lane only after following the auth,
billing, and drift checks in the hls-tech-playbook `harness-clis` reference:

```json
{
  "id": "optional-glm52-claude",
  "provider": "zai",
  "tier": "strong",
  "billing": "subscription",
  "enabled": false,
  "dispatch": "env -u ANTHROPIC_API_KEY ANTHROPIC_BASE_URL=https://api.z.ai/api/anthropic ANTHROPIC_AUTH_TOKEN=\"$Z_AI_API_KEY\" API_TIMEOUT_MS=3000000 claude -p --model glm-5.2 --strict-mcp-config --setting-sources project \"$(cat goal.txt)\"",
  "note": "enable only after the operator proves this secret is a Coding Plan subscription token"
}
```

If the key-type probe does not prove subscription auth, change the lane to
explicit API billing and obtain authority or keep it disabled. Never commit
the token or place the endpoint override in user-wide Claude settings.

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
  ([lane-setup.md](lane-setup.md)) — not something to strip around. The
  optional GLM variant's per-dispatch `ANTHROPIC_AUTH_TOKEN` is allowed only
  after its separate Coding Plan key-type proof.
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
2. **Lease resources** for the story (see
   [dispatch-resources.md](dispatch-resources.md)).
3. Create the worktree, compose the goal, dispatch into the lane, and append
   a `dispatch` event to the local metrics ledger.
4. On any story completion: verify → review → accept/park per the main loop,
   drop its lease, then refill lanes.

Assignment is next-ready-story to next-open-lane — no provider affinity by
default; the plan may pin a story to a lane in its notes when it matters.

## Where the procedures live

- **Lane preflight, metrics, limit signals, and pause/resume:**
  [dispatch-operations.md](dispatch-operations.md) — read at run start,
  after an `agents.json` change, at checkpoints, and when a limit fires.
- **Resource leases and verify scope under parallelism:**
  [dispatch-resources.md](dispatch-resources.md) — read at dispatch and
  verify/merge time.
- **Context budgets:** after any skill, reference, or lane-config change, run
  `python3 <skill-dir>/scripts/context_baseline.py --check`; optional live
  lane probing is defined in the operations reference.
