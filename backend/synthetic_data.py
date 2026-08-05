import random
from datetime import datetime, timedelta, timezone
from uuid import uuid4

from backend.database import SessionLocal
from backend.schemas import TransactionCreate
from backend.services.transaction_orchestration_service import (
    create_transaction_service,
)


SyntheticTransaction = tuple[TransactionCreate, datetime]


# --------------------------------------------------
# Synthetic reference values
# --------------------------------------------------

PAYMENT_METHODS = [
    "CARD",
    "APPLE_PAY",
    "GOOGLE_PAY",
]

COUNTRIES = [
    "US",
    "GB",
    "IN",
    "AU",
    "DE",
    "CA",
]

TRANSACTION_TYPES = [
    "PURCHASE",
    "RENEWAL",
    "SUBSCRIPTION",
]

TRANSACTION_STATUSES = [
    "AUTHORIZED",
    "DECLINED",
]

USER_AGENTS = [
    "Chrome / Windows",
    "Chrome / macOS",
    "Safari / iPhone",
    "Chrome / Android",
    "Firefox / Windows",
]

CARD_BINS = [
    "411111",
    "424242",
    "555555",
    "378282",
]


# --------------------------------------------------
# Customer population
# --------------------------------------------------

def generate_customer_profiles(
    count: int = 1000,
) -> dict[str, dict]:
    profiles = {}

    for customer_number in range(
        1000,
        1000 + count,
    ):
        customer_id = f"CUST-{customer_number}"

        cards = [
            {
                "fingerprint": f"CARD-{uuid4().hex[:12]}",
                "bin": random.choice(CARD_BINS),
                "last_four": f"{random.randint(0, 9999):04d}",
                "country": random.choice(COUNTRIES),
            }
            for _ in range(
                random.randint(1, 3)
            )
        ]

        devices = [
            {
                "device_id": f"DEVICE-{uuid4().hex[:8]}",
                "user_agent": random.choice(USER_AGENTS),
            }
            for _ in range(
                random.randint(1, 3)
            )
        ]

        profiles[customer_id] = {
            "email": (
                f"customer{customer_number}"
                "@example.com"
            ),
            "cards": cards,
            "devices": devices,
        }

    return profiles


CUSTOMER_PROFILES = generate_customer_profiles()


# --------------------------------------------------
# Base transaction
# --------------------------------------------------

def generate_transaction() -> TransactionCreate:
    customer_id = random.choice(
        list(CUSTOMER_PROFILES.keys())
    )

    customer = CUSTOMER_PROFILES[
        customer_id
    ]

    card = random.choice(
        customer["cards"]
    )

    device = random.choice(
        customer["devices"]
    )

    return TransactionCreate(
        transaction_id=(
            f"TXN-{uuid4().hex[:10]}"
        ),

        transaction_type=random.choice(
            TRANSACTION_TYPES + [None]
        ),

        transaction_status=random.choice(
            TRANSACTION_STATUSES
        ),

        customer_id=customer_id,
        email=customer["email"],

        card_fingerprint=card[
            "fingerprint"
        ],
        card_bin=card["bin"],
        card_last_four=card[
            "last_four"
        ],

        payment_method=random.choice(
            PAYMENT_METHODS
        ),

        card_country=card["country"],

        ip_address=(
            f"192.168."
            f"{random.randint(1, 254)}."
            f"{random.randint(1, 254)}"
        ),

        ip_country=random.choice(
            COUNTRIES
        ),

        device_id=device[
            "device_id"
        ],

        user_agent=device[
            "user_agent"
        ],

        session_id=(
            f"SESSION-{uuid4().hex[:10]}"
        ),

        amount=round(
            random.uniform(10, 800),
            2,
        ),

        # Keep USD until fraud thresholds
        # become currency-aware.
        currency="USD",
    )


# --------------------------------------------------
# High amount
# --------------------------------------------------

def generate_high_amount_transaction(
) -> TransactionCreate:
    transaction = generate_transaction()

    transaction.amount = round(
        random.uniform(
            1200,
            5000,
        ),
        2,
    )

    return transaction


# --------------------------------------------------
# IP velocity
# --------------------------------------------------

def generate_ip_velocity_transactions(
    count: int = 5,
) -> list[TransactionCreate]:
    shared_ip = (
        f"192.168."
        f"{random.randint(1, 254)}."
        f"{random.randint(1, 254)}"
    )

    shared_ip_country = (
        random.choice(COUNTRIES)
    )

    transactions = []

    for _ in range(count):
        transaction = (
            generate_transaction()
        )

        transaction.ip_address = (
            shared_ip
        )

        transaction.ip_country = (
            shared_ip_country
        )

        transactions.append(
            transaction
        )

    return transactions


