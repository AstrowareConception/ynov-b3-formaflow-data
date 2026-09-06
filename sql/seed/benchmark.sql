\set ON_ERROR_STOP on
\ir nominal.sql
INSERT INTO core.training (training_id, title, description, status)
SELECT 'TRN-' || lpad(number::text, 4, '0'), 'Formation benchmark ' || number, NULL, 'PUBLISHED'
FROM generate_series(1, 500) AS number
ON CONFLICT (training_id) DO NOTHING;
TRUNCATE analytics.consultation;
\copy analytics.consultation (consultation_id, training_id, profile_id, occurred_at, source) FROM '/workspace/build/generated/benchmark-consultations-small.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8', NULL '')
ANALYZE analytics.consultation;
REFRESH MATERIALIZED VIEW reporting.daily_consultations;
