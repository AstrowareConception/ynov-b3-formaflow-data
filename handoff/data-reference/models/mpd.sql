-- FormaFlow Data Reference 1.0.0 - standalone PostgreSQL 16 MPD
-- Generated deterministically by scripts/build_handoff.py; do not edit this copy directly.

-- BEGIN sql/schema/000_reset.sql
\set ON_ERROR_STOP on
DROP SCHEMA IF EXISTS reporting CASCADE;
DROP SCHEMA IF EXISTS analytics CASCADE;
DROP SCHEMA IF EXISTS core CASCADE;
DROP SCHEMA IF EXISTS student_start CASCADE;
-- END sql/schema/000_reset.sql

-- BEGIN sql/schema/010_types_and_schemas.sql
\set ON_ERROR_STOP on
CREATE SCHEMA core;
CREATE SCHEMA analytics;
CREATE SCHEMA reporting;

CREATE TYPE core.training_status AS ENUM ('DRAFT', 'PUBLISHED', 'ARCHIVED');
CREATE TYPE core.session_status AS ENUM ('DRAFT', 'SCHEDULED', 'OPEN', 'FULL', 'CANCELLED', 'COMPLETED');
CREATE TYPE core.order_status AS ENUM ('DRAFT', 'AWAITING_PAYMENT', 'CONFIRMED', 'PAYMENT_FAILED', 'CANCELLED');
CREATE TYPE core.enrollment_status AS ENUM ('PENDING', 'CONFIRMED', 'CANCELLED', 'COMPLETED');
CREATE TYPE core.payment_status AS ENUM ('PENDING', 'ACCEPTED', 'REFUSED', 'UNKNOWN');
CREATE TYPE core.invoice_status AS ENUM ('ISSUED', 'CANCELLED');
CREATE TYPE core.document_kind AS ENUM ('CONVOCATION', 'CERTIFICATE', 'INVOICE_COPY', 'OTHER');
-- END sql/schema/010_types_and_schemas.sql

-- BEGIN sql/schema/020_tables.sql
\set ON_ERROR_STOP on

CREATE TABLE core.organization (
    organization_id text PRIMARY KEY CHECK (organization_id ~ '^ORG-[A-Z0-9-]+$'),
    name text NOT NULL CHECK (length(btrim(name)) >= 2),
    billing_code text NOT NULL UNIQUE
);

CREATE TABLE core.participant (
    participant_id text PRIMARY KEY CHECK (participant_id ~ '^LRN-[A-Z0-9-]+$'),
    display_name text NOT NULL CHECK (length(btrim(display_name)) >= 2),
    email text NOT NULL UNIQUE CHECK (email LIKE '%@%.%'),
    organization_id text REFERENCES core.organization(organization_id) ON DELETE SET NULL,
    phone text
);

CREATE TABLE core.training (
    training_id text PRIMARY KEY CHECK (training_id ~ '^TRN-[A-Z0-9-]+$'),
    title text NOT NULL CHECK (length(btrim(title)) >= 3),
    description text,
    status core.training_status NOT NULL DEFAULT 'DRAFT'
);

CREATE TABLE core.tariff (
    tariff_id text PRIMARY KEY CHECK (tariff_id ~ '^TAR-[A-Z0-9-]+$'),
    training_id text NOT NULL REFERENCES core.training(training_id),
    amount_minor integer NOT NULL CHECK (amount_minor >= 0),
    currency char(3) NOT NULL CHECK (currency ~ '^[A-Z]{3}$'),
    valid_from date NOT NULL,
    valid_to date,
    UNIQUE (training_id, valid_from),
    CHECK (valid_to IS NULL OR valid_to >= valid_from)
);

CREATE TABLE core.training_session (
    session_id text PRIMARY KEY CHECK (session_id ~ '^SES-[A-Z0-9-]+$'),
    training_id text NOT NULL REFERENCES core.training(training_id),
    current_tariff_id text NOT NULL REFERENCES core.tariff(tariff_id),
    starts_at timestamptz NOT NULL,
    ends_at timestamptz NOT NULL,
    capacity integer NOT NULL CHECK (capacity > 0),
    status core.session_status NOT NULL DEFAULT 'DRAFT',
    CHECK (ends_at > starts_at)
);

