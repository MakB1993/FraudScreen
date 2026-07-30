from fastapi import APIRouter,status,Depends,HTTPException,Query
from sqlalchemy.orm import Session

from backend import models
from backend.database import get_db
from backend.schemas import FraudEvaluationResponse
from backend.services.fraud_evaluation_service import get_all_fraud_evaluations, get_fraud_evaluation



router=APIRouter(
    prefix="/fraud-evaluations",
    tags=["Fraud Evaluations"]
)

@router.get(
    "",
    response_model=list[FraudEvaluationResponse],
    status_code=status.HTTP_200_OK,
)
def list_fraud_evaluations(
    db: Session= Depends(get_db),
    decision: str | None = Query(None, description="Filter evaluations by decision"),
    min_score: int |None = Query(
        None,
        description="Filter transactions with total score greater than or equal to this value",
    ),
    max_score: int |None = Query(
        None,
        description="Filter transactions with score less than or equal to this value",
    ),
    limit: int = Query(10, ge=1, le=100, description="Number of records to return"),
    offset: int = Query(0, ge=0, description="Number of records to skip"),
) -> list[models.FraudEvaluation]:

    
    if min_score is not None and max_score is not None and min_score > max_score:
          raise HTTPException(
              status_code=status.HTTP_400_BAD_REQUEST,
              detail="min_score cannot be greater than max_score",
          )
    return get_all_fraud_evaluations(
         db=db,
         decision=decision,
         min_score=min_score,
         max_score=max_score,
         limit=limit,
         offset=offset
    )

@router.get(
    "/{id}",
    response_model=FraudEvaluationResponse,
    status_code=status.HTTP_200_OK,
)
def fraud_evaluation_by_id(
    id: int,
    db: Session= Depends(get_db),
  
) -> models.FraudEvaluation:
  
    evaluation = get_fraud_evaluation(db=db,id=id)

    if not evaluation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Fraud Evaluation with ID {id} not found",
          )
    
    return evaluation

