# KOMPASS | Decision Intelligence Studio

An original, interactive portfolio demonstration for the **Analyst in Governance and Product Management for Decision Support** vacancy at Försäkringskassan (FK 2026/034047). **Not affiliated with or endorsed by Försäkringskassan.** Every request, metric, organization and scenario is fictional. No citizen data is used.

## Experience

Seven connected workspaces: mission control, business demand intake, requirements discovery, prioritization simulator, data-product contracts, evidence quality and executive decision briefing. Create requests, edit constraints, record acceptance criteria and export reproducible artifacts.

## Launch

Double-click `index.html`. The full eight-request dataset is embedded in `data/seed.js`, so the app works completely offline without installation. Browser changes are stored in localStorage. Reset restores the original fictional scenario.

## Technical structure

- `index.html`: accessible semantic application shell
- `assets/style.css`: responsive visual design
- `assets/app.js`: state, interactions, exports, local persistence
- `assets/engine.js`: reusable deterministic scoring, governance, dependency-aware sequencing, data quality and safe CSV engine
- `data/seed.js`: offline-ready eight-request dataset and nine aggregate observations
- `data/requests.json`: eight synthetic product requests
- `data/observations.json`: nine synthetic aggregate records
- `tests/engine.test.js`: ten Node built-in test cases
- `docs/DECISION_MODEL.md`: scoring, limitations, assumptions and traceability
- `docs/DEMO_SCRIPT.md`: guided hiring-manager demo

## Test

`node --test tests/engine.test.js`

## What this is not

Not a government system, a production BI stack, a legal assessment, an AI prediction model or an optimized portfolio solver. Risk scores are simple user-adjustable heuristics, not approved agency policy. Privacy sensitivity 8+ always triggers a review hold; low quality blocks scheduling. Human review remains mandatory. There is no backend authentication, real data ingestion, external integration or secure storage. Never enter personal, protected or confidential information.
