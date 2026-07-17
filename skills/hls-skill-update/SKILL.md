---
name: hls-skill-update
description: Keep a consumer repo's installed factory skills current — record the installed source commit in a committed lock file, check against upstream, uptake updates by re-installing, reconcile local stopgap patches (drop forks superseded upstream, re-apply and re-register the rest), and log the uptake. Use at install time to create the record, on a maintenance cadence (weekly, or at run boundaries) to check and uptake, or whenever asked to update the skills.
---

# Skill Update

The uptake half of the evolution loop: hls-skill-feedback files defects from
the field, hls-skill-sweep releases fixes upstream — this skill brings those
fixes back into the consumer repo. Run it in the repo that *installed* the
skills.

Why this exists: `npx skills add` installs project-level skills with **no
per-repo tracking** — the skills CLI's lock file (`~/.agents/.skill-lock.json`)
is per-machine and only written for global (`-g`) installs, so `npx skills
check`/`update` cannot see project installs (verified against skills CLI
v1.3.7). A record that lives in one laptop's home directory is lost when the
operator moves to another host; the repo carries its own.

## The Install Record — `.factory/skills-lock.json`

Committed to the consumer repo. Created at first install, refreshed by every
uptake:

```json
{
  "sources": {
    "hls-uk/software-factory": {
      "url": "https://github.com/hls-uk/software-factory",
      "commit": "<source repo HEAD sha at install/update>",
      "installedAt": "2026-07-11T09:00:00Z",
      "updatedAt": "2026-07-11T09:00:00Z",
      "skills": ["hls-beads", "hls-factory-orchestrate"],
      "divergences": [
        {
          "skill": "hls-publish-report",
          "reason": "pinned md-to-pdf version — upstream cmd fails on this repo",
          "issue": "<tracker ref from hls-skill-feedback>",
          "since": "2026-07-11"
        }
      ]
    }
  }
}
```

- `commit` comes from `git ls-remote <url> HEAD | cut -f1` — no clone needed.
- `skills` lists what this repo actually installed (updates re-install
  exactly this set, not `'*'`).
- `divergences` is the local-stopgap register: every locally patched
  installed skill (the hls-skill-feedback Local Stopgap rule) is listed here
  with its filed issue. This is what makes reconciliation mechanical instead
  of archaeological.
- One entry per source repo — a repo consuming skills from two sources has
  two entries.

**At install time** (first install, or adding skills later): after
`npx skills add <source> --skill <names>`, create or refresh this file and
commit it with the installed skills. A feedback report's "skill + version"
field reads the `commit` from here.

## When Updating Is Unsafe

- **Never mid-orchestration-run.** If the repo has in-flight story worktrees
  (`git worktree list`) or an active coordinator, skills changing underneath
  a run means the process changes mid-story — wait for a run boundary
  (before a wave is cut, or after a promotion).
- **Multiple hosts:** installed skills are shared surface. Acquire one update
  lease in Beads and run the uptake on one host; other hosts refresh only
  after that uptake is accepted. Never let laptops update independently.
- A dirty working tree: stop and get it clean under the repo's active policy.
  Do not infer permission to commit or stash. The uptake diff must stand alone
  or it is unreviewable.

## The Uptake Ritual

1. **Check.** `git ls-remote <url> HEAD` vs the lock's `commit`. Equal →
   up to date; log the check if anyone asked for it, done. Not equal →
   continue.

2. **Read the delta before taking it.** Fetch the source repo's
   `CHANGELOG.md` at the new HEAD and read the entries since the recorded
   commit's version. Use the same git credentials the install used —
   private sources make anonymous raw URLs 404:

   ```sh
   git init -q /tmp/uptake-peek
   git -C /tmp/uptake-peek fetch -q --depth 1 <url> <new-head-sha>
   git -C /tmp/uptake-peek show FETCH_HEAD:CHANGELOG.md
   ```

   (`gh api repos/<source>/contents/CHANGELOG.md --jq .content | base64 -d`
   also works where gh is authenticated.) You are about to change the
   repo's process — know what's coming. In supervised mode, surface
   process-changing entries (new gates, changed loop shape) to the human
   before proceeding; mechanical fixes need no ceremony.

3. **Re-install.** `npx skills add <source> --skill <name> -y` for each
   skill in the lock's `skills` list. This overwrites the installed copies
   with upstream HEAD — including reverting any local stopgap patches, which
   is exactly what makes the next step honest.

4. **Reconcile divergences.** `git diff` now shows upstream's changes *and*
   every stopgap being reverted. For each entry in `divergences`:
   - **Superseded** — the filed issue is closed with an upstream fix (the
     sweep's close note says so), or the diff shows upstream now handles it:
     let the overwrite stand, remove the entry. The fork is retired.
   - **Still needed** — upstream hasn't addressed it: re-apply the patch,
     keep the entry, and nudge the filed issue (it has been outlived by a
     release). A divergence surviving two uptakes without upstream movement
     is worth escalating in the issue.
   A diff touching a skill *not* in `divergences` that you can't attribute
   to upstream means someone forked silently — register it now, file the
   missing feedback, then decide.

5. **Refresh the lock.** New `commit`, new `updatedAt`; divergences as
   reconciled.

6. **Validate.** Re-read each changed skill's diff — you are accepting new
   instructions into the repo's process. If the repo maintains its own
   internal skills with a validator, run it. If the changelog delta named
   changed verification behavior, run the repo's gates once.

7. **Log and prepare the change.** One log entry (repo wiki/log): old commit
   → new commit, skills changed, divergences dropped/kept. Keep the installed
   skills, lock, and log as one reviewable change. Commit/push only when the
   active repo policy or user grants that authority.

## Quality Bar

- The uptake is one reviewable commit; a reviewer sees exactly what upstream
  changed and which forks were dropped or kept, from the diff alone.
- No silent forks survive: every local difference from upstream is either
  reverted or registered in `divergences` with a filed issue.
- The lock never lies: after any install, add, or uptake, `commit` matches
  what the installed copies actually came from.

## The Cascade

Like the rest of the evolution loop, this works at every level: a repo
consuming any internal skills source records it in the same lock file and
runs the same ritual against it.
