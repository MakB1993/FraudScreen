from sqlalchemy.orm import Session
from sqlalchemy import func
from backend import models
from datetime import datetime, timedelta, timezone

## enforcing windows on velocity/count signals because recency is part of their meaning, but not blindly forcing a window onto every signal(historical).

def count_transactions_by_ip(
        db: Session,
        ip_address: str,
        window_minutes: int,
        reference_time: datetime,
) -> int: #Because Depends(get_db) is a FastAPI dependency-injection feature, and this function is not an API endpoint.
    cutoff_time = reference_time - timedelta(minutes=window_minutes)
    return (
        db.query(func.count(models.Transaction.id))
        .filter(models.Transaction.ip_address == ip_address)
        .filter(models.Transaction.created_at >= cutoff_time)
        .filter(models.Transaction.created_at <= reference_time)
        .scalar() #.scalar() is used on a query execution result. It fetches the first column of the first row and discards the rest, returning a single Python scalar value (or None if no rows are returned)
    )

def count_transactions_by_device(
        db: Session,
        device_id: str,
        window_minutes: int,
        reference_time: datetime,
) -> int:
    cutoff_time = reference_time - timedelta(minutes=window_minutes)
    return (
        db.query(func.count(models.Transaction.id))
        .filter(models.Transaction.device_id == device_id)
        .filter(models.Transaction.created_at >= cutoff_time)
        .filter(models.Transaction.created_at <= reference_time)
        .scalar()
    )

def count_transactions_by_card(
        db: Session,
        card_fingerprint: str,
        window_minutes: int,
        reference_time: datetime,
) -> int:
    cutoff_time =reference_time - timedelta(minutes=window_minutes)
    return (
        db.query(func.count(models.Transaction.id))
        .filter(models.Transaction.card_fingerprint == card_fingerprint)
        .filter(models.Transaction.created_at >= cutoff_time)
        .filter(models.Transaction.created_at <= reference_time)
        .scalar()
    )

def has_customer_used_device_before(
    db: Session,
    customer_id: str,
    device_id: str,
    reference_time: datetime,
) -> bool:

    count = (
        db.query(func.count(models.Transaction.id))
        .filter(models.Transaction.customer_id == customer_id)
        .filter(models.Transaction.device_id == device_id)
        .filter(models.Transaction.created_at < reference_time)
        .scalar()
    )

    return count > 0

def has_customer_used_card_before(
    db: Session,
    customer_id: str,
    card_fingerprint: str,
    reference_time: datetime,
) -> bool:

    count = (
         db.query(func.count(models.Transaction.id))
            .filter(models.Transaction.customer_id == customer_id)
            .filter(models.Transaction.card_fingerprint == card_fingerprint)
            .filter(models.Transaction.created_at < reference_time)
            .scalar()
        )

    return count > 0

def has_customer_used_ip_before(
    db: Session,
    customer_id: str,
    ip_address: str,
    reference_time: datetime,
) -> bool:
    count = (
        db.query(func.count(models.Transaction.id))
        .filter(
            models.Transaction.customer_id == customer_id,
            models.Transaction.ip_address == ip_address,
            models.Transaction.created_at < reference_time,
        )
        .scalar()
    )

    return count > 0

def count_distinct_customers_by_device(
    db: Session,
    device_id: str,
    reference_time: datetime,
    window_minutes: int,
) -> int:
    cutoff_time = reference_time - timedelta(minutes=window_minutes)

    count = (
        db.query(
            func.count(
                func.distinct(models.Transaction.customer_id)
            )
        )
        .filter(
            models.Transaction.device_id == device_id,
            models.Transaction.created_at >= cutoff_time,
            models.Transaction.created_at <= reference_time,
        )
        .scalar()
    )

    return count

def count_distinct_cards_by_device( #unique cards used this device in the window
    db: Session,
    device_id: str,
    reference_time: datetime,
    window_minutes: int,
) -> int:
    cutoff_time = reference_time - timedelta(minutes=window_minutes)

    count = (
        db.query(
            func.count(
                func.distinct(models.Transaction.card_fingerprint)
            )
        )
        .filter(
            models.Transaction.device_id == device_id,
            models.Transaction.created_at >= cutoff_time,
            models.Transaction.created_at <= reference_time,
        )
        .scalar()
    )

    return count