# --------------------------------------------------
# Device velocity
# --------------------------------------------------

def generate_device_velocity_transactions(
    count: int = 5,
) -> list[TransactionCreate]:
    shared_device_id = (
        f"DEVICE-{uuid4().hex[:8]}"
    )

    shared_user_agent = (
        random.choice(USER_AGENTS)
    )

    transactions = []

    for _ in range(count):
        transaction = (
            generate_transaction()
        )

        transaction.device_id = (
            shared_device_id
        )

        transaction.user_agent = (
            shared_user_agent
        )

        transactions.append(
            transaction
        )

    return transactions


# --------------------------------------------------
# High amount + IP velocity
# --------------------------------------------------

def generate_high_amount_ip_velocity_transactions(
    count: int = 5,
) -> list[TransactionCreate]:
    transactions = (
        generate_ip_velocity_transactions(
            count=count
        )
    )

    for transaction in transactions:
        transaction.amount = round(
            random.uniform(
                1200,
                5000,
            ),
            2,
        )

    return transactions


# --------------------------------------------------
# High amount + Device velocity
# --------------------------------------------------

def generate_high_amount_device_velocity_transactions(
    count: int = 5,
) -> list[TransactionCreate]:
    transactions = (
        generate_device_velocity_transactions(
            count=count
        )
    )

    for transaction in transactions:
        transaction.amount = round(
            random.uniform(
                1200,
                5000,
            ),
            2,
        )

    return transactions


# --------------------------------------------------
# IP + Device velocity
# --------------------------------------------------

def generate_ip_device_velocity_transactions(
    count: int = 5,
) -> list[TransactionCreate]:
    shared_ip = (
        f"192.168."
        f"{random.randint(1, 254)}."
        f"{random.randint(1, 254)}"
    )

    shared_ip_country = (
        random.choice(COUNTRIES)
    )

    shared_device = (
        f"DEVICE-{uuid4().hex[:8]}"
    )

    shared_user_agent = (
        random.choice(USER_AGENTS)
    )

    shared_session_id = (
        f"SESSION-{uuid4().hex[:10]}"
    )

    transactions = []

    for _ in range(count):
        transaction = (
            generate_transaction()
        )

        transaction.ip_address = (
            shared_ip
        )

        transaction.ip_country = (
            shared_ip_country
        )

        transaction.device_id = (
            shared_device
        )

        transaction.user_agent = (
            shared_user_agent
        )

        transaction.session_id = (
            shared_session_id
        )

        transactions.append(
            transaction
        )

    return transactions


# --------------------------------------------------
# High Amount + IP + Device velocity
# --------------------------------------------------

def generate_all_rules_transactions(
    count: int = 5,
) -> list[TransactionCreate]:
    transactions = (
        generate_ip_device_velocity_transactions(
            count=count
        )
    )

    for transaction in transactions:
        transaction.amount = round(
            random.uniform(
                1200,
                5000,
            ),
            2,
        )

    return transactions


# --------------------------------------------------
# Timestamp generation
# --------------------------------------------------

def generate_random_timestamp() -> datetime:
    now = datetime.now(
        timezone.utc
    )

    minutes_back = random.randint(
        0,
        29 * 24 * 60,
    )

    return now - timedelta(
        minutes=minutes_back
    )


def generate_velocity_base_timestamp(
    count: int = 5,
    interval_minutes: int = 2,
) -> datetime:
    now = datetime.now(
        timezone.utc
    )

    # Ensure the last transaction in a
    # velocity sequence does not fall
    # into the future.
    minimum_minutes_back = (
        count * interval_minutes
    )

    minutes_back = random.randint(
        minimum_minutes_back,
        29 * 24 * 60,
    )

    return now - timedelta(
        minutes=minutes_back
    )


def add_velocity_timestamps(
    transactions: list[
        TransactionCreate
    ],
    interval_minutes: int = 2,
) -> list[SyntheticTransaction]:
    base_timestamp = (
        generate_velocity_base_timestamp(
            count=len(transactions),
            interval_minutes=(
                interval_minutes
            ),
        )
    )

    timestamped_transactions = []

    for index, transaction in enumerate(
        transactions
    ):
        created_at = (
            base_timestamp
            + timedelta(
                minutes=(
                    index
                    * interval_minutes
                )
            )
        )

        timestamped_transactions.append(
            (
                transaction,
                created_at,
            )
        )

    return timestamped_transactions


