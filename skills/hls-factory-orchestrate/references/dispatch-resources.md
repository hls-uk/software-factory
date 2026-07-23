# Dispatch Resources — leases and parallel verification

Occurrence-driven resource procedures split out of
[parallel-dispatch.md](parallel-dispatch.md). Read this file when dispatching
a story and again before verify/merge.

## Resource leases

Grant leases at dispatch, record them in the story Bead and
`.worktrees/<slug>/.env.story`, inject them into the goal, and drop them at
retirement:

- **Ports:** allocate a non-overlapping host-namespaced block and pass
  `PORT`/`PORT_BASE`; verification must read the environment rather than
  hard-code a port.
- **Datastore/service state:** give each story its own namespace or disposable
  instance according to the repo's architecture. Reset only that leased state.
- **Idempotency:** every verification command is safe to rerun and touches
  only the story's leased resources.
- **Migration versions:** prefer coordination-free timestamp versions where
  the migration tool orders them safely. If a repo retains small integer
  versions, allocate ranges through the active coordinator and state the
  naming rule in the goal. A lease made independently on another host is not
  globally safe.

Namespace host-local resources with `hostId`, but remember that hosts are
capacity/failure domains for one operator, not ownership or authority
boundaries.

## Verify scope under parallelism

- **In the worktree:** run the story's exact commands and affected tests.
- **On the integration branch after merge:** run the required combined-tree
  gate. A failure is P0; stop new dispatch and revert or fix forward according
  to the repo's authority policy.
- **Before the second concurrent story merges:** rebase it onto the current
  integration branch and rerun its gate against the combined tree. Clean
  auto-merges can still create an unverified interaction.

Partition correctness interference (ports, datastores, migration names), but
serialize capacity-heavy gates until measurements prove concurrency safe.
Run at most one full-suite gate at a time by default. When a gate OOMs:

1. reproduce it serially before blaming parallelism;
2. inspect build-tool/forked-test heap limits;
3. preserve the story diff and apply a repo-approved non-invasive runtime
   adjustment where possible;
4. record a permanent build change as separate Beads work if it is outside
   the story scope.

An OOM after story tests passed is a verification bounce, not evidence that
the implementation is wrong. Release resources, retain the worktree, and
regate with the proven host fix.
