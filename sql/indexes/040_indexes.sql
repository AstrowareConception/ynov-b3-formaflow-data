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
