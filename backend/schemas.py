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