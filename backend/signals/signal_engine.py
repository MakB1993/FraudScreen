from sqlalchemy.orm import Session
from datetime import datetime

from backend import models
from backend.schemas import TransactionCreate
from backend.signals.signal_config import SignalWindowConfig
from backend.services.transaction_service import (
    count_transactions_by_device,
    count_transactions_by_ip,
    count_transactions_by_card,
    has_customer_used_device_before,
    has_customer_used_card_before,
    has_customer_used_ip_before,
    count_distinct_customers_by_device,
    count_distinct_cards_by_device,
    count_distinct_customers_by_ip,
    count_distinct_cards_by_ip,
    count_transactions_by_customer,
    count_transactions_by_session,
    has_customer_used_ip_country_before,
    has_customer_used_card_country_before,
    count_distinct_ip_countries_by_customer,
    count_declined_transactions_by_customer,
    count_declined_transactions_by_card,
    count_declined_transactions_by_ip,
    count_distinct_cards_by_session,
    count_declined_transactions_by_session,
    has_authorized_after_declines_in_session,
    count_distinct_devices_by_customer,
    count_distinct_ips_by_customer,
)
from backend.signals.signal_context import SignalContext


def build_signal_context(
    db: Session,
    transaction: TransactionCreate | models.Transaction,
    reference_time: datetime,
    window_config: SignalWindowConfig,
) -> SignalContext:

    ip_velocity = count_transactions_by_ip(
        db=db,
        ip_address=transaction.ip_address,
        window_minutes=window_config.ip_velocity,
        reference_time=reference_time,
    )

    device_velocity = count_transactions_by_device(
        db=db,
        device_id=transaction.device_id,
        window_minutes=window_config.device_velocity,
        reference_time=reference_time,
    )

    card_velocity = count_transactions_by_card(
            db=db,
            card_fingerprint=transaction.card_fingerprint,
            window_minutes=window_config.card_velocity,
            reference_time=reference_time,
    )

    used_device_before = has_customer_used_device_before(
        db=db,
        customer_id=transaction.customer_id,
        device_id=transaction.device_id,
        reference_time=reference_time,
    )

    new_device = not used_device_before

    used_card_before = has_customer_used_card_before(
            db=db,
            customer_id=transaction.customer_id,
            card_fingerprint=transaction.card_fingerprint,
            reference_time=reference_time,
        )
    
    new_card = not used_card_before

    used_ip_before = has_customer_used_ip_before(
            db=db,
            customer_id=transaction.customer_id,
            ip_address=transaction.ip_address,
            reference_time=reference_time,
        )
    
    new_ip_for_customer = not used_ip_before

    distinct_customers_per_device = count_distinct_customers_by_device(
        db=db,
        device_id=transaction.device_id,
        reference_time=reference_time,
        window_minutes=window_config.relationship_counts,
    )

    distinct_cards_per_device = count_distinct_cards_by_device(
        db=db,
        device_id=transaction.device_id,
        reference_time=reference_time,
        window_minutes=window_config.relationship_counts,
    )

    distinct_customers_per_ip = count_distinct_customers_by_ip(
        db=db,
        ip_address=transaction.ip_address,
        reference_time=reference_time,
        window_minutes=window_config.relationship_counts,
    )

    distinct_cards_per_ip = count_distinct_cards_by_ip(
        db=db,
        ip_address=transaction.ip_address,
        reference_time=reference_time,
        window_minutes=window_config.relationship_counts,
    )

    customer_velocity = count_transactions_by_customer(
        db=db,
        customer_id=transaction.customer_id,
        reference_time=reference_time,
        window_minutes=window_config.customer_velocity,
    )

    if transaction.session_id is not None:
        session_velocity = count_transactions_by_session(
            db=db,
            session_id=transaction.session_id,
            reference_time=reference_time,
            window_minutes=window_config.session_velocity,
        )
    else:
        session_velocity = 0 # 0 here means "session unavailable"

    card_ip_country_mismatch = (
        transaction.card_country is not None
        and transaction.ip_country is not None
        and transaction.card_country != transaction.ip_country
    )

    if transaction.ip_country is not None:
        used_ip_country_before = has_customer_used_ip_country_before(
            db=db,
            customer_id=transaction.customer_id,
            ip_country=transaction.ip_country,
            reference_time=reference_time,
        )
        new_ip_country_for_customer = not used_ip_country_before
    else:
        new_ip_country_for_customer = False

    if transaction.card_country is not None:
        used_card_country_before = has_customer_used_card_country_before(
            db=db,
            customer_id=transaction.customer_id,
            card_country=transaction.card_country,
            reference_time=reference_time,
        )
        new_card_country_for_customer = not used_card_country_before
    else:
        new_card_country_for_customer = False

    distinct_ip_countries_per_customer = count_distinct_ip_countries_by_customer(
        db=db,
        customer_id=transaction.customer_id,
        reference_time=reference_time,
        window_minutes=window_config.country_velocity,
    )

    customer_decline_velocity = count_declined_transactions_by_customer(
        db=db,
        customer_id=transaction.customer_id,
        reference_time=reference_time,
        window_minutes=window_config.decline_velocity,
    )

    card_decline_velocity = count_declined_transactions_by_card(
        db=db,
        card_fingerprint=transaction.card_fingerprint,
        reference_time=reference_time,
        window_minutes=window_config.decline_velocity,
    )

    ip_decline_velocity = count_declined_transactions_by_ip(
        db=db,
        ip_address=transaction.ip_address,
        reference_time=reference_time,
        window_minutes=window_config.decline_velocity,
    )

    if transaction.session_id is not None:
        distinct_cards_per_session = count_distinct_cards_by_session(
            db=db,
            session_id=transaction.session_id,
            reference_time=reference_time,
            window_minutes=window_config.relationship_counts,
        )
    else:
        distinct_cards_per_session = 0

    if transaction.session_id is not None:
        declines_per_session = count_declined_transactions_by_session(
            db=db,
            session_id=transaction.session_id,
            reference_time=reference_time,
            window_minutes=window_config.decline_velocity,
        )

        authorized_after_declines_in_session = (
            transaction.transaction_status == "AUTHORIZED"
            and has_authorized_after_declines_in_session(
                db=db,
                session_id=transaction.session_id,
                reference_time=reference_time,
                window_minutes=window_config.decline_velocity,
            )
        )
    else:
        declines_per_session = 0
        authorized_after_declines_in_session = False

    distinct_devices_per_customer = count_distinct_devices_by_customer(
        db=db,
        customer_id=transaction.customer_id,
        reference_time=reference_time,
        window_minutes=window_config.relationship_counts,
    )

    distinct_ips_per_customer = count_distinct_ips_by_customer(
        db=db,
        customer_id=transaction.customer_id,
        reference_time=reference_time,
        window_minutes=window_config.relationship_counts,
    )

    return SignalContext(
        amount=transaction.amount,
        ip_velocity=ip_velocity,
        device_velocity=device_velocity,
        card_velocity=card_velocity,
        new_device=new_device,
        new_card=new_card,
        new_ip_for_customer=new_ip_for_customer,
        distinct_customers_per_device=distinct_customers_per_device,
        distinct_cards_per_device=distinct_cards_per_device,
        distinct_customers_per_ip=distinct_customers_per_ip,
        distinct_cards_per_ip=distinct_cards_per_ip,
        customer_velocity=customer_velocity,
        session_velocity=session_velocity,
        card_ip_country_mismatch=card_ip_country_mismatch,
        new_ip_country_for_customer=new_ip_country_for_customer,
        new_card_country_for_customer=new_card_country_for_customer,
        distinct_ip_countries_per_customer=distinct_ip_countries_per_customer,
        customer_decline_velocity=customer_decline_velocity,
        card_decline_velocity=card_decline_velocity,
        ip_decline_velocity=ip_decline_velocity,
        distinct_cards_per_session=distinct_cards_per_session,
        declines_per_session=declines_per_session,
        authorized_after_declines_in_session=authorized_after_declines_in_session,
        distinct_devices_per_customer=distinct_devices_per_customer,
        distinct_ips_per_customer=distinct_ips_per_customer,
    )