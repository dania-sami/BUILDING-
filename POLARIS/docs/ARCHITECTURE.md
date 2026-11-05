# Architecture and boundaries

Synthetic CSV → Python validation → SQLite raw_claims and fact_claims → FastAPI → UI / deterministic evidence retrieval. Invalid records enter quarantine; each pipeline run writes an audit event.

**Production target:** Azure DevOps CI/CD → containerized Dagster assets → Snowflake RAW → dbt staging and marts → governed retrieval service → internal AI platform. The included Dagster asset and dbt project are reference examples, not a working Snowflake deployment.

**Operational requirements before production:** Key Vault credentials, least-privilege Snowflake roles, customer PII handling and encryption, row-level access, observability, alerting, retries, backfills, schema evolution, lineage, data retention, cost budgets, model evaluation, and incident response.

**AI honesty:** The evidence assistant is deterministic SQL-backed retrieval, not a live generative LLM, RAG vector index, MCP server, or autonomous agent. The distinction is intentional and explicit.
