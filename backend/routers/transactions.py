from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend import models
from backend.database import get_db
from backend.schemas import TransactionCreate, TransactionResponse, TransactionUpdate, FraudEvaluationResponse

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
    db_transaction = models.Transaction( #creating an object for sqlalchemy model Transaction and passing the values from pydantic model TransactionCreate to it
        transaction_id=transaction.transaction_id,
        customer_id=transaction.customer_id,
        email=transaction.email,
        card_bin=transaction.card_bin,
        card_last_four=transaction.card_last_four,
        ip_address=transaction.ip_address,
        device_id=transaction.device_id,
        amount=transaction.amount,
        currency=transaction.currency,
    )

    db.add(db_transaction)

    try:
        # db.commit() #commenting because we don't want to commit before trans is evaluated by rules and fraud evaluation is created and then commit both transaction and fraud evaluation together
        # db.refresh(db_transaction)
        db.flush()
          # Flush the session to generate the transaction ID without committing
        create_fraud_evaluation(db=db, db_transaction=db_transaction)

        db.commit()  # Commit both the transaction,fraud evaluation and rule evaluations together
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

    query = db.query(models.Transaction)

    if currency:
        query = query.filter(models.Transaction.currency == currency)
    if (
        min_amount is not None
    ):  # None → user didn't provide a value. 0 → user provided zero(Python can treat it as False so only if no value provided).
        query = query.filter(models.Transaction.amount >= min_amount)
    if max_amount is not None:
        query = query.filter(models.Transaction.amount <= max_amount)
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
