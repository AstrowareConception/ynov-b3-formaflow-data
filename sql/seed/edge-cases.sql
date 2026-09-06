\set ON_ERROR_STOP on
\ir nominal.sql

INSERT INTO core.organization VALUES
('ORG-EDGE-01', 'Organisation Cas Limite', 'SYNTH-EDGE-01');

INSERT INTO core.participant (participant_id, display_name, email, organization_id, phone) VALUES
('LRN-EDGE-01', 'Participant Limite Un', 'edge.one@example.test', NULL, NULL),
('LRN-EDGE-02', 'Participant Limite Deux', 'edge.two@example.test', 'ORG-EDGE-01', NULL),
('LRN-EDGE-03', 'Participant Limite Trois', 'edge.three@example.test', 'ORG-EDGE-01', NULL);

INSERT INTO core.training VALUES
('TRN-EDGE-01', 'Formation Cas Limites', NULL, 'PUBLISHED');

INSERT INTO core.tariff VALUES
('TAR-EDGE-01', 'TRN-EDGE-01', 42000, 'EUR', '2027-01-01', NULL);

INSERT INTO core.training_session VALUES
('SES-EDGE-FULL', 'TRN-EDGE-01', 'TAR-EDGE-01', '2027-04-01T09:00:00Z', '2027-04-01T17:00:00Z', 1, 'FULL'),
('SES-EDGE-PAY', 'TRN-EDGE-01', 'TAR-EDGE-01', '2027-05-01T09:00:00Z', '2027-05-01T17:00:00Z', 10, 'OPEN');

INSERT INTO core.customer_order VALUES
('ORD-EDGE-ACCEPT', NULL, 'ORG-EDGE-01', 'CONFIRMED', '2027-01-20T12:10:00Z', '2027-01-20T12:10:00Z'),
('ORD-EDGE-REFUSE', NULL, 'ORG-EDGE-01', 'PAYMENT_FAILED', '2027-01-20T12:11:00Z', NULL),
('ORD-EDGE-UNKNOWN', NULL, 'ORG-EDGE-01', 'AWAITING_PAYMENT', '2027-01-20T12:12:00Z', NULL);

INSERT INTO core.order_line VALUES
('OLN-EDGE-ACCEPT', 'ORD-EDGE-ACCEPT', 'SES-EDGE-FULL', 'LRN-EDGE-01', 'TAR-EDGE-01', 42000, 'EUR'),
('OLN-EDGE-REFUSE', 'ORD-EDGE-REFUSE', 'SES-EDGE-PAY', 'LRN-EDGE-02', 'TAR-EDGE-01', 42000, 'EUR'),
('OLN-EDGE-UNKNOWN', 'ORD-EDGE-UNKNOWN', 'SES-EDGE-PAY', 'LRN-EDGE-03', 'TAR-EDGE-01', 42000, 'EUR');

INSERT INTO core.enrollment (enrollment_id, order_line_id, session_id, participant_id, status, enrolled_at) VALUES
('ENR-EDGE-ACCEPT', 'OLN-EDGE-ACCEPT', 'SES-EDGE-FULL', 'LRN-EDGE-01', 'CONFIRMED', '2027-01-20T12:10:01Z');

INSERT INTO core.payment VALUES
('PAY-EDGE-ACCEPT', 'ORD-EDGE-ACCEPT', 'ACCEPTED', 42000, 'EUR', '2027-01-20T12:09:59Z', 'SIM-EDGE-ACCEPT'),
('PAY-EDGE-REFUSE', 'ORD-EDGE-REFUSE', 'REFUSED', 42000, 'EUR', '2027-01-20T12:10:59Z', 'SIM-EDGE-REFUSE'),
('PAY-EDGE-UNKNOWN', 'ORD-EDGE-UNKNOWN', 'UNKNOWN', 42000, 'EUR', '2027-01-20T12:11:59Z', 'SIM-EDGE-UNKNOWN');

INSERT INTO core.invoice VALUES
('INV-EDGE-ACCEPT', 'ORD-EDGE-ACCEPT', 'ISSUED', 42000, 'EUR', '2027-01-20T12:10:02Z');

-- The current price changes; the accepted order-line snapshot remains 42000.
UPDATE core.tariff SET amount_minor = 47000 WHERE tariff_id = 'TAR-EDGE-01';
REFRESH MATERIALIZED VIEW reporting.daily_consultations;
