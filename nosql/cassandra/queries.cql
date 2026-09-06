USE formaflow_analytics;
SELECT occurred_at, consultation_id, profile_id, source
FROM consultations_by_training_month
WHERE training_id = 'TRN-0001' AND bucket_month = '2027-01-01'
  AND occurred_at >= '2027-01-01T00:00:00Z' AND occurred_at < '2027-02-01T00:00:00Z'
LIMIT 100;

SELECT occurred_at, consultation_id, training_id
FROM consultations_by_profile_month
WHERE profile_id = 'PRO-0001' AND bucket_month = '2027-01-01'
LIMIT 50;
