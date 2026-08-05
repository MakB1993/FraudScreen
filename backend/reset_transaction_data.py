from backend.database import SessionLocal
from backend import models


def reset_transaction_data() -> None:
    db = SessionLocal()

    try:
        transactions = db.query(models.Transaction).all()

        for transaction in transactions:
            db.delete(transaction)

        db.commit()

        print(f"Deleted {len(transactions)} transactions")
        print("Related fraud and rule evaluations deleted automatically")
        print("Transaction data reset successfully")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    reset_transaction_data()