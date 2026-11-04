# CLEARSET | Retail Finance Resolution Studio

I built CLEARSET for a Stockholm retail finance role because I wanted to demonstrate how I approach receivables work: checking the details, resolving payment exceptions carefully, communicating respectfully, and leaving a clean handover.

## Launch in one click
Open `index.html` in any modern browser. No install, server, API keys or login needed.

## Ten workspaces
Morning Command; Reconciliation Detective; Customer Ledger & Aging; Dispute Desk; Customer Communications; Handover & Audit Trail; Exception Case Lab; Customer 360; Period Close; Controls & Exports.

## What actually works
- Allocate bank receipts to same-customer invoices, including partial amounts; reject over-allocation.
- Post a **demo** credit adjustment with a mandatory reason.
- Recalculate balances, aged receivables, unapplied cash and control checks.
- Investigate exceptions with recorded evidence and next actions.
- Draft customer communications for human review, without sending them.
- Save a period-close checklist, audit journal and handover notes.
- Export CSV ledger, CSV audit journal, TXT handover and period-close memo.
- Reset all browser-saved demo changes.

## Testing
Run `node tests/engine.test.js` (Node.js required for tests only). See `docs/WORKFLOWS.md` and `docs/CASE_STUDY.md`.

## Boundaries
All data is fictional. This is a client-side workflow simulation, **not** a production accounting system. It does not integrate with Business Central, Rillion, banks, email, or real customer data. It does not prove prior professional experience with those products. Browser storage is not an immutable audit log.
