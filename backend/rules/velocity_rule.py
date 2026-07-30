from backend.schemas import RuleResult
from backend.services.rule_service import get_rule
from sqlalchemy.orm import Session

def evaluate_ip_velocity(
    db: Session,
    ip_address: str,
    ip_transaction_count: int,
) -> RuleResult:
    
    """
    Evaluate IP transaction velocity using the rule configuration stored
    in the database.

    Args:
        db: Active SQLAlchemy database session.
        ip_address: IP address being evaluated.
        ip_transaction_count: Number of transactions from the IP address
            within the configured time window.

    Returns:
        The result of the IP velocity rule evaluation.

    Raises:
        ValueError: If the rule configuration does not exist.
    """

    rule = get_rule(db=db, rule_key="ip_velocity")

    if not rule:
        raise ValueError("IP Velocity Rule not found in the database.")

    if not rule.enabled:
        return RuleResult(
            rule_name=rule.rule_name,
            triggered=False,
            score=0,
            reason=rule.rule_name + " is disabled.",
        )

    threshold = rule.threshold_value
    score = rule.score

    triggered = ip_transaction_count >= threshold

    result_score = score if triggered else 0

    reason = (
        f"Number of transactions {ip_transaction_count} from IP address {ip_address} "
        f"meets or exceeds the threshold of {threshold}."
        if triggered
        else
        f"Number of transactions {ip_transaction_count} from IP address {ip_address} "
        f"does not exceed the threshold of {threshold}."
    )

    return RuleResult(
        rule_name=rule.rule_name,
        triggered=triggered,
        score=result_score,
        reason=reason,
    )