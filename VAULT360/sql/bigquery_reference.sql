-- Illustrative BigQuery target DDL. Not executed or deployed.
CREATE TABLE IF NOT EXISTS `demo_finance_vault.hub_transaction` (
 transaction_hk STRING NOT NULL, transaction_id STRING NOT NULL,
 load_dts TIMESTAMP NOT NULL, record_source STRING NOT NULL
) CLUSTER BY transaction_hk;
CREATE TABLE IF NOT EXISTS `demo_finance_vault.sat_transaction_detail` (
 transaction_hk STRING NOT NULL, load_dts TIMESTAMP NOT NULL,
 hashdiff STRING NOT NULL, amount NUMERIC NOT NULL,
 currency STRING NOT NULL, booked_at DATE NOT NULL,
 record_source STRING NOT NULL
) PARTITION BY DATE(load_dts) CLUSTER BY transaction_hk;
-- Example current-state query; use tie-breaking in production.
SELECT transaction_hk, amount, currency, booked_at
FROM `demo_finance_vault.sat_transaction_detail`
QUALIFY ROW_NUMBER() OVER(PARTITION BY transaction_hk ORDER BY load_dts DESC)=1;