CREATE TABLE core.customer_order (
    order_id text PRIMARY KEY CHECK (order_id ~ '^ORD-[A-Z0-9-]+$'),
    buyer_participant_id text REFERENCES core.participant(participant_id),
    organization_id text REFERENCES core.organization(organization_id),
    status core.order_status NOT NULL DEFAULT 'DRAFT',
    ordered_at timestamptz NOT NULL,
    confirmed_at timestamptz,
    CHECK (buyer_participant_id IS NOT NULL OR organization_id IS NOT NULL),
    CHECK ((status = 'CONFIRMED') = (confirmed_at IS NOT NULL))
);

CREATE TABLE core.order_line (
    order_line_id text PRIMARY KEY CHECK (order_line_id ~ '^OLN-[A-Z0-9-]+$'),
    order_id text NOT NULL REFERENCES core.customer_order(order_id) ON DELETE CASCADE,
    session_id text NOT NULL REFERENCES core.training_session(session_id),
    participant_id text NOT NULL REFERENCES core.participant(participant_id),
    source_tariff_id text REFERENCES core.tariff(tariff_id),
    accepted_unit_price_minor integer NOT NULL CHECK (accepted_unit_price_minor >= 0),
    currency char(3) NOT NULL CHECK (currency ~ '^[A-Z]{3}$')
);

CREATE TABLE core.enrollment (
    enrollment_id text PRIMARY KEY CHECK (enrollment_id ~ '^ENR-[A-Z0-9-]+$'),
    order_line_id text NOT NULL UNIQUE REFERENCES core.order_line(order_line_id),
    session_id text NOT NULL REFERENCES core.training_session(session_id),
    participant_id text NOT NULL REFERENCES core.participant(participant_id),
    status core.enrollment_status NOT NULL DEFAULT 'PENDING',
    enrolled_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (session_id, participant_id)
);

CREATE TABLE core.invoice (
    invoice_id text PRIMARY KEY CHECK (invoice_id ~ '^INV-[A-Z0-9-]+$'),
    order_id text NOT NULL UNIQUE REFERENCES core.customer_order(order_id),
    status core.invoice_status NOT NULL DEFAULT 'ISSUED',
    total_minor integer NOT NULL CHECK (total_minor >= 0),
    currency char(3) NOT NULL CHECK (currency ~ '^[A-Z]{3}$'),
    issued_at timestamptz NOT NULL
);

CREATE TABLE core.payment (
    payment_id text PRIMARY KEY CHECK (payment_id ~ '^PAY-[A-Z0-9-]+$'),
    order_id text NOT NULL REFERENCES core.customer_order(order_id),
    status core.payment_status NOT NULL,
    amount_minor integer NOT NULL CHECK (amount_minor >= 0),
    currency char(3) NOT NULL CHECK (currency ~ '^[A-Z]{3}$'),
    occurred_at timestamptz NOT NULL,
    provider_reference text UNIQUE
);

CREATE TABLE core.document (
    document_id text PRIMARY KEY CHECK (document_id ~ '^DOC-[A-Z0-9-]+$'),
    participant_id text REFERENCES core.participant(participant_id),
    enrollment_id text REFERENCES core.enrollment(enrollment_id),
    kind core.document_kind NOT NULL,
    storage_key text NOT NULL UNIQUE,
    expires_at timestamptz,
    CHECK (participant_id IS NOT NULL OR enrollment_id IS NOT NULL)
);

CREATE TABLE analytics.consultation (
    consultation_id text PRIMARY KEY CHECK (consultation_id ~ '^CST-[A-Z0-9-]+$'),
    training_id text NOT NULL REFERENCES core.training(training_id),
    profile_id text,
    occurred_at timestamptz NOT NULL,
    source text NOT NULL DEFAULT 'catalog'
);

CREATE TABLE core.skill (
    skill_id text PRIMARY KEY CHECK (skill_id ~ '^SKL-[A-Z0-9-]+$'),
    label text NOT NULL UNIQUE
);

