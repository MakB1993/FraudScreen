from backend.signals.signal_context import SignalContext
from backend import models
from backend.schemas import RuleResult

def get_signal_value(
    signal_context: SignalContext,
    signal_key: str,
) -> int | float | bool:

    if not hasattr(signal_context, signal_key):
        raise ValueError(f"Unknown signal: {signal_key}")

    return getattr(signal_context, signal_key)

def evaluate_condition(
    signal_value: int | float | bool,
    operator: str,
    comparison_value: int | float |bool,
) -> bool:

    if operator == ">":
        return signal_value > comparison_value

    if operator == ">=":
        return signal_value >= comparison_value

    if operator == "<":
        return signal_value < comparison_value

    if operator == "<=":
        return signal_value <= comparison_value

    if operator == "==":
        return signal_value == comparison_value

    if operator == "!=":
        return signal_value != comparison_value

    raise ValueError(f"Unsupported operator: {operator}")

def evaluate_dynamic_rule(
    rule: models.FraudRule,
    signal_context: SignalContext,
) -> RuleResult:

    if rule.signal_key is None:
        raise ValueError(
            f"Rule '{rule.rule_key}' has no signal_key."
        )

    if rule.operator is None:
        raise ValueError(
            f"Rule '{rule.rule_key}' has no operator."
        )

    signal_value = get_signal_value(
        signal_context=signal_context,
        signal_key=rule.signal_key,
    )

    comparison_value = (
        rule.comparison_value
        if rule.comparison_value is not None
        else rule.threshold_value
    )

    triggered = evaluate_condition(
        signal_value=signal_value,
        operator=rule.operator,
        comparison_value=comparison_value,
    )

    score = rule.score if triggered else 0

    reason = (
        f"{rule.signal_key} value {signal_value} "
        f"{rule.operator} {comparison_value}"
    )

    return RuleResult(
        rule_name=rule.rule_name,
        triggered=triggered,
        score=score,
        reason=reason,
    )

def evaluate_dynamic_rules(
    rules: list[models.FraudRule],
    signal_context: SignalContext,
) -> list[RuleResult]:

    results: list[RuleResult] = []

    for rule in rules:
        if not rule.enabled:
            continue

        result = evaluate_dynamic_rule(
            rule=rule,
            signal_context=signal_context,
        )

        results.append(result)

    return results

# if __name__ == "__main__":
#     from types import SimpleNamespace #SimpleNamespace is a small built-in Python utility that lets you quickly create an object with attributes
                                        
#     from backend.database import SessionLocal

#     db = SessionLocal()

#     try:
#         rule = (
#             db.query(models.FraudRule)
#             .filter(models.FraudRule.rule_key == "high_amount")
#             .first()
#         )

#         if rule is None:
#             raise ValueError("Rule not found")

#         print("Rule configuration:")
#         print("rule_key:", rule.rule_key)
#         print("signal_key:", rule.signal_key)
#         print("operator:", rule.operator)
#         print("comparison_value:", rule.comparison_value)
#         print("score:", rule.score)

#         signal_context = SimpleNamespace( #otw we would have to input all the attributes of SignalContext class, but with SimpleNamespace we can create an object with only the attributes we need for testing
#             new_device=True,
#         )

#         result = evaluate_dynamic_rule(
#             rule=rule,
#             signal_context=signal_context,
#         )

#         print("\nDynamic rule result:")
#         print("triggered:", result.triggered)
#         print("score:", result.score)
#         print("reason:", result.reason)

#     finally:
#         db.close()