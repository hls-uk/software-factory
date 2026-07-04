# Skill Feedback Issue Template

Title: `[skill-feedback] <skill-name>: <one-line defect>`

```markdown
## Skill

- Name: <skill-name>
- Version/commit: <installed version, source commit, or install date>
- Host project: <repo name> (private details omitted)

## Severity

broken | gap | friction | idea

## What happened

Followed: "<the instruction, quoted from SKILL.md>"

Result:
```
<exact trimmed command output or observed behavior>
```

## Expected

<what the skill implied would happen>

## Minimal repro

<steps a maintainer can run in a clean repo>

## Suggested fix

<the wording/command/section change you believe is correct>

## Local stopgap applied?

yes — <what was patched in the host repo's installed copy> | no
```

Keep host-project confidential material out of issues — repro steps must not
leak proprietary code or data. Reduce to the smallest neutral example.
