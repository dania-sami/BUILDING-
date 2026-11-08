# Architecture and caveats

This is a local, fictional banking warehouse lab, not a production deployment or regulatory compliance certification.

**Source → staging validation → Data Vault 2.0 inspired raw vault → latest-version mart → audit explorer.**

Business keys are hashed into hubs, relationships are stored in links, descriptive attributes and history are in satellites. The load timestamp, record source and hashdiff support traceability. The CSV SHA256 provides a source-file fingerprint and quarantine records preserve rejected rows.

## Known limitations

- SQLite is the executed backend; BigQuery DDL is a reference example only. No GCP, Cloud Composer, dbt, Dataform or Airflow deployment is claimed.
- Example transaction/account/customer relationships are synthetic; real banking identity, ownership and regulatory semantics require business signoff.
- Current loader is batch-idempotent, but real multi-source SCD2 loading needs stable event timestamps, deterministic ordering, effective dating, concurrency controls and more rigorous deduplication.
- This demo supports selected traceability concepts but does not demonstrate compliance with BCBS 239 or any other regulation.
- The UI is a static read-only report generated from fictional data. No confidential information is used.
