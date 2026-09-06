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
