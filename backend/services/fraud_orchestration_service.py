from sqlalchemy.orm import Session

from backend import models
from backend.schemas import TransactionCreate,FraudEvaluationResult
from backend.signals.signal_engine import build_signal_context
from backend.services.fraud_engine import evaluate_transaction
from backend.services.rule_service import get_rule
from backend.signals.signal_config import SignalWindowConfig

from backend.rules.dynamic_rule_engine import evaluate_dynamic_rules

from datetime import datetime, timezone


def run_fraud_evaluation(
        db: Session,
        transaction: TransactionCreate | models.Transaction,
        reference_time: datetime | None = None,
    ) -> FraudEvaluationResult:

    if reference_time is None:
        if isinstance(transaction, models.Transaction):
            reference_time = transaction.created_at
        else:
            reference_time = datetime.now(timezone.utc)

    ip_rule = get_rule(db=db, rule_key='ip_velocity')
    device_rule = get_rule(db=db, rule_key='device_velocity')
    
    if ip_rule is None:
        raise ValueError("IP Velocity rule not found!")
    if ip_rule.window_minutes is None:
        raise ValueError("IP Velocity requires window minutes.")
    
    if device_rule is None:
        raise ValueError("Device Velocity rule not found!")
    if device_rule.window_minutes is None:
        raise ValueError("Device Velocity requires window minutes.")

    window_config = SignalWindowConfig(
        ip_velocity=ip_rule.window_minutes,
        device_velocity=device_rule.window_minutes,
    )
        
    signal_context = build_signal_context(
            db=db,
            transaction=transaction,
            reference_time=reference_time,
            window_config=window_config,
        )

    high_amount_rule = get_rule(db=db, rule_key="high_amount")
    if high_amount_rule is None:
        raise ValueError("High Amount rule not found!")
    dynamic_results = evaluate_dynamic_rules(
        rules=[
            high_amount_rule,
            ip_rule,
            device_rule,
        ],
        signal_context=signal_context,
    )

    print("----- DYNAMIC RULE SHADOW -----")

    for result in dynamic_results:
        print(
            result.rule_name,
            result.triggered,
            result.score,
            result.reason,
        )
    
    return evaluate_transaction(
        db=db,
        signal_context=signal_context,
        ip_address=transaction.ip_address,
        device_id=transaction.device_id,
    )

if __name__ == "__main__":
    from backend.database import SessionLocal
    from backend.signals.signal_context import SignalContext

    db = SessionLocal()

    try:
        high_amount_rule = get_rule(db=db, rule_key="high_amount")
        ip_rule = get_rule(db=db, rule_key="ip_velocity")
        device_rule = get_rule(db=db, rule_key="device_velocity")

        if high_amount_rule is None:
            raise ValueError("High Amount rule not found.")

        if ip_rule is None:
            raise ValueError("IP Velocity rule not found.")

        if device_rule is None:
            raise ValueError("Device Velocity rule not found.")

        test_contexts = [
            (
                "NORMAL",
                SignalContext(
                    amount=500,
                    ip_velocity=1,
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
                ),
            ),
            (
                "HIGH AMOUNT",
                SignalContext(
                    amount=12000,
                    ip_velocity=1,
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
                ),
            ),
            (
                "VELOCITY",
                SignalContext(
                    amount=500,
                    ip_velocity=5,
                    device_velocity=5,
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
                ),
            ),
            (
                "COMBINED",
                SignalContext(
                    amount=12000,
                    ip_velocity=5,
                    device_velocity=5,
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
                ),
            ),
        ]

        for test_name, signal_context in test_contexts:
            print(f"\n===== {test_name} =====")

            dynamic_results = evaluate_dynamic_rules(
                rules=[
                    high_amount_rule,
                    ip_rule,
                    device_rule,
                ],
                signal_context=signal_context,
            )

            dynamic_total = sum(
                result.score for result in dynamic_results
            )

            for result in dynamic_results:
                print(
                    result.rule_name,
                    "triggered=",
                    result.triggered,
                    "score=",
                    result.score,
                )

            print("Dynamic total:", dynamic_total)

    finally:
        db.close()
  