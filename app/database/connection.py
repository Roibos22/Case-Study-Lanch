# app/database/connection.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.database.config import db_settings

# Create the declarative base
Base = declarative_base()

# Create engine
engine = create_engine(db_settings.DATABASE_URL)

# Create sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

__all__ = ['Base', 'engine', 'SessionLocal', 'get_db']