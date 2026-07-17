---
name: hls-factory-status
description: Render a live, read-only factory progress report for one operator across one or more repositories and laptop/VPS hosts — what landed, what is in flight, which lanes are active or silent, what is blocked, and what needs the operator. Use when asked for factory status, movement since the last check, queue health, host/lane activity, or blockers.
---

# Factory Status

Observe; never operate. Produce the same compact report shape every time so
two runs can be compared directly. Every row must trace to evidence read in
this run.

## Read-only contract

- Allowed: read repo files and Git state; read tracker/PR APIs; `git fetch`
  and documented tracker pull only when the active instructions allow local
  refresh; write only a gitignored local status snapshot.
- Never: claim/create/close/edit work, push, comment, merge, advance a gate,
  switch the user's checkout, start/stop lanes, or transfer coordinator
  authority.
- Report a gate exactly as its registry/evidence records it. A green local
  test, open PR, or agent claim is not a promotion.

If a source cannot be refreshed, use the current local state, label its age,
and never imply it is live.

## Discover scope

Prefer `.factory/programme.json` in the control repo:

```json
{
  "controlRepo": ".",
  "deliveryRepos": [
    {"name": "app", "path": "../app", "trackerPrefix": "app"}
  ],
  "operator": "<operator>",
  "activeCoordinator": {"hostId": "laptop-a", "leaseUntil": "<ISO-8601>"},
  "plannedLanes": [
    {"hostId": "laptop-a", "lane": "local-1", "roles": ["implement", "review"], "preflight": "pass"}
  ]
}
```

The file maps capacity and authority state, never human ownership. If it is
absent, report the current repo plus sibling delivery repos explicitly named
by its orientation docs, and state the inferred scope in the footer.

Also read the programme/status registry when present, the active plan current-
state block and criteria coverage, and the newest append-only log entries.

## Refresh and gather

For each delivery repo:

1. Record fetch/tracker-sync success or the freshness limitation.
2. Read current integration-branch SHA.
3. Query tracker in-progress, blocked, human/operator-gated, and ready items.
4. Query open PRs and window-bounded merged PRs.
5. Read remote branch tips moved inside the window.
6. Reconcile claimed lane ids/host ids with programme config and preflight.

Run repository-sensitive commands inside the per-repo subshell. In
particular, resolve and query the GitHub repository after changing directory;
otherwise every row silently reports the coordinator repo:

```sh
for repo in $REPO_PATHS; do
  git -C "$repo" fetch origin --quiet
  (cd "$repo" || exit
   bd dolt pull >/dev/null 2>&1
   bd list --status=in_progress --json
   bd blocked --json
   bd ready --json
   gh pr list -R "$(gh repo view --json nameWithOwner -q .nameWithOwner)" \
     --state open --json number,title,author,isDraft,updatedAt)
  git -C "$repo" for-each-ref --sort=-committerdate refs/remotes/origin \
    --format='%(committerdate:relative)|%(authorname)|%(refname:short)|%(subject)'
done
```

Default comparison window: 24 hours. Honour an explicit requester window.

## Fixed report

Use [references/report-template.md](references/report-template.md) and emit
all sections; write `none` for an empty section and state why for an unread
source.

1. **Headline** — timestamp, window, repo SHAs, one-sentence state, active
   coordinator host and lease expiry.
2. **Delta since last check** — landed, state changes, new/stalled work.
3. **Hosts and lanes** — every configured host/lane, role, preflight,
   current claim, newest activity and age; silent capacity is a finding.
4. **Needs the operator** — explicit decisions/actions, impact, and the
   evidence that will unblock each item.
5. **Gates** — stable gate, recorded state, exact evidence needed for green.
6. **In flight** — open PRs and recent PR-less branches.
7. **Landed** — window-bounded merges with stated consequence.
8. **Queue health** — ready/in-progress/blocked counts and standing backlog
   thresholds per repo.
9. **Footer** — scope, sources, freshness, window, and observation caveat.

Glyphs: `🟢` evidenced green, `🟡` in progress/provisional, `🔴` blocked,
`⚪` waiting/not started, `⚠️` operator action required.

Keep the report to roughly one screen per three lanes. Prefer exact ids, SHAs,
ages, and evidence paths over narrative.

## Delta snapshot

After composing, write only machine facts needed for the next delta: report
time, repo SHAs, tracker id/status/assignee/host/lane, open PR/head, and gate
states. Preferred path is `.factory/status-snapshot.local.json` when that
pattern is already gitignored; otherwise use session scratch. Never commit it.

## Cadence and failure modes

The skill is single-shot and can be scheduled. When nothing changed, emit one
line with the checked sources and last-movement time.

- Reporting remembered conversation state instead of rereading sources.
- Treating a quiet host as available without checking preflight or stale
  claims.
- Reporting two active coordinators without flagging split-brain risk.
- Burying the operator action below activity detail.
- Running `gh repo view` from the control repo for every delivery repo.
- Mutating delivery state from an observer run.