CREATE TABLE core.training_skill (
    training_id text NOT NULL REFERENCES core.training(training_id),
    skill_id text NOT NULL REFERENCES core.skill(skill_id),
    target_level smallint NOT NULL CHECK (target_level BETWEEN 1 AND 5),
    PRIMARY KEY (training_id, skill_id)
);

CREATE TABLE core.profile_skill (
    profile_id text NOT NULL,
    skill_id text NOT NULL REFERENCES core.skill(skill_id),
    current_level smallint NOT NULL CHECK (current_level BETWEEN 0 AND 5),
    PRIMARY KEY (profile_id, skill_id)
);

CREATE TABLE analytics.recommendation (
    recommendation_id text PRIMARY KEY CHECK (recommendation_id ~ '^REC-[A-Z0-9-]+$'),
    profile_id text NOT NULL,
    training_id text NOT NULL REFERENCES core.training(training_id),
    score_basis text NOT NULL,
    generated_at timestamptz NOT NULL,
    UNIQUE (profile_id, training_id, generated_at)
);
-- END sql/schema/020_tables.sql

-- BEGIN sql/constraints/030_capacity_guard.sql
\set ON_ERROR_STOP on

CREATE FUNCTION core.guard_session_capacity() RETURNS trigger
LANGUAGE plpgsql AS $$
DECLARE
    maximum integer;
    occupied integer;
BEGIN
    IF NEW.status NOT IN ('PENDING', 'CONFIRMED') THEN
        RETURN NEW;
    END IF;

    -- Locking the session serializes contenders for the last seat.
    SELECT capacity INTO maximum
    FROM core.training_session
    WHERE session_id = NEW.session_id
    FOR UPDATE;

    SELECT count(*) INTO occupied
    FROM core.enrollment
    WHERE session_id = NEW.session_id
      AND status IN ('PENDING', 'CONFIRMED')
      AND enrollment_id <> NEW.enrollment_id;

    IF occupied >= maximum THEN
        RAISE EXCEPTION 'session % capacity % exceeded', NEW.session_id, maximum
            USING ERRCODE = '23514', CONSTRAINT = 'enrollment_session_capacity';
    END IF;
    RETURN NEW;
END;
$$;

CREATE TRIGGER enrollment_capacity_guard
BEFORE INSERT OR UPDATE OF session_id, status ON core.enrollment
FOR EACH ROW EXECUTE FUNCTION core.guard_session_capacity();

CREATE FUNCTION core.protect_confirmed_price_snapshot() RETURNS trigger
LANGUAGE plpgsql AS $$
BEGIN
    IF (OLD.accepted_unit_price_minor, OLD.currency)
       IS DISTINCT FROM
       (NEW.accepted_unit_price_minor, NEW.currency)
       AND EXISTS (
           SELECT 1 FROM core.customer_order
           WHERE order_id = OLD.order_id AND status = 'CONFIRMED'
       ) THEN
        RAISE EXCEPTION 'accepted price of a confirmed order is immutable'
            USING ERRCODE = '23514', CONSTRAINT = 'confirmed_order_price_snapshot';
    END IF;
    RETURN NEW;
END;
$$;

CREATE TRIGGER order_line_price_snapshot_guard
BEFORE UPDATE OF accepted_unit_price_minor, currency ON core.order_line
FOR EACH ROW EXECUTE FUNCTION core.protect_confirmed_price_snapshot();
-- END sql/constraints/030_capacity_guard.sql

-- BEGIN sql/indexes/040_indexes.sql
\set ON_ERROR_STOP on
CREATE INDEX idx_session_training_start ON core.training_session (training_id, starts_at);
CREATE INDEX idx_enrollment_session_active ON core.enrollment (session_id, status)
    WHERE status IN ('PENDING', 'CONFIRMED');
