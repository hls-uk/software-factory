# Host Lanes — One Operator, Multiple Machines

The factory has one human operator and may execute on several laptops or VPS
hosts. Hosts are capacity and failure-domain boundaries, not ownership or
decision boundaries. One operator confirms requirements, signs architecture,
accepts risk, and authorises promotion.

## State model

- **One queue:** every host reads and atomically claims from the same Beads
  workspace. A story has one claim and one worktree at a time.
- **One integration authority:** only the active coordinator merges or
  promotes. Other hosts implement or review dispatched work; they do not run
  competing integration loops.
- **Durable handover:** the active coordinator identity, host, lease expiry,
  current wave, and in-flight lane ids live in Beads plus the plan current-
  state block. A session or host may disappear without taking authority state
  with it.
- **No host-owned scope:** do not partition source ownership by laptop. Route
  stories by capability, capacity, locality, and resource availability.

## Configuration

The committed `.factory/agents.json` declares portable requirements and
defaults: integration branch, delivery profile, billing policy, lane tiers,
review rules, and any required capabilities. It contains no credentials or
host-specific absolute paths.

Each host carries a gitignored `.factory/agents.local.json`, created by
[lane-setup.md](lane-setup.md), with:

```json
{
  "hostId": "workstation-a",
  "enabled": true,
  "capabilities": ["docker", "browser"],
  "coordinatorEligible": true,
  "implementers": [
    {"id": "local-strong", "tier": "strong", "dispatch": "<absolute command>"}
  ],
  "reviewer": {"dispatch": "<absolute read-only fresh-session command>"},
  "preflight": {"checkedAt": "<ISO-8601>", "status": "pass"}
}
```

The file is non-secret despite mode `0600`: commands and capability labels
are allowed; tokens, keys, cookie values, and secret-store output are not.

## Dispatch across hosts

1. Refresh the shared queue and plan state before claiming.
2. Confirm the active coordinator lease has not expired. Only the operator
   may transfer it to another host; record the transfer before starting the
   replacement coordinator.
3. Select a healthy host whose local preflight satisfies the story resources.
4. Claim the story, record `hostId`, lane id, worktree/branch, resource lease,
   and dispatch time in the Bead, then dispatch once.
5. A second host never recreates an apparently quiet story. Check the claim,
   remote branch, lane pid/log, and last checkpoint first; recover explicitly
   or mark the old dispatch dead before re-dispatch.

Repositories and Beads may use remotes for coordination, but sync/push rules
remain subordinate to the active repo and user instructions. Multi-host
capability never grants permission to push, deploy, or configure services.

## Review independence

Review independence is a fresh, read-only agent context, not another person
or necessarily another host. The reviewer receives only the deterministic
packet and may run on the same device, provider, subscription, and model as
the implementer. It must not receive the implementer conversation, reuse its
session, edit the tree, or review an unpinned head.

Running the reviewer on a different host is useful when it proves the packet
and verification evidence are portable, but it is an optional capability
check rather than a governance requirement.

## Failover

When a host fails:

1. Inspect the Bead, branch/PR, logs, and remote state from a healthy host.
2. Mark the old lane stopped and release only leases proven unused.
3. Recreate the worktree from the recorded branch; never copy an untracked
   working directory between hosts as the recovery mechanism.
4. Append the failure evidence to the existing goal and re-dispatch.
5. If the coordinator host failed, the operator records a coordinator lease
   transfer before launching the replacement.

## Failure modes

- **Two active coordinators:** both claim or merge from the same queue. Stop
  one; reconcile Beads and branch state before continuing.
- **Host config committed:** absolute paths or local capability assumptions
  leak into the repo. Remove them and keep only portable requirements.
- **Stale claims:** a dead lane still owns work. Audit claims against pid/log,
  branch, and PR evidence at every resume.
- **Shared resource collisions:** host-local port or database leases are
  assumed globally unique. Namespace leases with `hostId` or allocate them
  from the active coordinator.
- **Host equals authority:** a VPS silently promotes because it is always on.
  Availability does not grant decision rights; operator approval boundaries
  remain unchanged.
