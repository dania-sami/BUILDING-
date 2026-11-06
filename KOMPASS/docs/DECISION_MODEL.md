# Decision model and governance assumptions

The fictional score is `3*impact + 2*urgency + confidence + 2*reuse - 2*effort`, where each input is rated 1–10. Impact and reuse weights are adjustable. This is an **illustrative heuristic**, not an agency policy, decision rule or mathematically optimal portfolio solver.

## Planning

Requests are considered by descending score. Requests with privacy sensitivity >=8 are held for legal and security review. Requests below the adjustable data quality threshold are held for remediation. Dependencies must be selected before dependent products. The algorithm iterates until no more products can be scheduled and never exceeds capacity. Unscheduled requests are deferred with an explanation. The resulting sequence can change when capacity, data quality or scoring weights change.

## Why the gates matter

Business value never substitutes for a legal basis, data protection impact assessment where required, information classification, security controls, access review or human oversight. Even eligible products require formal approvals. No real social insurance cases or individual-level records appear in the demonstration.

## Traceability

Intake records preserve a problem, owner, KPI and estimated factors. Discovery notes preserve stakeholder, decision, acceptance criteria and definition of done. Product contracts show dependencies and governance status. Decision briefings capture the current assumptions, selected work, deferrals and holds. LocalStorage is not a tamper-proof audit trail.

## Data quality

The evidence workspace checks completeness and duplicate region-month keys over fictional aggregate observations. This is a small illustrative subset of a proper data-quality framework, not an actual agency statistic or certified data product.
