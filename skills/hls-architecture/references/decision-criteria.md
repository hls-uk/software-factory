# Architecture Decision Criteria

Derive weights from the confirmed requirements; do not import a preferred
stack. For each significant choice, record which criteria apply and how the
candidates compare.

Common criteria to consider:

- requirement and acceptance-criterion fit;
- reversibility and migration cost;
- local/offline verifiability and feedback-loop speed;
- operational burden for the actual operator and available hosts;
- security, privacy, compliance, and audit needs;
- compatibility with existing systems and skills;
- evidence of maturity, support horizon, and failure behaviour;
- total cost, including maintenance and exit cost;
- performance or scale only where a quantified requirement creates it;
- observability, backup, recovery, and incident ergonomics.

Use a compact table:

| Criterion | Weight / constraint | Candidate A | Candidate B | Evidence |
|---|---|---|---|---|
| Local verification | MUST | pass | partial | commands/prototype |

A MUST failure eliminates a candidate. Weighted preferences help compare the
remaining options but never override a hard requirement. Record uncertainty
and a revisit trigger instead of manufacturing precision.

Prefer the smallest decision that meets the evidence. Avoid speculative
scaling machinery, but do not label any particular technology as the default:
the requirements, existing estate, and operator constraints decide.
