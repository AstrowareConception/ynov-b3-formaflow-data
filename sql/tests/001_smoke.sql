\set ON_ERROR_STOP on
DO $$
BEGIN
    IF (SELECT count(*) FROM core.training) <> 3 THEN
        RAISE EXCEPTION 'smoke: expected 3 trainings';
    END IF;
    IF (SELECT count(*) FROM core.enrollment) <> 2 THEN
        RAISE EXCEPTION 'smoke: expected 2 enrollments';
    END IF;
    IF (SELECT revenue_minor FROM reporting.revenue_by_training WHERE training_id = 'TRN-0001') <> 69000 THEN
        RAISE EXCEPTION 'smoke: unexpected revenue for TRN-0001';
    END IF;
END
$$;
SELECT current_setting('server_version') AS postgres_version, 'smoke ok' AS result;
