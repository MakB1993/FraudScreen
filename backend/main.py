from fastapi import FastAPI

from backend import models
from backend.routers import (
  transactions, health, rules, fraud_evaluations, dashboard, signals
)
from backend.database import Base, engine

from fastapi.middleware.cors import CORSMiddleware



Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(transactions.router)
app.include_router(rules.router)
app.include_router(fraud_evaluations.router)
app.include_router(dashboard.router)
app.include_router(signals.router)