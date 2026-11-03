# ARCHITECTIQ

I built ARCHITECTIQ to explore how an AI idea becomes a system a client can actually operate and trust.

The lab follows an enterprise knowledge assistant from architecture and evidence retrieval to evaluation, cost planning, and technical decisions. It uses synthetic company policies and records the work in SQLite.

## Run

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000. Run the tests with `python -m pytest -q`.

The retrieval engine is deliberately deterministic and extractive. There is no live LLM, real client data, or cloud deployment. The interface distinguishes what works today from what a production implementation would still need.

Built by Dania Sami.
