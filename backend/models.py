from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    transaction_id: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    currency: Mapped[str] = mapped_column(String, nullable=False)
    fraud_evaluation: Mapped[list["FraudEvaluation"]] = relationship("FraudEvaluation", back_populates="transaction")

class FraudEvaluation(Base):
    __tablename__ = "fraud_evaluations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    transaction_db_id: Mapped[int] = mapped_column(Integer, ForeignKey("transactions.id"), nullable=False)
    total_score: Mapped[int]= mapped_column(Integer, nullable=False)
    decision: Mapped[str]= mapped_column(String, nullable=False)
    transaction: Mapped["Transaction"] = relationship("Transaction", back_populates="fraud_evaluation")
