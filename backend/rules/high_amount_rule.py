from backend.schemas import RuleResult
from backend.services.rule_service import get_rule
from sqlalchemy.orm import Session


def evaluate_high_amount(
    db: Session,
    amount: float,
) -> RuleResult:
    """
    Evaluate the transaction amount against a threshold.

    Args:
        amount (float): The transaction amount.
        threshold (float, optional): The threshold for high amounts. Defaults to 10000.0.
        score (int, optional): The score to return if the amount exceeds the threshold. Defaults to 40.

    Returns:
        int: The score if the amount exceeds the threshold, otherwise 0.
    """

    rule = get_rule(db=db, rule_key="high_amount")

    if not rule:
        raise ValueError("High Amount Rule not found in the database.")

    if not rule.enabled:
        return RuleResult(
            rule_name=rule.rule_name,
            triggered=False,
            score=0,
            reason=rule.rule_name + " is disabled.",
        )
    
    if amount > rule.threshold_value:
        return RuleResult(
            rule_name=rule.rule_name,
            triggered=True,
            score=rule.score,
            reason=f"Transaction amount {amount} exceeds the threshold of {rule.threshold_value}.",
        )
    
    return RuleResult(
        rule_name=rule.rule_name,
        triggered=False,
        score=0,
        reason=f"Transaction amount {amount} does not exceed the threshold of {rule.threshold_value}.",
    )