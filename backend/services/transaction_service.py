from sqlalchemy.orm import Session
from sqlalchemy import func
from backend import models
from datetime import datetime, timedelta, timezone

def count_transactions_by_ip(
        db: Session,
        ip_address: str,
        window_minutes: int
) -> int: #Because Depends(get_db) is a FastAPI dependency-injection feature, and this function is not an API endpoint.
    cutoff_time = datetime.now(timezone.utc) - timedelta(minutes=window_minutes)
    return (
        db.query(func.count(models.Transaction.id))
        .filter(models.Transaction.ip_address == ip_address)
        .filter(models.Transaction.created_at >= cutoff_time)
        .scalar() #.scalar() is used on a query execution result. It fetches the first column of the first row and discards the rest, returning a single Python scalar value (or None if no rows are returned)
    )

def count_transactions_by_device(
        db: Session,
        device_id: str,
        window_minutes: int
) -> int:
    cutoff_time = datetime.now(timezone.utc) - timedelta(minutes=window_minutes)
    return (
        db.query(func.count(models.Transaction.id))
        .filter(models.Transaction.device_id == device_id)
        .filter(models.Transaction.created_at >= cutoff_time)
        .scalar()
    )