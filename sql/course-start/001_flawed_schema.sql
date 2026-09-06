\set ON_ERROR_STOP on
DROP SCHEMA IF EXISTS student_start CASCADE;
CREATE SCHEMA student_start;

-- This table intentionally mixes multiple granularities and leaves nullability ambiguous.
CREATE TABLE student_start.enrollment_export (
    registration_id text,
    participant_id text,
    participant_name text,
    participant_email text,
    organization_id text,
    organization_name text,
    training_id text,
    training_title text,
    session_id text,
    session_start text,
    session_capacity text,
    current_price_minor text,
    order_id text,
    order_line_id text,
    accepted_price_minor text,
    invoice_id text,
    invoice_total_minor text,
    payment_id text,
    payment_status text,
    optional_phone text
);
