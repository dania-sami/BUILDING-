# VANTAGE | Private Equity Decision Studio

I built VANTAGE as an independent project to explore the work of an Investment Controller: portfolio performance, valuation judgment, reporting quality, ESG completeness and clear investment decisions.

## Launch

Double-click `index.html`. Everything works offline using a bundled fictional dataset. For local development, `python -m http.server 8000` and open http://localhost:8000.

## Seven workspaces

- Portfolio cockpit: portfolio KPI aggregation and quarterly revenue profile.
- Challenge room: company-specific exception detection, analyst evidence requests and saved decisions.
- Valuation lab: interactive EBITDA, exit multiple and debt scenarios with a sensitivity matrix.
- Investor reporting: editable narrative, company review statuses, TXT and CSV exports.
- ESG and risk: score and reporting completeness analysis.
- Data quality: deterministic exception checks and exportable exception register.
- Operating playbook: end-to-end investment controller workflow.

## Structure

- `index.html`: application shell.
- `assets/styles.css`: responsive design.
- `assets/engine.js`: financial calculations and control rules.
- `assets/app.js`: interactive screens, reports and local decision records.
- `assets/offline-data.js`: bundled dataset for opening the app directly.
- `data/portfolio.json`: editable synthetic source dataset when served locally.
- `tests/test_engine.js`: automated financial logic tests.
- `docs/METHODOLOGY.md`: definitions, assumptions, limitations and controls.

## Verify

`node tests/test_engine.js` (requires Node.js only for tests, not for using the app).

## Important

All six companies and all figures are fictional. Simplified EV = EBITDA × EV/EBITDA multiple; equity value = EV − net debt. Aggregated equity values are **not** fund NAV. The app does not calculate IRR, MOIC, fund fees, carried interest or actual investor capital accounts. ESG indicators are fictional, not audited or regulatory. Analyst decisions are stored in browser localStorage. No external API, LLM, financial system or company information is accessed. Not affiliated with Norvestor.