CREATE INDEX idx_enrollment_participant ON core.enrollment (participant_id, enrolled_at DESC);
CREATE INDEX idx_order_status_date ON core.customer_order (status, ordered_at DESC);
CREATE INDEX idx_order_line_session ON core.order_line (session_id);
CREATE INDEX idx_payment_order_date ON core.payment (order_id, occurred_at DESC);
CREATE INDEX idx_invoice_issued ON core.invoice (issued_at DESC) WHERE status = 'ISSUED';
CREATE INDEX idx_consultation_training_time ON analytics.consultation (training_id, occurred_at DESC);
CREATE INDEX idx_recommendation_profile ON analytics.recommendation (profile_id, generated_at DESC);
-- END sql/indexes/040_indexes.sql

-- BEGIN sql/reporting/050_views.sql
\set ON_ERROR_STOP on

CREATE VIEW reporting.revenue_by_training AS
SELECT t.training_id, t.title,
       count(DISTINCT o.order_id) AS confirmed_orders,
       sum(ol.accepted_unit_price_minor)::bigint AS revenue_minor,
       min(ol.currency) AS currency
FROM core.training t
JOIN core.training_session s USING (training_id)
JOIN core.order_line ol USING (session_id)
JOIN core.customer_order o USING (order_id)
WHERE o.status = 'CONFIRMED'
GROUP BY t.training_id, t.title;

CREATE VIEW reporting.session_fill AS
SELECT s.session_id, s.training_id, s.capacity,
       count(e.enrollment_id) FILTER (WHERE e.status IN ('PENDING', 'CONFIRMED')) AS occupied,
       s.capacity - count(e.enrollment_id) FILTER (WHERE e.status IN ('PENDING', 'CONFIRMED')) AS available,
       round(100.0 * count(e.enrollment_id) FILTER (WHERE e.status IN ('PENDING', 'CONFIRMED')) / s.capacity, 2) AS fill_percent
FROM core.training_session s
LEFT JOIN core.enrollment e USING (session_id)
GROUP BY s.session_id, s.training_id, s.capacity;

CREATE VIEW reporting.enrollment_tracking AS
SELECT e.enrollment_id, e.status, e.enrolled_at, p.participant_id, p.display_name,
       o.organization_id, s.session_id, t.training_id, t.title
FROM core.enrollment e
JOIN core.participant p USING (participant_id)
JOIN core.training_session s USING (session_id)
JOIN core.training t USING (training_id)
JOIN core.order_line ol USING (order_line_id)
JOIN core.customer_order o USING (order_id);

CREATE VIEW reporting.billing_status AS
SELECT i.invoice_id, i.order_id, i.status AS invoice_status, i.total_minor, i.currency,
       coalesce(sum(p.amount_minor) FILTER (WHERE p.status = 'ACCEPTED'), 0)::bigint AS accepted_paid_minor,
       coalesce(string_agg(DISTINCT p.status::text, ',' ORDER BY p.status::text), 'NONE') AS payment_states
FROM core.invoice i
LEFT JOIN core.payment p USING (order_id)
GROUP BY i.invoice_id, i.order_id, i.status, i.total_minor, i.currency;

CREATE VIEW reporting.payment_status AS
SELECT p.payment_id, p.order_id, p.status, p.amount_minor, p.currency, p.occurred_at,
       o.status AS order_status
FROM core.payment p JOIN core.customer_order o USING (order_id);

CREATE VIEW reporting.accepted_price_history AS
SELECT ol.order_line_id, ol.order_id, ol.session_id, ol.accepted_unit_price_minor,
       ol.currency AS accepted_currency, tf.amount_minor AS current_tariff_minor,
       tf.currency AS current_currency,
       tf.amount_minor - ol.accepted_unit_price_minor AS current_difference_minor
FROM core.order_line ol
JOIN core.training_session s USING (session_id)
JOIN core.tariff tf ON tf.tariff_id = s.current_tariff_id;

CREATE MATERIALIZED VIEW reporting.daily_consultations AS
SELECT occurred_at::date AS consultation_date, training_id, count(*)::bigint AS consultation_count
FROM analytics.consultation
GROUP BY occurred_at::date, training_id
WITH NO DATA;

CREATE UNIQUE INDEX idx_daily_consultations_key
ON reporting.daily_consultations (consultation_date, training_id);
-- END sql/reporting/050_views.sql
