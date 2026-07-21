# Host Lane Setup — one operator, one machine profile

Run this first-use ritual on every laptop or VPS before dispatching there,
and rerun it after any CLI, model, subscription, OS, or hardware change. The
repo declares portable requirements; each host records its actual tools and
capabilities.

- **Committed `.factory/agents.json` carries portable requirements:** tiers,
  `operatingMode`, `modelRoutingProfile`, `assuranceProfile`, `releaseStage`,
  billing policy, independence rules, and capabilities a lane may need. It
  contains no personal paths or credentials.
- **Gitignored `.factory/agents.local.json` carries one host's reality:**
  host id, absolute CLI paths, exact locally available model ids, dispatch
  commands, capabilities, and redacted preflight results.
- **One provider is enough.** Coordinator, implementer, and reviewer may use
  the same provider in separate sessions. Review independence is context
  separation, not a second subscription or second person.

## Interview the host

Record:

1. Stable `hostId`, operating system, and whether the host may coordinate,
   implement, review, or any combination.
2. Available capabilities such as Docker, browser automation, local database,
   GPU, VPN/private-network access, and expected online windows.
3. For each role/lane: absolute CLI path, exact model id currently exposed by
   that authentication mode, effort level, and literal dispatch command.
4. The review command: it must start a fresh session and default to read-only.
5. Resource bounds: safe concurrency, memory/disk floor, port ranges, and any
   host-local database namespace.

Do not assume another host has the same binaries, models, subscriptions, or
filesystem paths.

## Verify before writing

Run probes through the same shell and absolute binaries used by real dispatch:

1. **Authentication and billing.** Verify the configured auth mode. If the
   repo declares `subscriptions-only`, a detected AI API-key variable is a
   preflight failure: ask the operator to remove it and rerun. Do not hide it
   with a wrapper or silently switch billing modes.
2. **Model probe.** For every selected lane and reviewer command, request a
   trivial exact response.
3. **Workspace probe.** In a disposable worktree, run a build-tool probe and
   make a no-op commit. This proves access to build caches and the shared Git
   common directory.
4. **Capability probes.** Test only declared capabilities: for example Docker
   reachability, browser launch, required private-network route, and free disk.
5. **Read-only review probe.** Start the reviewer command against a disposable
   packet and confirm it cannot modify the repo.

A failed probe disables the lane with a reason. Never convert failure into an
undocumented local workaround.

## Write the local profile

- Confirm `.factory/agents.local.json` is gitignored.
- Write atomically, then set mode `0600`.
- Store non-secret configuration only. Never write tokens, keys, cookie
  values, credential-helper output, or resolved secret-store values.
- Include redacted probe evidence and an expiry/recheck timestamp.

Example:

```json
{
  "hostId": "vps-a",
  "enabled": true,
  "coordinatorEligible": true,
  "capabilities": ["containers", "database"],
  "limits": {"maxStories": 2, "minFreeDiskGb": 20},
  "implementers": [
    {"id": "frontier-a", "tier": "frontier", "dispatch": "<absolute command>"}
  ],
  "reviewer": {"dispatch": "<absolute read-only fresh-session command>"},
  "preflight": {"checkedAt": "<ISO-8601>", "status": "pass"}
}
```

Rerun the whole ritual instead of hand-editing after a host, CLI, model,
subscription, capability, or auth change. Multi-host coordination and
failover are defined in [host-lanes.md](host-lanes.md).
