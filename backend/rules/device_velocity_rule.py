from backend.schemas import RuleResult
from backend.services.rule_service import get_rule
from sqlalchemy.orm import Session

def evaluate_device_velocity(
    db: Session,
    device_id: str,
    device_transaction_count: int,
) -> RuleResult:
    
    """
    Evaluate the number of transactions from a specific device ID against a threshold.

    Args:
        device_id (str): The device ID to evaluate.
        device_transaction_count (int): The number of transactions from the device ID.

    Returns:
        RuleResult: The result of the evaluation.
    """
    
    rule = get_rule(db=db, rule_key="device_velocity")

    if not rule:
        raise ValueError("Device Velocity Rule not found in the database.")

    if not rule.enabled:
        return RuleResult(
            rule_name=rule.rule_name,
            triggered=False,
            score=0,
            reason=rule.rule_name + " is disabled.",
        )

    threshold = rule.threshold_value
    triggered = device_transaction_count >= threshold

    result_score = rule.score if triggered else 0

    reason = (
        f"Transaction count {device_transaction_count} from device "
        f"{device_id} meets or exceeds the threshold of {threshold}."
        if triggered
        else
        f"Transaction count {device_transaction_count} from device "
        f"{device_id} is below the threshold of {threshold}."
    )

    return RuleResult(
        rule_name=rule.rule_name,
        triggered=triggered,
        score=result_score,
        reason=reason,
    )