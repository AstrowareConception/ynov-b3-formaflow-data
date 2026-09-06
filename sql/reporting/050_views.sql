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
