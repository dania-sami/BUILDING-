# SUPPLIER//SCOPE

**See the risk. Trace the evidence. Make the decision.**

An independent supplier intelligence and risk workflow concept built by Dania to demonstrate practical fit for NCC's Supplier Data Analyst role. This is not an NCC product, endorsement, integration, or assessment.

## Launch in one click
Open `index.html` in a modern browser. No dependencies, Docker, API keys or server.

## Explore
- Command center with Nordic supplier performance overview
- Searchable, filterable supplier portfolio with CSV export
- Supplier investigation room with checklists and locally saved notes
- Interactive mitigation scenario with transparent, illustrative calculations
- Data quality and governance register distinguishing checked structures from unverified evidence
- Copyable and downloadable purchasing decision brief
- 30-day implementation and stakeholder discovery plan
- Dark and light themes, responsive layout

## Data and assumptions
All 24 suppliers, spend figures, scores, deviations and dates are synthetic. Risk index is an illustrative weighted screening formula: `(100-quality)*0.22 + (100-delivery)*0.20 + (100-esg)*0.16 + (100-compliance)*0.30 + deviations*2.4`. This index is not validated for purchasing decisions. The scenario lab models assumed improvements to that index and a fictional effort cost.

This prototype does not verify sanctions, taxes, labor law, construction regulations, supplier contracts, or environmental compliance. These require authoritative sources, legal specialists and human review.

## Project files
- `index.html` application shell
- `assets/styles.css` responsive interface
- `assets/app.js` state, interactions and exports
- `assets/data.js` embedded fictional data for offline launch
- `assets/suppliers.json` reusable structured sample data
- `docs/ANALYST_PLAYBOOK.md` operational method and pilot KPIs

## Suggested demo path
Command center → Supplier portfolio → Investigation room → Decision simulator → Decision brief → Data trust.

## Future implementation
Connect approved ERP/procurement sources, master supplier IDs, Power BI semantic model, access control, case management, evidence provenance, audit logs and validated legal/compliance checks.
