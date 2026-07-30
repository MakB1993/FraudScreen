from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

class TransactionCreate(BaseModel):
    transaction_id: str
    customer_id: str
    email: str
    card_bin: str
    card_last_four: str
    ip_address: str
    device_id: str
    amount: float
    currency: str

class TransactionResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    transaction_id: str
    customer_id: str
    email: str
    card_bin: str
    card_last_four: str
    ip_address: str
    device_id: str
    amount: float
    currency: str
    created_at: datetime

class TransactionUpdate(BaseModel):
    amount: float | None = None
    currency: str | None = None

class RuleResult(BaseModel): #becoz dict have no validation and we want to validate the response from rules
    rule_name: str
    triggered: bool
    score: int
    reason: str

class FraudEvaluationResult(BaseModel):
    total_score: int
    decision: str
    rule_results: list[RuleResult]

class RuleEvaluationResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    fraud_evaluation_id: int
    rule_name: str
    triggered: bool
    score: int
    reason: str

class FraudEvaluationResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    transaction_db_id: int
    total_score: int
    decision: str
    rule_evaluations: list[RuleEvaluationResponse]

class FraudRuleCreate(BaseModel):
    rule_key: str
    rule_name: str
    enabled: bool = True
    threshold_value: int
    score: int
    window_minutes: int | None = None

class FraudRuleResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    rule_key: str
    rule_name: str
    enabled: bool
    threshold_value: int
    score: int
    window_minutes: int | None = None

class FraudRuleUpdate(BaseModel):
    enabled: bool | None = None
    threshold_value: int | None = Field(default= None, gt= 0)
    score: int | None = Field(default= None, ge= 0)
    window_minutes: int | None = Field(default= None, gt= 0)