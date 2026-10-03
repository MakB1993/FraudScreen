import os
import sqlite3

from sqlalchemy import create_engine, text

from backend.models import (
    Transaction,
    FraudEvaluation,
    RuleEvaluation,
    FraudRule,
)


# ---------------------------------------------------------
# 1. Configuration
# ---------------------------------------------------------

SQLITE_DB_PATH = "fraudscreen.db"

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")


# ---------------------------------------------------------
# 2. Connect to SQLite
# ---------------------------------------------------------

sqlite_conn = sqlite3.connect(SQLITE_DB_PATH)

# Makes rows accessible using their column names
sqlite_conn.row_factory = sqlite3.Row

cursor = sqlite_conn.cursor()


# ---------------------------------------------------------
# 3. Read existing SQLite data
# ---------------------------------------------------------

cursor.execute("SELECT * FROM transactions")
transactions = cursor.fetchall()

cursor.execute("SELECT * FROM fraud_evaluations")
fraud_evaluations = cursor.fetchall()

cursor.execute("SELECT * FROM rule_evaluations")
rule_evaluations = cursor.fetchall()

cursor.execute("SELECT * FROM fraud_rules")
fraud_rules = cursor.fetchall()


print("SQLite data found:")
print(f"  transactions:       {len(transactions)}")
print(f"  fraud_evaluations:  {len(fraud_evaluations)}")
print(f"  rule_evaluations:   {len(rule_evaluations)}")
print(f"  fraud_rules:        {len(fraud_rules)}")


# ---------------------------------------------------------
# 4. Connect to PostgreSQL
# ---------------------------------------------------------

postgres_engine = create_engine(DATABASE_URL)


# ---------------------------------------------------------
# 5. Safety check
# ---------------------------------------------------------

tables = [
    "transactions",
    "fraud_evaluations",
    "rule_evaluations",
    "fraud_rules",
]

with postgres_engine.connect() as connection:

    for table in tables:

        result = connection.execute(
            text(f"SELECT COUNT(*) FROM {table}")
        )

        count = result.scalar()

        if count != 0:
            raise RuntimeError(
                f"Migration stopped: PostgreSQL table "
                f"'{table}' already contains {count} rows."
            )


print("Destination tables are empty. Starting migration...")


# ---------------------------------------------------------
# 6. Copy data
# ---------------------------------------------------------

with postgres_engine.begin() as connection:

    # Parent table first
    connection.execute(
        Transaction.__table__.insert(),
        [dict(row) for row in transactions],
    )

    # Depends on transactions
    connection.execute(
        FraudEvaluation.__table__.insert(),
        [dict(row) for row in fraud_evaluations],
    )

    # Depends on fraud_evaluations
    connection.execute(
        RuleEvaluation.__table__.insert(),
        [dict(row) for row in rule_evaluations],
    )

    # Independent table
    connection.execute(
        FraudRule.__table__.insert(),
        [dict(row) for row in fraud_rules],
    )


print("Data migration completed.")


# ---------------------------------------------------------
# 7. Verify PostgreSQL row counts
# ---------------------------------------------------------

print("\nPostgreSQL data:")

with postgres_engine.connect() as connection:

    for table in tables:

        result = connection.execute(
            text(f"SELECT COUNT(*) FROM {table}")
        )

        count = result.scalar()

        print(f"  {table}: {count}")


# ---------------------------------------------------------
# 8. Close SQLite connection
# ---------------------------------------------------------

sqlite_conn.close()

print("\nMigration finished successfully.")