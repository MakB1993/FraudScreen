from pydantic import BaseModel

class TransactionCreate(BaseModel):
    transaction_id: str
    amount: float
    currency: str

class TransactionResponse(BaseModel):
    id: int
    transaction_id: str
    amount: float
    currency: str

    class Config:
        from_attributes = True