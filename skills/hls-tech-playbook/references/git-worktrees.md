# Git Worktrees (factory story isolation)

## Sandboxed lanes cannot commit from a worktree

- **Symptom:** a lane finishes engineering, verification is green, then
  `git add` fails with `…/.git/worktrees/<name>/index.lock: Operation not
  permitted` (or similar) as its very last step.
- **Root cause:** a worktree's `.git` is a *pointer file*; the real index,
  refs, and object store live in the main repository's common dir — outside
  the lane's workspace-write sandbox.
- **Fix:** grant the main repo's `.git` directory (the common dir) as a
  writable root in the lane's dispatch flags. Preflight with a no-op commit
  through the sandboxed lane, not just a build probe — this failure hides
  until the end of an otherwise perfect story.
- **Interim mitigation** (before the config fix): the coordinator, which is
  unsandboxed, commits the lane's verified diff verbatim on its behalf —
  acceptable once, but fix the sandbox rather than institutionalizing it.

## Lifecycle notes

- Worktrees share the object store — creation is cheap; disk cost is the
  checkout plus per-worktree build output and dependency installs.
- A branch checked out in any worktree can't be checked out elsewhere or
  deleted; retire with `git worktree remove` then `git branch -D`, and run
  `git worktree prune` after force-removals.
- Worktree-in-worktree is fine (all register against the main repo), but
  every nested checkout multiplies the paths that must be gitignored
  (`.worktrees/`) and cleaned at retirement — a worktree with no open story
  is an orphan.
- The coordinator's own checkout can itself be a worktree of the developer's
  clone; keep the developer's checkout untouched by doing all factory git
  operations (including `bd`, whose state may live at the main repo) from
  the coordinator's worktree.
