from dataclasses import dataclass, fields

from backend.signals.signal_context import SignalContext

NUMERIC_OPERATORS = (
    ">",
    ">=",
    "<",
    "<=",
    "==",
    "!=",
)

BOOLEAN_OPERATORS = (
    "==",
    "!=",
)

@dataclass(frozen=True)
class SignalDefinition:
    display_name: str
    data_type: str
    category: str
    uses_window: bool
    description: str

AVAILABLE_SIGNALS = {
    field.name
    for field in fields(SignalContext)
}

SIGNAL_DEFINITIONS = {
    "amount": SignalDefinition(
        display_name="Transaction Amount",
        data_type="float",
        category="Transaction",
        uses_window=False,
        description="Transaction amount being evaluated.",
    ),
    "ip_velocity": SignalDefinition(
        display_name="IP Velocity",
        data_type="integer",
        category="Velocity",
        uses_window=True,
        description="Number of transactions from the same IP address within the configured time window.",
    ),
    "device_velocity": SignalDefinition(
        display_name="Device Velocity",
        data_type="integer",
        category="Velocity",
        uses_window=True,
        description="Number of transactions from the same device within the configured time window.",
    ),
    "card_velocity": SignalDefinition(
        display_name="Card Velocity",
        data_type="integer",
        category="Velocity",
        uses_window=True,
        description="Number of transactions using the same card fingerprint within the configured time window.",
    ),
    "new_device": SignalDefinition(
        display_name="New Device",
        data_type="boolean",
        category="Customer History",
        uses_window=False,
        description="Whether the customer has not used this device before the current transaction.",
    ),
    "new_card": SignalDefinition(
        display_name="New Card",
        data_type="boolean",
        category="Customer History",
        uses_window=False,
        description="Whether the customer has not used this card fingerprint before the current transaction.",
    ),
    "new_ip_for_customer": SignalDefinition(
        display_name="New IP for Customer",
        data_type="boolean",
        category="Customer History",
        uses_window=False,
        description="Whether the customer has not used this IP address before the current transaction.",
    ),
    "customer_velocity": SignalDefinition(
        display_name="Customer Velocity",
        data_type="integer",
        category="Velocity",
        uses_window=True,
        description="Number of transactions from the same customer within the configured time window.",
    ),
    "distinct_customers_per_device": SignalDefinition(
        display_name="Distinct Customers per Device",
        data_type="integer",
        category="Relationship",
        uses_window=True,
        description="Number of distinct customers associated with the same device within the configured time window.",
    ),
    "distinct_cards_per_device": SignalDefinition(
        display_name="Distinct Cards per Device",
        data_type="integer",
        category="Relationship",
        uses_window=True,
        description="Number of distinct card fingerprints used on the same device within the configured time window.",
    ),
    "distinct_customers_per_ip": SignalDefinition(
        display_name="Distinct Customers per IP",
        data_type="integer",
        category="Relationship",
        uses_window=True,
        description="Number of distinct customers associated with the same IP address within the configured time window.",
    ),
    "distinct_cards_per_ip": SignalDefinition(
        display_name="Distinct Cards per IP",
        data_type="integer",
        category="Relationship",
        uses_window=True,
        description="Number of distinct card fingerprints used from the same IP address within the configured time window.",
    ),
    "session_velocity": SignalDefinition(
        display_name="Session Velocity",
        data_type="integer",
        category="Session",
        uses_window=True,
        description="Number of transactions associated with the same session within the configured time window.",
    ),
    "distinct_cards_per_session": SignalDefinition(
        display_name="Distinct Cards per Session",
        data_type="integer",
        category="Session",
        uses_window=True,
        description="Number of distinct card fingerprints used within the same session during the configured time window.",
    ),
    "declines_per_session": SignalDefinition(
        display_name="Declines per Session",
        data_type="integer",
        category="Session",
        uses_window=True,
        description="Number of declined transactions within the same session during the configured time window.",
    ),
    "authorized_after_declines_in_session": SignalDefinition(
        display_name="Authorized After Declines in Session",
        data_type="boolean",
        category="Session",
        uses_window=True,
        description="Whether an authorized transaction occurred after one or more declines in the same session within the configured time window.",
    ),
    "card_ip_country_mismatch": SignalDefinition(
        display_name="Card and IP Country Mismatch",
        data_type="boolean",
        category="Geography",
        uses_window=False,
        description="Whether the card country and IP country differ for the current transaction.",
    ),
    "new_ip_country_for_customer": SignalDefinition(
        display_name="New IP Country for Customer",
        data_type="boolean",
        category="Geography",
        uses_window=False,
        description="Whether the customer has not previously used the current IP country before the current transaction.",
    ),
    "new_card_country_for_customer": SignalDefinition(
        display_name="New Card Country for Customer",
        data_type="boolean",
        category="Geography",
        uses_window=False,
        description="Whether the customer has not previously used the current card country before the current transaction.",
    ),
    "distinct_ip_countries_per_customer": SignalDefinition(
        display_name="Distinct IP Countries per Customer",
        data_type="integer",
        category="Geography",
        uses_window=True,
        description="Number of distinct IP countries associated with the customer within the configured time window.",
    ),
    "customer_decline_velocity": SignalDefinition(
        display_name="Customer Decline Velocity",
        data_type="integer",
        category="Declines",
        uses_window=True,
        description="Number of declined transactions for the same customer within the configured time window.",
    ),
    "card_decline_velocity": SignalDefinition(
        display_name="Card Decline Velocity",
        data_type="integer",
        category="Declines",
        uses_window=True,
        description="Number of declined transactions using the same card fingerprint within the configured time window.",
    ),
    "ip_decline_velocity": SignalDefinition(
        display_name="IP Decline Velocity",
        data_type="integer",
        category="Declines",
        uses_window=True,
        description="Number of declined transactions from the same IP address within the configured time window.",
    ),
    "distinct_devices_per_customer": SignalDefinition(
        display_name="Distinct Devices per Customer",
        data_type="integer",
        category="Relationship",
        uses_window=True,
        description="Number of distinct devices associated with the same customer within the configured time window.",
    ),
    "distinct_ips_per_customer": SignalDefinition(
        display_name="Distinct IPs per Customer",
        data_type="integer",
        category="Relationship",
        uses_window=True,
        description="Number of distinct IP addresses associated with the same customer within the configured time window.",
    ),
}

        # SignalContext → every signal must have metadata
        # Metadata → every key must exist in SignalContext

