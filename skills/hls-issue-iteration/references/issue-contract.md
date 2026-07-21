# Issue Iteration Contract

Use the existing GitHub Issue rather than creating a duplicate. Add missing
fields to its body or a comment when remote-write authority exists; otherwise
prepare the update for the operator. Keep secret values and personal data out.

```markdown
## Observed problem

- **Expected:** <user-visible behaviour>
- **Actual:** <user-visible behaviour>
- **Impact / users:** <who is affected and how>
- **Environment / release head:** <non-secret context and exact ref>

## Reproduction

1. <smallest reliable step>
2. ...

Evidence: <redacted screenshot, log, or failing check>

## Delivery decision

- **Severity:** P0 | P1 | P2 | P3
- **Release milestone:** experiment | beta | operational | canonical
- **Risk review:** routine | mandatory — <trigger or reason no trigger applies>
- **Desired outcome:** <observable user result>
- **Scope / preserve:** <bounded surface and authority that must remain intact>
- **Verification:** <exact regression and user-journey checks>
- **Execution Bead:** <id when selected for multi-session work; otherwise none>
```

## Bead pointer

Create a Bead only for selected execution work when the repo's rules or the
multi-session/dependency shape require it. One Bead may represent a small
same-risk batch.

```text
Title: Iterate <issue number(s)>: <bounded outcome>
Description: Human-facing source: <issue URL(s)>. Outcome and verification are
defined there. Covers current release milestone <stage>.
External reference: <primary issue URL>
Acceptance: focused regression + affected user journey; apply delivery
contract and mandatory review triggers.
```

## Completion evidence

Before closing the human-facing issue, record:

- exact fixed/released head or PR;
- focused and affected verification results;
- full-suite and user-journey result when required by the slice/profile;
- independent review evidence when a trigger applied;
- linked known P2/P3 follow-ups;
- reproduction and verified-fix timestamps; and
- any assurance/release-stage transition or recovery action.
