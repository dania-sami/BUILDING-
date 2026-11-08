# VEHICLE//GUARD LAB

A **working, local, full-stack automotive PSIRT training environment** built independently as a portfolio project inspired by Scania/TRATON's Vehicle CS IR Specialist vacancy. **Not affiliated with Scania or TRATON.** All cases and components are fictional and synthetic.

## Run (Python 3.10+; no pip installation)

From this folder:

```bash
python server.py
```

Then visit **http://127.0.0.1:8765** in a browser. On Windows, double-click `START_WINDOWS.bat`; on macOS/Linux run `bash START_MAC_LINUX.sh`.

The app uses the Python standard library for its HTTP server, SQLite persistence, SHA-256 event integrity and JSON API. The browser frontend uses plain JavaScript and CSS. It has no remote services or API keys. Optional Google Fonts are requested if online; system fonts are used offline.

## Features

- Five original synthetic automotive security cases covering telematics, OTA, cloud, infotainment and charging controllers.
- Searchable incident queue, scenario-specific signals, transparent priority rubric and operational playbooks.
- Analyst findings, decisions, cross-team handoffs and state transitions stored in a real SQLite database.
- **Hash-linked evidence events**: the application checks the full chain before adding records. Tampering with an earlier event is detectable (not tamper-proof against a privileged attacker who can rewrite the database and all hashes).
- Exportable executive case brief grounded in current recorded actions.
- JSON API: `GET /api/cases`, `GET /api/evidence`, `GET /api/health`, `POST /api/action`.
- Automated Python tests for triage boundaries and evidence tamper detection.

## Test

```bash
python -m unittest discover -s tests -v
```

## Security and limitations

Local-only service bound to 127.0.0.1. **Do not expose it publicly**: it intentionally has no authentication or authorization. The triage score is an illustrative weighted heuristic, **not a CVSS calculation**, a verified safety assessment, or regulatory compliance evidence. The app is a safe training simulator and does not connect to real vehicles, scan targets, or collect forensic evidence from actual incidents. The SQLite database is created automatically in `data/lab.sqlite3` on first launch. Delete that file to reset the demo.

See `docs/ENGINEERING_NOTES.md` for threat model, architecture, and manager demo walkthrough.
