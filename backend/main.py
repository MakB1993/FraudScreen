from fastapi import FastAPI

from backend import models
from backend.routers import transactions, health, rules, fraud_evaluations
from backend.database import Base, engine




Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(health.router)
app.include_router(transactions.router)
app.include_router(rules.router)
app.include_router(fraud_evaluations.router)