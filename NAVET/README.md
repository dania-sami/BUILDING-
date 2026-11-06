# NAVET | AI & Data Operations Studio

An interactive, local-first portfolio prototype inspired by the **Junior Business Developer, AI and Data** vacancy at Försäkringskassan (FK 2026/033639). **Independent demonstration; not affiliated with or endorsed by the agency.**

## Launch in one click

Extract the folder and open `index.html` in a modern browser. No build process, backend, sign-in, or installation required. Google Fonts is optional; system fonts are used when offline.

## What works

- Command center with live metrics, risk flags, progress and follow-ups
- Initiative portfolio with create/edit/delete, search, ownership, due dates and progress
- Action tracker for meeting follow-up
- Decision register with rationale, owner and status
- Workshop planner with desired outcomes and facilitators
- Improvement lab with explicit impact, effort and confidence scoring
- Auto-generated leadership briefing downloadable as TXT
- CSV export per workspace and JSON export for the entire dataset
- Local change history and demo reset
- Responsive desktop and mobile layout
- Data persisted in browser localStorage; no external data collection

## Architecture

`index.html` loads `data/seed.js`, `assets/engine.js` (pure data helpers) and `assets/app.js` (rendering and interactions). `assets/style.css` defines the visual system. The app deliberately avoids dependencies and uses synthetic data only.

## Tests

Run `node --test tests/engine.test.js` from the project root. JavaScript source syntax can be checked with `node --check assets/app.js`.

## Important limitations

This is a **portfolio simulation**, not a deployable public-sector system. It does not provide real authentication, authorization, protected information handling, GDPR compliance, immutable audit logs, secure retention, archival/diary registration, invoice approval, AI model governance, or integration with Försäkringskassan systems. LocalStorage can be inspected and edited by anyone with browser access. No real personal data should be entered. The improvement scoring is an illustrative prioritization aid, not a formal policy or automated decision.

## How it maps to the vacancy

| Vacancy duty | Demonstration |
| --- | --- |
| Support management and business planning | Command center, initiative ownership and briefing |
| Prepare meetings and follow-up | Decision register and action tracker |
| Plan workshops and presentations | Workshop planner and downloadable briefing |
| Administrative coordination | Work items with owners, due dates and statuses |
| Improvement initiatives | Transparent improvement prioritization |
| Statistical follow-up | Portfolio metrics and progress reporting |
| High security awareness | Synthetic data, clear restrictions and governance notes |

## Interview demo (3 minutes)

1. Open the command center and point out an at-risk initiative.
2. Edit its status or progress; the metrics update immediately.
3. Add a follow-up action and a pending decision.
4. Generate a leadership briefing and download it.
5. Open governance to explain why a real deployment would need approved identity, records management, and security controls.

All names and scenarios are invented. Built to demonstrate initiative, coordination, systems thinking and practical delivery.
