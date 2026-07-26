from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker #object relational mapping

DATABASE_URL = "sqlite:///./fraudscreen.db"  # Using SQLite for demonstration; replace with your database URL

engine = create_engine(
  DATABASE_URL,
  connect_args={"check_same_thread": False}  # Needed for SQLite not for postgres or mysql
  )
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