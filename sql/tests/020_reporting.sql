\set ON_ERROR_STOP on
DO $$
BEGIN
    IF (SELECT revenue_minor FROM reporting.revenue_by_training WHERE training_id = 'TRN-0001') <> 69000 THEN
        RAISE EXCEPTION 'reporting revenue mismatch for TRN-0001';
    END IF;
    IF (SELECT occupied FROM reporting.session_fill WHERE session_id = 'SES-2027-0001') <> 1 THEN
        RAISE EXCEPTION 'reporting occupancy mismatch';
    END IF;
    IF (SELECT accepted_paid_minor FROM reporting.billing_status WHERE invoice_id = 'INV-2027-000002') <> 59000 THEN
        RAISE EXCEPTION 'reporting billing mismatch';
    END IF;
    IF (SELECT accepted_unit_price_minor FROM reporting.accepted_price_history WHERE order_line_id = 'OLN-2027-000001') <> 69000 THEN
        RAISE EXCEPTION 'reporting price history mismatch';
    END IF;
END
$$;
SELECT 'reporting consistency verified' AS result;
