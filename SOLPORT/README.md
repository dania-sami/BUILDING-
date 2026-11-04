# SOLPORT | The CFO's Daily Desk

I built SOLPORT to show how I would approach the everyday finance responsibilities at a small property company: staying organized, following up carefully, documenting decisions, and making it easier for a CFO to see what needs attention.

The app uses a fictional property portfolio and synthetic invoices, rents, and bank entries. It supports invoice approval, rent follow-up notes, bank reconciliation references, a morning briefing, an activity journal, and a clearly labeled demo payment CSV preview.

## Run

```bash
pip install -r requirements.txt
uvicorn app:app --reload
```

Open http://127.0.0.1:8000

Run tests with `pytest -q`.

**Important:** No real banking, tenant communications, Fenix, or Pigello integrations. This is a workflow demonstration, not an accounting system or authorized payment mechanism. The app stores demo changes in `solport.db`.