# --------------------------------------------------
# Full 5,000 row dataset
# --------------------------------------------------

def generate_dataset(
) -> list[SyntheticTransaction]:
    transactions: list[
        SyntheticTransaction
    ] = []

    # --------------------------------------------------
    # Normal transactions
    # 3,200
    # --------------------------------------------------

    for _ in range(3200):
        transaction = (
            generate_transaction()
        )

        transactions.append(
            (
                transaction,
                generate_random_timestamp(),
            )
        )

    # --------------------------------------------------
    # High amount only
    # 400
    # --------------------------------------------------

    for _ in range(400):
        transaction = (
            generate_high_amount_transaction()
        )

        transactions.append(
            (
                transaction,
                generate_random_timestamp(),
            )
        )

    # --------------------------------------------------
    # IP velocity only
    # 60 groups × 5 = 300
    # --------------------------------------------------

    for _ in range(60):
        group = (
            generate_ip_velocity_transactions(
                count=5
            )
        )

        transactions.extend(
            add_velocity_timestamps(
                group
            )
        )

    # --------------------------------------------------
    # Device velocity only
    # 60 groups × 5 = 300
    # --------------------------------------------------

    for _ in range(60):
        group = (
            generate_device_velocity_transactions(
                count=5
            )
        )

        transactions.extend(
            add_velocity_timestamps(
                group
            )
        )

    # --------------------------------------------------
    # High amount + IP velocity
    # 50 groups × 5 = 250
    # --------------------------------------------------

    for _ in range(50):
        group = (
            generate_high_amount_ip_velocity_transactions(
                count=5
            )
        )

        transactions.extend(
            add_velocity_timestamps(
                group
            )
        )

    # --------------------------------------------------
    # High amount + Device velocity
    # 50 groups × 5 = 250
    # --------------------------------------------------

    for _ in range(50):
        group = (
            generate_high_amount_device_velocity_transactions(
                count=5
            )
        )

        transactions.extend(
            add_velocity_timestamps(
                group
            )
        )

    # --------------------------------------------------
    # IP velocity + Device velocity
    # 30 groups × 5 = 150
    # --------------------------------------------------

    for _ in range(30):
        group = (
            generate_ip_device_velocity_transactions(
                count=5
            )
        )

        transactions.extend(
            add_velocity_timestamps(
                group
            )
        )

    # --------------------------------------------------
    # High amount + IP velocity + Device velocity
    # 30 groups × 5 = 150
    # --------------------------------------------------

    for _ in range(30):
        group = (
            generate_all_rules_transactions(
                count=5
            )
        )

        transactions.extend(
            add_velocity_timestamps(
                group
            )
        )

    # Critical for time-window rules:
    #
    # Transactions must be inserted in
    # chronological order.
    #
    # Otherwise an older synthetic transaction
    # could be evaluated against transactions
    # that occurred in its "future".

    transactions.sort(
        key=lambda item: item[1]
    )

    return transactions


# --------------------------------------------------
# Database loader
# --------------------------------------------------

def save_dataset(
    transactions: list[
        SyntheticTransaction
    ],
) -> None:
    db = SessionLocal()

    try:
        for index, (
            transaction,
            created_at,
        ) in enumerate(
            transactions,
            start=1,
        ):
            create_transaction_service(
                db=db,
                transaction=transaction,
                created_at=created_at,
            )

            # create_transaction_service currently
            # creates the transaction and its fraud
            # evaluation through the existing service
            # flow.
            db.commit()

            if index % 500 == 0:
                print(
                    f"Loaded "
                    f"{index}/"
                    f"{len(transactions)}"
                )

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()

# --------------------------------------------------
# Script entry point
# --------------------------------------------------

# if __name__ == "__main__":
#     transactions = (
#         generate_dataset()
#     )

#     print(
#         f"Generated "
#         f"{len(transactions)} "
#         f"transactions"
#     )

#     save_dataset(
#         transactions
#     )

