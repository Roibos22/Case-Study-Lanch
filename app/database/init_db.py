from sqlalchemy import create_engine
import logging
from app.database.models import Base
from app.database.config import db_settings

logger = logging.getLogger(__name__)

def init_db():
    default_db_url = db_settings.DATABASE_URL.rsplit('/', 1)[0] + '/postgres'
    engine = create_engine(default_db_url)
    print(default_db_url)
    db_name = db_settings.DATABASE_URL.rsplit('/', 1)[1]
    print(db_name)

    try:
        with engine.connect() as conn:
            try:
                conn.execute(f"CREATE DATABASE {db_name}")
                logger.info(f"Created database {db_name}")
            except Exception as e:
                logger.info(f"Database {db_name} already exists or error: {e}")
    except Exception as e:
        logger.error(f"Error during database creation: {e}")
        raise

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