from app.scraper.lieferando_api import LieferandoAPI
from app.parser.restaurant_parser import RestaurantParser
from app.database import SessionLocal, Base
from app.database.repository import RankingRepository
from app.database.config import db_settings
import logging
import time
from typing import List, Dict
from sqlalchemy import create_engine


def init_db():
    """Initialize database and create tables"""
    try:
        engine = create_engine(db_settings.DATABASE_URL)
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def store_ranking(ranking_data: dict):
    db = SessionLocal()
    try:
        repo = RankingRepository(db)
        ranking = repo.create_ranking(ranking_data)
        return ranking
    finally:
        db.close()

class LieferandoScraper:
    def __init__(self, delay_seconds: float = 2.0):
        self.api = LieferandoAPI(delay_seconds=delay_seconds)

    def process_slugs(self, slugs: List[str]) -> List[Dict]:
        """Process all restaurant slugs and return aggregated results"""
        
        results = []
        for slug in slugs:
            try:
                result = self.process_slug(slug)
                logger.info(f"Processing {slug}")
                if "error" not in result:
                    results.append({
                        "slug": slug,
                        "rank": result["rank"],
                        "rank_total": result["rank_total"],
                        "total_restaurants": result["total_restaurants"]
                    })
                    logger.info(f"✓ {slug}")
                else:
                    logger.error(f"✗ {slug}: {result['error']}")

            except Exception as e:
                logger.error(f"Error processing {slug}: {e}")
                continue

            time.sleep(self.api.delay_seconds)
        
        return results
 
    def process_slug(self, slug: str) -> dict:
        logger.info(f"Processing restaurant: {slug}")
        
        try:
            if not slug:
                raise ValueError("Empty slug provided")
            
            address_params = self.api.get_slug_address(slug)
            logger.info(f"{slug} - address found: {address_params}")
            restaurants_data = self.api.get_restaurants_by_address(address_params)
            parser = RestaurantParser(restaurants_data)
            parsed_ranking = parser.parse_restaurant(slug)
            
            # Parse restaurant data
            logger.info(f"Parsed ranking data: {parsed_ranking}")
            
            # Store in database
            ranking = store_ranking(parsed_ranking)
            logger.info(f"Stored ranking with ID: {ranking.id}")
            
            return parsed_ranking
            
        except Exception as e:
            logger.error(f"Error processing {slug}: {str(e)}")
            return {
                "slug": slug,
                "error": str(e)
            }

SLUGS: List[str] = [
        "x",
        "loco-chicken-i-frechen",
        # "loco-chicken-bielefeld",
        # "happy-slice-suedstadt",
        #  "happy-slice-pizza-i-wandsbek-markt"
]

if __name__ == "__main__":
    try:
        scraper = LieferandoScraper()
        results = scraper.process_slugs(SLUGS)
    except Exception as e:
        print("Scraper Error")
