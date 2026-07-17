# Factory Status Report Template

```markdown
# Factory status — <timestamp> (<window>)

Repos: `<repo-a>@<sha>` · `<repo-b>@<sha>`
Coordinator: `<host-id>` lease `<expiry or none>`

<One evidence-based sentence. Put the most important operator action here.>

## Delta since last check

- 🟢 <landed or turned green>
- 🟡 <started or materially changed>
- 🔴 <newly blocked or stalled>

## Hosts and lanes

| Host | Lane / role | Preflight | Current claim | Latest activity |
|---|---|---:|---|---|
| `laptop-a` | `local-1` implement | 🟢 | `<bead-id>` | `<PR/commit/claim> · <age>` |
| `vps-a` | `review-1` review | 🟢 | none | idle · `<age>` |

## Needs the operator

1. ⚠️ **<decision/action>** — blocks `<ids/gate>`; done when `<evidence>`.

## Gates

| Gate | State | Turns green / evidence |
|---|---:|---|
| `<gate>` | 🟡 | `<exact merged evidence or remaining condition>` |

## In flight

| Repo | PR/branch | State | Head | Age |
|---|---|---:|---|---:|

## Landed

- 🟢 `<repo>#<pr>` — <stated consequence> (`<merge-sha>`, <age>)

## Queue health

| Repo | Ready | In progress | Blocked | Standing backlog |
|---|---:|---:|---:|---:|

---
Scope: `<repos>` · Sources: `<tracker, Git, PR, registry, plan, log>` ·
Freshness: `<per-source result>` · This report observes; it is not gate evidence.
```

Omit no section. Replace example rows with live evidence or `none`.