def count_distinct_customers_by_ip( #unique customers used this IP
    db: Session,
    ip_address: str,
    reference_time: datetime,
    window_minutes: int,
) -> int:
    cutoff_time = reference_time - timedelta(minutes=window_minutes)

    count = (
        db.query(
            func.count(
                func.distinct(models.Transaction.customer_id)
            )
        )
        .filter(
            models.Transaction.ip_address == ip_address,
            models.Transaction.created_at >= cutoff_time,
            models.Transaction.created_at <= reference_time,
        )
        .scalar()
    )

    return count

def count_distinct_cards_by_ip( #unique card fingerprints
    db: Session,
    ip_address: str,
    reference_time: datetime,
    window_minutes: int,
) -> int:
    cutoff_time = reference_time - timedelta(minutes=window_minutes)

    count = (
        db.query(
            func.count(
                func.distinct(models.Transaction.card_fingerprint)
            )
        )
        .filter(
            models.Transaction.ip_address == ip_address,
            models.Transaction.created_at >= cutoff_time,
            models.Transaction.created_at <= reference_time,
        )
        .scalar()
    )

    return count

def count_transactions_by_customer( #customer_velocity: transactions customer made in the window)
    db: Session,
    customer_id: str,
    reference_time: datetime,
    window_minutes: int,
) -> int:
    cutoff_time = reference_time - timedelta(minutes=window_minutes)

    count = (
        db.query(func.count(models.Transaction.id))
        .filter(
            models.Transaction.customer_id == customer_id,
            models.Transaction.created_at >= cutoff_time,
            models.Transaction.created_at <= reference_time,
        )
        .scalar()
    )

    return count

def count_transactions_by_session( ##transactions occurred in particular session
    db: Session,
    session_id: str,
    reference_time: datetime,
    window_minutes: int,
) -> int:
    cutoff_time = reference_time - timedelta(minutes=window_minutes)

    count = (
        db.query(func.count(models.Transaction.id))
        .filter(
            models.Transaction.session_id == session_id,
            models.Transaction.created_at >= cutoff_time,
            models.Transaction.created_at <= reference_time,
        )
        .scalar()
    )

    return count

def has_customer_used_ip_country_before(
    db: Session,
    customer_id: str,
    ip_country: str,
    reference_time: datetime,
) -> bool:
    count = (
        db.query(func.count(models.Transaction.id))
        .filter(
            models.Transaction.customer_id == customer_id,
            models.Transaction.ip_country == ip_country,
            models.Transaction.created_at < reference_time,
        )
        .scalar()
    )

    return count > 0

def has_customer_used_card_country_before(
    db: Session,
    customer_id: str,
    card_country: str,
    reference_time: datetime,
) -> bool:
    count = (
        db.query(func.count(models.Transaction.id))
        .filter(
            models.Transaction.customer_id == customer_id,
            models.Transaction.card_country == card_country,
            models.Transaction.created_at < reference_time,
        )
        .scalar()
    )

    return count > 0

def count_distinct_ip_countries_by_customer(
    db: Session,
    customer_id: str,
    reference_time: datetime,
    window_minutes: int,
) -> int:
    cutoff_time = reference_time - timedelta(minutes=window_minutes)

    count = (
        db.query(
            func.count(
                func.distinct(models.Transaction.ip_country)
            )
        )
        .filter(
            models.Transaction.customer_id == customer_id,
            models.Transaction.created_at >= cutoff_time,
            models.Transaction.created_at <= reference_time,
            models.Transaction.ip_country.isnot(None),
        )
        .scalar()
    )

    return count

