from sqlalchemy.orm import Session
from backend import models

def get_rule(
    db: Session,
    rule_key: str,
) -> models.FraudRule | None:
    return (
        db.query(models.FraudRule)
        .filter(models.FraudRule.rule_key == rule_key)
        .first()
    )

def get_all_rules(
    db: Session,
    limit:int,
    offset:int
) -> list[models.FraudRule]:
    return (
        db.query(models.FraudRule)
        .order_by(models.FraudRule.rule_name.asc())
        .offset(offset)
        .limit(limit)   
        .all()
    )

def update_rule(
    db: Session,
    rule: models.FraudRule,
    update_data: dict,
) -> models.FraudRule:
    
    # if enabled is not None:
    #     rule.enabled = enabled
    # if threshold_value is not None:
    #     rule.threshold_value = threshold_value
    # if score is not None:
    #     rule.score = score
    # if window_minutes is not None:
    #     rule.window_minutes = window_minutes
    #instead of above commented code, we can use setattr to update the attributes dynamically based on the keys in the update_data dictionary. This way, we can avoid writing multiple if statements for each attribute.

    if rule.rule_key == "high_amount":
        if (
            "window_minutes" in update_data
            and update_data["window_minutes"] is not None
        ):
            raise ValueError(
                "High Amount Rule does not support window_minutes."
            )

    if rule.rule_key in {"ip_velocity", "device_velocity"}:
        if (
            "window_minutes" in update_data
            and update_data["window_minutes"] is None
        ):
            raise ValueError(
                "Velocity rules require window_minutes."
            )

    for field, value in update_data.items():
        setattr(rule, field, value)


    for key, value in update_data.items():
        setattr(rule, key, value)

    db.commit()
    db.refresh(rule)
    return rule
