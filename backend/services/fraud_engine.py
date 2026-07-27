from backend.schemas import RuleResult,FraudEvaluation
from backend.rules.high_amount_rule import evaluate_high_amount

def evaluate_transaction(amount: float,) -> FraudEvaluation:
    """
    Evaluate a transaction against all defined rules.

    Args:
        amount (float): The transaction amount.

    Returns:
        FraudEvaluation: An evaluation of the transaction based on all defined rules.
    """
    rules=[evaluate_high_amount,]
    results: list[RuleResult] = []   # Add more rule functions here as needed
    for rule in rules:
        result = rule(amount)
        results.append(result)
    
    # Add more rule evaluations here as needed

    total_score = sum(result.score for result in results)
    if total_score >= 70:
        decision = "REJECT"
    elif total_score >= 30:
        decision = "REVIEW"
    else:
        decision = "APPROVE"

    return FraudEvaluation(
        total_score=total_score,
        decision=decision,
        rule_results=results
    )