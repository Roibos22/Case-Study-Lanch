from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import db_settings

engine = create_engine(db_settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()