from sqlalchemy.orm import Session
from datetime import datetime

from backend import models
from backend.schemas import TransactionCreate
from backend.services.fraud_evaluation_service import create_fraud_evaluation


def create_transaction_service(
    db: Session,
    transaction: TransactionCreate,
    created_at: datetime | None= None
) -> models.Transaction:
    db_transaction = models.Transaction(    #db_transaction = models.Transaction(**transaction.model_dump()) :=  as transaction is a pydantic model and we can convert it to dict
        transaction_id=transaction.transaction_id,
        transaction_type=transaction.transaction_type,
        transaction_status=transaction.transaction_status,

        customer_id=transaction.customer_id,
        email=transaction.email,

        card_fingerprint=transaction.card_fingerprint,
        card_bin=transaction.card_bin,
        card_last_four=transaction.card_last_four,
        payment_method=transaction.payment_method,
        card_country=transaction.card_country,

        ip_address=transaction.ip_address,
        ip_country=transaction.ip_country,
        device_id=transaction.device_id,
        user_agent=transaction.user_agent,
        session_id=transaction.session_id,

        amount=transaction.amount,
        currency=transaction.currency,
    )

    if created_at is not None:
      db_transaction.created_at = created_at

    db.add(db_transaction)
    db.flush()

    create_fraud_evaluation(
        db=db,
        db_transaction=db_transaction,
    )

    return db_transaction