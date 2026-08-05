from sqlalchemy import Boolean, Integer, String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime,timezone
from .database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    transaction_id: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    transaction_type: Mapped[str | None] = mapped_column(String, nullable=True, index=True)
    transaction_status: Mapped[str] = mapped_column(String, nullable=False, index=True)

    customer_id: Mapped[str] = mapped_column(String,nullable=False, index=True)
    email: Mapped[str] = mapped_column(String,nullable=False, index=True)

    card_fingerprint: Mapped[str] = mapped_column(String, nullable=False, index=True)
    card_bin: Mapped[str] = mapped_column(String,nullable=False, index=True)
    card_last_four: Mapped[str] = mapped_column(String,nullable=False)
    payment_method: Mapped[str] = mapped_column(String, nullable=False, index=True)
    card_country: Mapped[str | None] = mapped_column(String, nullable=True, index=True)
    
    ip_address: Mapped[str] = mapped_column(String,nullable=False, index=True)
    ip_country: Mapped[str | None] = mapped_column(String, nullable=True, index=True)
    device_id: Mapped[str] = mapped_column(String,nullable=False, index=True)
    user_agent: Mapped[str | None] = mapped_column(String, nullable=True)
    session_id: Mapped[str | None] = mapped_column(String, nullable=True, index=True)

    amount: Mapped[float] = mapped_column(Float, nullable=False)
    currency: Mapped[str] = mapped_column(String, nullable=False)
   
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc), nullable=False,index=True)
    #without lambda datetime.now() would run once, when the application starts, and every new transaction would get the same timestamp.
    #with lambda, datetime.now() is called each time a new transaction is created, ensuring that each transaction gets the correct current timestamp.
    fraud_evaluations: Mapped[list["FraudEvaluation"]] = relationship("FraudEvaluation", back_populates="transaction",cascade="all, delete-orphan")  # Ensure that fraud evaluations are deleted when the transaction is deleted

class FraudEvaluation(Base):
    __tablename__ = "fraud_evaluations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    transaction_db_id: Mapped[int] = mapped_column(Integer, ForeignKey("transactions.id"), nullable=False)
    total_score: Mapped[int]= mapped_column(Integer, nullable=False)
    decision: Mapped[str]= mapped_column(String, nullable=False)
    transaction: Mapped["Transaction"] = relationship("Transaction", back_populates="fraud_evaluations")
    rule_evaluations: Mapped[list["RuleEvaluation"]] = relationship("RuleEvaluation", back_populates="fraud_evaluation",cascade="all, delete-orphan")  # Ensure that rule evaluations are deleted when the fraud evaluation is deleted

class RuleEvaluation(Base):
    __tablename__ = "rule_evaluations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    fraud_evaluation_id: Mapped[int] = mapped_column(Integer, ForeignKey("fraud_evaluations.id"), nullable=False,index=True)
    rule_name: Mapped[str] = mapped_column(String, nullable=False)
    triggered: Mapped[bool] = mapped_column(Boolean, nullable=False)
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    reason: Mapped[str] = mapped_column(String, nullable=False)
    fraud_evaluation: Mapped["FraudEvaluation"] = relationship("FraudEvaluation", back_populates="rule_evaluations")

class FraudRule(Base):
    __tablename__ = "fraud_rules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    rule_key: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    rule_name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    signal_key: Mapped[str | None] = mapped_column(String, nullable=True)
    operator: Mapped[str | None] = mapped_column(String, nullable=True)
    enabled: Mapped[bool] = mapped_column(Boolean,default=True, nullable=False)
    threshold_value: Mapped[int] = mapped_column(Integer, nullable=False)
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    window_minutes: Mapped[int|None] = mapped_column(Integer, nullable=True)
    