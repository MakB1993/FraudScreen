from backend import models
from backend.database import SessionLocal


def seed_rules() -> None:
    db = SessionLocal()

    try:
        initial_rules = [
            {
                "rule_key": "high_amount",
                "rule_name": "High Amount Rule",
                "signal_key": "amount",
                "operator": ">",
                "enabled": True,
                "threshold_value": 10000,
                "score": 50,
                "window_minutes": None,
            },
            {
                "rule_key": "ip_velocity",
                "rule_name": "IP Velocity Rule",
                "signal_key": "ip_velocity",
                "operator": ">",
                "enabled": True,
                "threshold_value": 3,
                "score": 40,
                "window_minutes": 15,
            },
            {
                "rule_key": "device_velocity",
                "rule_name": "Device Velocity Rule",
                "signal_key": "device_velocity",
                "operator": ">",
                "enabled": True,
                "threshold_value": 3,
                "score": 40,
                "window_minutes": 15,
            },
        ]

        for rule_data in initial_rules:
            existing_rule = (
                db.query(models.FraudRule)
                .filter(models.FraudRule.rule_key == rule_data["rule_key"])
                .first()
            )

            if existing_rule:
                existing_rule.signal_key = rule_data["signal_key"]
                existing_rule.operator = rule_data["operator"]

                print(f"Updated dynamic fields: {rule_data['rule_key']}")
                continue

            db.add(models.FraudRule(**rule_data))  #unpacking dictionary with **
            print(f"Added: {rule_data['rule_key']}")

        db.commit()
        print("Fraud rules seeded successfully.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_rules()