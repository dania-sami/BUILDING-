# Data dictionary and research protocol

## Research question
How are perceived safety ratings associated with lighting, activity, maintenance, time of day and neighborhood in a simulated urban survey?

## Fields
| Field | Type | Meaning |
|---|---|---|
| response_id | string | Synthetic record identifier |
| area | category | Fictional neighborhood grouping based on real Stockholm-area names |
| lat, lon | decimal | Synthetic WGS84 coordinates |
| time | category | day or evening |
| lighting | integer 1–5 | Perceived lighting |
| activity | integer 1–5 | Perceived street activity |
| maintenance | integer 1–5 | Perceived maintenance |
| safety | integer 1–5 | Perceived safety |
| gender_group | category | Simulated demographic grouping; excluded from browser survey |

## Workflow
1. Draft bilingual survey questions with consistent anchors and pilot test translations.
2. Secure appropriate approvals, recruitment procedures and information/consent notices before real distribution.
3. Validate ranges, missingness, duplicate IDs and geospatial consistency.
4. Aggregate and analyze with Python and R; avoid publishing precise participant locations.
5. Report uncertainty, sample limitations, sensitivity analysis and non-causal interpretation.

## Data protection
Never treat localStorage as secure storage for confidential or sensitive research data. This prototype is for synthetic and demonstration responses only. No network submission is implemented.
