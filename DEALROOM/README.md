# DEALROOM

I built DEALROOM to explore how AI and automation can make M&A due diligence more efficient without losing the evidence behind important decisions.

It reviews a fictional company's financial data, flags discrepancies, links findings to sources, and supports human review. There's also a small prompt library and an automated workflow walkthrough.

Run with `pip install -r requirements.txt` and `uvicorn app.main:app --reload`, then open http://127.0.0.1:8000.

All company data is synthetic. The financial checks are deterministic; the prompts are reusable templates, not a live LLM integration.

Dania
