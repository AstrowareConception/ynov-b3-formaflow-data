DROP KEYSPACE IF EXISTS formaflow_analytics;
CREATE KEYSPACE formaflow_analytics
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};
USE formaflow_analytics;

CREATE TABLE consultations_by_training_month (
    training_id text,
    bucket_month date,
    occurred_at timestamp,
    consultation_id text,
    profile_id text,
    source text,
    PRIMARY KEY ((training_id, bucket_month), occurred_at, consultation_id)
) WITH CLUSTERING ORDER BY (occurred_at DESC, consultation_id ASC)
  AND default_time_to_live = 7776000;

CREATE TABLE consultations_by_profile_month (
    profile_id text,
    bucket_month date,
    occurred_at timestamp,
    consultation_id text,
    training_id text,
    source text,
    PRIMARY KEY ((profile_id, bucket_month), occurred_at, consultation_id)
) WITH CLUSTERING ORDER BY (occurred_at DESC, consultation_id ASC)
  AND default_time_to_live = 7776000;

INSERT INTO consultations_by_training_month (training_id, bucket_month, occurred_at, consultation_id, profile_id, source)
VALUES ('TRN-0001', '2027-01-01', '2027-01-18T09:00:00Z', 'CST-0001', 'PRO-0001', 'catalog');
INSERT INTO consultations_by_training_month (training_id, bucket_month, occurred_at, consultation_id, profile_id, source)
VALUES ('TRN-0002', '2027-01-01', '2027-01-18T09:05:00Z', 'CST-0002', null, 'catalog');
INSERT INTO consultations_by_profile_month (profile_id, bucket_month, occurred_at, consultation_id, training_id, source)
VALUES ('PRO-0001', '2027-01-01', '2027-01-18T09:00:00Z', 'CST-0001', 'TRN-0001', 'catalog');

SELECT count(*) AS training_month_count FROM consultations_by_training_month
WHERE training_id = 'TRN-0001' AND bucket_month = '2027-01-01';
