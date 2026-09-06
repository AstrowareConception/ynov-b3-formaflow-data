\set ON_ERROR_STOP on
TRUNCATE student_start.enrollment_export;
\copy student_start.enrollment_export FROM '/workspace/fixtures/flawed-schema/enrollment-export.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8')
