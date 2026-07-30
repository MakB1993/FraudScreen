from sqlalchemy.orm import Session

from backend import models
from backend.schemas import TransactionCreate,FraudEvaluationResult
from backend.services.transaction_service import count_transactions_by_device,count_transactions_by_ip
from backend.services.fraud_engine import evaluate_transaction
from backend.services.rule_service import get_rule


def run_fraud_evaluation(
    db: Session,
    transaction: TransactionCreate | models.Transaction,
) -> FraudEvaluationResult:

  ip_rule = get_rule(db=db, rule_key='ip_velocity')
  device_rule =get_rule(db=db, rule_key='device_velocity')
  
  if ip_rule is None:
      raise ValueError("IP Velocity rule not found!")
  if ip_rule.window_minutes is None:
      raise ValueError("IP Velocity requires window minutes.")
  
  if device_rule is None:
      raise ValueError("Device Velocity rule not found!")
  if device_rule.window_minutes is None:
      raise ValueError("Device Velocity requires window minutes.")
  
  
    
  ip_transaction_count = count_transactions_by_ip(db= db, ip_address= transaction.ip_address, window_minutes= ip_rule.window_minutes) + 1
  device_transaction_count = count_transactions_by_device(db= db, device_id= transaction.device_id, window_minutes= device_rule.window_minutes) + 1 

  return evaluate_transaction(
    db=db,
    amount=transaction.amount,
    ip_address=transaction.ip_address,
    ip_transaction_count=ip_transaction_count,
    device_id=transaction.device_id,
    device_transaction_count=device_transaction_count,
  )

  