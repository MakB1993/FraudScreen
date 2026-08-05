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
    threshold_value: int | float,
) -> bool:

    if operator == ">":
        return signal_value > threshold_value

    if operator == ">=":
        return signal_value >= threshold_value

    if operator == "<":
        return signal_value < threshold_value

    if operator == "<=":
        return signal_value <= threshold_value

    if operator == "==":
        return signal_value == threshold_value

    if operator == "!=":
        return signal_value != threshold_value

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

    triggered = evaluate_condition(
        signal_value=signal_value,
        operator=rule.operator,
        threshold_value=rule.threshold_value,
    )

    score = rule.score if triggered else 0

    reason = (
        f"{rule.signal_key} value {signal_value} "
        f"{rule.operator} {rule.threshold_value}"
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

if __name__ == "__main__":
    from backend.database import SessionLocal

    db = SessionLocal()

    try:
        rules = db.query(models.FraudRule).all()

        signal_context = SignalContext(
            amount=12000,
            ip_velocity=5,
            device_velocity=1,
            card_velocity=1,
            new_device=False,
            new_card=False,
            new_ip_for_customer=False,
            distinct_customers_per_device=1,
            distinct_cards_per_device=1,
            distinct_customers_per_ip=1,
            distinct_cards_per_ip=1,
            customer_velocity=1,
            session_velocity=1,
            card_ip_country_mismatch=False,
            new_ip_country_for_customer=False,
            new_card_country_for_customer=False,
            distinct_ip_countries_per_customer=1,
            customer_decline_velocity=0,
            card_decline_velocity=0,
            ip_decline_velocity=0,
            distinct_cards_per_session=1,
            declines_per_session=0,
            authorized_after_declines_in_session=False,
            distinct_devices_per_customer=1,
            distinct_ips_per_customer=1,
        )

        results = evaluate_dynamic_rules(
            rules=rules,
            signal_context=signal_context,
        )

        total_score = 0

        for result in results:
            print(result)
            total_score += result.score

        print(f"Total score: {total_score}")

    finally:
        db.close()