#     print(
#         "Dataset loaded successfully"
#     )



            # def generate_card_velocity_transactions(
            #     count: int = 3,
            # ) -> list[TransactionCreate]:
            #     customer_id = random.choice(
            #         list(CUSTOMER_PROFILES.keys())
            #     )

            #     customer = CUSTOMER_PROFILES[customer_id]
            #     shared_card = random.choice(customer["cards"])

            #     transactions = []

            #     for _ in range(count):
            #         transaction = generate_transaction()

            #         transaction.customer_id = customer_id
            #         transaction.email = customer["email"]

            #         transaction.card_fingerprint = shared_card["fingerprint"]
            #         transaction.card_bin = shared_card["bin"]
            #         transaction.card_last_four = shared_card["last_four"]
            #         transaction.card_country = shared_card["country"]

            #         transactions.append(transaction)

            #     return transactions


            # if __name__ == "__main__":
            #   group = generate_card_velocity_transactions(
            #       count=3
            #   )

            #   timestamped = add_velocity_timestamps(
            #       group,
            #       interval_minutes=2,
            #   )

            #   save_dataset(timestamped)



            # def generate_new_device_test_transactions(
            # ) -> list[TransactionCreate]:
            #     customer_id = random.choice(
            #         list(CUSTOMER_PROFILES.keys())
            #     )

            #     customer = CUSTOMER_PROFILES[customer_id]

            #     shared_device_id = f"DEVICE-{uuid4().hex[:8]}"
            #     shared_user_agent = random.choice(USER_AGENTS)

            #     transactions = []

            #     for _ in range(2):
            #         transaction = generate_transaction()

            #         transaction.customer_id = customer_id
            #         transaction.email = customer["email"]

            #         transaction.device_id = shared_device_id
            #         transaction.user_agent = shared_user_agent

            #         transactions.append(transaction)

            #     return transactions

            # if __name__ == "__main__":
            #   group = generate_new_device_test_transactions()

            #   timestamped = add_velocity_timestamps(
            #       group,
            #       interval_minutes=2,
            #   )

            #   save_dataset(timestamped)


def generate_relationship_signal_test_transactions() -> list[SyntheticTransaction]:
    base_time = datetime.now(timezone.utc) - timedelta(minutes=10)

    shared_device = "device_relationship_test"
    shared_ip = "192.168.100.200"
    shared_session = "session_relationship_test"

    transactions: list[SyntheticTransaction] = [
        (
            TransactionCreate(
                transaction_id="REL_TEST_001",
                customer_id="customer_A",
                email="customer_a@test.com",
                card_fingerprint="card_fp_A",
                card_bin="411111",
                card_last_four="1111",
                payment_method="CARD",
                card_country="US",
                ip_address=shared_ip,
                ip_country="US",
                device_id=shared_device,
                user_agent="Mozilla/5.0 Test",
                session_id=shared_session,
                amount=100.00,
                currency="USD",
                transaction_status="AUTHORIZED",
                transaction_type=None,
            ),
            base_time,
        ),
        (
            TransactionCreate(
                transaction_id="REL_TEST_002",
                customer_id="customer_B",
                email="customer_b@test.com",
                card_fingerprint="card_fp_B",
                card_bin="555555",
                card_last_four="2222",
                payment_method="CARD",
                card_country="US",
                ip_address=shared_ip,
                ip_country="US",
                device_id=shared_device,
                user_agent="Mozilla/5.0 Test",
                session_id=shared_session,
                amount=110.00,
                currency="USD",
                transaction_status="AUTHORIZED",
                transaction_type=None,
            ),
            base_time + timedelta(minutes=1),
        ),
        (
            TransactionCreate(
                transaction_id="REL_TEST_003",
                customer_id="customer_C",
                email="customer_c@test.com",
                card_fingerprint="card_fp_C",
                card_bin="400000",
                card_last_four="3333",
                payment_method="CARD",
                card_country="US",
                ip_address=shared_ip,
                ip_country="US",
                device_id=shared_device,
                user_agent="Mozilla/5.0 Test",
                session_id=shared_session,
                amount=120.00,
                currency="USD",
                transaction_status="AUTHORIZED",
                transaction_type=None,
            ),
            base_time + timedelta(minutes=2),
        ),
        (
            TransactionCreate(
                transaction_id="REL_TEST_004",
                customer_id="customer_A",
                email="customer_a@test.com",
                card_fingerprint="card_fp_A",
                card_bin="411111",
                card_last_four="1111",
                payment_method="CARD",
                card_country="US",
                ip_address=shared_ip,
                ip_country="US",
                device_id=shared_device,
                user_agent="Mozilla/5.0 Test",
                session_id=shared_session,
                amount=130.00,
                currency="USD",
                transaction_status="AUTHORIZED",
                transaction_type=None,
            ),
            base_time + timedelta(minutes=3),
        ),
    ]

    return transactions

if __name__ == "__main__":
      trasactions = (generate_relationship_signal_test_transactions())
      save_dataset(
        trasactions
    )

