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