METADATA_SIGNALS = set(SIGNAL_DEFINITIONS)

UNKNOWN_METADATA_SIGNALS = METADATA_SIGNALS - AVAILABLE_SIGNALS
MISSING_METADATA_SIGNALS = AVAILABLE_SIGNALS - METADATA_SIGNALS

if UNKNOWN_METADATA_SIGNALS:
    raise ValueError(
        f"Signal metadata contains unknown signals: {UNKNOWN_METADATA_SIGNALS}"
    )

if MISSING_METADATA_SIGNALS:
    raise ValueError(
        f"Signals are missing metadata: {MISSING_METADATA_SIGNALS}"
    )


#registry helpers
def get_signal_definition(signal_key: str) -> SignalDefinition:
    try:
        return SIGNAL_DEFINITIONS[signal_key]
    except KeyError:
        raise ValueError(f"Unknown signal '{signal_key}'")


def get_all_signal_definitions() -> dict[str, SignalDefinition]:
    return SIGNAL_DEFINITIONS.copy()

# returns allowed operators based on a signal's data_type. used for schema validation and frontend dropdown population.
def get_allowed_operators(signal_key: str) -> tuple[str, ...]:
    definition = get_signal_definition(signal_key)

    if definition.data_type in {"integer", "float"}:
        return NUMERIC_OPERATORS

    if definition.data_type == "boolean":
        return BOOLEAN_OPERATORS

    raise ValueError(
        f"Unsupported data type '{definition.data_type}' "
        f"for signal '{signal_key}'"
    )

# backend validation of signal/operator compatibility.
def is_operator_allowed(
    signal_key: str,
    operator: str,
) -> bool:
    allowed_operators = get_allowed_operators(signal_key)

    return operator in allowed_operators


def is_comparison_value_valid(
    signal_key: str,
    comparison_value: int | float | bool,
) -> bool:
    definition = get_signal_definition(signal_key)

    if definition.data_type == "boolean":
        return isinstance(comparison_value, bool)

    if definition.data_type == "integer":
        return (
            isinstance(comparison_value, int)
            and not isinstance(comparison_value, bool)  #because bool is a subclass of int in Python, we need to explicitly exclude bool values when checking for integer type.
        )

    if definition.data_type == "float":
        return (
            isinstance(comparison_value, (int, float))
            and not isinstance(comparison_value, bool)
        )

    return False