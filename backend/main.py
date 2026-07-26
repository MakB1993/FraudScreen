from fastapi import Depends, FastAPI, status, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend.routers import transactions, health
from backend.schemas import TransactionCreate,TransactionResponse
from backend import models #importing it causes Python to execute models.py. That registers Transaction with Base.metadata. Without importing the model, SQLAlchemy might not know the table exists.
from backend.database import Base, engine, get_db




Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(health.router)
app.include_router(transactions.router)