def count_declined_transactions_by_customer(
    db: Session,
    customer_id: str,
    reference_time: datetime,
    window_minutes: int,
) -> int:
    cutoff_time = reference_time - timedelta(minutes=window_minutes)

    return (
        db.query(func.count(models.Transaction.id))
        .filter(
            models.Transaction.customer_id == customer_id,
            models.Transaction.transaction_status == "DECLINED",
            models.Transaction.created_at >= cutoff_time,
            models.Transaction.created_at <= reference_time,
        )
        .scalar()
    )

def count_declined_transactions_by_card(
    db: Session,
    card_fingerprint: str,
    reference_time: datetime,
    window_minutes: int,
) -> int:
    cutoff_time = reference_time - timedelta(minutes=window_minutes)

    return (
        db.query(func.count(models.Transaction.id))
        .filter(
            models.Transaction.card_fingerprint == card_fingerprint,
            models.Transaction.transaction_status == "DECLINED",
            models.Transaction.created_at >= cutoff_time,
            models.Transaction.created_at <= reference_time,
        )
        .scalar()
    )

def count_declined_transactions_by_ip(
    db: Session,
    ip_address: str,
    reference_time: datetime,
    window_minutes: int,
) -> int:
    cutoff_time = reference_time - timedelta(minutes=window_minutes)

    return (
        db.query(func.count(models.Transaction.id))
        .filter(
            models.Transaction.ip_address == ip_address,
            models.Transaction.transaction_status == "DECLINED",
            models.Transaction.created_at >= cutoff_time,
            models.Transaction.created_at <= reference_time,
        )
        .scalar()
    )

def count_distinct_cards_by_session(
    db: Session,
    session_id: str,
    reference_time: datetime,
    window_minutes: int,
) -> int:
    cutoff_time = reference_time - timedelta(minutes=window_minutes)

    return (
        db.query(
            func.count(
                func.distinct(models.Transaction.card_fingerprint)
            )
        )
        .filter(
            models.Transaction.session_id == session_id,
            models.Transaction.created_at >= cutoff_time,
            models.Transaction.created_at <= reference_time,
        )
        .scalar()
    )

def count_declined_transactions_by_session(
    db: Session,
    session_id: str,
    reference_time: datetime,
    window_minutes: int,
) -> int:
    cutoff_time = reference_time - timedelta(minutes=window_minutes)

    return (
        db.query(func.count(models.Transaction.id))
        .filter(
            models.Transaction.session_id == session_id,
            models.Transaction.transaction_status == "DECLINED",
            models.Transaction.created_at >= cutoff_time,
            models.Transaction.created_at <= reference_time,
        )
        .scalar()
    )

def has_authorized_after_declines_in_session(
    db: Session,
    session_id: str,
    reference_time: datetime,
    window_minutes: int,
) -> bool:
    cutoff_time = reference_time - timedelta(minutes=window_minutes)

    decline_count = (
        db.query(func.count(models.Transaction.id))
        .filter(
            models.Transaction.session_id == session_id,
            models.Transaction.transaction_status == "DECLINED",
            models.Transaction.created_at >= cutoff_time,
            models.Transaction.created_at < reference_time,
        )
        .scalar()
    )

    return decline_count > 0

def count_distinct_devices_by_customer(
    db: Session,
    customer_id: str,
    reference_time: datetime,
    window_minutes: int,
) -> int:
    cutoff_time = reference_time - timedelta(minutes=window_minutes)

    return (
        db.query(
            func.count(
                func.distinct(models.Transaction.device_id)
            )
        )
        .filter(
            models.Transaction.customer_id == customer_id,
            models.Transaction.created_at >= cutoff_time,
            models.Transaction.created_at <= reference_time,
        )
        .scalar()
    )

def count_distinct_ips_by_customer(
    db: Session,
    customer_id: str,
    reference_time: datetime,
    window_minutes: int,
) -> int:
    cutoff_time = reference_time - timedelta(minutes=window_minutes)

    return (
        db.query(
            func.count(
                func.distinct(models.Transaction.ip_address)
            )
        )
        .filter(
            models.Transaction.customer_id == customer_id,
            models.Transaction.created_at >= cutoff_time,
            models.Transaction.created_at <= reference_time,
        )
        .scalar()
    )