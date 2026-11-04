# Workflow and control notes

## Accounts receivable versus payable
The job title says accounts payable but the detailed duties and mandatory experience specify accounts receivable. CLEARSET focuses on the latter. Supplier invoices are accounts payable and are deliberately not treated as customer receivables.

## Investigation procedure
1. Confirm customer identity and bank payment amount.
2. Check invoice reference and open balance.
3. Investigate short payments, deductions and missing references.
4. Apply only the supported amount to the correct customer.
5. Record the investigation, supporting evidence and next action.
6. Prepare a handover with unresolved issues.

## Controls
- No cross-customer payment allocation.
- No allocation greater than payment remaining or invoice balance.
- Partial allocations supported.
- Credits require a reason and cannot exceed invoice balance.
- Outstanding = original invoice amount minus allocations and credits.
- Aging is based on fixed demo date 2026-11-04.
- Journal is a local demonstration history, not an immutable audit system.

## Boundaries
No real Business Central, Rillion, banking, customer email or payment functionality. All customer data and financial amounts are synthetic. Browser localStorage is used for demo state and is not appropriate for production accounting.
