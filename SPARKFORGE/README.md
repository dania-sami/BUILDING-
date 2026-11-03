# SPARKFORGE

I built SPARKFORGE to explore a challenge I find exciting: helping teams turn AI curiosity into something useful, measurable and safe.

It brings together customer discovery, pilot economics, solution architecture, knowledge retrieval, evaluation, developer coaching and workshop planning in one working lab.

## Run

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000. Run tests with `python -m pytest -q`.

Everything uses fictional examples. Retrieval is deterministic and extractive, not a live LLM. The cost estimates are assumptions to challenge in a real pilot.

Dania
