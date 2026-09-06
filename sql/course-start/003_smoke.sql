\set ON_ERROR_STOP on
DO $$
BEGIN
    IF (SELECT count(*) FROM student_start.enrollment_export) <> 5 THEN
        RAISE EXCEPTION 'expected 5 synthetic flawed rows';
    END IF;
END
$$;
SELECT 'course-start smoke ok' AS result;
