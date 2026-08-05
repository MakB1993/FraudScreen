from fastapi import APIRouter, Depends, HTTPException, status,Query
from sqlalchemy.orm import Session
from backend import models
from backend.database import get_db
from backend.schemas import FraudRuleResponse, FraudRuleUpdate, TransactionCreate, FraudEvaluationResult
from backend.services.rule_service import get_all_rules, get_rule, update_rule
from backend.services.fraud_orchestration_service import run_fraud_evaluation

router = APIRouter(
    prefix="/rules",
    tags=["Rules"],
)


@router.get(
    "",
    response_model=list[FraudRuleResponse],
    status_code=status.HTTP_200_OK,
)
def list_rules(
    db: Session = Depends(get_db),
    limit: int = Query(10, ge=1, le=100, description="Number of records to return"),
    offset: int = Query(0, ge=0, description="Number of records to skip"),
) -> list[models.FraudRule]:

    rules = get_all_rules(db=db,limit=limit,offset=offset)

    return rules


@router.get(
    "/{rule_key}",
    response_model=FraudRuleResponse,
    status_code=status.HTTP_200_OK,
)
def get_rule_with_key(rule_key: str, db: Session = Depends(get_db)) -> models.FraudRule:
    rule = get_rule(db=db, rule_key=rule_key)
    if not rule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Fraud rule with ID {rule_key} not found",
        )
    return rule


@router.put(
    "/{rule_key}",
    response_model=FraudRuleResponse,
    status_code=status.HTTP_200_OK,
)
def update_rule_with_key(
    rule_key: str, rule_update: FraudRuleUpdate, db: Session = Depends(get_db)
) -> models.FraudRule:

    existing_rule = get_rule(db=db, rule_key=rule_key)
    if not existing_rule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Fraud rule with {rule_key} not found",
        )
    updated_rule = rule_update.model_dump(exclude_unset=True)

    try:
        return update_rule(
            db=db,
            rule=existing_rule,
            update_data=updated_rule,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )
    
#Adding rules/test endpoint
@router.post(
    "/test",
    response_model=FraudEvaluationResult
)
def test_transaction_result(
    transaction: TransactionCreate,
    db: Session= Depends(get_db),
) -> FraudEvaluationResult:

    test_result= run_fraud_evaluation(db= db, transaction=transaction)
    return test_result 
    

