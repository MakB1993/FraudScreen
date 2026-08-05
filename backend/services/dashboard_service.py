from sqlalchemy.orm import Session
from sqlalchemy import func

from backend import models


def get_dashboard_summary(db: Session):
    total_transactions = (
        db.query(func.count(models.Transaction.id))
        .scalar()
    )

    approved = (
        db.query(func.count(models.FraudEvaluation.id))
        .filter(models.FraudEvaluation.decision == "APPROVE")
        .scalar()
    )

    review = (
        db.query(func.count(models.FraudEvaluation.id))
        .filter(models.FraudEvaluation.decision == "REVIEW")
        .scalar()
    )

    rejected = (
        db.query(func.count(models.FraudEvaluation.id))
        .filter(models.FraudEvaluation.decision == "REJECT")
        .scalar()
    )

    return {
        "total_transactions": total_transactions,
        "approved": approved,
        "review": review,
        "rejected": rejected,
    }

def get_transactions_over_time(db: Session):
    results = (
        db.query(
            func.date(models.Transaction.created_at).label("date"),
            func.count(models.Transaction.id).label("count"),
        )
        .group_by(
            func.date(models.Transaction.created_at)
        )
        .order_by(
            func.date(models.Transaction.created_at)
        )
        .all()
    )

    return [
        {
            "date": row.date,
            "count": row.count,
        }
        for row in results
    ]