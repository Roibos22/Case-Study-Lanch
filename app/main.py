from app.database import Base
from app.api.main import app
from app.database.config import db_settings
from app.scraper.lieferando_scraper import LieferandoScraper
import logging
from typing import List
from sqlalchemy import create_engine

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def init_db():
    """Initialize database and create tables"""
    try:
        engine = create_engine(db_settings.DATABASE_URL)
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise


SLUGS: List[str] = [
        "x",
        "loco-chicken-i-frechen",
        # "loco-chicken-bielefeld",
        # "happy-slice-suedstadt",
        #  "happy-slice-pizza-i-wandsbek-markt"
]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)