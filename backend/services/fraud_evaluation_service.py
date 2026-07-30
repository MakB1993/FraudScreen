from sqlalchemy.orm import Session, selectinload
from backend import models
from backend.services.fraud_orchestration_service import run_fraud_evaluation

def create_fraud_evaluation(
    db: Session,
    db_transaction: models.Transaction
):
    
    fraud_result= run_fraud_evaluation(db=db, transaction=db_transaction)
    
    db_fraud_evaluation = models.FraudEvaluation(
        transaction_db_id=db_transaction.id,
        total_score=fraud_result.total_score,
        decision=fraud_result.decision,
    )
    db.add(db_fraud_evaluation)
    db.flush()  # Flush the session to generate the fraud evaluation ID without committing

    for rule_result in fraud_result.rule_results:
        db_rule_evaluation = models.RuleEvaluation(
            fraud_evaluation_id=db_fraud_evaluation.id,
            rule_name=rule_result.rule_name,
            triggered=rule_result.triggered,
            score=rule_result.score,
            reason=rule_result.reason,
        )
        db.add(db_rule_evaluation)

    db.commit()  # Commit both the fraud evaluation and rule evaluations together
    db.refresh(db_fraud_evaluation)
    return db_fraud_evaluation

def get_all_fraud_evaluations(
        db: Session,
        decision: str | None,
        min_score: int | None,
        max_score: int | None,
        limit: int,
        offset: int,
) -> list[models.FraudEvaluation]:
    query = db.query(models.FraudEvaluation).options(selectinload(models.FraudEvaluation.rule_evaluations))
    if decision:
        query = query.filter(models.FraudEvaluation.decision == decision)
    if min_score is not None:
        query = query.filter(models.FraudEvaluation.total_score >= min_score)
    if max_score is not None:
        query = query.filter(models.FraudEvaluation.total_score <= max_score)

    evaluations = (
        query.order_by(models.FraudEvaluation.id.desc()).offset(offset).limit(limit).all()
    )

    return evaluations

def get_fraud_evaluation(
        db:Session,
        id:int,
) -> models.FraudEvaluation | None:
    return (
        db.query(models.FraudEvaluation)
        .options(selectinload(models.FraudEvaluation.rule_evaluations))
        .filter(models.FraudEvaluation.id==id)
        .first()
    )

