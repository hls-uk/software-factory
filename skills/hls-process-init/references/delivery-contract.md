# Delivery contract

Record one contract at the top level of `.factory/agents.json`:

| Field | Values | Safe default |
|---|---|---|
| `operatingMode` | `supervised`, `autonomous` | `supervised` |
| `modelRoutingProfile` | `quality`, `balanced`, `throughput` | `balanced` |
| `assuranceProfile` | `rapid`, `standard`, `assured` | `standard` |
| `releaseStage` | `experiment`, `beta`, `operational`, `canonical` | `operational` |

Consequence determines assurance, not appetite for speed. Only an explicit
valid `rapid` reduces review depth. Missing, misspelled, wrongly typed, or
unknown fields resolve to the safe defaults through the executable resolver
bundled with `hls-factory-orchestrate`; do not duplicate its logic.

For a rapid contract, `spotReviewRate` may be an integer from 3 through 10.
It means every Nth routine rapid story receives full independent review.
Missing, invalid, or out-of-range values mean full review for every story.
Mandatory-review stories and promotion review are never sampled.

`deliveryProfile` is a read alias for `modelRoutingProfile` during migration.
The explicit new field wins. New configurations write the four fields
separately.

The contract never grants external authority, lowers a failing gate, changes
the mandatory-review trigger list, or makes another host a decision-maker.
One operator retains sign-off and waiver authority across every host.
