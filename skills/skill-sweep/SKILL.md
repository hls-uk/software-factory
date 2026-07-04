---
name: skill-sweep
description: Sweep the feedback tracker for skill-feedback issues, triage them, apply the fixes to the skills in this repo, validate, and release — closing each issue with evidence. Use on a maintenance cadence (weekly) or on demand in a repo that maintains skills, whether the central skills repo or a project's internal one.
---

# Skill Sweep

The consuming half of the feedback loop: skill-feedback files defects from the
field; this skill turns them into released fixes. Run it in the repo that owns
the skills.

## Process

1. **Collect.** Query the tracker configured in `.factory/feedback.json` for
   open `skill-feedback` issues (Jira via the configured access, or
   `gh issue list --label skill-feedback --state open`). Also check
   `docs/skill-feedback-outbox.md` files surfaced from projects without
   tracker access, and this repo's own outbox.

2. **Triage each issue** before touching any skill:
   - **Valid:** the skill is wrong, gapped, or high-friction → fix queue.
   - **Duplicate:** link to the original, close with a pointer.
   - **Project-specific:** correct behavior, wrong context — the host repo
     should carry a local convention instead; close explaining why, kindly.
     A rejection with reasoning prevents re-litigating; record it.
   - **Idea (new skill):** park in the backlog unless it recurs from multiple
     projects — recurrence is the signal it's generic.
   Track the fix queue in beads (`bd create` per accepted fix) when the sweep
   is more than a couple of items.

3. **Apply fixes.** Edit the skill's SKILL.md / references. Honor the
   reporter's suggested fix when sound — they did the debugging. For `broken`
   reports quoting command output, reproduce first when cheap; a fix you
   haven't seen fail and then pass is a guess.

4. **Validate.** Run the repo's skill validator (here:
   `node scripts/validate-skills.mjs`). Re-read each changed skill start to
   finish — a patched paragraph that contradicts a later section ships
   confusion to every consumer.

5. **Release.** Update `CHANGELOG.md` (one line per fix, linking the issue),
   commit, push per the repo's process. Consumers pick up fixes on their next
   `npx skills add` install/update.

6. **Close with evidence.** Close each issue naming the commit, the change
   made, and how it was validated. If the reporter recorded a local stopgap,
   note that the upstream fix supersedes it so their next sweep/update can
   drop the fork.

## Quality Bar

- Every open feedback issue leaves the sweep in a terminal state: fixed,
  duplicate-closed, rejected-with-reasoning, or explicitly parked with a
  reason. A silently ignored report kills the loop — contributors stop filing.
- Fixes are minimal and targeted. A sweep is not a rewrite; wholesale skill
  revisions get their own reviewed change.
- Recurring `friction` reports on the same skill are a design smell — consider
  restructuring (or splitting) the skill rather than patching wording again.

## The Cascade

Any repo that maintains internal skills can run this loop: point its
`.factory/feedback.json` at its own tracker, let its projects file with
skill-feedback, and sweep on a cadence. Improvements that prove generic can
then be re-filed upstream to the central skills repo — the same loop, one
level up.
