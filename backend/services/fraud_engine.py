from backend.schemas import RuleResult,FraudEvaluationResult
from backend.rules.high_amount_rule import evaluate_high_amount
from backend.rules.velocity_rule import evaluate_ip_velocity
from backend.rules.device_velocity_rule import evaluate_device_velocity
from backend.signals.signal_context import SignalContext
from sqlalchemy.orm import Session

def evaluate_transaction(
        db: Session,
        signal_context: SignalContext,
        ip_address: str,
        device_id: str,
    ) -> FraudEvaluationResult:
    """
    Evaluate a transaction against all defined rules.

    Args:
        amount (float): The transaction amount.
        ip_address (str): The IP address of the transaction.
        ip_transaction_count (int): The number of transactions from the IP address.
        device_id (str): The device ID of the transaction.
        device_transaction_count (int): The number of transactions from the device ID.

    Returns:
        FraudEvaluationResult: An evaluation of the transaction based on all defined rules.
    """


    results: list[RuleResult] = [
        evaluate_high_amount(db=db, amount=signal_context.amount),
        evaluate_ip_velocity(db=db, ip_address=ip_address, ip_transaction_count=signal_context.ip_velocity),
        evaluate_device_velocity(db=db, device_id=device_id, device_transaction_count=signal_context.device_velocity)    
    ]   # Add more rule functions here as needed
    
    

    total_score = sum(result.score for result in results)
    if total_score >= 70:
        decision = "REJECT"
    elif total_score >= 45:
        decision = "REVIEW"
    else:
        decision = "APPROVE"

    return FraudEvaluationResult(
        total_score=total_score,
        decision=decision,
        rule_results=results
    )