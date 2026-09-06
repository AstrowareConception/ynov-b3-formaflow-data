\set ON_ERROR_STOP on
BEGIN;

-- Authorized write: the second and final seat is accepted.
INSERT INTO core.customer_order VALUES
('ORD-TEST-ALLOW', 'LRN-0003', NULL, 'CONFIRMED', '2027-01-21T10:00:00Z', '2027-01-21T10:00:00Z');
INSERT INTO core.order_line VALUES
('OLN-TEST-ALLOW', 'ORD-TEST-ALLOW', 'SES-2027-0001', 'LRN-0003', 'TAR-0001', 69000, 'EUR');
INSERT INTO core.enrollment (enrollment_id, order_line_id, session_id, participant_id, status) VALUES
('ENR-TEST-ALLOW', 'OLN-TEST-ALLOW', 'SES-2027-0001', 'LRN-0003', 'CONFIRMED');

-- Refused write: another learner cannot exceed capacity.
INSERT INTO core.customer_order VALUES
('ORD-TEST-FULL', 'LRN-0002', NULL, 'CONFIRMED', '2027-01-21T10:01:00Z', '2027-01-21T10:01:00Z');
INSERT INTO core.order_line VALUES
('OLN-TEST-FULL', 'ORD-TEST-FULL', 'SES-2027-0001', 'LRN-0002', 'TAR-0001', 69000, 'EUR');
DO $$
BEGIN
    BEGIN
        INSERT INTO core.enrollment (enrollment_id, order_line_id, session_id, participant_id, status)
        VALUES ('ENR-TEST-FULL', 'OLN-TEST-FULL', 'SES-2027-0001', 'LRN-0002', 'CONFIRMED');
        RAISE EXCEPTION 'capacity violation was accepted';
    EXCEPTION WHEN check_violation THEN
        IF SQLERRM = 'capacity violation was accepted' THEN RAISE; END IF;
    END;
END
$$;

-- Refused write: a participant cannot be enrolled twice in one session.
INSERT INTO core.customer_order VALUES
('ORD-TEST-DUP', 'LRN-0002', NULL, 'CONFIRMED', '2027-01-21T10:02:00Z', '2027-01-21T10:02:00Z');
INSERT INTO core.order_line VALUES
('OLN-TEST-DUP', 'ORD-TEST-DUP', 'SES-2027-0002', 'LRN-0002', 'TAR-0002', 59000, 'EUR');
DO $$
BEGIN
    BEGIN
        INSERT INTO core.enrollment (enrollment_id, order_line_id, session_id, participant_id, status)
        VALUES ('ENR-TEST-DUP', 'OLN-TEST-DUP', 'SES-2027-0002', 'LRN-0002', 'CONFIRMED');
        RAISE EXCEPTION 'duplicate enrollment was accepted';
    EXCEPTION WHEN unique_violation THEN NULL;
    END;
END
$$;

-- Changing a current tariff cannot rewrite accepted history.
UPDATE core.tariff SET amount_minor = 71000 WHERE tariff_id = 'TAR-0001';
DO $$
BEGIN
    IF (SELECT accepted_unit_price_minor FROM core.order_line WHERE order_line_id = 'OLN-2027-000001') <> 69000 THEN
        RAISE EXCEPTION 'historical price changed with current tariff';
    END IF;
    BEGIN
        UPDATE core.order_line SET accepted_unit_price_minor = 1 WHERE order_line_id = 'OLN-2027-000001';
        RAISE EXCEPTION 'confirmed snapshot update was accepted';
    EXCEPTION WHEN check_violation THEN
        IF SQLERRM = 'confirmed snapshot update was accepted' THEN RAISE; END IF;
    END;
END
$$;

ROLLBACK;
SELECT '3 invariants: authorized and refused writes verified' AS result;
