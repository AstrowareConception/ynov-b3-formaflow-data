\set ON_ERROR_STOP on
TRUNCATE TABLE
    analytics.recommendation, analytics.consultation, core.document, core.payment,
    core.invoice, core.enrollment, core.order_line, core.customer_order,
    core.profile_skill, core.training_skill, core.skill, core.training_session,
    core.tariff, core.training, core.participant, core.organization
CASCADE;

INSERT INTO core.organization VALUES
('ORG-0001', 'Organisation Démonstration', 'SYNTH-ORG-01');

INSERT INTO core.participant (participant_id, display_name, email, organization_id, phone) VALUES
('LRN-0001', 'Participant Alpha', 'participant.alpha@example.test', NULL, NULL),
('LRN-0002', 'Participant Bêta', 'participant.beta@example.test', 'ORG-0001', NULL),
('LRN-0003', 'Participant Gamma', 'participant.gamma@example.test', 'ORG-0001', NULL);

INSERT INTO core.training VALUES
('TRN-0001', 'Concevoir une API robuste', 'Formation synthétique sur les contrats API.', 'PUBLISHED'),
('TRN-0002', 'Modéliser des données métier', 'Formation synthétique sur les modèles de données.', 'PUBLISHED'),
('TRN-0003', 'Sécuriser une application web', NULL, 'ARCHIVED');

INSERT INTO core.tariff VALUES
('TAR-0001', 'TRN-0001', 69000, 'EUR', '2027-01-01', NULL),
('TAR-0002', 'TRN-0002', 59000, 'EUR', '2027-01-01', NULL);

INSERT INTO core.training_session VALUES
('SES-2027-0001', 'TRN-0001', 'TAR-0001', '2027-02-15T08:45:00Z', '2027-02-16T16:45:00Z', 2, 'OPEN'),
('SES-2027-0002', 'TRN-0002', 'TAR-0002', '2027-03-08T08:45:00Z', '2027-03-09T16:45:00Z', 12, 'SCHEDULED');

INSERT INTO core.customer_order VALUES
('ORD-2027-000001', 'LRN-0001', NULL, 'CONFIRMED', '2027-01-20T10:15:30Z', '2027-01-20T10:15:30Z'),
('ORD-2027-000002', NULL, 'ORG-0001', 'CONFIRMED', '2027-01-20T11:00:00Z', '2027-01-20T11:00:00Z');

INSERT INTO core.order_line VALUES
('OLN-2027-000001', 'ORD-2027-000001', 'SES-2027-0001', 'LRN-0001', 'TAR-0001', 69000, 'EUR'),
('OLN-2027-000002', 'ORD-2027-000002', 'SES-2027-0002', 'LRN-0002', 'TAR-0002', 59000, 'EUR');

INSERT INTO core.enrollment (enrollment_id, order_line_id, session_id, participant_id, status, enrolled_at) VALUES
('ENR-2027-000001', 'OLN-2027-000001', 'SES-2027-0001', 'LRN-0001', 'CONFIRMED', '2027-01-20T10:15:31Z'),
('ENR-2027-000002', 'OLN-2027-000002', 'SES-2027-0002', 'LRN-0002', 'CONFIRMED', '2027-01-20T11:00:01Z');

INSERT INTO core.invoice VALUES
('INV-2027-000001', 'ORD-2027-000001', 'ISSUED', 69000, 'EUR', '2027-01-20T10:16:00Z'),
('INV-2027-000002', 'ORD-2027-000002', 'ISSUED', 59000, 'EUR', '2027-01-20T11:01:00Z');

INSERT INTO core.payment VALUES
('PAY-2027-000001', 'ORD-2027-000001', 'ACCEPTED', 69000, 'EUR', '2027-01-20T10:15:29Z', 'SIM-ACCEPT-0001'),
('PAY-2027-000002', 'ORD-2027-000002', 'ACCEPTED', 59000, 'EUR', '2027-01-20T10:59:59Z', 'SIM-ACCEPT-0002');

INSERT INTO core.document VALUES
('DOC-0001', 'LRN-0001', 'ENR-2027-000001', 'CONVOCATION', 'synthetic/DOC-0001.pdf', NULL);

INSERT INTO analytics.consultation VALUES
('CST-0001', 'TRN-0001', 'PRO-0001', '2027-01-18T09:00:00Z', 'catalog'),
('CST-0002', 'TRN-0002', NULL, '2027-01-18T09:05:00Z', 'catalog');

INSERT INTO core.skill VALUES
('SKL-001', 'Modélisation de données'),
('SKL-002', 'Conception API'),
('SKL-003', 'Sécurité web');

INSERT INTO core.training_skill VALUES
('TRN-0001', 'SKL-002', 2),
('TRN-0002', 'SKL-001', 2);

INSERT INTO core.profile_skill VALUES
('PRO-0001', 'SKL-001', 1);

INSERT INTO analytics.recommendation VALUES
('REC-0001', 'PRO-0001', 'TRN-0002', 'skill-gap', '2027-01-20T12:00:00Z');

REFRESH MATERIALIZED VIEW reporting.daily_consultations;
