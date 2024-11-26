# app/database/init_db.py
from sqlalchemy import create_engine, inspect
from sqlalchemy.exc import OperationalError
import logging
import time
from app.database.models import Base
from app.database.config import db_settings

logger = logging.getLogger(__name__)

def init_db():
    """Initialize database with simple retry logic"""
    # Connect to default postgres database
    default_db_url = db_settings.DATABASE_URL.rsplit('/', 1)[0] + '/postgres'
    engine = create_engine(default_db_url)
    db_name = db_settings.DATABASE_URL.rsplit('/', 1)[1]

    # Try to create database
    try:
        with engine.connect() as conn:
            conn.execute("commit")
            # Try to create database
            try:
                conn.execute(f"CREATE DATABASE {db_name}")
                logger.info(f"Created database {db_name}")
            except Exception as e:
                logger.info(f"Database {db_name} already exists or error: {e}")
    except Exception as e:
        logger.error(f"Error during database creation: {e}")
        raise

    # Connect to the actual database and create tables
    try:
        engine = create_engine(db_settings.DATABASE_URL)
        Base.metadata.create_all(engine)
        logger.info("Tables created successfully")
    except Exception as e:
        logger.error(f"Error creating tables: {e}")
        raise

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    init_db()