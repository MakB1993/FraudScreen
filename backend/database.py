from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker #object relational mapping
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./fraudscreen.db"
)  # Using SQLite for local; replaced with database URL in prod

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(
  autocommit=False,
  autoflush=False, 
  bind=engine
  )

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()