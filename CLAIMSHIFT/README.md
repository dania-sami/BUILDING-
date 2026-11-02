# CLAIMSHIFT

I built CLAIMSHIFT to explore a question I find genuinely interesting: what makes an AI agent dependable enough to support real customers?

This is a small, hands-on prototype inspired by the Generative AI Specialist role at If. Rather than building another chatbot, I focused on the parts that make agents useful in practice: grounded answers, read-only tools, visible execution traces, safe handovers, and repeatable evaluations.

## Run locally

Requires Python 3.10 or newer.

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open **http://127.0.0.1:8000**. Try the scenario buttons, switch between Nordic markets, inspect the execution trace, and run the evaluation suite.

To run tests:

```bash
pytest -q
```

## What it demonstrates

- A simple stateful workflow with input validation, routing, retrieval, tool use, and response checks
- Synthetic policy retrieval for Sweden, Denmark, Norway and Finland
- Read-only demo claim lookup
- Human review gates for claim approvals, payments, and sensitive account changes
- Basic prompt injection screening and safe fallback for unknown topics
- Traceable decisions, latency measurement and a five-case regression suite

## Scope and next steps

This is a deliberately small **deterministic demonstration**, not an LLM-powered production agent. The policy excerpts and claims are fictional. It has no customer data or connection to If's systems. The injection filter is illustrative, not a comprehensive security boundary; there is no real authentication, authorization, or persistent memory.

I'd extend it with LangGraph orchestration, authenticated API integrations, Qdrant-based retrieval with source verification, Langfuse tracing, richer adversarial evaluations, and Azure deployment. Before handling real claims, I'd add strict identity and access controls, audit logging, data protection, and human approval workflows.

**Dania Sami**
