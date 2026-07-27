from pydantic import BaseModel, ConfigDict

class TransactionCreate(BaseModel):
    transaction_id: str
    amount: float
    currency: str

class TransactionResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    transaction_id: str
    amount: float
    currency: str

class TransactionUpdate(BaseModel):
    amount: float | None = None
    currency: str | None = None

class RuleResult(BaseModel): #becoz dict have no validation and we want to validate the response from rules
    rule_name: str
    triggered: bool
    score: int
    reason: str

class FraudEvaluation(BaseModel):
    total_score: int
    decision: str
    rule_results: list[RuleResult]