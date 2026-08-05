from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.schemas import DashboardSummary, TransactionsOverTimeItem
from backend.services.dashboard_service import get_dashboard_summary, get_transactions_over_time


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get(
    "/summary",
    response_model=DashboardSummary,
)
def dashboard_summary(
    db: Session = Depends(get_db),
):
    return get_dashboard_summary(db)

@router.get(
    "/transactions-over-time",
    response_model=list[TransactionsOverTimeItem],
)
def transactions_over_time(
    db: Session = Depends(get_db),
):
    return get_transactions_over_time(db)