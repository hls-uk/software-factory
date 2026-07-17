---
name: hls-skill-feedback
description: File structured improvement feedback against the skills repo when an installed skill misfires — wrong instructions, outdated APIs, gaps, or friction. Use whenever a skill's guidance was incorrect or incomplete during real work, when you had to work around a skill, or when you notice a missing skill a project keeps needing.
---

# Skill Feedback

Skills compound only if the projects using them feed corrections back. When a
skill steers you wrong — an instruction that doesn't work, an API that changed,
a gap you had to fill by hand — file it. A workaround that lives only in your
session is lost; a filed issue fixes it for every project.

## When to File

- A skill's instruction is wrong or outdated (command fails, API changed).
- A skill is silent on a case it clearly should cover.
- You had to deviate from a skill to succeed — the deviation is the feedback.
- A pattern keeps recurring across work that no installed skill covers.

File at the moment it happens, not at session end. One issue per problem.

## Where to File

Look for the host repo's feedback configuration at `.factory/feedback.json`:

```json
{
  "tracker": "jira",
  "baseUrl": "<JIRA_BASE_URL>",
  "project": "<PROJECT_KEY>",
  "labels": ["skill-feedback"]
}
```

or

```json
{
  "tracker": "github",
  "repo": "<owner>/<skills-repo>",
  "labels": ["skill-feedback"]
}
```

- **Jira:** use the environment's configured Jira access (MCP tool or CLI).
  Never invent or hard-code credentials; if access isn't configured, say so
  and fall back to recording the feedback in the host repo (below).
- **GitHub:** `gh issue create --repo <repo> --label skill-feedback ...`
- **No config or no access:** append the feedback to
  `docs/skill-feedback-outbox.md` in the host repo so a later session (or a
  human) can file it. Note this in your session summary.

## What to File

Use [references/feedback-template.md](references/feedback-template.md). The
non-negotiables:

- **Skill + version:** skill name and the installed source commit — read it
  from the repo's install record (`.factory/skills-lock.json`, maintained by
  the hls-skill-update skill); if the repo has no record yet, say so in the
  issue and note the install date.
- **What happened vs. expected:** the exact instruction followed, the exact
  failure (trimmed command output beats prose).
- **Minimal repro:** enough for a maintainer in a clean repo to see it.
- **Suggested fix:** the wording or command change you believe is right — you
  just did the debugging; don't discard it.
- **Severity:** `broken` (skill misleads), `gap` (skill silent), `friction`
  (works but costs time), `idea` (new skill).

## Local Stopgap

If the defect blocks current work, you may patch the *installed copy* in the
host repo — but record the divergence in the filed issue, in the host repo's
log, **and in the `divergences` list of `.factory/skills-lock.json`** (the
hls-skill-update skill's install record) — that register is what lets the
next uptake drop your fork the moment upstream supersedes it. Never let a
silent local fork become permanent.

## The Cascade

This pattern is not exclusive to the central skills repo. A project
maintaining its own internal skills can point its own `.factory/feedback.json`
at its own tracker and run hls-skill-sweep against it — the loop is the same at
every level.
