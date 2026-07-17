# Schema Migrations Under Parallel Delivery

Applies to any single-sequence migration tool (Flyway `V<N>__`, Liquibase
ordered changelogs, Rails/Django timestamped migrations already sidestep
most of this).

## Version-namespace collision (two lanes, one sequence)

- **Symptom:** two concurrent stories both add `V19__*.sql`; the first
  merges clean, the second fails the repo's migration-order gate (or worse,
  merges and breaks migrate-on-boot).
- **Root cause:** "next free number" is a read-then-write race — every lane
  branched from the same base computes the same next number. The same
  applies across *branches*: an integration branch and `main` allocating
  independently collided on V19 in a live trial even though each was
  internally leased.
- **Fix (preferred): timestamp-based versions.** Name migrations
  `V<yyyyMMddHHmm>__desc.sql` (e.g. `V202607091027__add_profile.sql`).
  Flyway compares versions numerically, so timestamps are valid versions;
  two lanes collide only by writing a migration the same minute — append
  seconds or a lane digit if that's plausible. No allocation authority, no
  coordination, no gaps, works across branches and machines.
- **Fix (fallback): leased integer ranges.** Where a repo is committed to
  small integers, lease each story a range at dispatch (~5 numbers, stated
  in the goal, recorded in `.env.story`) — but leases only work within one
  allocation authority; reserve ranges in a shared plan doc when several
  branches or machines allocate. Expect gaps from unused lease numbers;
  Flyway doesn't care, but contiguity-checking gates and humans might.

## Coordinator notes

- **Out-of-order arrival is the timestamp trade-off.** Against a fresh
  database (typical test runs) ordering never bites. Against a *long-lived*
  database (staging/prod), a story branched earlier but merged later carries
  an older timestamp than one already applied — Flyway then skips-or-fails
  it unless `flyway.out-of-order=true`. Decide per repo: enable out-of-order
  on long-lived environments, or renumber the late migration at merge. Say
  which in the goal when it matters.
- **Repo gates may assume integers.** A `check-migration-versions` script
  that asserts contiguous small integers will reject timestamps — switching
  schemes is a small tracked-build/story change (update the gate + document
  the naming rule), not something the coordinator does mid-run. File it,
  don't hack it.
- Whatever the scheme, the story goal must state the naming rule explicitly
  ("timestamp-version your migrations as V<yyyyMMddHHmm>__desc") — an
  implementer left to guess will read the existing files and revert to
  next-free-integer.
