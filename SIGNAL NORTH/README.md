# SIGNAL//NORTH ✳

### See the signals. Connect the decisions. Move the business.

**An independent, browser-based Global Revenue Intelligence Studio** designed by Dania as a portfolio demonstration inspired by the work of global Sales and Marketing business analysts.

## Why I built this

I wanted to demonstrate how I think about business analysis beyond building charts: align definitions, find friction in the funnel, test assumptions, communicate uncertainty, and turn insights into practical decisions. The studio is tailored to the responsibilities of an internal business analyst supporting global sales and marketing teams.

## One-click launch

1. Download and extract the project.
2. Double-click `index.html`.
3. Explore the seven workspaces. No terminal, dependencies, or account required.

## Seven interactive workspaces

1. **Mission Control** — global commercial overview, revenue by region, investigation prompts.
2. **Market Intelligence** — filter markets, compare targets and export CSV.
3. **Funnel Diagnostics** — inspect lead → MQL → SQL → win conversion.
4. **Marketing Mix** — compare spend, leads, wins and directional efficiency.
5. **What If Lab** — adjustable assumptions, live modeled revenue, downloadable scenario JSON.
6. **Data Trust Center** — interactive quality and governance checklist, exportable as CSV.
7. **Executive Briefing** — customizable leadership brief, copy and text download.

The demo remembers your inputs in browser local storage. Reset returns everything to defaults. The entire experience works offline, apart from the optional Google Fonts request; local fonts are used automatically when offline.

## What is real and what is illustrative

- **Real:** functioning interface, filtering, calculations, scenario modeling, exports, checklist, briefing generation, local persistence.
- **Illustrative:** all market figures, pipeline stages, marketing performance, and recommendations based on those figures.
- **Not included:** access to Knowit systems, actual Knowit financials, production connectors, AI model APIs, live attribution, predictive forecasts.

This is an independent portfolio concept, not affiliated with or endorsed by Knowit. No actual employee or customer data is used.

## Analysis assumptions

The What If Lab multiplies baseline revenue by `(1 + lead growth) × (1 + relative win conversion change) × (1 + average deal value change)`. Marketing spend is displayed separately, not treated as a causal driver. The model ignores lag, sales capacity, correlated drivers, uncertainty and margins. It is for scenario conversations, not decision-grade forecasts.

## Project structure

```text
SIGNAL_NORTH_Studio/
├── index.html
├── assets/
│   ├── styles.css
│   └── app.js
├── data/
│   └── demo.json
├── docs/
│   ├── DISCOVERY_WORKSHOP.md
│   ├── METRIC_DICTIONARY.md
│   └── PILOT_PLAN.md
└── README.md
```

## How I would extend this with a real team

I would begin with stakeholder interviews and a shared KPI dictionary, then validate CRM and campaign data, build role-based dashboards, and measure a small pilot. Production deployment would need secure integration, access control, monitoring, data protection and governance.

**Created by Dania · 2026**
