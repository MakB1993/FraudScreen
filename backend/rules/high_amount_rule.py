from backend.schemas import RuleResult


def evaluate_high_amount(
    amount: float,
    threshold: float = 10000.0,
    score: int = 40,
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
    if amount > threshold:
        return RuleResult(
            rule_name="High Amount Rule",
            triggered=True,
            score=score,
            reason=f"Transaction amount {amount} exceeds the threshold of {threshold}.",
        )
    
    return RuleResult(
        rule_name="High Amount Rule",
        triggered=False,
        score=0,
        reason=f"Transaction amount {amount} does not exceed the threshold of {threshold}.",
    )