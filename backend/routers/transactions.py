from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from datetime import datetime, date, timedelta

from backend import models
from backend.database import get_db
from backend.schemas import TransactionCreate, TransactionResponse, TransactionUpdate, FraudEvaluationResponse
from backend.services.transaction_orchestration_service import create_transaction_service
from backend.services.fraud_evaluation_service import create_fraud_evaluation

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"],
)


@router.post(
    "",
    response_model=TransactionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_transaction(
    transaction: TransactionCreate, #creating an object of pydantic model TransactionCreate and passing the values from request body to it
    db: Session = Depends(get_db),
):
    try:
        db_transaction = create_transaction_service(
            db=db,
            transaction=transaction,
        )

        db.commit()
        db.refresh(db_transaction)


    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Transaction ID already exists",
        )

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the transaction",
        )
    return db_transaction


@router.get(
    "", response_model=list[TransactionResponse], status_code=status.HTTP_200_OK
)
def list_transactions(
    transaction_id: str | None = Query(
        None,
        description="Filter by transaction ID",
    ),
    customer_id: str | None = Query(
        None,
        description="Filter transactions by customer ID",
    ),
    email: str | None = Query(
        None,
        description="Filter transactions by email",
    ),
    ip_address: str | None = Query(
        None,
        description="Filter transactions by IP address",
    ),
    device_id: str | None = Query(
            None,
            description="Filter transactions by IP address",
        ),
    currency: str | None = Query(None, description="Filter transactions by currency"),
    min_amount: float | None = Query(
        None,
        description="Filter transactions with amount greater than or equal to this value",
    ),
    max_amount: float | None = Query(
        None,
        description="Filter transactions with amount less than or equal to this value",
    ),
    db: Session = Depends(get_db),
    start_date: datetime | None = Query(
        None,
        description="Filter transactions from this date",
    ),
    end_date: datetime | None = Query(
        None,
        description="Filter transactions up to this date",
    ),
    limit: int = Query(
        20, ge=1, le=100, description="Number of transactions to return"
    ),
    offset: int = Query(0, ge=0, description="Number of transactions to skip"),
):
    if min_amount is not None and max_amount is not None and min_amount > max_amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="min_amount cannot be greater than max_amount",
        )

    if start_date is not None and end_date is not None and start_date > end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="start_date cannot be greater than end_date",
        )

    query = db.query(models.Transaction)

    if transaction_id:
        query = query.filter(
            models.Transaction.transaction_id == transaction_id
        )

    if customer_id:
        query = query.filter(
            models.Transaction.customer_id == customer_id
        )
    if email:
        query = query.filter(
            models.Transaction.email.ilike(f"%{email}%")
        )
    if ip_address:
        query = query.filter(
            models.Transaction.ip_address == ip_address
        )
    if device_id:
        query = query.filter(
            models.Transaction.ip_address == device_id
        )
    if currency:
        query = query.filter(models.Transaction.currency == currency)
    if (
        min_amount is not None
    ):  # None → user didn't provide a value. 0 → user provided zero(Python can treat it as False so only if no value provided).
        query = query.filter(models.Transaction.amount >= min_amount)
    if max_amount is not None:
        query = query.filter(models.Transaction.amount <= max_amount)
    if start_date is not None:
        query = query.filter(
            models.Transaction.created_at >= datetime.combine(start_date,datetime.min.time())
        )
    if end_date is not None:
        query = query.filter(
            models.Transaction.created_at <= datetime.combine(end_date,datetime.min.time())
        )
    transactions = (
        query.order_by(models.Transaction.id.desc()).offset(offset).limit(limit).all()
    )
    return transactions


@router.get(
    "/{transaction_id}",
    response_model=TransactionResponse,
    # FastAPI passes the SQLAlchemy object through your Pydantic TransactionResponse schema before returning JSON.
    # This gives us:controlled API output;automatic OpenAPI documentation;response validation;protection against accidentally exposing additional database columns.
    status_code=status.HTTP_200_OK,
)
def get_transaction(
    transaction_id: str,
    db: Session = Depends(get_db),
):
    db_transaction = (
        db.query(models.Transaction)
        .filter(models.Transaction.transaction_id == transaction_id)
        .first()
    )

    if not db_transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Transaction with ID {transaction_id} not found",
        )

    return db_transaction

@router.get(
    "/{transaction_id}/fraud-evaluation",
    response_model=FraudEvaluationResponse,
    status_code=status.HTTP_200_OK,
)
def get_fraud_evaluation(
    transaction_id: str,
    db: Session = Depends(get_db),
):
    db_transaction = (
        db.query(models.Transaction)
        .filter(models.Transaction.transaction_id == transaction_id)
        .first()
    )

    if not db_transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Transaction with ID {transaction_id} not found",
        )

    
    db_fraud_evaluation = (
        db.query(models.FraudEvaluation)
        .filter(models.FraudEvaluation.transaction_db_id == db_transaction.id)
        .order_by(models.FraudEvaluation.id.desc())  # Get the latest fraud evaluation
        .first()
    )

    if not db_fraud_evaluation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Fraud evaluation for transaction ID {transaction_id} not found",
        )

    return db_fraud_evaluation

@router.put( # TODO: Re-run fraud evaluation when fraud-relevant fields are updated.
    "/{transaction_id}",
    response_model=TransactionResponse,
    status_code=status.HTTP_200_OK,
)
def update_transaction(
    transaction_id: str,
    transaction: TransactionUpdate,
    db: Session = Depends(get_db),
):
    db_transaction = (
        db.query(models.Transaction)
        .filter(models.Transaction.transaction_id == transaction_id)
        .first()
    )

    if not db_transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Transaction with ID {transaction_id} not found",
        )

    if transaction.amount is not None:
        db_transaction.amount = float(transaction.amount)
    if transaction.currency is not None:
        db_transaction.currency = transaction.currency

    db.commit()
    db.refresh(db_transaction)

    return db_transaction
