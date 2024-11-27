from app.scraper.lieferando_api import LieferandoAPI, LieferandoAPIError
from app.parser.restaurant_parser import RestaurantParser
import time
from typing import List, Dict
from app.database.repository import RankingRepository
from app.database import SessionLocal
from app.utils.logger import setup_logger

def store_ranking(ranking_data: dict):
    db = SessionLocal()
    try:
        repo = RankingRepository(db)
        ranking = repo.create_ranking(ranking_data)
        return ranking
    finally:
        db.close()

class LieferandoScraper:
    def __init__(self):
        self.api = LieferandoAPI()
        self.logger = setup_logger("app.scraper")

    def process_slugs(self, slugs: List[str]) -> List[Dict]:
        self.logger.info(f"Starting to process {len(slugs)} restaurants")
        for slug in slugs:
            try:
                self.process_slug(slug, store_in_db=True)
            except LieferandoAPIError as e:
                self.logger.error(f"Error processing '{slug}': {str(e)}")
                continue
            except Exception as e:
                self.logger.error(f"Error processing {slug}: {e}")
                continue
        self.logger.info(f"Finished processing {len(slugs)} restaurants")

    def process_slug(self, slug: str, store_in_db: bool) -> dict:
        try:
            if not slug:
                raise ValueError("Empty slug provided")
            
            address_params = self.api.get_slug_address(slug)
            self.logger.info(f"{slug} - address found at postal code: {address_params.get('postalCode')}")
            
            restaurants_data = self.api.get_restaurants_by_address(address_params)
            
            parser = RestaurantParser(restaurants_data)
            parsed_ranking = parser.parse_restaurant(slug)
            self.logger.info(f"Parsed ranking data: {parsed_ranking}")
            
            if store_in_db:
                ranking = store_ranking(parsed_ranking)
                self.logger.info(f"Stored ranking with ID: {ranking.id}")
            
            return parsed_ranking
        except LieferandoAPIError as e:
            self.logger.error(f"Error retrieving data for '{slug}': {str(e)}")
            return {"slug": slug, "error": str(e)}
        except Exception as e:
            self.logger.error(f"Error processing {slug}: {str(e)}")
            return { "slug": slug, "error": str(e)}
