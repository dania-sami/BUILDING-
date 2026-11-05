-- Snowflake source table is illustrative; configure the source before use.
select claim_id, policy_id, product, try_to_decimal(reported_amount,18,2) as reported_amount, status, event_date from {{ source('insurance', 'raw_claims') }}
