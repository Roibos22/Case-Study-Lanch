from app.scraper.lieferando_api import LieferandoAPI
from app.parser.restaurant_parser import RestaurantParser
import logging
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
    def __init__(self, delay_seconds: float = 2.0):
        self.api = LieferandoAPI(delay_seconds=delay_seconds)
        self.logger = setup_logger("app.scraper")



    def process_slugs(self, slugs: List[str]) -> List[Dict]:
        self.logger.info(f"Starting to process {len(slugs)} restaurants")
        for slug in slugs:
            try:
                self.process_slug(slug, True)
            except Exception as e:
                self.logger.error(f"Error processing {slug}: {e}")
                continue
            time.sleep(self.api.delay_seconds)
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
            
        except Exception as e:
            self.logger.error(f"Error processing {slug}: {str(e)}")
            return {
                "slug": slug,
                "error": str(e)
            }
