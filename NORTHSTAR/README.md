# NORTHSTAR

I built NORTHSTAR to explore how complex engineering work stays traceable from the first requirement to the final technical review.

It uses a fictional civilian harbor monitoring system to connect requirements, components, interfaces, verification and risks. Change a requirement and the app shows what needs another look.

## Run

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000

Run tests with `python -m pytest -q`.

All data is synthetic. No defense or operational systems are represented.

Dania Sami
